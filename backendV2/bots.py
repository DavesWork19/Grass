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
from datetime import datetime, timedelta
import pandas as pd
from constants import NBA_TEAMS, current_season_year
import warnings
warnings.filterwarnings('ignore')

team_names = [team["acronym"] for team in NBA_TEAMS]
year = current_season_year()
columns_to_drop = ['id','full_game_start_time','team_name','last_opp_team_name', 'next_opp_team_name', 'season_year','home_spread', 'spread', 'over_under', 'home_money_line','away_money_line', 'money_line', 'actual_spread', 'actual_over_under', 'actual_money_line', 'calculated_spread', 'calculated_over_under','calculated_money_line', 'created_at', 'home_calculated_spread','home_calculated_money_line','parlay1_spread','parlay1_over_under','parlay1_money_line','parlay2_spread','parlay2_over_under','parlay2_money_line','parlay3_spread','parlay3_over_under','parlay3_money_line']
reg_columns_to_predict = ['points_for','points_against']
class_columns_to_predict = ['actual_spread','actual_over_under','actual_money_line']
MIN_TRAINING_ROWS = 8


def _build_team_feature_df(team_df, include_class_columns=False):
    """
    Per-team, per-game feature rows shared by runDaBot (points regression) and
    runDaParlays (bet-outcome classification).

    Rows are ordered chronologically across seasons. A game's actual points
    live on the team's next row (as last_game_point_for/against), but only
    when that row is the same season and links straight back to this game -
    otherwise points stay -1 (unplayed, a scrape gap, or a season boundary).
    Keying on next_game_in_season alone would collide game N of this season
    with game N of last season.

    `row_id` is the BBALL7 id, kept so callers can pick today's row; drop it
    before modeling.
    """
    team_df = (team_df.sort_values(['season_year', 'next_game_in_season', 'id'])
               .drop_duplicates(['season_year', 'next_game_in_season'], keep='last')
               .reset_index(drop=True))
    team_updated_dict = {}

    for index in range(len(team_df)):
        current = team_df.iloc[index]
        game = current['next_game_in_season']

        points_for = points_against = -1
        if index + 1 < len(team_df):
            nxt = team_df.iloc[index + 1]
            if nxt['season_year'] == current['season_year'] and nxt['last_game_in_season'] == game:
                points_for = nxt['last_game_point_for']
                points_against = nxt['last_game_point_against']

        row = { 'days_since_last_game': current['days_since_last_game'],
                'last_game_was_win': current['last_game_was_win'],
                'curr_streak': current['curr_streak'],
                'home_games_win_percent': current['home_games_win_percent']*100,
                'away_games_win_percent': current['away_games_win_percent']*100,
                'league_avg_pace': current['league_avg_pace'],
                'team_off_rank': current['team_off_rank'],
                'league_avg_off_rank': current['league_avg_off_rank'],
                'team_def_rank': current['team_def_rank'],
                'league_avg_def_rank': current['league_avg_def_rank'],
                'team_mov': current['team_mov'],
                'team_mov_pos': current['team_mov_pos'],
                'league_avg_mov': current['league_avg_mov'],
                'team_srs': current['team_srs'],
                'team_srs_pos': current['team_srs_pos'],
                'league_avg_srs': current['league_avg_srs'],
                'game_start_time': current['game_start_time'],
                'points_for': points_for,
                'points_against': points_against,
                'last_game_field_goal_attempts': current['last_game_field_goal_attempts'],
                'last_game_field_goal': current['last_game_field_goal'],
                'last_game_turnovers': current['last_game_turnovers'],
                'last_game_rebounds': current['last_game_rebounds'],
                'all_field_goal_attempts': current['all_field_goal_attempts'],
                'all_field_goal': current['all_field_goal'],
                'all_rebounds': current['all_rebounds'],
                'all_turnovers': current['all_turnovers'],
                'team_avg_points_for': current['team_avg_points_for'],
                'team_avg_points_against': current['team_avg_points_against'],
                'is_home': current['is_home'],
                'game_in_season': game,
                'row_id': current['id'],
                }

        if include_class_columns:
            for column in ['calculated_spread_test', 'calculated_over_under_test', 'calculated_money_line_test'] + class_columns_to_predict:
                row[column] = current[column]

        team_updated_dict[index] = row

    return pd.DataFrame.from_dict(team_updated_dict, orient='index')


