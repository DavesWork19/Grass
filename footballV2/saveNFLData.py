from datetime import date
import pandas as pd
import psycopg2

from scrapes import (
    scrape_all_game_data_by_team,
    scrape_weekly_gambling_data,
    scrape_weekly_weather_and_schedule,
)
from legends import getTeamNumber, get_current_week
from constants import NFL_TEAMS, SEASON_YEAR, WEEK_DATE_RANGES

TEAM_NUMBER_TO_ACRONYM = {i: team["acronym"] for i, team in enumerate(NFL_TEAMS)}
TEAM_NUMBER_TO_PFR = {i: team["pfr"] for i, team in enumerate(NFL_TEAMS)}

DB_CONFIG = {
    'host': 'localhost',
    'database': 'postgres',
    'user': 'postgres',
    'password': 'Sinorrabb1t',
    'port': 5432,
}


def _clean_game_log(raw_df):
    """
    Normalize scrape_all_game_data_by_team's DataFrame (already named, one row
    per played game) into typed columns, sorted oldest -> newest.
    """
    cols = [
        'week', 'game_result', 'game_location', 'opp_name', 'pts_for',
        'pts_against', 'pass_yds', 'pass_int', 'sacks_allowed', 'rush_yds',
        'third_down_conv', 'third_down_att',
    ]
    if raw_df.empty:
        return pd.DataFrame(columns=cols)

    clean = pd.DataFrame({
        'week': pd.to_numeric(raw_df['week'], errors='coerce'),
        'game_result': raw_df['game_result'],
        'game_location': raw_df['game_location'].fillna(''),
        'opp_name': raw_df['opp_name'],
        'pts_for': pd.to_numeric(raw_df['pts_for'], errors='coerce'),
        'pts_against': pd.to_numeric(raw_df['pts_against'], errors='coerce'),
        'pass_yds': pd.to_numeric(raw_df['pass_yds'], errors='coerce'),
        'pass_int': pd.to_numeric(raw_df['pass_int'], errors='coerce'),
        'sacks_allowed': pd.to_numeric(raw_df['sacks_allowed'], errors='coerce'),
        'rush_yds': pd.to_numeric(raw_df['rush_yds'], errors='coerce'),
        'third_down_conv': pd.to_numeric(raw_df['third_down_conv'], errors='coerce'),
        'third_down_att': pd.to_numeric(raw_df['third_down_att'], errors='coerce'),
    })
    clean = clean.dropna(subset=['week'])
    clean['week'] = clean['week'].astype(int)
    return clean.sort_values('week').reset_index(drop=True)


def _team_season_features(game_log):
    """
    Derive the streak/win%/rolling-average features for one team from its
    cleaned season game log (may be empty for a team's week-1 game).
    """
    if len(game_log) == 0:
        return {
            'last_game_in_season': None,
            'last_opp_name': '',
            'weeks_since_last_game': 0,
            'last_game_was_win': 0,
            'curr_streak': 0,
            'home_games_win_percent': 0.0,
            'away_games_win_percent': 0.0,
            'team_avg_total_yards': 0,
            'team_third_down_pct': 0.0,
            'team_avg_points_against': 0,
            'team_point_diff': 0,
            'team_point_diff_pos': 1,
            'team_giveaways_season': 0,
            'last_game_point_for': 0,
            'last_game_point_against': 0,
            'last_game_pass_yards': 0,
            'last_game_rush_yards': 0,
            'last_game_turnovers': 0,
            'last_game_sacks_allowed': 0,
            'all_pass_yards': 0,
            'all_rush_yards': 0,
            'all_sacks_allowed': 0,
            'all_turnovers': 0,
            'team_avg_points_for': 0,
        }

    last_game = game_log.iloc[-1]

    last_game_was_win = 1 if last_game['game_result'] == 'W' else 0
    curr_streak = 0
    for result in game_log['game_result'].iloc[::-1]:
        if result == last_game['game_result']:
            curr_streak += 1
        else:
            break

    # '@' marks an away game on PFR's gamelog; blank marks home.
    home_games = game_log[game_log['game_location'] != '@']
    away_games = game_log[game_log['game_location'] == '@']
    home_win_pct = (
        (home_games['game_result'] == 'W').sum() / len(home_games) if len(home_games) else 0.0
    )
    away_win_pct = (
        (away_games['game_result'] == 'W').sum() / len(away_games) if len(away_games) else 0.0
    )

    total_third_down_att = int(game_log['third_down_att'].fillna(0).sum())
    total_third_down_conv = int(game_log['third_down_conv'].fillna(0).sum())
    third_down_pct = (total_third_down_conv / total_third_down_att) if total_third_down_att else 0.0

    point_diff = int(game_log['pts_for'].sum() - game_log['pts_against'].sum())

    return {
        'last_game_in_season': int(last_game['week']),
        'last_opp_name': last_game['opp_name'],
        'last_game_was_win': last_game_was_win,
        'curr_streak': curr_streak,
        'home_games_win_percent': home_win_pct * 100,
        'away_games_win_percent': away_win_pct * 100,
        'team_avg_total_yards': int((game_log['pass_yds'] + game_log['rush_yds']).mean()),
        'team_third_down_pct': third_down_pct,
        'team_avg_points_against': int(game_log['pts_against'].mean()),
        'team_point_diff': abs(point_diff),
        'team_point_diff_pos': 1 if point_diff >= 0 else 0,
        'team_giveaways_season': int(game_log['pass_int'].sum()),
        'last_game_point_for': int(last_game['pts_for']),
        'last_game_point_against': int(last_game['pts_against']),
        'last_game_pass_yards': int(last_game['pass_yds']),
        'last_game_rush_yards': int(last_game['rush_yds']),
        'last_game_turnovers': int(last_game['pass_int']),
        'last_game_sacks_allowed': int(last_game['sacks_allowed']),
        'all_pass_yards': int(game_log['pass_yds'].mean()),
        'all_rush_yards': int(game_log['rush_yds'].mean()),
        'all_sacks_allowed': int(game_log['sacks_allowed'].mean()),
        'all_turnovers': int(game_log['pass_int'].mean()),
        'team_avg_points_for': int(game_log['pts_for'].mean()),
    }


