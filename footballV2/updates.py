import psycopg2
import pandas as pd
from datetime import datetime, timedelta

from constants import NFL_TEAMS, SEASON_YEAR, WEEK_DATE_RANGES
from saveNFLData import DB_CONFIG, _clean_game_log, TEAM_NUMBER_TO_PFR
from scrapes import scrape_all_game_data_by_team
from frontend import _week_start_date, _DEFAULT_DAY_CODE

team_names = [team["acronym"] for team in NFL_TEAMS]
ACRONYM_TO_PFR = {team["acronym"]: team["pfr"] for team in NFL_TEAMS}
season_year = SEASON_YEAR


def updateDBActuals(week=None):
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("SELECT * FROM NFL1 WHERE actual_spread is NULL;")
    all_data = cur.fetchall()

    colnames = [desc[0] for desc in cur.description]
    df = pd.DataFrame(all_data, columns=colnames)

    game_log_cache = {}

    for index, row in df.iterrows():
        team_name = row['team_name']
        current_game_in_season = row['next_game_in_season']

        pfr_code = ACRONYM_TO_PFR[team_name]
        if pfr_code not in game_log_cache:
            try:
                game_log_cache[pfr_code] = _clean_game_log(
                    scrape_all_game_data_by_team(pfr_code, season_year)
                )
            except Exception as exc:
                print(f"  couldn't scrape gamelog for {team_name}: {exc!r}")
                game_log_cache[pfr_code] = _clean_game_log(pd.DataFrame())
        game_log = game_log_cache[pfr_code]

        played_row = game_log[game_log['week'] == current_game_in_season]
        if played_row.empty:
            continue

        played_row = played_row.iloc[0]
        points_for = int(played_row['pts_for'])
        points_against = int(played_row['pts_against'])

        given_spread = row['spread']
        given_over_under = row['over_under']
        if given_spread[0] == '-':
            given_spread = float(given_spread[1:])
        elif given_spread[0] == '+':
            given_spread = float(given_spread[1:]) * -1
        else:
            given_spread = 0.0

        spread = points_for - points_against
        actual_spread = True if spread >= given_spread else False
        over_under = points_for + points_against
        actual_over_under = True if over_under >= float(given_over_under) else False
        actual_money_line = True if points_for > points_against else False

        try:
            update_query = f"""
            UPDATE NFL1
            SET actual_spread = {actual_spread}, actual_over_under = {actual_over_under}, actual_money_line = {actual_money_line}
            WHERE team_name = '{team_name}' and next_game_in_season = {current_game_in_season} and season_year = {season_year};"""

            cur.execute(update_query)
            conn.commit()

            print(f'Saved {team_name} for week: {current_game_in_season}')
        except Exception:
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


def _played_date(row):
    """Calendar date the game was actually played, derived the same way as the
    frontend's game-day headers (week start + day-of-week offset) - created_at
    is just when the row was scraped/inserted and doesn't track game day."""
    week_start = _week_start_date(int(row['next_game_in_season']), int(row['season_year']), WEEK_DATE_RANGES)
    day_code = row['game_day_code']
    day_code = int(day_code) if pd.notna(day_code) else _DEFAULT_DAY_CODE
    return week_start + timedelta(days=day_code)


def getPreviousPercentages():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    # Every graded game up to and including this season - early in a new season
    # that's just the prior season's backtest, which is what the frontend's
    # "model record" panel should fall back to until live results accrue.
    cur.execute(
        f"SELECT * FROM NFL1 WHERE actual_spread is not NULL and calculated_spread_test is not NULL and season_year <= {season_year};"
    )
    all_data = cur.fetchall()

    colnames = [desc[0] for desc in cur.description]
    df = pd.DataFrame(all_data, columns=colnames)

    totals = {}

    df['game_date'] = df.apply(_played_date, axis=1)
    last_games = sorted(df['game_date'].unique())[:4:-1]

    totals = getTotals(df, totals, 'overall')
    for i in range(min(5, len(last_games))):
        totals = getTotals(df[df['game_date'] == last_games[i]], totals, f'overall_prev_{i + 1}')

    for team in team_names:
        updated_df = df[df['team_name'] == team]
        totals = getTotals(updated_df, totals, team)

        all_weeks = sorted(updated_df['next_game_in_season'].unique().tolist())
        for i in range(1, 6):
            if len(all_weeks) >= i:
                week_df = updated_df[updated_df['next_game_in_season'] == all_weeks[-i]]
                totals = getTotals(week_df, totals, f'{team}_prev_{i}')

    with open('../../../Health App/health-app/app/commonComps/newPercentsFootball.js', 'w') as f:
        f.write('export const newPercentagesFootball = {\n')
        for key, value in totals.items():
            f.write(f"{key}: {value},\n")
        f.write("};")

    cur.close()
    conn.close()

    return totals