def _todays_rows(all_data_df):
    today = datetime.now().date()
    return all_data_df[(pd.to_datetime(all_data_df['created_at']).dt.date == today) & (all_data_df['season_year'] == year)]


def runDaBot():
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
    cur.execute(f"SELECT * FROM BBALL7;")
    all_data = cur.fetchall()

    # Get column names
    colnames = [desc[0] for desc in cur.description]
    all_data_df = pd.DataFrame(all_data, columns=colnames)

    todays_games = _todays_rows(all_data_df)

    list_of_games = todays_games[todays_games['is_home'] == 1][['team_name', 'next_opp_team_name', 'id']].values.tolist()
    # Structure: hometeam pos 0 , awayteam pos 1 [['CHO', 'SAS', id], ['IND', 'ATL', id], ...]
    both_team_errors = {}


    for game in list_of_games:
        home_team = game[0]
        away_team = game[1]
        home_team_current_game_id = game[2]

        away_today = todays_games[todays_games['team_name'] == away_team]
        if away_today.empty:
            print(f'Skipping {away_team} @ {home_team}: no row saved today for {away_team}')
            continue
        away_team_current_game_id = away_today['id'].values[0]

        all_home_team_df = all_data_df[all_data_df['team_name'] == home_team]
        all_away_team_df = all_data_df[all_data_df['team_name'] == away_team]

        both_team_predictions = {f'{home_team}_points_for': 0, f'{home_team}_points_against': 0,f'{away_team}_points_for': 0,f'{away_team}_points_against': 0}
        game_error = 0
        insufficient_history = False

        for team_index, (team_df, current_id) in enumerate([(all_home_team_df, home_team_current_game_id), (all_away_team_df, away_team_current_game_id)]):
            team_updated_df = _build_team_feature_df(team_df)
            team_data_to_predict = team_updated_df[team_updated_df['row_id'] == current_id].drop(columns=reg_columns_to_predict + ['row_id'])
            team_updated_df = team_updated_df[(team_updated_df['points_for'] != -1) & (team_updated_df['row_id'] != current_id)].drop(columns=['row_id'])

            if len(team_updated_df) < MIN_TRAINING_ROWS:
                insufficient_history = True
                break

            for column in reg_columns_to_predict:
                y = team_updated_df[column]
                X = team_updated_df.drop(columns=reg_columns_to_predict)

                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.19, random_state = 19)

                #Scale training and testing data
                scalar = StandardScaler()
                
                scalar.fit(X_train)
                X_train = scalar.transform(X_train)
                X_test = scalar.transform(X_test)

                #Model Selection with hyper parameter tuning with cross validation grid search
                alphas = [0.0001, 0.001, 0.01, 0.1, 1.0, 10.0, 100.0, 1000.0]
                elasticNetParams = [{'alpha': alphas}]
                lassoParams = [{'alpha': alphas}]
                SGDParams = [{'alpha': alphas}]
                ridgeParams = [{'alpha': alphas}]

                elasticNet = ElasticNet(random_state=19)
                lasso = Lasso(random_state=19)
                SGD = SGDRegressor(max_iter=1000, tol=1e-3)
                ridge = Ridge(random_state=19)

                #CV 3 folds
                #Elastic Net
                elasticNetGS = GridSearchCV(elasticNet, elasticNetParams, cv=3, scoring='neg_mean_absolute_error')
                elasticNetGS.fit(X_train, y_train)
                bestElasticNet3 = ElasticNet(alpha = elasticNetGS.best_params_['alpha'], random_state=19)
                #Lasso
                lassoGS = GridSearchCV(lasso, lassoParams, cv=3, scoring='neg_mean_absolute_error')
                lassoGS.fit(X_train, y_train)
                bestLasso3 = Lasso(alpha = lassoGS.best_params_['alpha'], random_state=19)
                #Stochastic gradient decent regression
                SGDGS = GridSearchCV(SGD, SGDParams, cv=3, scoring='neg_mean_absolute_error')
                SGDGS.fit(X_train, y_train)
                bestSGD3 = SGDRegressor(alpha = SGDGS.best_params_['alpha'], max_iter=1000, tol=1e-3, random_state=19)
                #Ridge
                ridgeGS = GridSearchCV(ridge, ridgeParams, cv=3, scoring='neg_mean_absolute_error')
                ridgeGS.fit(X_train, y_train)
                bestRidge3 = Ridge(alpha = ridgeGS.best_params_['alpha'], random_state=19)

                #Score all models with mean absolute error to see the average error in points predicted (lower better)
                bestElasticNet3.fit(X_train, y_train)
                elasticNet3Score = mean_squared_error(y_test, bestElasticNet3.predict(X_test))
                bestLasso3.fit(X_train, y_train)
                lasso3Score = mean_squared_error(y_test, bestLasso3.predict(X_test))
                bestSGD3.fit(X_train, y_train)
                SGD3Score = mean_squared_error(y_test, bestSGD3.predict(X_test))
                bestRidge3.fit(X_train, y_train)
                ridge3Score = mean_squared_error(y_test, bestRidge3.predict(X_test))

                allScores = {'elasticNet3Score' : elasticNet3Score,'lasso3Score' : lasso3Score,'SGD3Score' : SGD3Score,'ridge3Score' : ridge3Score}
                allBestModels = {'elasticNet3Score' : bestElasticNet3,'lasso3Score' : bestLasso3,'SGD3Score' : bestSGD3,'ridge3Score' : bestRidge3}

                bestScore = min(allScores, key=allScores.get)
                bestModel = allBestModels[bestScore]

                updated_team_data_to_predict = scalar.transform(team_data_to_predict)

                result = int(bestModel.predict(updated_team_data_to_predict)[0])

                game_error = game_error + allScores[bestScore]

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

        if insufficient_history:
            print(f'Skipping {away_team} @ {home_team}: fewer than {MIN_TRAINING_ROWS} trainable games')
            continue

        both_team_errors[f'{away_team}_{home_team}'] = game_error

        home_team_current_game = all_home_team_df[all_home_team_df['id'] == home_team_current_game_id]
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


        # Insert data
        home_team_insert_query = f"""
        UPDATE BBALL7
        SET calculated_spread_test = {home_spread}, calculated_money_line_test = {home_money_line}, calculated_over_under_test = {over_under}, home_calculated_spread_test = {home_spread}, home_calculated_money_line_test = {home_money_line} 
        WHERE id = {home_team_current_game_id};"""

        cur.execute(home_team_insert_query)
                    
        conn.commit()

        # Insert data
        away_team_insert_query = f"""
        UPDATE BBALL7
        SET calculated_spread_test = {away_spread}, calculated_money_line_test = {away_money_line}, calculated_over_under_test = {over_under}, home_calculated_spread_test = {home_spread}, home_calculated_money_line_test = {home_money_line} 
        WHERE id = {away_team_current_game_id};"""

        cur.execute(away_team_insert_query)
                    
        conn.commit()

    cur.close()
    conn.close()

    sorted_teams_by_errors = sorted(both_team_errors.items(), key=lambda item: item[1])
    return sorted_teams_by_errors

            



