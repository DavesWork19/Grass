import psycopg2
import pandas as pd
from datetime import datetime, timedelta
import random
import time
from constants import NBA_TEAMS
from scrapes import scrape_upcoming_game_by_team

team_names = [team["acronym"] for team in NBA_TEAMS]
season_year = 2026


def updateDBActuals():
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
    cur.execute(f"SELECT * FROM BBALL7 WHERE actual_spread is NULL;")
    all_data = cur.fetchall()

    # Get column names
    colnames = [desc[0] for desc in cur.description]
    df = pd.DataFrame(all_data, columns=colnames)

    for index, row in df.iterrows():
        team_name = row['team_name']
        current_game_in_season = row['next_game_in_season']

        upcoming_game_url = f'https://www.basketball-reference.com/teams/{team_name}/2026_games.html'
        upcoimng_game_df = scrape_upcoming_game_by_team(upcoming_game_url)
        last_game_from_upcoming_df = upcoimng_game_df[upcoimng_game_df['game_result'] != ''].iloc[-1]

        initial_delay = random.uniform(1.5, 3.5)
        time.sleep(initial_delay)

        if int(last_game_from_upcoming_df['g']) == current_game_in_season:
            points_for = int(last_game_from_upcoming_df['pts'])
            points_against = int(last_game_from_upcoming_df['opp_pts'])

            given_spread = row['spread']
            given_over_under = row['over_under']
            if given_spread[0] == '-':
                given_spread = float(given_spread[1:])
            elif given_spread[0] == '+':
                given_spread = float(given_spread[1:]) * -1
            

            spread = points_for - points_against
            actual_spread = True if spread >= given_spread else False
            over_under = points_for + points_against
            actual_over_under = True if over_under >= float(given_over_under) else False
            actual_money_line = True if points_for > points_against else False


            try:
                # Insert data
                insert_query = f"""
                UPDATE BBALL7
                SET actual_spread = {actual_spread}, actual_over_under = {actual_over_under}, actual_money_line = {actual_money_line}
                WHERE team_name = '{team_name}' and next_game_in_season = {current_game_in_season} and season_year = {season_year};"""

                cur.execute(insert_query)   
                conn.commit()
                
                print(f'Saved {team_name} for game number: {current_game_in_season}')
            except:
                print(f"Couldn't save row for team: {team_name}, next_game_in_season: {current_game_in_season}, year: {season_year}")



    cur.close()
    conn.close()



def getTotals(df, totals, name):
    dfLen = len(df)

    totals[f'{name}_spread'] = 0
    totals[f'{name}_overUnder'] = 0
    totals[f'{name}_moneyLine'] = 0
    if 'overall' in name:
        totals[f'{name}_total_games'] = dfLen / 2
    if not df.empty:
        for index, row in df.iterrows():
            actual_spread = row['actual_spread']
            actual_over_under = row['actual_over_under']
            actual_money_line = row['actual_money_line']

            calculated_spread = row['calculated_spread_test']
            calculated_over_under = row['calculated_over_under_test']
            calculated_money_line = row['calculated_money_line_test']

            correct_spread = actual_spread == calculated_spread
            correct_over_under = actual_over_under == calculated_over_under
            correct_money_line = actual_money_line == calculated_money_line

            totals[f'{name}_spread'] = totals[f'{name}_spread'] + int(correct_spread)
            totals[f'{name}_overUnder'] = totals[f'{name}_overUnder'] + int(correct_over_under)
            totals[f'{name}_moneyLine'] = totals[f'{name}_moneyLine'] + int(correct_money_line)

        totals[f'{name}_spread'] = totals[f'{name}_spread'] / dfLen
        totals[f'{name}_overUnder'] = totals[f'{name}_overUnder'] / dfLen
        totals[f'{name}_moneyLine'] = totals[f'{name}_moneyLine'] / dfLen
    
    return totals



def getPreviousPercentages():
    db_config = {
        'host': 'localhost',
        'database': 'postgres',
        'user': 'postgres',
        'password': 'Sinorrabb1t',
        'port': 5432
    }

    today = datetime.now().date()

    # Connect to PostgreSQL
    conn = psycopg2.connect(**db_config)
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM BBALL7 WHERE actual_spread is not NULL and calculated_spread_test is not NULL and season_year = {season_year};")
    all_data = cur.fetchall()

    # Get column names
    colnames = [desc[0] for desc in cur.description]
    df = pd.DataFrame(all_data, columns=colnames)


    totals = {}

    last_games = sorted(df['created_at'].unique())[:4:-1]

    totals = getTotals(df, totals, 'overall')
    totals = getTotals(df[df['created_at'] == last_games[0]], totals, 'overall_prev_1')
    totals = getTotals(df[df['created_at'] == last_games[1]], totals, 'overall_prev_2')
    totals = getTotals(df[df['created_at'] == last_games[2]], totals, 'overall_prev_3')
    totals = getTotals(df[df['created_at'] == last_games[3]], totals, 'overall_prev_4')
    totals = getTotals(df[df['created_at'] == last_games[4]], totals, 'overall_prev_5')

    for team in team_names:
        updated_df = df[df['team_name'] == team]
        totals = getTotals(updated_df, totals, team)

        all_games = sorted(updated_df['next_game_in_season'].unique().tolist())
        prev_1_game = all_games[-1]
        prev_2_game = all_games[-2]
        prev_3_game = all_games[-3]
        prev_4_game = all_games[-4]
        prev_5_game = all_games[-5]

        prev_1_game_df = updated_df[updated_df['next_game_in_season'] == prev_1_game]
        prev_2_game_df = updated_df[updated_df['next_game_in_season'] == prev_2_game]
        prev_3_game_df = updated_df[updated_df['next_game_in_season'] == prev_3_game]
        prev_4_game_df = updated_df[updated_df['next_game_in_season'] == prev_4_game]
        prev_5_game_df = updated_df[updated_df['next_game_in_season'] == prev_5_game]

        totals = getTotals(prev_1_game_df, totals, f'{team}_prev_1')
        totals = getTotals(prev_2_game_df, totals, f'{team}_prev_2')
        totals = getTotals(prev_3_game_df, totals, f'{team}_prev_3')
        totals = getTotals(prev_4_game_df, totals, f'{team}_prev_4')
        totals = getTotals(prev_5_game_df, totals, f'{team}_prev_5')

    # sorted_totals = {k: v for k, v in sorted(totals.items(), key=lambda item: item[1])}
    # print(totals)

    # Write to file
    with open('../../../Health App/health-app/app/commonComps/newPercents.js', 'w') as f:
        f.write('export const newPercentages = {\n')
        for key, value in totals.items():
            f.write(f"{key}: {value},\n")
        f.write("};")

    cur.close()
    conn.close()

    return totals


