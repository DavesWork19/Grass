"""
One-off historical seed for the NFL1 table.

The weekly pipeline (main.py) can't cold-start: week 1 of a season has no played
games, so runDaBot/runDaParlays have nothing to train on. This script backfills
the 2025 regular season into NFL1 (season_year=2025) so the models have history.

Game stats come from Pro Football Reference (via scrapes.py's
undetected-chromedriver browser). Betting lines, final scores and weather come
from nflverse's games.csv - PFR's schedule table doesn't carry closing lines,
and scraping ~270 boxscore pages for them would be slow and Cloudflare-heavy.

It mimics the natural weekly cadence: for each week W it inserts that week's
feature rows (built from games < W), runs runDaBot for (W, 2025) to fill the
calculated_* columns, then records the actual bet outcomes from the final score.
No predictions are published anywhere - this only populates the training table.
"""

import sys

import pandas as pd
import psycopg2

from constants import NFL_TEAMS, SEASON_YEAR
from saveNFLData import (
    DB_CONFIG,
    TEAM_NUMBER_TO_ACRONYM,
    TEAM_NUMBER_TO_PFR,
    _clean_game_log,
    _team_season_features,
    compute_league_averages,
    store_nfl_data,
)
from scrapes import scrape_all_game_data_by_team, close_driver
from legends import getTeamNumber
from bots import runDaBot

SEED_YEAR = 2025
NFLVERSE_GAMES_URL = 'https://github.com/nflverse/nfldata/raw/master/data/games.csv'

ACRONYM_TO_NUMBER = {acr: num for num, acr in TEAM_NUMBER_TO_ACRONYM.items()}
# nflverse abbreviations that differ from our constants.py acronyms.
NFLVERSE_ABBR_FIX = {'LA': 'LAR'}


def _team_number_from_nflverse(abbr):
    acr = NFLVERSE_ABBR_FIX.get(abbr, abbr)
    return ACRONYM_TO_NUMBER.get(acr)


def _fmt_spread(value):
    """nflverse spread_line is home-favored-positive; format as a signed string
    the way the DraftKings scraper / updates.py expect (always a leading sign)."""
    return f'{value:+.1f}'


def _fmt_money_line(value):
    try:
        return f'{int(round(float(value))):+d}'
    except (TypeError, ValueError):
        return '+0'


def _game_start_ints(gametime):
    """'HH:MM' -> (full_game_start_time str, game_start_time int in the same
    ballpark as saveData's `hour * 6`)."""
    if not isinstance(gametime, str) or ':' not in gametime:
        return '', 0
    h, m = gametime.split(':')[:2]
    try:
        minutes = int(h) * 60 + int(m)
    except ValueError:
        return '', 0
    return f'{gametime}:00', round(minutes / 10)


def _weather_ints(row):
    roof = str(row.get('roof', '') or '').lower()
    indoors = roof in ('dome', 'closed')
    temp = row.get('temp')
    wind = row.get('wind')
    temp_f = 70 if indoors or pd.isna(temp) else int(round(float(temp)))
    wind_mph = 0 if indoors or pd.isna(wind) else int(round(float(wind)))
    return 0, temp_f, wind_mph  # weather_code 0 (nflverse has no condition text)


def _load_nflverse():
    games = pd.read_csv(NFLVERSE_GAMES_URL)
    games = games[(games['season'] == SEED_YEAR) & (games['game_type'] == 'REG')]
    return games.sort_values(['week', 'gameday', 'gametime']).reset_index(drop=True)


def _prefetch_gamelogs():
    logs = {}
    for number in range(len(NFL_TEAMS)):
        pfr_code = TEAM_NUMBER_TO_PFR[number]
        print(f'  gamelog {pfr_code} ...')
        logs[pfr_code] = _clean_game_log(scrape_all_game_data_by_team(pfr_code, SEED_YEAR))
    return logs


