import psycopg2
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import ElasticNet
from sklearn.linear_model import Lasso
from sklearn.linear_model import SGDRegressor
from sklearn.linear_model import Ridge
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_squared_error
from sklearn.metrics import accuracy_score
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import SGDClassifier
import pandas as pd
from constants import NFL_TEAMS, SEASON_YEAR
from saveNFLData import DB_CONFIG
import warnings
warnings.filterwarnings('ignore')

team_names = [team["acronym"] for team in NFL_TEAMS]
year = SEASON_YEAR
# NB: season_year is deliberately kept - _build_team_feature_dict needs it to
# order a team's games across seasons without week-number collisions.
columns_to_drop = ['id', 'full_game_start_time', 'team_name', 'last_opp_team_name', 'next_opp_team_name', 'home_spread', 'spread', 'over_under', 'home_money_line', 'away_money_line', 'money_line', 'actual_spread', 'actual_over_under', 'actual_money_line', 'calculated_spread', 'calculated_over_under', 'calculated_money_line', 'created_at', 'home_calculated_spread', 'home_calculated_money_line', 'parlay1_spread', 'parlay1_over_under', 'parlay1_money_line', 'parlay2_spread', 'parlay2_over_under', 'parlay2_money_line', 'parlay3_spread', 'parlay3_over_under', 'parlay3_money_line']
reg_columns_to_predict = ['points_for', 'points_against']
class_columns_to_predict = ['actual_spread', 'actual_over_under', 'actual_money_line']


def _build_team_feature_dict(team_df, class_columns=None):
    """
    Shared per-team, per-game feature extraction used by both runDaBot (points
    regression) and runDaParlays (bet-outcome classification). Mirrors
    backendV2/bots.py's feature dict, with the 5 basketball analytics columns
    (pace/off_rtg/def_rtg/mov/srs) swapped for their football equivalents and
    weather added as extra prediction inputs.
    """
    # Order the team's rows chronologically across seasons so "the next row"
    # really is the team's next game. team_df must still carry season_year
    # (runDaBot keeps it out of columns_to_drop for this reason) - otherwise a
    # week-1 row from a new season collides with week 1 of the previous one.
    team_df = team_df.sort_values(['season_year', 'next_game_in_season']).reset_index(drop=True)
    team_updated_dict = {}

    for index in range(len(team_df)):
        current = team_df.iloc[index]
        game = current['next_game_in_season']

        # This game's actual points live on the team's NEXT chronological row
        # (as last_game_point_for/against) - but only when that row is the same
        # season and links straight back to this game. Otherwise it's unplayed
        # (or a season boundary) and stays -1, i.e. a prediction target.
        points_for = points_against = -1
        if index + 1 < len(team_df):
            nxt = team_df.iloc[index + 1]
            if nxt['season_year'] == current['season_year'] and nxt['last_game_in_season'] == game:
                points_for = nxt['last_game_point_for']
                points_against = nxt['last_game_point_against']

        row = {
            'weeks_since_last_game': current['weeks_since_last_game'],
            'last_game_was_win': current['last_game_was_win'],
            'curr_streak': current['curr_streak'],
            'home_games_win_percent': current['home_games_win_percent'],
            'away_games_win_percent': current['away_games_win_percent'],
            'league_avg_total_yards': current['league_avg_total_yards'],
            'team_third_down_pct': current['team_third_down_pct'],
            'league_avg_third_down_pct': current['league_avg_third_down_pct'],
            'team_avg_points_against': current['team_avg_points_against'],
            'league_avg_points_against': current['league_avg_points_against'],
            'team_point_diff': current['team_point_diff'],
            'team_point_diff_pos': current['team_point_diff_pos'],
            'league_avg_point_diff': current['league_avg_point_diff'],
            'team_giveaways_season': current['team_giveaways_season'],
            'league_avg_giveaways_season': current['league_avg_giveaways_season'],
            'game_start_time': current['game_start_time'],
            'weather_code': current['weather_code'],
            'temp_f': current['temp_f'],
            'wind_mph': current['wind_mph'],
            'game_channel': current['game_channel'],
            'points_for': points_for,
            'points_against': points_against,
            'last_game_pass_yards': current['last_game_pass_yards'],
            'last_game_rush_yards': current['last_game_rush_yards'],
            'last_game_turnovers': current['last_game_turnovers'],
            'last_game_sacks_allowed': current['last_game_sacks_allowed'],
            'all_pass_yards': current['all_pass_yards'],
            'all_rush_yards': current['all_rush_yards'],
            'all_sacks_allowed': current['all_sacks_allowed'],
            'all_turnovers': current['all_turnovers'],
            'team_avg_points_for': current['team_avg_points_for'],
            'is_home': current['is_home'],
            'game_in_season': game,
            'season': current['season_year'],
        }

        if class_columns is not None:
            row['calculated_spread_test'] = current['calculated_spread_test']
            row['calculated_over_under_test'] = current['calculated_over_under_test']
            row['calculated_money_line_test'] = current['calculated_money_line_test']
            row['actual_spread'] = current['actual_spread']
            row['actual_over_under'] = current['actual_over_under']
            row['actual_money_line'] = current['actual_money_line']

        team_updated_dict[index] = row

    return pd.DataFrame.from_dict(team_updated_dict, orient='index')