def runDaParlays(confidenceScores, percentTotals):
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
    cur.execute(f"SELECT * FROM BBALL7;")
    all_data = cur.fetchall()

    # Get column names
    colnames = [desc[0] for desc in cur.description]
    all_data_df = pd.DataFrame(all_data, columns=colnames)

    # lessThan200Games = [(name, val) for name, val in confidenceScores if val < 300]
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

            #Get all data needed for each team to use reallyRunEm
            todays_games = _todays_rows(all_data_df)
            home_today = todays_games[todays_games['team_name'] == homeTeam]
            away_today = todays_games[todays_games['team_name'] == awayTeam]
            if home_today.empty or away_today.empty:
                print(f'Skipping {awayTeam} @ {homeTeam}: no row saved today')
                continue
            teamIds['home'] = home_today['id'].values[0]
            teamIds['away'] = away_today['id'].values[0]

            home_team_df = all_data_df[(all_data_df['team_name'] == homeTeam) & (all_data_df['home_calculated_spread_test'].notna())]
            away_team_df = all_data_df[(all_data_df['team_name'] == awayTeam) & (all_data_df['home_calculated_spread_test'].notna())]
                
            for team_index, (team_df, current_id) in enumerate([(home_team_df, teamIds['home']), (away_team_df, teamIds['away'])]):
                team_updated_df = _build_team_feature_df(team_df, include_class_columns=True)
                team_data_to_predict = team_updated_df[team_updated_df['row_id'] == current_id].drop(columns=['row_id'])
                team_updated_df = team_updated_df[team_updated_df['actual_spread'].notna() & (team_updated_df['row_id'] != current_id)].drop(columns=['row_id'])

                if team_data_to_predict.empty:
                    # Game already graded, or runDaBot skipped it.
                    break

                for column in class_columns_to_predict:
                    y = team_updated_df[column]
                    X = team_updated_df.drop(columns=class_columns_to_predict)
                    X_to_predict = team_data_to_predict.drop(columns=class_columns_to_predict)

                    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.19, random_state = 19)
                    if y_train.nunique() == 1:
                        break
                    
                    y_train = y_train.astype(int)
                    y_test = y_test.astype(int)

                    if len(X_train) == 1:
                        break

                    #Scale training and testing data
                    scalar = StandardScaler()

                    scalar.fit(X_train)
                    X_train = scalar.transform(X_train)
                    X_test = scalar.transform(X_test)

                    #Test models
                    C = [0.00001, 0.0001, 0.001, 0.01, 0.1, 1.0, 10.0, 100.0, 1000.0]
                    alphas = [0.000001, 0.00001, 0.0001, 0.001, 0.01, 0.1, 1.0, 10.0, 100.0, 1000.0]
                    neighbors = [2,3,5,7]

                    CParams = [{'C': C}]
                    alphaParams = [{'alpha' : alphas}]
                    KNNParams = [{'n_neighbors' : neighbors}]

                    #Models
                    SVCModel = SVC(probability=True, random_state=19)
                    KNN = KNeighborsClassifier()
                    LogReg = LogisticRegression(max_iter=7000, random_state=19)
                    SGDCModel = SGDClassifier(loss='log_loss', max_iter=7000, tol=1e-3, random_state=19)

                    SVCGS3 = GridSearchCV(SVCModel, CParams, cv=3)
                    SVCGS3.fit(X_train, y_train)
                    bestSVC3 = SVC(C = SVCGS3.best_params_['C'], probability=True, random_state=19)
                    #K Nearest Neighbor
                    KNNGS3 = GridSearchCV(KNN, KNNParams, cv=3)
                    KNNGS3.fit(X_train, y_train)
                    bestKNN3 = KNeighborsClassifier(n_neighbors = KNNGS3.best_params_['n_neighbors'])
                    #Logistic Regression
                    LRGS3 = GridSearchCV(LogReg, CParams, cv=3)
                    LRGS3.fit(X_train, y_train)
                    bestLR3 = LogisticRegression(C = LRGS3.best_params_['C'], max_iter=1000, random_state=19)
                    #Stochastic Gradient Descent 
                    SGDCGS3 = GridSearchCV(SGDCModel, alphaParams, cv=3)
                    SGDCGS3.fit(X_train, y_train)
                    bestSGDC3 = SGDClassifier(loss='log_loss', alpha = SGDCGS3.best_params_['alpha'], max_iter=1000, tol=1e-3, random_state=19)

                    bestSVC3.fit(X_train, y_train)
                    bestSVC3Score = accuracy_score(y_test, bestSVC3.predict(X_test))
                    bestKNN3.fit(X_train, y_train)
                    bestKNN3Score = accuracy_score(y_test, bestKNN3.predict(X_test))
                    bestLR3.fit(X_train, y_train)
                    bestLR3Score = accuracy_score(y_test, bestLR3.predict(X_test))
                    bestSGDC3.fit(X_train, y_train)
                    bestSGDC3Score = accuracy_score(y_test, bestSGDC3.predict(X_test))

                    allScores = {'bestSVC3Score' : bestSVC3Score,'bestKNN3Score' : bestKNN3Score,'bestLR3Score' : bestLR3Score,'bestSGDC3Score' : bestSGDC3Score}
                    allBestModels = {'bestSVC3Score' : bestSVC3,'bestKNN3Score' : bestKNN3,'bestLR3Score' : bestLR3,'bestSGDC3Score' : bestSGDC3}

                    bestScore = max(allScores, key=allScores.get)
                    bestModel = allBestModels[bestScore]
                    firstClass, secondClass = bestModel.classes_
                    updated_team_data_to_predict = scalar.transform(X_to_predict)                                       
                    
                    if column == 'actual_spread':
                        teamSpread = int(X_to_predict['calculated_spread_test'].iloc[0])
                        prediction = bestModel.predict(updated_team_data_to_predict)[0]
                        prediction_prob = bestModel.predict_proba(updated_team_data_to_predict)[0]

                        if teamSpread == prediction:
                            if teamSpread == 0:
                                teamsScores['spread'] = teamsScores['spread'] + prediction_prob[0]

                            if teamSpread == 1:
                                teamsScores['spread'] = teamsScores['spread'] + prediction_prob[1]
    
                    elif column == 'actual_over_under':
                        teamOverUnder = int(X_to_predict['calculated_over_under_test'].iloc[0])
                        prediction = bestModel.predict(updated_team_data_to_predict)[0]
                        prediction_prob = bestModel.predict_proba(updated_team_data_to_predict)[0]

                        if teamOverUnder == prediction:
                            if teamOverUnder == 0:
                                teamsScores['overUnder'] = teamsScores['overUnder'] + prediction_prob[0]

                            if teamOverUnder == 1:
                                teamsScores['overUnder'] = teamsScores['overUnder'] + prediction_prob[1]

                    elif column == 'actual_money_line':
                            teamMoneyLine = int(X_to_predict['calculated_money_line_test'].iloc[0])
                            prediction = bestModel.predict(updated_team_data_to_predict)[0]
                            prediction_prob = bestModel.predict_proba(updated_team_data_to_predict)[0]

                            if teamMoneyLine == prediction:
                                if teamMoneyLine == 0:
                                    teamsScores['moneyLine'] = teamsScores['moneyLine'] + prediction_prob[0]

                                if teamMoneyLine == 1:
                                    teamsScores['moneyLine'] = teamsScores['moneyLine'] + prediction_prob[1]

            if sectionIndex != 1:       
                if teamsScores['spread'] > 1:
                    print(homeTeam, awayTeam, 'spread')
                    print(teamsScores['spread'])
                    # Insert data
                    home_team_insert_query = f"""
                    UPDATE BBALL7
                    SET parlay{sectionIndex}_spread = true
                    WHERE id = {teamIds['home']};"""
                    cur.execute(home_team_insert_query)   
                    conn.commit()

                    away_team_insert_query = f"""
                    UPDATE BBALL7
                    SET parlay{sectionIndex}_spread = true
                    WHERE id = {teamIds['away']};"""
                    cur.execute(away_team_insert_query)
                    conn.commit()
                else:
                    # Insert data
                    home_team_insert_query = f"""
                    UPDATE BBALL7
                    SET parlay{sectionIndex}_spread = false
                    WHERE id = {teamIds['home']};"""
                    cur.execute(home_team_insert_query)   
                    conn.commit()

                    away_team_insert_query = f"""
                    UPDATE BBALL7
                    SET parlay{sectionIndex}_spread = false
                    WHERE id = {teamIds['away']};"""
                    cur.execute(away_team_insert_query)
                    conn.commit()

                if teamsScores['overUnder'] > 1:
                    print(homeTeam, awayTeam, 'overUnder')
                    print(teamsScores['overUnder'])
                    # Insert data
                    home_team_insert_query = f"""
                    UPDATE BBALL7
                    SET parlay{sectionIndex}_over_under = true
                    WHERE id = {teamIds['home']};"""
                    cur.execute(home_team_insert_query)   
                    conn.commit()

                    away_team_insert_query = f"""
                    UPDATE BBALL7
                    SET parlay{sectionIndex}_over_under = true
                    WHERE id = {teamIds['away']};"""
                    cur.execute(away_team_insert_query)
                    conn.commit()
                else:
                    # Insert data
                    home_team_insert_query = f"""
                    UPDATE BBALL7
                    SET parlay{sectionIndex}_over_under = false
                    WHERE id = {teamIds['home']};"""
                    cur.execute(home_team_insert_query)   
                    conn.commit()

                    away_team_insert_query = f"""
                    UPDATE BBALL7
                    SET parlay{sectionIndex}_over_under = false
                    WHERE id = {teamIds['away']};"""
                    cur.execute(away_team_insert_query)
                    conn.commit()
                
                if teamsScores['moneyLine'] > 1:
                    print(homeTeam, awayTeam, 'moneyline')
                    print(teamsScores['moneyLine'])
                    # Insert data
                    home_team_insert_query = f"""
                    UPDATE BBALL7
                    SET parlay{sectionIndex}_money_line = true
                    WHERE id = {teamIds['home']};"""
                    cur.execute(home_team_insert_query)   
                    conn.commit()

                    away_team_insert_query = f"""
                    UPDATE BBALL7
                    SET parlay{sectionIndex}_money_line = true
                    WHERE id = {teamIds['away']};"""
                    cur.execute(away_team_insert_query)
                    conn.commit()
                else:
                    # Insert data
                    home_team_insert_query = f"""
                    UPDATE BBALL7
                    SET parlay{sectionIndex}_money_line = false
                    WHERE id = {teamIds['home']};"""
                    cur.execute(home_team_insert_query)   
                    conn.commit()

                    away_team_insert_query = f"""
                    UPDATE BBALL7
                    SET parlay{sectionIndex}_money_line = false
                    WHERE id = {teamIds['away']};"""
                    cur.execute(away_team_insert_query)
                    conn.commit()
            
            else:
                if teamsScores['spread'] > 1.69:
                    print(homeTeam, awayTeam, 'spread')
                    print(teamsScores['spread'])
                    # Insert data
                    home_team_insert_query = f"""
                    UPDATE BBALL7
                    SET parlay{sectionIndex}_spread = true
                    WHERE id = {teamIds['home']};"""
                    cur.execute(home_team_insert_query)   
                    conn.commit()

                    away_team_insert_query = f"""
                    UPDATE BBALL7
                    SET parlay{sectionIndex}_spread = true
                    WHERE id = {teamIds['away']};"""
                    cur.execute(away_team_insert_query)
                    conn.commit()
                else:
                    # Insert data
                    home_team_insert_query = f"""
                    UPDATE BBALL7
                    SET parlay{sectionIndex}_spread = false
                    WHERE id = {teamIds['home']};"""
                    cur.execute(home_team_insert_query)   
                    conn.commit()

                    away_team_insert_query = f"""
                    UPDATE BBALL7
                    SET parlay{sectionIndex}_spread = false
                    WHERE id = {teamIds['away']};"""
                    cur.execute(away_team_insert_query)
                    conn.commit()

                if teamsScores['overUnder'] > 1.69:
                    print(homeTeam, awayTeam, 'overUnder')
                    print(teamsScores['overUnder'])
                    # Insert data
                    home_team_insert_query = f"""
                    UPDATE BBALL7
                    SET parlay{sectionIndex}_over_under = true
                    WHERE id = {teamIds['home']};"""
                    cur.execute(home_team_insert_query)   
                    conn.commit()

                    away_team_insert_query = f"""
                    UPDATE BBALL7
                    SET parlay{sectionIndex}_over_under = true
                    WHERE id = {teamIds['away']};"""
                    cur.execute(away_team_insert_query)
                    conn.commit()
                else:
                    # Insert data
                    home_team_insert_query = f"""
                    UPDATE BBALL7
                    SET parlay{sectionIndex}_over_under = false
                    WHERE id = {teamIds['home']};"""
                    cur.execute(home_team_insert_query)   
                    conn.commit()

                    away_team_insert_query = f"""
                    UPDATE BBALL7
                    SET parlay{sectionIndex}_over_under = false
                    WHERE id = {teamIds['away']};"""
                    cur.execute(away_team_insert_query)
                    conn.commit()
                
                if teamsScores['moneyLine'] > 1.69:
                    print(homeTeam, awayTeam, 'moneyline')
                    print(teamsScores['moneyLine'])
                    # Insert data
                    home_team_insert_query = f"""
                    UPDATE BBALL7
                    SET parlay{sectionIndex}_money_line = true
                    WHERE id = {teamIds['home']};"""
                    cur.execute(home_team_insert_query)   
                    conn.commit()

                    away_team_insert_query = f"""
                    UPDATE BBALL7
                    SET parlay{sectionIndex}_money_line = true
                    WHERE id = {teamIds['away']};"""
                    cur.execute(away_team_insert_query)
                    conn.commit()
                else:
                    # Insert data
                    home_team_insert_query = f"""
                    UPDATE BBALL7
                    SET parlay{sectionIndex}_money_line = false
                    WHERE id = {teamIds['home']};"""
                    cur.execute(home_team_insert_query)   
                    conn.commit()

                    away_team_insert_query = f"""
                    UPDATE BBALL7
                    SET parlay{sectionIndex}_money_line = false
                    WHERE id = {teamIds['away']};"""
                    cur.execute(away_team_insert_query)
                    conn.commit()      