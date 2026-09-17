import psycopg2
import pandas as pd
from datetime import datetime, date, timedelta

from constants import NFL_TEAMS, SEASON_YEAR, WEEK_DATE_RANGES
from saveNFLData import DB_CONFIG

ACRONYM_TO_TEAM_NAME = {team["acronym"]: team["name"] for team in NFL_TEAMS}

# The default day (Sunday, the main NFL slate) used for a game whose day
# couldn't be scraped - keeps it grouped somewhere reasonable rather than
# crashing the header logic.
_DEFAULT_DAY_CODE = 4  # Wed=0 ... Sun=4 ... Tue=6, see legends.getDay


def _week_start_date(week, season_year, week_date_ranges):
    """First (Wednesday) date of `week` in `season_year`'s season - weeks past
    the turn of the year (late-season weeks) roll into season_year + 1."""
    start_str, _ = week_date_ranges[week]
    start_month, start_day = (int(x) for x in start_str.split('/'))
    start_year = season_year if start_month >= 8 else season_year + 1
    return date(start_year, start_month, start_day)


def updateFrontendGames(week):
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute(
        f"SELECT * FROM NFL1 WHERE next_game_in_season = {week} AND season_year = {SEASON_YEAR} ORDER BY game_start_time ASC"
    )
    all_data = cur.fetchall()

    colnames = [desc[0] for desc in cur.description]
    df = pd.DataFrame(all_data, columns=colnames)

    cur.close()
    conn.close()

    week_start = _week_start_date(week, SEASON_YEAR, WEEK_DATE_RANGES)

    team_exists = []
    games = []
    for index, game in df.iterrows():
        team_name = game['team_name']
        opp_team_name = game['next_opp_team_name']
        if (opp_team_name in team_exists) or (team_name in team_exists):
            continue
        team_exists.append(team_name)
        team_exists.append(opp_team_name)

        day_code = game['game_day_code']
        day_code = int(day_code) if pd.notna(day_code) else _DEFAULT_DAY_CODE
        game_date = week_start + timedelta(days=day_code)

        if game['is_home']:
            away, home = opp_team_name, team_name
        else:
            away, home = team_name, opp_team_name

        row = f"{game['full_game_start_time']},{ACRONYM_TO_TEAM_NAME[away]},{ACRONYM_TO_TEAM_NAME[home]},{game['home_spread']},{int(bool(game['home_calculated_spread_test']))},{game['over_under']},{int(bool(game['calculated_over_under_test']))},{game['away_money_line']},{game['home_money_line']},{int(bool(game['home_calculated_money_line_test']))}"
        games.append((game_date, game['game_start_time'], row))

    games.sort(key=lambda g: (g[0], g[1]))

    with open('../../../Health App/health-app/app/commonComps/todaysGamesFootball.js', 'w') as f:
        f.write('export const todaysGamesFootball = [\n')
        if not games:
            today = datetime.now().date()
            f.write(f"'{today.strftime('%A')}|{today.strftime('%B %d, %Y')}',\n")
        last_date = None
        for game_date, _, row in games:
            if game_date != last_date:
                f.write(f"'{game_date.strftime('%A')}|{game_date.strftime('%B %d, %Y')}',\n")
                last_date = game_date
            f.write(f"'{row}',\n")
        f.write("];")


def applyNameChange(name):
    return ACRONYM_TO_TEAM_NAME[name]


def updateFrontendParlays(week):
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM NFL1 WHERE next_game_in_season = {week} AND season_year = {SEASON_YEAR}")
    all_data = cur.fetchall()

    colnames = [desc[0] for desc in cur.description]
    df = pd.DataFrame(all_data, columns=colnames)

    cur.close()
    conn.close()

    if df.empty:
        with open('../../../Health App/health-app/app/commonComps/todaysParlaysFootball.js', 'w') as f:
            day_name = datetime.now().strftime('%A')
            month_day = datetime.now().strftime('%B %-d, %Y')
            for num in (1, 2, 3):
                f.write(f"export const todaysParlayFootball{num} = [\n  '{day_name}',\n  '{month_day}',\n];\n\n")
        return

    parlays = ['parlay1', 'parlay2', 'parlay3']
    bet_types = ['spread', 'over_under', 'money_line']
    results = {
        'parlay1': [],
        'parlay2': [],
        'parlay3': [],
    }

    team_to_opp = dict(zip(df['team_name'].apply(applyNameChange), df['next_opp_team_name'].apply(applyNameChange)))

    for _, row in df.iterrows():
        for parlay in parlays:
            for bet in bet_types:
                col = f'{parlay}_{bet}'
                val = row.get(col)
                if bet == 'over_under':
                    if val is not None and str(val) not in ('None', 'False', '') and row[f'calculated_{bet}_test'] is not None:
                        results[parlay].append({
                            'team_name': ACRONYM_TO_TEAM_NAME[row['team_name']],
                            'bet_type': bet,
                            'line': row[bet],
                            'calculated': row[f'calculated_{bet}_test']
                        })
                elif (bet == 'money_line') or (bet == 'spread'):
                    if val is not None and str(val) not in ('None', 'False', '') and row[f'calculated_{bet}_test'] is not False:
                        results[parlay].append({
                            'team_name': ACRONYM_TO_TEAM_NAME[row['team_name']],
                            'bet_type': bet,
                            'line': row[bet],
                            'calculated': row[f'calculated_{bet}_test']
                        })

    for parlay in parlays:
        seen_ou_matchups = set()
        deduped = []
        for pick in results[parlay]:
            if pick['bet_type'] == 'over_under':
                team = pick['team_name']
                opp = team_to_opp.get(team)
                matchup_key = frozenset([team, opp])
                if matchup_key in seen_ou_matchups:
                    continue
                seen_ou_matchups.add(matchup_key)
            deduped.append(pick)
        results[parlay] = deduped

    day_name = datetime.now().strftime('%A')
    month_day = datetime.now().strftime('%B %-d, %Y')

    lines = []
    parlay_map = {'parlay1': '1', 'parlay2': '2', 'parlay3': '3'}

    for parlay, picks in results.items():
        num = parlay_map[parlay]
        lines.append(f"export const todaysParlayFootball{num} = [")
        lines.append(f"  '{day_name}',")
        lines.append(f"  '{month_day}',")
        for pick in picks:
            team = pick['team_name']
            bet = pick['bet_type']
            value = pick['line']
            calc = pick['calculated']
            lines.append(f"  '{team}','{value}','{bet}','{calc}',")
        lines.append("];\n")

    js_content = "\n".join(lines)

    with open('../../../Health App/health-app/app/commonComps/todaysParlaysFootball.js', "w") as f:
        f.write(js_content)
