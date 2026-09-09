import psycopg2
import pandas as pd
from datetime import date, datetime, timedelta
from constants import NBA_TEAMS

ACRONYM_TO_TEAM_NAME = {team["acronym"]: team["name"] for team in NBA_TEAMS}


def updateFrontendGames():

    today = datetime.now().date()

    db_config = {
        'host': 'localhost',
        'database': 'postgres',
        'user': 'postgres',
        'password': 'Sinorrabb1t',
        'port': 5432
    }

    # Connect to PostgreSQL
    conn = psycopg2.connect(**db_config)
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM BBALL7 WHERE created_at = '{today}' ORDER BY game_start_time ASC")
    all_data = cur.fetchall()

    # Get column names
    colnames = [desc[0] for desc in cur.description]

    # Create DataFrame
    df = pd.DataFrame(all_data, columns=colnames)

    cur.close()
    conn.close()
        
    team_exists = []
    # Write to file
    with open('../../../Health App/health-app/app/commonComps/todaysGames.js', 'w') as f:
        f.write('export const todaysGames = [\n')
        f.write(f"'{today.strftime('%A')}',\n")
        f.write(f"'{today.strftime('%B %d, %Y')}',\n")
        for index, game in df.iterrows():
            team_name = game['team_name']
            opp_team_name = game['next_opp_team_name']
            if (opp_team_name not in team_exists) and (team_name not in team_exists):
                team_exists.append(team_name)
                team_exists.append(opp_team_name)
                if game['is_home']:
                    f.write(f"'{game['full_game_start_time']},{ACRONYM_TO_TEAM_NAME[opp_team_name]},{ACRONYM_TO_TEAM_NAME[team_name]},{game['home_spread']},{int(game['home_calculated_spread_test'])},{game['over_under']},{int(game['calculated_over_under_test'])},{game['away_money_line']},{game['home_money_line']},{int(game['home_calculated_money_line_test'])}',\n")
                else:
                    f.write(f"'{game['full_game_start_time']},{ACRONYM_TO_TEAM_NAME[team_name]},{ACRONYM_TO_TEAM_NAME[opp_team_name]},{game['home_spread']},{int(game['home_calculated_spread_test'])},{game['over_under']},{int(game['calculated_over_under_test'])},{game['away_money_line']},{game['home_money_line']},{int(game['home_calculated_money_line_test'])}',\n")
        f.write("];")



def df_to_js_const(df):
    lines = []

    # Get the date info from the first row
    first_row = df.iloc[0]
    game_date = pd.to_datetime(first_row['full_game_start_time'])
    day_name = game_date.strftime('%A')
    month_day = game_date.strftime('%B %-d, %Y')

    # Build game pairs once
    game_rows = []
    visited = set()

    for _, row in df.iterrows():
        team = row['team_name']
        opp = row['next_opp_team_name']

        game_key = tuple(sorted([team, opp]))
        if game_key in visited:
            continue
        visited.add(game_key)

        opp_rows = df[df['team_name'] == opp]
        if opp_rows.empty:
            continue
        opp_row = opp_rows.iloc[0]

        if row['is_home']:
            away, home = opp_row, row
        else:
            away, home = row, opp_row

        game_rows.append((away, home))

    def get_parlay_flag(row_away, row_home, parlay, col):
        away_val = row_away.get(f'{parlay}_{col}')
        home_val = row_home.get(f'{parlay}_{col}')
        # If either value is None/False/empty, this game has no pick for this parlay
        if away_val is None or str(away_val) in ('None', 'False', ''):
            if home_val is None or str(home_val) in ('None', 'False', ''):
                return None  # no pick at all for this parlay+col
        return 1 if bool(home_val) and str(home_val) not in ('None', 'False', '') else 0

    for parlay in ['parlay1', 'parlay2', 'parlay3']:
        const_name = f"todaysParlay{parlay[-1]}"
        lines.append(f"export const {const_name} = [")
        lines.append(f"  '{day_name}',")
        lines.append(f"  '{month_day}',")

        for away, home in game_rows:
            away_team = away['team_name']
            home_team = home['team_name']
            time = pd.to_datetime(away['full_game_start_time']).strftime('%-I:%M%p').lower().replace('am', 'a').replace('pm', 'p')

            spread = home['home_spread']
            ou = away['over_under']
            away_ml = away['away_money_line']
            home_ml = away['home_money_line']

            spread_h = get_parlay_flag(away, home, parlay, 'spread')
            ou_h = get_parlay_flag(away, home, parlay, 'over_under')
            ml_h = get_parlay_flag(away, home, parlay, 'money_line')

            # Skip game entirely if it has no picks in this parlay
            if spread_h is None and ou_h is None and ml_h is None:
                continue

            # Default None flags to 0
            spread_h = spread_h if spread_h is not None else 0
            ou_h = ou_h if ou_h is not None else 0
            ml_h = ml_h if ml_h is not None else 0

            line = f"  '{time},{away_team},{home_team},{spread},{spread_h},{ou},{ou_h},{away_ml},{home_ml},{ml_h}',"
            lines.append(line)

        lines.append("];")
        lines.append("")  # blank line between exports

    return "\n".join(lines)

def get_parlay_picks(df):
    parlays = ['parlay1', 'parlay2', 'parlay3']
    bet_types = ['spread', 'over_under', 'money_line']

    results = {
        'parlay1': [],
        'parlay2': [],
        'parlay3': [],
    }

    for _, row in df.iterrows():
        for parlay in parlays:
            for bet in bet_types:
                col = f'{parlay}_{bet}'
                val = row.get(col)
                if val is not None and str(val) not in ('None', 'False', '') and bool(val) and row[f'calculated_{bet}_test'] != False:
                    results[parlay].append({
                        'team_name': row['team_name'],
                        f'calculated_{bet}_test': row[f'calculated_{bet}_test'],
                        'bet_type': bet
                    })

    return results

def applyNameChange(name):
    return ACRONYM_TO_TEAM_NAME[name]

def updateFrontendParlays():
    today = datetime.now().date()
    db_config = {
        'host': 'localhost',
        'database': 'postgres',
        'user': 'postgres',
        'password': 'Sinorrabb1t',
        'port': 5432
    }

    # Connect to PostgreSQL
    conn = psycopg2.connect(**db_config)
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM BBALL7 WHERE created_at = '{today}'")
    all_data = cur.fetchall()

    # Get column names
    colnames = [desc[0] for desc in cur.description]
    # Create DataFrame
    df = pd.DataFrame(all_data, columns=colnames)

    cur.close()
    conn.close()

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
                # Create a frozenset so {A,B} == {B,A}
                matchup_key = frozenset([team, opp])
                if matchup_key in seen_ou_matchups:
                    continue  # skip duplicate
                seen_ou_matchups.add(matchup_key)
            deduped.append(pick)
        results[parlay] = deduped

    # Build JS file content
    day_name = datetime.now().strftime('%A')        # e.g. "Friday"
    month_day = datetime.now().strftime('%B %-d, %Y')  # e.g. "March 13, 2026"

    lines = []
    parlay_map = {'parlay1': '1', 'parlay2': '2', 'parlay3': '3'}

    for parlay, picks in results.items():
        num = parlay_map[parlay]
        lines.append(f"export const todaysParlay{num} = [")
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

    with open('../../../Health App/health-app/app/commonComps/todaysParlays.js', "w") as f:
        f.write(js_content)

