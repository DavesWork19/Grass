import psycopg2
import pandas as pd
from datetime import datetime

from constants import NFL_TEAMS, SEASON_YEAR
from saveNFLData import DB_CONFIG

ACRONYM_TO_TEAM_NAME = {team["acronym"]: team["name"] for team in NFL_TEAMS}


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

    today = datetime.now().date()

    team_exists = []
    with open('../../../Health App/health-app/app/commonComps/todaysGamesFootball.js', 'w') as f:
        f.write('export const todaysGamesFootball = [\n')
        f.write(f"'{today.strftime('%A')}',\n")
        f.write(f"'{today.strftime('%B %d, %Y')}',\n")
        for index, game in df.iterrows():
            team_name = game['team_name']
            opp_team_name = game['next_opp_team_name']
            if (opp_team_name not in team_exists) and (team_name not in team_exists):
                team_exists.append(team_name)
                team_exists.append(opp_team_name)
                if game['is_home']:
                    f.write(f"'{game['full_game_start_time']},{ACRONYM_TO_TEAM_NAME[opp_team_name]},{ACRONYM_TO_TEAM_NAME[team_name]},{game['home_spread']},{int(bool(game['home_calculated_spread_test']))},{game['over_under']},{int(bool(game['calculated_over_under_test']))},{game['away_money_line']},{game['home_money_line']},{int(bool(game['home_calculated_money_line_test']))}',\n")
                else:
                    f.write(f"'{game['full_game_start_time']},{ACRONYM_TO_TEAM_NAME[team_name]},{ACRONYM_TO_TEAM_NAME[opp_team_name]},{game['home_spread']},{int(bool(game['home_calculated_spread_test']))},{game['over_under']},{int(bool(game['calculated_over_under_test']))},{game['away_money_line']},{game['home_money_line']},{int(bool(game['home_calculated_money_line_test']))}',\n")
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
