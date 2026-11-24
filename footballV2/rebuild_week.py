"""
Rebuild a past week's NFL1 rows from the todaysGamesFootball.js that was
published for it, then grade it and refresh the model record.

    python3 rebuild_week.py <week> <frontend git ref>

e.g. `python3 rebuild_week.py 11 ad51272` reads
app/commonComps/todaysGamesFootball.js as of commit ad51272 in the Health App
repo. That file has every game's lines and the published picks, so the rebuilt
rows grade exactly what users saw. Team features are re-scraped from PFR but
cut off at games before <week>, matching what the model saw at the time.

Only for recovering lost data - DK and nflweather list upcoming games only,
so a past week can't be re-scraped. Existing rows for the week are archived,
never silently dropped (see saveNFLData._replace_existing_matchup).
"""

import subprocess
import sys
from datetime import datetime

import pandas as pd
import psycopg2

from constants import SEASON_YEAR, WEEK_DATE_RANGES
from frontend import _week_start_date
from legends import getTeamNumber
from saveNFLData import DB_CONFIG, TEAM_NUMBER_TO_ACRONYM, saveData
from scrapes import close_driver
from updates import updateDBActuals, getPreviousPercentages

FRONTEND_REPO = '../../../Health App/health-app'
GAMES_FILE = 'app/commonComps/todaysGamesFootball.js'


def _flip(line):
    line = line.strip()
    if line.startswith('-'):
        return '+' + line[1:]
    if line.startswith('+'):
        return '-' + line[1:]
    return line


def parse_games_file(text, week):
    """Return one dict per game: lines, picks, and kickoff day/time."""
    week_start = _week_start_date(week, SEASON_YEAR, WEEK_DATE_RANGES)
    games, game_date = [], None
    for raw in text.splitlines():
        raw = raw.strip().rstrip(',').strip("'")
        if not raw or raw.startswith('export') or raw.startswith(']'):
            continue
        if '|' in raw:
            game_date = datetime.strptime(raw.split('|')[1], '%B %d, %Y').date()
            continue
        time_, away, home, home_spread, spread_pick, ou, ou_pick, away_ml, home_ml, ml_pick = raw.split(',')
        games.append({
            'awayTeam': away, 'homeTeam': home,
            'homeSpread': home_spread, 'awaySpread': _flip(home_spread),
            'overUnder': float(ou), 'awayMoneyLine': away_ml, 'homeMoneyLine': home_ml,
            'home_spread_pick': spread_pick == '1', 'over_pick': ou_pick == '1',
            'home_ml_pick': ml_pick == '1',
            'full_game_start_time': time_, 'hour': int(time_.split(':')[0]),
            'day_code': (game_date - week_start).days,
        })
    return games


def restore_published_picks(week, games):
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    for g in games:
        away = TEAM_NUMBER_TO_ACRONYM[getTeamNumber(g['awayTeam'])]
        home = TEAM_NUMBER_TO_ACRONYM[getTeamNumber(g['homeTeam'])]
        for team, is_home in ((away, False), (home, True)):
            cur.execute(
                """UPDATE NFL1 SET
                       calculated_spread_test = %s, calculated_money_line_test = %s,
                       calculated_over_under_test = %s,
                       home_calculated_spread_test = %s, home_calculated_money_line_test = %s,
                       full_game_start_time = %s, game_start_time = %s, game_day_code = %s
                   WHERE team_name = %s AND next_game_in_season = %s AND season_year = %s""",
                (
                    g['home_spread_pick'] if is_home else not g['home_spread_pick'],
                    g['home_ml_pick'] if is_home else not g['home_ml_pick'],
                    g['over_pick'], g['home_spread_pick'], g['home_ml_pick'],
                    g['full_game_start_time'], g['hour'] * 6, g['day_code'],
                    team, week, SEASON_YEAR,
                ),
            )
            if cur.rowcount != 1:
                raise RuntimeError(f'expected 1 row for {team} week {week}, updated {cur.rowcount}')
    conn.commit()
    cur.close()
    conn.close()


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)
    week, ref = int(sys.argv[1]), sys.argv[2]

    text = subprocess.run(
        ['git', '-C', FRONTEND_REPO, 'show', f'{ref}:{GAMES_FILE}'],
        check=True, capture_output=True, text=True,
    ).stdout
    games = parse_games_file(text, week)
    print(f'Parsed {len(games)} week {week} games from {ref}')

    gambling_data = pd.DataFrame([
        {k: g[k] for k in ('awayTeam', 'homeTeam', 'awaySpread', 'overUnder', 'awayMoneyLine', 'homeSpread', 'homeMoneyLine')}
        for g in games
    ])

    try:
        # Empty weather frame = don't filter against nflweather's (now later)
        # schedule; kickoff day/time come from the published file instead.
        saveData(week, gambling_data=gambling_data, weather_data=pd.DataFrame())
        restore_published_picks(week, games)
        print(f'Restored published picks for {len(games)} games')
        updateDBActuals(week)
    finally:
        close_driver()

    getPreviousPercentages()
    print('Done - newPercentsFootball.js refreshed')


if __name__ == '__main__':
    main()
