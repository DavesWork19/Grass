import psycopg2
from datetime import date, datetime
import pandas as pd
import time
import random

from scrapes import scrape_all_game_data_by_team, scrape_misc_data_by_team, scrape_todays_gambling_data, scrape_upcoming_game_by_team
from legends import time_to_int
from constants import NBA_TEAMS, DK_TO_BBREF, MAX_DAYS_SINCE_LAST_GAME, current_season_year

TEAM_NAME_TO_ACRONYM = {team["name"]: team["acronym"] for team in NBA_TEAMS}
year = current_season_year()

DB_CONFIG = {
    'host': 'localhost',
    'database': 'postgres',
    'user': 'postgres',
    'password': 'Sinorrabb1t',
    'port': 5432
}

def store_bball_data(
    days_since_last_game,
    last_game_was_win,
    curr_streak,
    home_games_win_percent,
    away_games_win_percent,
    team_pace,
    league_avg_pace,
    team_off_rank,
    league_avg_off_rank,
    team_def_rank,
    league_avg_def_rank,
    team_mov,
    team_mov_pos,
    league_avg_mov,
    team_srs,
    team_srs_pos,
    league_avg_srs,
    full_game_start_time,
    game_start_time,
    last_game_point_for,
    last_game_point_against,
    last_game_field_goal_attempts,
    last_game_field_goal,
    last_game_turnovers,
    last_game_rebounds,
    all_field_goal_attempts,
    all_field_goal,
    all_rebounds,
    all_turnovers,
    team_avg_points_for,
    team_avg_points_against,
    is_home,
    last_game_in_season,
    next_game_in_season,
    team_name, 
    last_opp_team_name,
    next_opp_team_name,
    season_year, 
    home_spread,
    spread, 
    over_under, 
    home_money_line,
    away_money_line,
    money_line
):
    """
    Store basketball game variables into PostgreSQL database.
    
    Parameters:
    -----------
    all_game_data_df : DataFrame
        All historical game data
    upcoming_game_df : DataFrame
        Upcoming games data with results
    misc_team_data_df : DataFrame
        Team miscellaneous statistics
    db_config : dict
        Database configuration with keys: host, database, user, password, port
    
    Returns:
    --------
    int : ID of inserted record
    """

    today = datetime.now().date()
    
    # Connect to PostgreSQL
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    
    # Create table if it doesn't exist
    create_table_query = """
    CREATE TABLE IF NOT EXISTS BBALL7 (
        id SERIAL PRIMARY KEY,
        days_since_last_game INT,
        last_game_was_win INT,
        curr_streak INT,
        home_games_win_percent FLOAT,
        away_games_win_percent FLOAT,
        team_pace FLOAT,
        league_avg_pace FLOAT,
        team_off_rank FLOAT,
        league_avg_off_rank FLOAT,
        team_def_rank FLOAT,
        league_avg_def_rank FLOAT,
        team_mov FLOAT,
        team_mov_pos INT,
        league_avg_mov FLOAT,
        team_srs FLOAT,
        team_srs_pos INT,
        league_avg_srs FLOAT,
        full_game_start_time VARCHAR(10),
        game_start_time INT,
        last_game_point_for INT,
        last_game_point_against INT,
        last_game_field_goal_attempts INT,
        last_game_field_goal INT,
        last_game_turnovers INT,
        last_game_rebounds INT,
        all_field_goal_attempts INT,
        all_field_goal INT,
        all_rebounds INT,
        all_turnovers INT,
        team_avg_points_for INT,
        team_avg_points_against INT,
        is_home INT,
        last_game_in_season INT,
        next_game_in_season INT,
        team_name VARCHAR(100),
        last_opp_team_name VARCHAR(100),
        next_opp_team_name VARCHAR(100),
        season_year INT,
        home_spread VARCHAR(10),
        spread VARCHAR(10),
        over_under FLOAT,
        home_money_line VARCHAR(10),
        away_money_line VARCHAR(10),
        money_line VARCHAR(10),
        actual_spread BOOLEAN,
        actual_over_under BOOLEAN,
        actual_money_line BOOLEAN,
        calculated_spread BOOLEAN,
        calculated_over_under BOOLEAN,
        calculated_money_line BOOLEAN,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
    cur.execute(create_table_query)
    
    # Insert data
    insert_query = f"""
    INSERT INTO BBALL7 (
        days_since_last_game, last_game_was_win, curr_streak,
        home_games_win_percent, away_games_win_percent,
        team_pace, league_avg_pace, team_off_rank, league_avg_off_rank,
        team_def_rank, league_avg_def_rank, team_mov, team_mov_pos,
        league_avg_mov, team_srs, team_srs_pos, league_avg_srs, full_game_start_time,
        game_start_time, last_game_point_for, last_game_point_against,
        last_game_field_goal_attempts, last_game_field_goal,
        last_game_turnovers, last_game_rebounds, all_field_goal_attempts,
        all_field_goal, all_rebounds, all_turnovers, team_avg_points_for,
        team_avg_points_against, is_home, last_game_in_season, next_game_in_season, team_name, last_opp_team_name,
        next_opp_team_name, season_year, home_spread, spread, over_under, home_money_line, away_money_line, money_line, created_at
    ) VALUES (
        {days_since_last_game}, {last_game_was_win}, {curr_streak},
        {home_games_win_percent}, {away_games_win_percent},
        {team_pace}, {league_avg_pace}, {team_off_rank}, {league_avg_off_rank},
        {team_def_rank}, {league_avg_def_rank}, {team_mov}, {team_mov_pos},
        {league_avg_mov}, {team_srs}, {team_srs_pos}, {league_avg_srs}, '{full_game_start_time}',
        {game_start_time}, {last_game_point_for}, {last_game_point_against},
        {last_game_field_goal_attempts}, {last_game_field_goal},
        {last_game_turnovers}, {last_game_rebounds}, {all_field_goal_attempts},
        {all_field_goal}, {all_rebounds}, {all_turnovers}, {team_avg_points_for},
        {team_avg_points_against}, {is_home}, {last_game_in_season}, {next_game_in_season}, '{team_name}', '{last_opp_team_name}',
        '{next_opp_team_name}', {season_year}, '{home_spread}', '{spread}', {over_under}, '{home_money_line}', '{away_money_line}', '{money_line}', '{today}'
    ) RETURNING id
    """

    cur.execute(insert_query)
    
    record_id = cur.fetchone()[0]
    
    conn.commit()
    cur.close()
    conn.close()
    
    return record_id



def dk_to_bball_ref(team_extended_name):
    """'NY Knicks' -> 'NYK', 'LA Lakers' -> 'LAL', 'BOS Celtics' -> 'BOS'."""
    team_name = team_extended_name.split()[0]
    if team_name == 'LA':
        return 'LAL' if 'Lakers' in team_extended_name else 'LAC'
    return DK_TO_BBREF.get(team_name, team_name)


def _clear_existing_day(today, season_year):
    """Re-running saveData on the same day must not duplicate that day's rows."""
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM BBALL7 WHERE created_at = %s AND season_year = %s", (today, season_year))
        if cur.rowcount:
            print(f'Cleared {cur.rowcount} existing rows for {today}')
        conn.commit()
    except psycopg2.errors.UndefinedTable:
        conn.rollback()
    finally:
        cur.close()
        conn.close()