def store_nfl_data(
    weeks_since_last_game,
    last_game_was_win,
    curr_streak,
    home_games_win_percent,
    away_games_win_percent,
    team_avg_total_yards,
    team_third_down_pct,
    team_avg_points_against,
    team_point_diff,
    team_point_diff_pos,
    team_giveaways_season,
    full_game_start_time,
    game_start_time,
    last_game_point_for,
    last_game_point_against,
    last_game_pass_yards,
    last_game_rush_yards,
    last_game_turnovers,
    last_game_sacks_allowed,
    all_pass_yards,
    all_rush_yards,
    all_sacks_allowed,
    all_turnovers,
    team_avg_points_for,
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
    money_line,
    weather_code,
    temp_f,
    wind_mph,
    game_channel,
    game_day_code=None,
):
    """
    Store one team's weekly NFL prediction-input row into Postgres.

    game_day_code is the game's day within its NFL week (0=Wed ... 6=Tue, see
    legends.getDay) - the frontend groups a week's games by actual calendar
    day, so this is what lets updateFrontendGames rebuild that day per game.

    Returns:
        int: ID of inserted record
    """
    today = date.today()

    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    create_table_query = """
    CREATE TABLE IF NOT EXISTS NFL1 (
        id SERIAL PRIMARY KEY,
        weeks_since_last_game INT,
        last_game_was_win INT,
        curr_streak INT,
        home_games_win_percent FLOAT,
        away_games_win_percent FLOAT,
        team_avg_total_yards FLOAT,
        league_avg_total_yards FLOAT,
        team_third_down_pct FLOAT,
        league_avg_third_down_pct FLOAT,
        team_avg_points_against FLOAT,
        league_avg_points_against FLOAT,
        team_point_diff FLOAT,
        team_point_diff_pos INT,
        league_avg_point_diff FLOAT,
        team_giveaways_season INT,
        league_avg_giveaways_season FLOAT,
        full_game_start_time VARCHAR(20),
        game_start_time INT,
        last_game_point_for INT,
        last_game_point_against INT,
        last_game_pass_yards INT,
        last_game_rush_yards INT,
        last_game_turnovers INT,
        last_game_sacks_allowed INT,
        all_pass_yards INT,
        all_rush_yards INT,
        all_sacks_allowed INT,
        all_turnovers INT,
        team_avg_points_for INT,
        is_home INT,
        last_game_in_season INT,
        next_game_in_season INT,
        team_name VARCHAR(10),
        last_opp_team_name VARCHAR(10),
        next_opp_team_name VARCHAR(10),
        season_year INT,
        home_spread VARCHAR(10),
        spread VARCHAR(10),
        over_under FLOAT,
        home_money_line VARCHAR(10),
        away_money_line VARCHAR(10),
        money_line VARCHAR(10),
        weather_code INT,
        temp_f INT,
        wind_mph INT,
        game_channel INT,
        actual_spread BOOLEAN,
        actual_over_under BOOLEAN,
        actual_money_line BOOLEAN,
        calculated_spread BOOLEAN,
        calculated_over_under BOOLEAN,
        calculated_money_line BOOLEAN,
        calculated_spread_test BOOLEAN,
        calculated_over_under_test BOOLEAN,
        calculated_money_line_test BOOLEAN,
        home_calculated_spread BOOLEAN,
        home_calculated_money_line BOOLEAN,
        home_calculated_spread_test BOOLEAN,
        home_calculated_money_line_test BOOLEAN,
        parlay1_spread BOOLEAN,
        parlay1_over_under BOOLEAN,
        parlay1_money_line BOOLEAN,
        parlay2_spread BOOLEAN,
        parlay2_over_under BOOLEAN,
        parlay2_money_line BOOLEAN,
        parlay3_spread BOOLEAN,
        parlay3_over_under BOOLEAN,
        parlay3_money_line BOOLEAN,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
    cur.execute(create_table_query)
    # NFL1 predates this column - add it for tables created before this change.
    cur.execute("ALTER TABLE NFL1 ADD COLUMN IF NOT EXISTS game_day_code SMALLINT")

    insert_query = f"""
    INSERT INTO NFL1 (
        weeks_since_last_game, last_game_was_win, curr_streak,
        home_games_win_percent, away_games_win_percent,
        team_avg_total_yards, team_third_down_pct, team_avg_points_against,
        team_point_diff, team_point_diff_pos, team_giveaways_season,
        full_game_start_time, game_start_time, last_game_point_for, last_game_point_against,
        last_game_pass_yards, last_game_rush_yards, last_game_turnovers, last_game_sacks_allowed,
        all_pass_yards, all_rush_yards, all_sacks_allowed, all_turnovers, team_avg_points_for,
        is_home, last_game_in_season, next_game_in_season, team_name, last_opp_team_name,
        next_opp_team_name, season_year, home_spread, spread, over_under, home_money_line,
        away_money_line, money_line, weather_code, temp_f, wind_mph, game_channel, game_day_code, created_at
    ) VALUES (
        {weeks_since_last_game}, {last_game_was_win}, {curr_streak},
        {home_games_win_percent}, {away_games_win_percent},
        {team_avg_total_yards}, {team_third_down_pct}, {team_avg_points_against},
        {team_point_diff}, {team_point_diff_pos}, {team_giveaways_season},
        '{full_game_start_time}', {game_start_time}, {last_game_point_for}, {last_game_point_against},
        {last_game_pass_yards}, {last_game_rush_yards}, {last_game_turnovers}, {last_game_sacks_allowed},
        {all_pass_yards}, {all_rush_yards}, {all_sacks_allowed}, {all_turnovers}, {team_avg_points_for},
        {is_home}, {last_game_in_season if last_game_in_season is not None else 'NULL'}, {next_game_in_season}, '{team_name}', '{last_opp_team_name}',
        '{next_opp_team_name}', {season_year}, '{home_spread}', '{spread}', {over_under}, '{home_money_line}',
        '{away_money_line}', '{money_line}', {weather_code}, {temp_f}, {wind_mph}, {game_channel},
        {game_day_code if game_day_code is not None else 'NULL'}, '{today}'
    ) RETURNING id
    """

    cur.execute(insert_query)
    record_id = cur.fetchone()[0]

    conn.commit()
    cur.close()
    conn.close()

    return record_id


def compute_league_averages(week, season_year=SEASON_YEAR):
    """
    Fill in this week's league_avg_* columns from the average of every team's
    own-team value inserted this week - the football equivalent of scraping
    basketball-reference's "Team vs Lg Rank" misc page, which PFR has no
    analogue for.
    """
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    league_avg_pairs = [
        ('team_avg_total_yards', 'league_avg_total_yards'),
        ('team_third_down_pct', 'league_avg_third_down_pct'),
        ('team_avg_points_against', 'league_avg_points_against'),
        ('team_point_diff', 'league_avg_point_diff'),
        ('team_giveaways_season', 'league_avg_giveaways_season'),
    ]

    for own_col, league_col in league_avg_pairs:
        update_query = f"""
        UPDATE NFL1 SET {league_col} = (
            SELECT AVG({own_col}) FROM NFL1
            WHERE next_game_in_season = {week} AND season_year = {season_year}
        )
        WHERE next_game_in_season = {week} AND season_year = {season_year}
        """
        cur.execute(update_query)
        conn.commit()

    cur.close()
    conn.close()


def _find_weather_row(weather_df, away_team_number, home_team_number):
    if weather_df.empty:
        return None
    for _, row in weather_df.iterrows():
        if (
            getTeamNumber(row['away_team_full']) == away_team_number
            and getTeamNumber(row['home_team_full']) == home_team_number
        ):
            return row
    return None


def _clear_existing_week(week, season_year):
    """Make saveData safe to re-run for a week it already inserted (crash
    recovery, or just running it twice) - without this, every rerun would
    duplicate that week's rows instead of replacing them."""
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    try:
        cur.execute(
            "DELETE FROM NFL1 WHERE next_game_in_season = %s AND season_year = %s",
            (week, season_year),
        )
        if cur.rowcount:
            print(f'Cleared {cur.rowcount} existing rows for week {week}, {season_year} before reinserting.')
        conn.commit()
    except psycopg2.errors.UndefinedTable:
        conn.rollback()  # first run ever - table doesn't exist yet
    finally:
        cur.close()
        conn.close()


