from datetime import date, datetime

from scrapes import scrape_all_game_data_by_team, scrape_misc_data_by_team, scrape_todays_gambling_data, scrape_upcoming_game_by_team
from legends import time_to_int

today = date.today()

teams = ['DAL']


for team in teams:
    all_game_data_url = f'https://www.basketball-reference.com/teams/{team}/2026/gamelog'
    misc_team_data_url = f'https://www.basketball-reference.com/teams/{team}/2026.html'
    upcoming_game_url = f'https://www.basketball-reference.com/teams/{team}/2026_games.html'

    all_game_data_df = scrape_all_game_data_by_team(all_game_data_url)
    misc_team_data_df = scrape_misc_data_by_team(misc_team_data_url)
    gambling_data = scrape_todays_gambling_data()
    upcoimng_game_df = scrape_upcoming_game_by_team(upcoming_game_url)

    last_game_from_all_df = all_game_data_df.iloc[-1]
    last_game_from_upcoming_df = upcoimng_game_df[upcoimng_game_df['game_result'] != ''].iloc[-1]
    next_game_df = upcoimng_game_df[upcoimng_game_df['game_result'] == ''].iloc[0]
    Need to update upcoming_game_df to latest game
    
    days_since_last_game = today - datetime.strptime(last_game_from_upcoming_df['date_game'], "%a, %b %d, %Y").date()
    days_since_last_game = days_since_last_game.days
    last_game_win_loss, curr_streak = last_game_from_upcoming_df['game_streak'].split(' ')
    last_game_was_win = 0

    if last_game_win_loss == 'W':
        last_game_was_win = 1
    
    all_home_games = all_game_data_df['team_game_result'][all_game_data_df['game_location'] == '@']
    all_away_games = all_game_data_df['team_game_result'][all_game_data_df['game_location'] != '@']
    home_games_win_percent = len(all_home_games[all_home_games == 'W']) / len(all_home_games)
    away_games_win_percent = len(all_away_games[all_away_games == 'W']) / len(all_away_games)

    team_pace = float(misc_team_data_df['pace_Team'].values[0])
    league_avg_pace = float(misc_team_data_df['pace_Lg Rank'].values[0])
    team_off_rank = float(misc_team_data_df['off_rtg_Team'].values[0])
    league_avg_off_rank = float(misc_team_data_df['off_rtg_Lg Rank'].values[0])
    team_def_rank = float(misc_team_data_df['def_rtg_Team'].values[0])
    league_avg_def_rank = float(misc_team_data_df['def_rtg_Lg Rank'].values[0])
    team_mov = float(misc_team_data_df['mov_Team'].values[0])
    team_mov_pos = 0
    league_avg_mov = float(misc_team_data_df['mov_Lg Rank'].values[0])
    team_srs = float(misc_team_data_df['srs_Team'].values[0])
    team_srs_pos = 0
    league_avg_srs = float(misc_team_data_df['srs_Lg Rank'].values[0])

    if team_mov > 0:
        team_mov_pos = 1
    if team_srs > 0:
        team_srs_pos = 1

    game_start_time = time_to_int(next_game_df['game_start_time'])
    
    last_game_point_for = int(last_game_from_upcoming_df['pts'])
    last_game_point_against = int(last_game_from_upcoming_df['opp_pts'])
    last_game_field_goal_attempts = int(last_game_from_all_df['fga'])
    last_game_field_goal = int(last_game_from_all_df['fg'])
    last_game_turnovers = int(last_game_from_all_df['trb'])
    last_game_rebounds = int(last_game_from_all_df['tov'])
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

    is_home = 1 if next_game_df['game_location'] == '@' else 0
    next_game_in_season = next_game_df['g']





    