def _team_urls(bball_ref_team_name, season):
    base = f'https://www.basketball-reference.com/teams/{bball_ref_team_name}'
    return f'{base}/{season}/gamelog', f'{base}/{season}.html', f'{base}/{season}_games.html'


def saveData():
    today = date.today()

    all_gambling_data = scrape_todays_gambling_data()
    print(f'DraftKings listed {len(all_gambling_data)} games')

    _clear_existing_day(today, year)

    failed_teams = []
    skipped_teams = []

    for _, game in all_gambling_data.iterrows():
        for side in ('away', 'home'):
            team_extended_name = game[f'{side}Team']
            bball_ref_team_name = dk_to_bball_ref(team_extended_name)
            try:
                saved = saveTeam(today, bball_ref_team_name, game, is_home_side=(side == 'home'))
                if not saved:
                    skipped_teams.append(bball_ref_team_name)
            except Exception as e:
                print(f'FAILED {bball_ref_team_name}: {e!r}')
                failed_teams.append(bball_ref_team_name)

    if skipped_teams:
        print(f'Skipped (next game is not today): {skipped_teams}')
    if failed_teams:
        print(f'FAILED teams: {failed_teams}')


def saveTeam(today, bball_ref_team_name, gambling_data, is_home_side):
    all_game_data_url, misc_team_data_url, upcoming_game_url = _team_urls(bball_ref_team_name, year)

    upcoimng_game_df = scrape_upcoming_game_by_team(upcoming_game_url)
    next_game_df = upcoimng_game_df[upcoimng_game_df['game_result'] == ''].iloc[0]

    # DraftKings' board runs on into the next day's slate; only keep teams
    # actually playing today.
    next_game_date = datetime.strptime(next_game_df['date_game'], "%a, %b %d, %Y").date()
    if next_game_date != today:
        return False

    all_game_data_df = scrape_all_game_data_by_team(all_game_data_url)
    misc_team_data_df = scrape_misc_data_by_team(misc_team_data_url)
    played_df = upcoimng_game_df[upcoimng_game_df['game_result'] != '']

    # Cold start: before a team's first game of the season its gamelog/misc
    # tables are empty, so "last game" + season aggregates come from the end
    # of last season instead. last_game_in_season = 0 means "no game this
    # season yet" so bots.py never links this row back to a prior-season game.
    carried_over = all_game_data_df.empty or played_df.empty
    if carried_over:
        prev_gamelog_url, _, prev_upcoming_url = _team_urls(bball_ref_team_name, year - 1)
        all_game_data_df = scrape_all_game_data_by_team(prev_gamelog_url)
        prev_upcoming_df = scrape_upcoming_game_by_team(prev_upcoming_url)
        played_df = prev_upcoming_df[prev_upcoming_df['game_result'] != '']
    if misc_team_data_df is None or misc_team_data_df.empty:
        _, prev_misc_url, _ = _team_urls(bball_ref_team_name, year - 1)
        misc_team_data_df = scrape_misc_data_by_team(prev_misc_url)

    last_game_from_all_df = all_game_data_df.iloc[-1]
    last_game_from_upcoming_df = played_df.iloc[-1]

    days_since_last_game = today - datetime.strptime(last_game_from_upcoming_df['date_game'], "%a, %b %d, %Y").date()
    days_since_last_game = min(days_since_last_game.days, MAX_DAYS_SINCE_LAST_GAME)
    last_game_win_loss, curr_streak = last_game_from_upcoming_df['game_streak'].split(' ')
    last_game_was_win = 0

    if last_game_win_loss == 'W':
        last_game_was_win = 1

    all_home_games = all_game_data_df['team_game_result'][all_game_data_df['game_location'] == '@']
    all_away_games = all_game_data_df['team_game_result'][all_game_data_df['game_location'] != '@']
    home_games_win_percent = len(all_home_games[all_home_games == 'W']) / len(all_home_games) if len(all_home_games) else 0
    away_games_win_percent = len(all_away_games[all_away_games == 'W']) / len(all_away_games) if len(all_away_games) else 0

    team_pace = float(misc_team_data_df['pace_Team'].values[0])
    league_avg_pace = float(misc_team_data_df['pace_Lg Rank'].values[0])
    team_off_rank = float(misc_team_data_df['off_rtg_Team'].values[0])
    league_avg_off_rank = float(misc_team_data_df['off_rtg_Lg Rank'].values[0])
    team_def_rank = float(misc_team_data_df['def_rtg_Team'].values[0])
    league_avg_def_rank = float(misc_team_data_df['def_rtg_Lg Rank'].values[0])
    team_mov = float(misc_team_data_df['mov_Team'].values[0])
    team_mov_pos = 1
    league_avg_mov = float(misc_team_data_df['mov_Lg Rank'].values[0])
    team_srs = float(misc_team_data_df['srs_Team'].values[0])
    team_srs_pos = 1
    league_avg_srs = float(misc_team_data_df['srs_Lg Rank'].values[0])

    if team_mov < 0:
        team_mov = float(str(team_mov)[1:])
        team_mov_pos = 0
    if team_srs < 0:
        team_srs = float(str(team_srs)[1:])
        team_srs_pos = 0

    full_game_start_time = next_game_df['game_start_time']
    game_start_time = time_to_int(full_game_start_time)

    last_game_point_for = int(last_game_from_upcoming_df['pts'])
    last_game_point_against = int(last_game_from_upcoming_df['opp_pts'])
    last_game_field_goal_attempts = int(last_game_from_all_df['fga'])
    last_game_field_goal = int(last_game_from_all_df['fg'])
    last_game_turnovers = int(last_game_from_all_df['tov'])
    last_game_rebounds = int(last_game_from_all_df['trb'])
    all_field_goal_attempts = all_game_data_df['fga'].astype(int)
    all_field_goal_attempts = sum(all_field_goal_attempts) // len(all_field_goal_attempts)
    all_field_goal = all_game_data_df['fg'].astype(int)
    all_field_goal = sum(all_field_goal) // len(all_field_goal)
    all_rebounds = all_game_data_df['trb'].astype(int)
    all_rebounds = sum(all_rebounds) // len(all_rebounds)
    all_turnovers = all_game_data_df['tov'].astype(int)
    all_turnovers = sum(all_turnovers) // len(all_turnovers)

    team_avg_points_for = all_game_data_df['team_game_score'].astype(int)
    team_avg_points_for = sum(team_avg_points_for) // len(team_avg_points_for)
    team_avg_points_against = all_game_data_df['opp_team_game_score'].astype(int)
    team_avg_points_against = sum(team_avg_points_against) // len(team_avg_points_against)

    is_home = 0 if next_game_df['game_location'] == '@' else 1
    if is_home != int(is_home_side):
        raise ValueError(f'home/away mismatch between DraftKings and Basketball Reference')
    last_game_in_season = 0 if carried_over else last_game_from_upcoming_df['g']
    next_game_in_season = next_game_df['g']

    if is_home:
        spread = str(gambling_data['homeSpread'])
        money_line = str(gambling_data['homeMoneyLine'])
    else:
        spread = str(gambling_data['awaySpread'])
        money_line = str(gambling_data['awayMoneyLine'])

    last_opp_team_name = TEAM_NAME_TO_ACRONYM[last_game_from_upcoming_df['opp_name']]
    next_opp_team_name = TEAM_NAME_TO_ACRONYM[next_game_df['opp_name']]
    season_year = year
    home_spread = str(gambling_data['homeSpread'])
    over_under = gambling_data['overUnder']
    away_money_line = gambling_data['awayMoneyLine']
    home_money_line = gambling_data['homeMoneyLine']


    record_id = store_bball_data(
    days_since_last_game,
    last_game_was_win,
    curr_streak,
    home_games_win_percent,
    away_games_win_percent,
    team_pace,
    league_avg_pace,
    team_off_rank,
    league_avg_off_rank,
    team_def_rank,
    league_avg_def_rank,
    team_mov,
    team_mov_pos,
    league_avg_mov,
    team_srs,
    team_srs_pos,
    league_avg_srs,
    full_game_start_time,
    game_start_time,
    last_game_point_for,
    last_game_point_against,
    last_game_field_goal_attempts,
    last_game_field_goal,
    last_game_turnovers,
    last_game_rebounds,
    all_field_goal_attempts,
    all_field_goal,
    all_rebounds,
    all_turnovers,
    team_avg_points_for,
    team_avg_points_against,
    is_home,
    last_game_in_season,
    next_game_in_season,
    bball_ref_team_name,
    last_opp_team_name,
    next_opp_team_name,
    season_year,
    home_spread,
    spread,
    over_under,
    home_money_line,
    away_money_line,
    money_line)


    print(f"{bball_ref_team_name}: record inserted with ID: {record_id}" + (' (carried over from last season)' if carried_over else ''))
    return True