def runDaBot(week, season=None):
    season = year if season is None else season

    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("SELECT * FROM NFL1;")
    all_data = cur.fetchall()

    colnames = [desc[0] for desc in cur.description]
    all_data_df = pd.DataFrame(all_data, columns=colnames)

    weeks_games = all_data_df[
        (all_data_df['next_game_in_season'] == week) & (all_data_df['season_year'] == season)
    ]

    list_of_games = weeks_games[weeks_games['is_home'] == 1][['team_name', 'next_opp_team_name']].values.tolist()
    # Structure: hometeam pos 0, awayteam pos 1
    both_team_errors = {}

    for game in list_of_games:
        home_team = game[0]
        away_team = game[1]

        all_home_team_df = all_data_df[all_data_df['team_name'] == home_team]
        all_away_team_df = all_data_df[all_data_df['team_name'] == away_team]

        home_team_df = all_home_team_df.drop(columns=columns_to_drop)
        away_team_df = all_away_team_df.drop(columns=columns_to_drop)

        both_team_errors[f'{away_team}_{home_team}'] = 0
        both_team_predictions = {f'{home_team}_points_for': 0, f'{home_team}_points_against': 0, f'{away_team}_points_for': 0, f'{away_team}_points_against': 0}

        # Not enough played games yet (early season) to train a regression -
        # leave this matchup's calculated_* columns null and move on.
        insufficient_history = False
        for team_df in (home_team_df, away_team_df):
            trainable = _build_team_feature_dict(team_df)
            if len(trainable[trainable['points_for'] != -1]) < 8:
                insufficient_history = True
        if insufficient_history:
            print(f"  skipping {away_team} @ {home_team} (week {week}, {season}) - not enough history")
            continue

        for team_index, team_df in enumerate([home_team_df, away_team_df]):
            team_updated_df = _build_team_feature_dict(team_df)
            # The row we're predicting is this exact (week, season) game - not
            # just "any row without a result" (a team's last game of a prior
            # season also has no linked result).
            target_mask = (
                (team_updated_df['game_in_season'] == week)
                & (team_updated_df['season'] == season)
            )
            team_updated_df = team_updated_df.drop(columns=['season'])
            team_data_to_predict = team_updated_df[target_mask.values]
            team_data_to_predict = team_data_to_predict.drop(columns=reg_columns_to_predict)
            team_updated_df = team_updated_df[team_updated_df['points_for'] != -1]

            for column in reg_columns_to_predict:
                y = team_updated_df[column]
                X = team_updated_df.drop(columns=reg_columns_to_predict)

                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.19, random_state=19)

                if len(X_train) == 1:
                    break

                scalar = StandardScaler()
                scalar.fit(X_train)
                X_train = scalar.transform(X_train)
                X_test = scalar.transform(X_test)

                alphas = [0.0001, 0.001, 0.01, 0.1, 1.0, 10.0, 100.0, 1000.0]
                elasticNetParams = [{'alpha': alphas}]
                lassoParams = [{'alpha': alphas}]
                SGDParams = [{'alpha': alphas}]
                ridgeParams = [{'alpha': alphas}]

                elasticNet = ElasticNet(random_state=19)
                lasso = Lasso(random_state=19)
                SGD = SGDRegressor(max_iter=1000, tol=1e-3)
                ridge = Ridge(random_state=19)

                elasticNetGS = GridSearchCV(elasticNet, elasticNetParams, cv=3, scoring='neg_mean_absolute_error')
                elasticNetGS.fit(X_train, y_train)
                bestElasticNet3 = ElasticNet(alpha=elasticNetGS.best_params_['alpha'], random_state=19)
                lassoGS = GridSearchCV(lasso, lassoParams, cv=3, scoring='neg_mean_absolute_error')
                lassoGS.fit(X_train, y_train)
                bestLasso3 = Lasso(alpha=lassoGS.best_params_['alpha'], random_state=19)
                SGDGS = GridSearchCV(SGD, SGDParams, cv=3, scoring='neg_mean_absolute_error')
                SGDGS.fit(X_train, y_train)
                bestSGD3 = SGDRegressor(alpha=SGDGS.best_params_['alpha'], max_iter=1000, tol=1e-3, random_state=19)
                ridgeGS = GridSearchCV(ridge, ridgeParams, cv=3, scoring='neg_mean_absolute_error')
                ridgeGS.fit(X_train, y_train)
                bestRidge3 = Ridge(alpha=ridgeGS.best_params_['alpha'], random_state=19)

                bestElasticNet3.fit(X_train, y_train)
                elasticNet3Score = mean_squared_error(y_test, bestElasticNet3.predict(X_test))
                bestLasso3.fit(X_train, y_train)
                lasso3Score = mean_squared_error(y_test, bestLasso3.predict(X_test))
                bestSGD3.fit(X_train, y_train)
                SGD3Score = mean_squared_error(y_test, bestSGD3.predict(X_test))
                bestRidge3.fit(X_train, y_train)
                ridge3Score = mean_squared_error(y_test, bestRidge3.predict(X_test))

                allScores = {'elasticNet3Score': elasticNet3Score, 'lasso3Score': lasso3Score, 'SGD3Score': SGD3Score, 'ridge3Score': ridge3Score}
                allBestModels = {'elasticNet3Score': bestElasticNet3, 'lasso3Score': bestLasso3, 'SGD3Score': bestSGD3, 'ridge3Score': bestRidge3}

                bestScore = min(allScores, key=allScores.get)
                bestModel = allBestModels[bestScore]

                updated_team_data_to_predict = scalar.transform(team_data_to_predict)
                result = int(bestModel.predict(updated_team_data_to_predict)[0])

                both_team_errors[f'{away_team}_{home_team}'] = both_team_errors[f'{away_team}_{home_team}'] + allScores[bestScore]

                if team_index == 0:
                    if column == 'points_for':
                        both_team_predictions[f'{home_team}_points_for'] = result
                    else:
                        both_team_predictions[f'{home_team}_points_against'] = result
                else:
                    if column == 'points_for':
                        both_team_predictions[f'{away_team}_points_for'] = result
                    else:
                        both_team_predictions[f'{away_team}_points_against'] = result

        home_team_current_game = all_home_team_df[
            (all_home_team_df['next_game_in_season'] == week)
            & (all_home_team_df['season_year'] == season)
        ]
        away_team_current_game = all_away_team_df[
            (all_away_team_df['next_game_in_season'] == week)
            & (all_away_team_df['season_year'] == season)
        ]

        home_team_current_game_id = home_team_current_game['id'].values[0]
        away_team_current_game_id = away_team_current_game['id'].values[0]
        home_team_spread = home_team_current_game['spread'].values[0]
        home_team_over_under = home_team_current_game['over_under'].values[0]

        home_team_points_for = (both_team_predictions[f'{home_team}_points_for'] + both_team_predictions[f'{away_team}_points_against']) // 2
        away_team_points_for = (both_team_predictions[f'{home_team}_points_against'] + both_team_predictions[f'{away_team}_points_for']) // 2

        home_money_line = False
        away_money_line = False
        if home_team_points_for >= away_team_points_for:
            home_money_line = True
        else:
            away_money_line = True

        home_spread = False
        away_spread = False
        if home_team_spread[0] == '-':
            home_team_spread = float(home_team_spread[1:])
            if home_team_points_for - away_team_points_for > home_team_spread:
                home_spread = True
            else:
                away_spread = True
        else:
            home_team_spread = float(home_team_spread[1:]) * -1
            if home_team_points_for - away_team_points_for > home_team_spread:
                home_spread = True
            else:
                away_spread = True

        over_under = False
        if (home_team_points_for + away_team_points_for) > home_team_over_under:
            over_under = True

        home_team_insert_query = f"""
        UPDATE NFL1
        SET calculated_spread_test = {home_spread}, calculated_money_line_test = {home_money_line}, calculated_over_under_test = {over_under}, home_calculated_spread_test = {home_spread}, home_calculated_money_line_test = {home_money_line}
        WHERE id = {home_team_current_game_id};"""
        cur.execute(home_team_insert_query)
        conn.commit()

        away_team_insert_query = f"""
        UPDATE NFL1
        SET calculated_spread_test = {away_spread}, calculated_money_line_test = {away_money_line}, calculated_over_under_test = {over_under}, home_calculated_spread_test = {home_spread}, home_calculated_money_line_test = {home_money_line}
        WHERE id = {away_team_current_game_id};"""
        cur.execute(away_team_insert_query)
        conn.commit()

    cur.close()
    conn.close()

    sorted_teams_by_errors = sorted(both_team_errors.items(), key=lambda item: item[1])
    return sorted_teams_by_errors