def saveData(week=None):
    today = date.today()

    if week is None:
        week = get_current_week(today, WEEK_DATE_RANGES)
        if week is None:
            print('No active NFL week found for today - nothing to save.')
            return

    _clear_existing_week(week, SEASON_YEAR)

    gambling_data = scrape_weekly_gambling_data(week, SEASON_YEAR, WEEK_DATE_RANGES)
    weather_data = scrape_weekly_weather_and_schedule(SEASON_YEAR, week)

    for _, matchup in gambling_data.iterrows():
        away_team_number = getTeamNumber(matchup['awayTeam'])
        home_team_number = getTeamNumber(matchup['homeTeam'])

        if away_team_number is None or home_team_number is None:
            print(f"Could not resolve teams for matchup: {matchup['awayTeam']} @ {matchup['homeTeam']}")
            continue

        weather_row = _find_weather_row(weather_data, away_team_number, home_team_number)
        if weather_row is not None:
            full_game_start_time = f"{weather_row['time_code']}:00"
            game_start_time = int(weather_row['time_code']) * 6
            weather_code = int(weather_row['weather_code'])
            temp_f = int(weather_row['temp_f'])
            wind_mph = int(weather_row['wind_mph'])
            game_channel = int(weather_row['channel_code'])
            game_day_code = int(weather_row['day_code'])
        else:
            full_game_start_time = ''
            game_start_time = 0
            weather_code = 0
            temp_f = 70
            wind_mph = 0
            game_channel = 0
            game_day_code = None

        for team_number, is_home, opp_team_number in (
            (away_team_number, 0, home_team_number),
            (home_team_number, 1, away_team_number),
        ):
            pfr_code = TEAM_NUMBER_TO_PFR[team_number]
            acronym = TEAM_NUMBER_TO_ACRONYM[team_number]
            opp_acronym = TEAM_NUMBER_TO_ACRONYM[opp_team_number]

            game_log = _clean_game_log(scrape_all_game_data_by_team(pfr_code, SEASON_YEAR))
            features = _team_season_features(game_log)

            last_game_in_season = features['last_game_in_season']
            weeks_since_last_game = (
                (week - last_game_in_season) if last_game_in_season is not None else 0
            )

            last_opp_team_number = getTeamNumber(features['last_opp_name']) if features['last_opp_name'] else None
            last_opp_acronym = (
                TEAM_NUMBER_TO_ACRONYM[last_opp_team_number]
                if last_opp_team_number is not None
                else opp_acronym
            )

            spread = str(matchup['homeSpread'] if is_home else matchup['awaySpread'])
            money_line = str(matchup['homeMoneyLine'] if is_home else matchup['awayMoneyLine'])
            home_spread = str(matchup['homeSpread'])
            over_under = matchup['overUnder']
            home_money_line = str(matchup['homeMoneyLine'])
            away_money_line = str(matchup['awayMoneyLine'])

            record_id = store_nfl_data(
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
                full_game_start_time,
                game_start_time,
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
                SEASON_YEAR,
                home_spread,
                spread,
                over_under,
                home_money_line,
                away_money_line,
                money_line,
                weather_code,
                temp_f,
                wind_mph,
                game_channel,
                game_day_code,
            )

            print(f"Record inserted with ID: {record_id}")

    compute_league_averages(week, SEASON_YEAR)