def _insert_week(week, week_games, gamelogs):
    for _, matchup in week_games.iterrows():
        away_number = _team_number_from_nflverse(matchup['away_team'])
        home_number = _team_number_from_nflverse(matchup['home_team'])
        if away_number is None or home_number is None:
            print(f"  ?? unresolved teams {matchup['away_team']} @ {matchup['home_team']}")
            continue

        full_start, start_int = _game_start_ints(matchup.get('gametime'))
        weather_code, temp_f, wind_mph = _weather_ints(matchup)

        spread_line = float(matchup['spread_line'])
        home_spread = _fmt_spread(-spread_line)
        away_spread = _fmt_spread(spread_line)
        home_ml = _fmt_money_line(matchup['home_moneyline'])
        away_ml = _fmt_money_line(matchup['away_moneyline'])
        over_under = float(matchup['total_line'])

        for number, is_home, opp_number in (
            (away_number, 0, home_number),
            (home_number, 1, away_number),
        ):
            acronym = TEAM_NUMBER_TO_ACRONYM[number]
            opp_acronym = TEAM_NUMBER_TO_ACRONYM[opp_number]
            game_log = gamelogs[TEAM_NUMBER_TO_PFR[number]]
            prior = game_log[game_log['week'] < week]
            features = _team_season_features(prior)

            last_game_in_season = features['last_game_in_season']
            weeks_since_last_game = (
                (week - last_game_in_season) if last_game_in_season is not None else 0
            )

            last_opp_number = (
                getTeamNumber(features['last_opp_name']) if features['last_opp_name'] else None
            )
            last_opp_acronym = (
                TEAM_NUMBER_TO_ACRONYM[last_opp_number]
                if last_opp_number is not None
                else opp_acronym
            )

            spread = home_spread if is_home else away_spread
            money_line = home_ml if is_home else away_ml

            store_nfl_data(
                weeks_since_last_game,
                features['last_game_was_win'],
                features['curr_streak'],
                features['home_games_win_percent'],
                features['away_games_win_percent'],
                features['team_avg_total_yards'],
                features['team_third_down_pct'],
                features['team_avg_points_against'],
                features['team_point_diff'],
                features['team_point_diff_pos'],
                features['team_giveaways_season'],
                full_start,
                start_int,
                features['last_game_point_for'],
                features['last_game_point_against'],
                features['last_game_pass_yards'],
                features['last_game_rush_yards'],
                features['last_game_turnovers'],
                features['last_game_sacks_allowed'],
                features['all_pass_yards'],
                features['all_rush_yards'],
                features['all_sacks_allowed'],
                features['all_turnovers'],
                features['team_avg_points_for'],
                is_home,
                last_game_in_season,
                week,
                acronym,
                last_opp_acronym,
                opp_acronym,
                SEED_YEAR,
                home_spread,
                spread,
                over_under,
                home_ml,
                away_ml,
                money_line,
                weather_code,
                temp_f,
                wind_mph,
                0,
            )


def _record_actuals(week, week_games):
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    for _, matchup in week_games.iterrows():
        away_number = _team_number_from_nflverse(matchup['away_team'])
        home_number = _team_number_from_nflverse(matchup['home_team'])
        if away_number is None or home_number is None:
            continue
        if pd.isna(matchup['home_score']) or pd.isna(matchup['away_score']):
            continue

        home_score = int(matchup['home_score'])
        away_score = int(matchup['away_score'])
        total_line = float(matchup['total_line'])
        spread_line = float(matchup['spread_line'])  # home favored positive

        for acronym, pf, pa, team_spread in (
            (TEAM_NUMBER_TO_ACRONYM[home_number], home_score, away_score, -spread_line),
            (TEAM_NUMBER_TO_ACRONYM[away_number], away_score, home_score, spread_line),
        ):
            # Same rule as updates.updateDBActuals: a '-' spread must be beaten
            # outright, a '+' spread is a cushion.
            if team_spread < 0:
                needed = -team_spread
            elif team_spread > 0:
                needed = team_spread * -1
            else:
                needed = 0.0

            actual_spread = (pf - pa) >= needed
            actual_over_under = (pf + pa) >= total_line
            actual_money_line = pf > pa

            cur.execute(
                """
                UPDATE NFL1
                SET actual_spread = %s, actual_over_under = %s, actual_money_line = %s
                WHERE team_name = %s AND next_game_in_season = %s AND season_year = %s
                """,
                (actual_spread, actual_over_under, actual_money_line,
                 acronym, int(week), SEED_YEAR),
            )
    conn.commit()
    cur.close()
    conn.close()


def _table_is_seeded():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    try:
        cur.execute(
            "SELECT count(*) FROM NFL1 WHERE season_year = %s", (SEED_YEAR,)
        )
        return cur.fetchone()[0] > 0
    except psycopg2.errors.UndefinedTable:
        conn.rollback()
        return False
    finally:
        cur.close()
        conn.close()


def main():
    if _table_is_seeded() and '--force' not in sys.argv:
        print(f'NFL1 already has {SEED_YEAR} rows - pass --force to reseed anyway.')
        return

    print(f'Loading nflverse games for {SEED_YEAR} ...')
    games = _load_nflverse()
    weeks = sorted(games['week'].unique())

    print('Prefetching PFR gamelogs (32 teams) ...')
    try:
        gamelogs = _prefetch_gamelogs()
    finally:
        close_driver()

    for week in weeks:
        week_games = games[games['week'] == week]
        print(f'Week {week}: {len(week_games)} games -> insert')
        _insert_week(week, week_games, gamelogs)
        compute_league_averages(int(week), SEED_YEAR)

        print(f'Week {week}: runDaBot')
        try:
            runDaBot(int(week), season=SEED_YEAR)
        except Exception as exc:  # noqa: BLE001 - keep seeding even if a week fails
            print(f'  runDaBot failed for week {week}: {exc!r}')

        _record_actuals(week, week_games)

    print('Seed complete.')


if __name__ == '__main__':
    main()