def runDaParlays(confidenceScores, percentTotals):
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("SELECT * FROM NFL1;")
    all_data = cur.fetchall()

    colnames = [desc[0] for desc in cur.description]
    all_data_df = pd.DataFrame(all_data, columns=colnames)

    lessThan200Games = confidenceScores
    lessThan500Games = [(name, val) for name, val in confidenceScores if val < 500]
    allGames = confidenceScores

    for sectionIndex, confidenceScoreSection in enumerate([lessThan200Games, lessThan500Games, allGames]):
        sectionIndex = sectionIndex + 1
        print('----------------')
        for confidenceScore in confidenceScoreSection:
            teams, score = confidenceScore
            awayTeam, homeTeam = teams.split('_')
            teamsScores = {'spread': 0, 'overUnder': 0, 'moneyLine': 0}
            teamIds = {'home': -1, 'away': -1}

            home_team_df = all_data_df[(all_data_df['team_name'] == homeTeam) & (all_data_df['home_calculated_spread_test'].notna())]
            away_team_df = all_data_df[(all_data_df['team_name'] == awayTeam) & (all_data_df['home_calculated_spread_test'].notna())]

            for team_index, team_df in enumerate([home_team_df, away_team_df]):
                team_updated_df = _build_team_feature_dict(team_df, class_columns=class_columns_to_predict)
                team_updated_df = team_updated_df.drop(columns=['season'])
                team_data_to_predict = team_updated_df[team_updated_df['actual_spread'].isna()]
                team_data_to_predict = team_data_to_predict.iloc[[-1]] if len(team_data_to_predict) > 1 else team_data_to_predict
                team_updated_df = team_updated_df[team_updated_df['actual_spread'].notna()]

                # The row we're predicting (and writing parlay_* back to) is the
                # team's game that hasn't been played yet - NOT team_df's last
                # row, which isn't reliably ordered and may be a prior season.
                pending = team_df[team_df['actual_spread'].isna()]
                target_id = (pending if not pending.empty else team_df).iloc[-1]['id']
                teamIds['home' if team_index == 0 else 'away'] = target_id

                for column in class_columns_to_predict:
                    y = team_updated_df[column]
                    X = team_updated_df.drop(columns=class_columns_to_predict)
                    X_to_predict = team_data_to_predict.drop(columns=class_columns_to_predict)

                    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.19, random_state=19)
                    if y_train.nunique() == 1:
                        break

                    y_train = y_train.astype(int)
                    y_test = y_test.astype(int)

                    if len(X_train) == 1:
                        break

                    scalar = StandardScaler()
                    scalar.fit(X_train)
                    X_train = scalar.transform(X_train)
                    X_test = scalar.transform(X_test)

                    C = [0.00001, 0.0001, 0.001, 0.01, 0.1, 1.0, 10.0, 100.0, 1000.0]
                    alphas = [0.000001, 0.00001, 0.0001, 0.001, 0.01, 0.1, 1.0, 10.0, 100.0, 1000.0]
                    neighbors = [2, 3, 5, 7]

                    CParams = [{'C': C}]
                    alphaParams = [{'alpha': alphas}]
                    KNNParams = [{'n_neighbors': neighbors}]

                    SVCModel = SVC(probability=True, random_state=19)
                    KNN = KNeighborsClassifier()
                    LogReg = LogisticRegression(max_iter=7000, random_state=19)
                    SGDCModel = SGDClassifier(loss='log_loss', max_iter=7000, tol=1e-3, random_state=19)

                    SVCGS3 = GridSearchCV(SVCModel, CParams, cv=3)
                    SVCGS3.fit(X_train, y_train)
                    bestSVC3 = SVC(C=SVCGS3.best_params_['C'], probability=True, random_state=19)
                    KNNGS3 = GridSearchCV(KNN, KNNParams, cv=3)
                    KNNGS3.fit(X_train, y_train)
                    bestKNN3 = KNeighborsClassifier(n_neighbors=KNNGS3.best_params_['n_neighbors'])
                    LRGS3 = GridSearchCV(LogReg, CParams, cv=3)
                    LRGS3.fit(X_train, y_train)
                    bestLR3 = LogisticRegression(C=LRGS3.best_params_['C'], max_iter=1000, random_state=19)
                    SGDCGS3 = GridSearchCV(SGDCModel, alphaParams, cv=3)
                    SGDCGS3.fit(X_train, y_train)
                    bestSGDC3 = SGDClassifier(loss='log_loss', alpha=SGDCGS3.best_params_['alpha'], max_iter=1000, tol=1e-3, random_state=19)

                    bestSVC3.fit(X_train, y_train)
                    bestSVC3Score = accuracy_score(y_test, bestSVC3.predict(X_test))
                    bestKNN3.fit(X_train, y_train)
                    bestKNN3Score = accuracy_score(y_test, bestKNN3.predict(X_test))
                    bestLR3.fit(X_train, y_train)
                    bestLR3Score = accuracy_score(y_test, bestLR3.predict(X_test))
                    bestSGDC3.fit(X_train, y_train)
                    bestSGDC3Score = accuracy_score(y_test, bestSGDC3.predict(X_test))

                    allScores = {'bestSVC3Score': bestSVC3Score, 'bestKNN3Score': bestKNN3Score, 'bestLR3Score': bestLR3Score, 'bestSGDC3Score': bestSGDC3Score}
                    allBestModels = {'bestSVC3Score': bestSVC3, 'bestKNN3Score': bestKNN3, 'bestLR3Score': bestLR3, 'bestSGDC3Score': bestSGDC3}

                    bestScore = max(allScores, key=allScores.get)
                    bestModel = allBestModels[bestScore]
                    firstClass, secondClass = bestModel.classes_
                    updated_team_data_to_predict = scalar.transform(X_to_predict)

                    if column == 'actual_spread':
                        teamSpread = int(X_to_predict['calculated_spread_test'])
                        prediction = bestModel.predict(updated_team_data_to_predict)[0]
                        prediction_prob = bestModel.predict_proba(updated_team_data_to_predict)[0]

                        if teamSpread == prediction:
                            if teamSpread == 0:
                                teamsScores['spread'] = teamsScores['spread'] + prediction_prob[0]
                            if teamSpread == 1:
                                teamsScores['spread'] = teamsScores['spread'] + prediction_prob[1]

                    elif column == 'actual_over_under':
                        teamOverUnder = int(X_to_predict['calculated_over_under_test'])
                        prediction = bestModel.predict(updated_team_data_to_predict)[0]
                        prediction_prob = bestModel.predict_proba(updated_team_data_to_predict)[0]

                        if teamOverUnder == prediction:
                            if teamOverUnder == 0:
                                teamsScores['overUnder'] = teamsScores['overUnder'] + prediction_prob[0]
                            if teamOverUnder == 1:
                                teamsScores['overUnder'] = teamsScores['overUnder'] + prediction_prob[1]

                    elif column == 'actual_money_line':
                        teamMoneyLine = int(X_to_predict['calculated_money_line_test'])
                        prediction = bestModel.predict(updated_team_data_to_predict)[0]
                        prediction_prob = bestModel.predict_proba(updated_team_data_to_predict)[0]

                        if teamMoneyLine == prediction:
                            if teamMoneyLine == 0:
                                teamsScores['moneyLine'] = teamsScores['moneyLine'] + prediction_prob[0]
                            if teamMoneyLine == 1:
                                teamsScores['moneyLine'] = teamsScores['moneyLine'] + prediction_prob[1]

            threshold = 1 if sectionIndex != 1 else 1.69

            for bet_type, column_name in (('spread', 'spread'), ('overUnder', 'over_under'), ('moneyLine', 'money_line')):
                hit = teamsScores[bet_type] > threshold
                if hit:
                    print(homeTeam, awayTeam, bet_type)
                    print(teamsScores[bet_type])

                home_query = f"""
                UPDATE NFL1
                SET parlay{sectionIndex}_{column_name} = {hit}
                WHERE id = {teamIds['home']};"""
                cur.execute(home_query)
                conn.commit()

                away_query = f"""
                UPDATE NFL1
                SET parlay{sectionIndex}_{column_name} = {hit}
                WHERE id = {teamIds['away']};"""
                cur.execute(away_query)
                conn.commit()

    cur.close()
    conn.close()
