import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import mysql.connector
from datetime import date, datetime
import random
import matplotlib.pyplot as plt

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import VarianceThreshold
from sklearn.linear_model import ElasticNet
from sklearn.linear_model import Lasso
from sklearn.linear_model import SGDRegressor
from sklearn.linear_model import Ridge
from sklearn.model_selection import GridSearchCV, cross_val_predict
from sklearn.metrics import accuracy_score
from sklearn.metrics import mean_absolute_error
from sklearn.feature_selection import RFECV

from selenium import webdriver
from selenium.webdriver.common.by import By

from legends import *
from constants import ALL_TEAMS, ALL_YEARS, ALL_COLUMNS, ALL_PERCENTAGES, TEAM_LAST_5_GAME_COUNT


sleepTimes = [17,23,27]


def updateNBAGames():
    teams = getTeam(ALL_TEAMS)
    year = 2024

    #Connect to mysql
    mydb = mysql.connector.connect(
        host='127.0.0.1',
        user='davidcarney',
        password='Sinorrabb1t',
        database='NBA'
        )
    mycursor = mydb.cursor()
    
    
    for team in teams:
        originalTeamNumber = getTeam(team)['number']

        #Get previous games from Database
        mycursor.execute(f"SELECT id, gameNumber, isWin FROM nbaStats WHERE teamNumber = {originalTeamNumber} and year = {year};")

        teamData = mycursor.fetchall()
        teamDF = pd.DataFrame(teamData, columns = ['id', 'gameNumber', 'isWin'])
        lastSavedGame = teamDF['gameNumber'][teamDF['isWin'].notna()].values[-1]
        unsavedGameDF = teamDF[['id','gameNumber']][teamDF['isWin'].isna()]

        unsavedGameID = -1
        unsavedGameNumber = -1
        if len(unsavedGameDF) != 0:
            unsavedGameID = int(unsavedGameDF['id'].values[0])
            unsavedGameNumber = int(unsavedGameDF['gameNumber'].values[0])

        #Update database with new season games
        url = f'https://www.basketball-reference.com/teams/{team}/{year}_games.html'
        HEADERS = {
            'User-Agent': 'Safari/537.36',
        }
        page = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(page.content, 'html.parser')
        time.sleep(random.choice(sleepTimes))
        moreSoup = soup.find('div', id='wrap')
        evenMoreSoup = moreSoup.find('div', id='content')
        allGamesWrapper = evenMoreSoup.find('div', id='all_games')
        allGamesTable = allGamesWrapper.find('table', id='games')
        tableBody = allGamesTable.find('tbody')
        time.sleep(random.choice(sleepTimes))

        for row in tableBody.find_all('tr'):

            if row.attrs == {}:
                gameNumber = row.find('th').text

                if int(gameNumber) > lastSavedGame:
   
                    gameDay = row.find('td', attrs={'data-stat': 'date_game'}).text.split(',')
                    day = gameDay[0].strip()
                    monthAndDate = gameDay[1].strip()
                    year = gameDay[2].strip()
                    date_time = ' '.join([monthAndDate, year])
                    datetime_str = datetime.strptime(date_time, '%b %d %Y')
                    date = datetime_str.strftime('%m/%d/%y')

                    gameStart = row.find('td', attrs={'data-stat': 'game_start_time'}).text
                    gameLocation = row.find('td', attrs={'data-stat': 'game_location'}).text
                    gameOppTeam = row.find('td', attrs={'data-stat': 'opp_name'}).text
                    gameResult = row.find('td', attrs={'data-stat': 'game_result'}).text
                    inSeasonTournament = row.find('td', attrs={'data-stat': 'game_remarks'}).text
                    primaryKey = int(f'{gameNumber}0{originalTeamNumber}{str(year)[-2:]}')

                    oppTeamNumber = getTeam(gameOppTeam)['number']
                    gameDayNumber = getDay(day)['dayNumber']
                    gameStartNumber = getTimeCode(gameStart)
                    isInSeasonT = getIsInSeasonT(inSeasonTournament)

                    isHome = 0
                    if gameLocation == '@':
                        homeTeam = gameOppTeam
                    else:
                        isHome = 1


                    
                    if gameResult != '':
                        gameOT = row.find('td', attrs={'data-stat': 'overtimes'}).text
                        gamePoints = row.find('td', attrs={'data-stat': 'pts'}).text
                        gameOppPoints = row.find('td', attrs={'data-stat': 'opp_pts'}).text
                        teamWins = row.find('td', attrs={'data-stat': 'wins'}).text
                        teamLosses = row.find('td', attrs={'data-stat': 'losses'}).text
                        teamStreak = row.find('td', attrs={'data-stat': 'game_streak'}).text
                        
                        isWin = getIsWin(gameResult)
                        isOT = getIsOT(gameOT)
                        teamStreakCode = getTeamStreakCode(teamStreak)
                        

                        #Store data:
                        if int(gameNumber) == unsavedGameNumber:
                            #Update existing row
                            updateData = (
                                f"UPDATE nbaStats "
                                f"SET isWin = {isWin}, "
                                f"isOT = {isOT}, "
                                f"gameDayNumber = {gameDayNumber}, "
                                f"gameStartNumber = {gameStartNumber}, "
                                f"teamPoints = {gamePoints}, "
                                f"oppTeamPoints = {gameOppPoints}, "
                                f"teamWins = {teamWins}, "
                                f"teamLosses = {teamLosses}, "
                                f"teamStreakCode = {teamStreakCode} "
                                f"WHERE id = {primaryKey};"
                            )
                            mycursor.execute(updateData)
                            mydb.commit()
                        
                        else:
                            #Create new row
                            insertData = (
                                f"INSERT INTO nbaStats "
                                f"("
                                f"id, "
                                f"gameNumber, "
                                f"teamNumber, "
                                f"isHome, "
                                f"oppTeamNumber, "
                                f"isWin, "
                                f"isOT, "
                                f"gameDayNumber, "
                                f"gameStartNumber, "
                                f"teamPoints, "
                                f"oppTeamPoints, "
                                f"teamWins, "
                                f"teamLosses, "
                                f"teamStreakCode, "
                                f"isInSeasonTournament, "
                                f"year, "
                                f"date "
                                f") "
                                f"VALUES ("
                                f"{primaryKey},"
                                f"{gameNumber},"
                                f"{originalTeamNumber},"
                                f"{isHome},"
                                f"{oppTeamNumber},"
                                f"{isWin},"
                                f"{isOT},"
                                f"{gameDayNumber},"
                                f"{gameStartNumber},"
                                f"{gamePoints},"
                                f"{gameOppPoints},"
                                f"{teamWins},"
                                f"{teamLosses},"
                                f"{teamStreakCode},"
                                f"{isInSeasonT},"
                                f"{year},"
                                f"'{date}'"
                                f")"
                            )
                            mycursor.execute(insertData)
                            mydb.commit()
                    
                    
                    else:
                        if unsavedGameID != primaryKey:
                            #Create new row for teams next game
                            insertData = (
                                f"INSERT INTO nbaStats "
                                f"("
                                f"id, "
                                f"gameNumber, "
                                f"teamNumber, "
                                f"isHome, "
                                f"oppTeamNumber, "
                                f"gameDayNumber, "
                                f"gameStartNumber, "
                                f"isInSeasonTournament, "
                                f"year, "
                                f"gameTimeActual, "
                                f"date "
                                f") "
                                f"VALUES ("
                                f"{primaryKey},"
                                f"{gameNumber},"
                                f"{originalTeamNumber},"
                                f"{isHome},"
                                f"{oppTeamNumber},"
                                f"{gameDayNumber}, "
                                f"{gameStartNumber}, "
                                f"{isInSeasonT},"
                                f"{year},"
                                f"'{gameStart}',"
                                f"'{date}'"
                                f")"
                            )
                            mycursor.execute(insertData)
                            mydb.commit()
                        
                        break
                                   
        time.sleep(random.choice(sleepTimes))
        print(f"{getTeam(team)['number'] + 1}/30 {team} completed.")



def getGamblingData():
    year = 2024

    #Connect to MySQL
    mydb = mysql.connector.connect(
    host='127.0.0.1',
    user='davidcarney',
    password='Sinorrabb1t',
    database='NBA'
    )
    mycursor = mydb.cursor()


    #Get previous games from Database
    mycursor.execute(f"SELECT * FROM nbaStats WHERE isWin is NULL and spread is NULL;")

    teamData = mycursor.fetchall()
    nextGames = pd.DataFrame(teamData, columns = ALL_COLUMNS)

    #Start Selenium driver
    driver = webdriver.Chrome()
    driver.get("https://sportsbook.draftkings.com/leagues/basketball/nba")
    time.sleep(random.choice(sleepTimes))
    
    container = driver.find_element(By.CLASS_NAME, 'sportsbook-responsive-card-container')
    time.sleep(random.choice(sleepTimes))
    todaysGames = driver.find_element(By.CLASS_NAME, 'parlay-card-10-a')
    time.sleep(random.choice(sleepTimes))
    todayGamesTable = driver.find_element(By.CLASS_NAME, 'sportsbook-table__body')
    todayGamesTableHTML = todayGamesTable.get_attribute('innerHTML')
    soup = BeautifulSoup(todayGamesTableHTML, 'html.parser')
    time.sleep(random.choice(sleepTimes))
    allRows = soup.find_all('tr')

    sameGame = True
    awayTeam = {}
    homeTeam = {}

    for row in allRows:
        teamName = row.find('th').find('div', class_='event-cell__name-text').text.split(' ')[1]

        someSpread, someOverUnder, someML = row.find_all('td')
        moreSpread = someSpread.find('div', class_='sportsbook-outcome-body-wrapper')
        spread, spreadOdds = moreSpread.find_all('span')
        spread = spread.text
        spreadOdds = spreadOdds.text
        time.sleep(random.choice(sleepTimes))

        moreOverUnder = someOverUnder.find('div', class_='sportsbook-outcome-body-wrapper')
        evenMoreOverUnder = moreOverUnder.find_all('span')
        overUnderOdds  = evenMoreOverUnder[-1]
        overUnder = evenMoreOverUnder[-2]
        overUnder = overUnder.text
        overUnderOdds = overUnderOdds.text
        time.sleep(random.choice(sleepTimes))

        moreML = someML.find('div', class_='sportsbook-outcome-body-wrapper')
        MLOdds = moreML.find('span')
        MLOdds = MLOdds.text
        time.sleep(random.choice(sleepTimes))

        if sameGame == True:
            #away team
            awayTeam = {'teamNumber' : getTeam(teamName)['number'], 'spread' : spread, 'spreadOdds' : spreadOdds, 'overUnder' : overUnder, 'overUnderOdds' : overUnderOdds, 'MLOdds' : MLOdds}
            sameGame = False
        
        else:
            #home team            
            homeTeam = {'teamNumber' : getTeam(teamName)['number'], 'spread' : spread, 'spreadOdds' : spreadOdds, 'overUnder' : overUnder, 'overUnderOdds' : overUnderOdds, 'MLOdds' : MLOdds}

            #away team next game
            awayTeamNextGame = nextGames[nextGames['teamNumber'] == awayTeam['teamNumber']]
        
            #home team next game
            homeTeamNextGame = nextGames[nextGames['teamNumber'] == homeTeam['teamNumber']]

            #Store sameGames
            #Store data:
            mycursor = mydb.cursor()

            updateData = (
                f"UPDATE nbaStats "
                f"SET spread = '{awayTeam['spread']}', "
                f"spreadOdds = '{awayTeam['spreadOdds']}', "
                f"overUnder = '{awayTeam['overUnder']}', "
                f"overUnderOdds = '{awayTeam['overUnderOdds']}', "
                f"moneyLine = '{awayTeam['MLOdds']}' "
                f"WHERE id = {awayTeamNextGame['id'].values[0]};"
            )
            mycursor.execute(updateData)
            mydb.commit()

            updateData = (
                f"UPDATE nbaStats "
                f"SET spread = '{homeTeam['spread']}', "
                f"spreadOdds = '{homeTeam['spreadOdds']}', "
                f"overUnder = '{homeTeam['overUnder']}', "
                f"overUnderOdds = '{homeTeam['overUnderOdds']}', "
                f"moneyLine = '{homeTeam['MLOdds']}' "
                f"WHERE id = {homeTeamNextGame['id'].values[0]};"
            )
            mycursor.execute(updateData)
            mydb.commit()

            sameGame = True
           
        time.sleep(random.choice(sleepTimes))
    driver.quit()
    print('All gambling data has been saved!')



def runML():
    #Initial variables
    teams = getTeam(ALL_TEAMS)
    columnsToPredict = ['teamPoints','oppTeamPoints']
    columnsToRemove = ['isWin','isOT','teamWins','teamLosses','teamStreakCode','spread','spreadOdds','overUnder','overUnderOdds','moneyLine','gameTimeActual','date']
    gamblingColumns = ['spread','spreadOdds','overUnder','overUnderOdds','moneyLine']
    year = 2024


    #Open frontend file
    todaysGamesFilename = '../frontend/src/nbaPages/todaysGames.js'
    todaysGamesFile = open(todaysGamesFilename, 'w')
    todaysGamesFile.write('export const todaysGames = [\n')
    todaysDate = date.today().strftime("%B %d, %Y")
    todaysDayName = date.today().strftime("%A")
    todaysGamesFile.write(f"'{todaysDayName}',\n")
    todaysGamesFile.write(f"'{todaysDate}',\n")

    #Connect to MySQL Database
    mydb = mysql.connector.connect(
        host='127.0.0.1',
        user='davidcarney',
        password='Sinorrabb1t',
        database='NBA'
        )
    mycursor = mydb.cursor()

    #Get all data from Database
    mycursor.execute(f"SELECT * FROM nbaStats;")
    teamData = mycursor.fetchall()
    allTeamsDF = pd.DataFrame(teamData, columns = ALL_COLUMNS)
    allTeamsDF = allTeamsDF.drop(columns=['spreadCalculated','overUnderCalculated','spreadActual','overUnderActual'])

    #Iterate over each team
    gamesToBePredictedDF = allTeamsDF[(allTeamsDF['isWin'].isna()) & (allTeamsDF['spread'].notna())]
    gamesToBePredictedDFWoGD = gamesToBePredictedDF.drop(columns = columnsToRemove)
    gamesToBePredictedDFWoGD = gamesToBePredictedDFWoGD.drop(columns = columnsToPredict)
    gamesAlreadyPredicted = []

    for eachGame in gamesToBePredictedDF.sort_values(by=['gameStartNumber'])[['teamNumber','oppTeamNumber']].values:        
        team1, team2 = list(eachGame)
        
        if (team1 not in gamesAlreadyPredicted) or (team2 not in gamesAlreadyPredicted):
            #Get updated Dataframe
            df = allTeamsDF[((allTeamsDF['teamNumber'] == team1) & (allTeamsDF['year'] == year)) | ((allTeamsDF['teamNumber'] == team2) & (allTeamsDF['year'] == year)) | ((allTeamsDF['teamNumber'] == team1) & (allTeamsDF['oppTeamNumber'] == team2) & (allTeamsDF['year'] < year)) | ((allTeamsDF['teamNumber'] == team2) & (allTeamsDF['oppTeamNumber'] == team1) & (allTeamsDF['year'] < year))]
            df = df[df['isWin'].notna()]
            df = df.drop(columns=columnsToRemove)
            df = df.sort_values(by=['year', 'gameNumber'])
            predictedScores = {'team1' : 0, 'team2' : 0}
            
            #Predicts column from columnsToPredict from dataframe for team1 and team2
            for column in columnsToPredict:
                y = df[column]
                X = df.drop(columns=columnsToPredict)

                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.19, random_state = 19)
                
                #Scale training and testing data
                scalar = StandardScaler()
                
                scalar.fit(X_train)
                X_train = scalar.transform(X_train)
                X_test = scalar.transform(X_test)

                #Feature selection
                #Need to add this feature selection before gridsearch
                #featureSelection =  RFECV(estimator, step=1, cv=5)
                featureSelection = VarianceThreshold(threshold=(.8 * (1 - .8)))
                X_train = featureSelection.fit_transform(X_train)

                #Model Selection with hyper parameter tuning with cross validation grid search
                alphas = [0.0001, 0.001, 0.01, 0.1, 1.0, 10.0, 100.0, 1000.0]
                elasticNetParams = [{'alpha': alphas}]
                lassoParams = [{'alpha': alphas}]
                SGDParams = [{'alpha': alphas}]
                ridgeParams = [{'alpha': alphas}]
                
                #Models
                elasticNet = ElasticNet(random_state=19)
                lasso = Lasso(random_state=19)
                SGD = SGDRegressor(max_iter=1000, tol=1e-3)
                ridge = Ridge(random_state=19)
                
                #CV 2 folds
                #Elastic Net
                elasticNetGS = GridSearchCV(elasticNet, elasticNetParams, cv=2, scoring='neg_mean_absolute_error')
                elasticNetGS.fit(X_train, y_train)
                bestElasticNet2 = ElasticNet(alpha = elasticNetGS.best_params_['alpha'], random_state=19)
                #Lasso
                lassoGS = GridSearchCV(lasso, lassoParams, cv=2, scoring='neg_mean_absolute_error')
                lassoGS.fit(X_train, y_train)
                bestLasso2 = Lasso(alpha = lassoGS.best_params_['alpha'], random_state=19)
                #Stochastic gradient decent regression
                SGDGS = GridSearchCV(SGD, SGDParams, cv=2, scoring='neg_mean_absolute_error')
                SGDGS.fit(X_train, y_train)
                bestSGD2 = SGDRegressor(alpha = SGDGS.best_params_['alpha'], max_iter=1000, tol=1e-3, random_state=19)
                #Ridge
                ridgeGS = GridSearchCV(ridge, ridgeParams, cv=2, scoring='neg_mean_absolute_error')
                ridgeGS.fit(X_train, y_train)
                bestRidge2 = Ridge(alpha = ridgeGS.best_params_['alpha'], random_state=19)

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

                #CV 5 folds
                #Elastic Net
                elasticNetGS = GridSearchCV(elasticNet, elasticNetParams, cv=5, scoring='neg_mean_absolute_error')
                elasticNetGS.fit(X_train, y_train)
                bestElasticNet5 = ElasticNet(alpha = elasticNetGS.best_params_['alpha'], random_state=19)
                #Lasso
                lassoGS = GridSearchCV(lasso, lassoParams, cv=5, scoring='neg_mean_absolute_error')
                lassoGS.fit(X_train, y_train)
                bestLasso5 = Lasso(alpha = lassoGS.best_params_['alpha'], random_state=19)
                #Stochastic gradient decent regression
                SGDGS = GridSearchCV(SGD, SGDParams, cv=5, scoring='neg_mean_absolute_error')
                SGDGS.fit(X_train, y_train)
                bestSGD5 = SGDRegressor(alpha = SGDGS.best_params_['alpha'], max_iter=1000, tol=1e-3, random_state=19)
                #Ridge
                ridgeGS = GridSearchCV(ridge, ridgeParams, cv=5, scoring='neg_mean_absolute_error')
                ridgeGS.fit(X_train, y_train)
                bestRidge5 = Ridge(alpha = ridgeGS.best_params_['alpha'], random_state=19)

                #Score all models with mean absolute error to see the average error in points predicted (lower better)
                bestElasticNet2.fit(X_train, y_train)
                elasticNet2Score = mean_absolute_error(y_test, bestElasticNet2.predict(X_test))
                bestElasticNet3.fit(X_train, y_train)
                elasticNet3Score = mean_absolute_error(y_test, bestElasticNet3.predict(X_test))
                bestElasticNet5.fit(X_train, y_train)
                elasticNet5Score = mean_absolute_error(y_test, bestElasticNet5.predict(X_test))

                bestLasso2.fit(X_train, y_train)
                lasso2Score = mean_absolute_error(y_test, bestLasso2.predict(X_test))
                bestLasso3.fit(X_train, y_train)
                lasso3Score = mean_absolute_error(y_test, bestLasso3.predict(X_test))
                bestLasso5.fit(X_train, y_train)
                lasso5Score = mean_absolute_error(y_test, bestLasso5.predict(X_test))

                bestSGD2.fit(X_train, y_train)
                SGD2Score = mean_absolute_error(y_test, bestSGD2.predict(X_test))
                bestSGD3.fit(X_train, y_train)
                SGD3Score = mean_absolute_error(y_test, bestSGD3.predict(X_test))
                bestSGD5.fit(X_train, y_train)
                SGD5Score = mean_absolute_error(y_test, bestSGD5.predict(X_test))

                bestRidge2.fit(X_train, y_train)
                ridge2Score = mean_absolute_error(y_test, bestRidge2.predict(X_test))
                bestRidge3.fit(X_train, y_train)
                ridge3Score = mean_absolute_error(y_test, bestRidge3.predict(X_test))
                bestRidge5.fit(X_train, y_train)
                ridge5Score = mean_absolute_error(y_test, bestRidge5.predict(X_test))

                allScores = {'elasticNet2Score' : elasticNet2Score,'elasticNet3Score' : elasticNet3Score,'elasticNet5Score' : elasticNet5Score,'lasso2Score' : lasso2Score,'lasso3Score' : lasso3Score,'lasso5Score' : lasso5Score,'SGD2Score' : SGD2Score,'SGD3Score' : SGD3Score,'SGD5Score' : SGD5Score,'ridge2Score' : ridge2Score,'ridge3Score' : ridge3Score,'ridge5Score' : ridge5Score}
                allBestModels = {'elasticNet2Score' : bestElasticNet2,'elasticNet3Score' : bestElasticNet3,'elasticNet5Score' : bestElasticNet5,'lasso2Score' : bestLasso2,'lasso3Score' : bestLasso3,'lasso5Score' : bestLasso5,'SGD2Score' : bestSGD2,'SGD3Score' : bestSGD3,'SGD5Score' : bestSGD5,'ridge2Score' : bestRidge2,'ridge3Score' : bestRidge3,'ridge5Score' : bestRidge5}

                bestScore = min(allScores, key=allScores.get)
                bestModel = allBestModels[bestScore]

                team1DataToPredict = scalar.transform(gamesToBePredictedDFWoGD[gamesToBePredictedDFWoGD['teamNumber'] == team1])
                team2DataToPredict = scalar.transform(gamesToBePredictedDFWoGD[gamesToBePredictedDFWoGD['teamNumber'] == team2])

                if column == 'teamPoints':
                    predictedScores['team1'] = bestModel.predict(team1DataToPredict)
                    predictedScores['team2'] = bestModel.predict(team2DataToPredict)
                elif column == 'oppTeamPoints':
                    predictedScores['team2'] = predictedScores['team2'] + bestModel.predict(team1DataToPredict)
                    predictedScores['team2'] = predictedScores['team2'] / 2
                    predictedScores['team1'] = predictedScores['team1'] + bestModel.predict(team2DataToPredict)
                    predictedScores['team1'] = predictedScores['team1'] / 2

            
            team1GamblingData = gamesToBePredictedDF[gamesToBePredictedDF['teamNumber'] == team1]
            team2GamblingData = gamesToBePredictedDF[gamesToBePredictedDF['teamNumber'] == team2]
            team1PrimaryKey = team1GamblingData['id'].values[0]
            team2PrimaryKey = team2GamblingData['id'].values[0]

            predictedTeam1Spread = predictedScores['team1'] - predictedScores['team2']
            predictedTeam2Spread = predictedScores['team2'] - predictedScores['team1']

            team1SpreadValues = team1GamblingData['spread'].values[0]
            team2SpreadValues = team2GamblingData['spread'].values[0]

            team1SpreadSign = team1SpreadValues[0]
            spreadValue = float(team1SpreadValues[1:])
            

            predictedTeam1SpreadResults = 0
            predictedTeam2SpreadResults = 0
            if team1SpreadSign == '-':
                if predictedTeam1Spread > spreadValue:
                    predictedTeam1SpreadResults = 1
                else:
                    predictedTeam2SpreadResults = 1
            else:
                if predictedTeam2Spread > spreadValue:
                    predictedTeam2SpreadResults = 1
                else:
                    predictedTeam1SpreadResults = 1



            overUnderValues = team1GamblingData['overUnder'].values[0]
            predictedOverUnder = predictedScores['team1'] + predictedScores['team2']
            predictedOverUnderResults = 0
            if predictedOverUnder[0] > float(overUnderValues):
                predictedOverUnderResults = 1

            gameTime = team1GamblingData['gameTimeActual'].values[0]

            mycursor = mydb.cursor()

            #Update database for team 1
            updateData = (
                f"UPDATE nbaStats "
                f"SET spreadCalculated = {predictedTeam1SpreadResults}, "
                f"overUnderCalculated = {predictedOverUnderResults} "
                f"WHERE id = {team1PrimaryKey};"
            )
            mycursor.execute(updateData)
            mydb.commit()

            #Update database for team 2
            updateData = (
                f"UPDATE nbaStats "
                f"SET spreadCalculated = '{predictedTeam2SpreadResults}', "
                f"overUnderCalculated = '{predictedOverUnderResults}' "
                f"WHERE id = {team2PrimaryKey};"
            )
            mycursor.execute(updateData)
            mydb.commit()

            #Write to file : awayTeam,homeTeam,spread,homeTeamSpread,ifHomeTeamCovered,OverUnder, ifTeamsCoveredOverUnder
            if len(team1GamblingData[team1GamblingData['isHome'] == 1]) != 0:
                todaysGamesFile.write(f"'{gameTime},")
                todaysGamesFile.write(f"{getTeam(str(team2))['fullName']},")
                todaysGamesFile.write(f"{getTeam(str(team1))['fullName']},")
                todaysGamesFile.write(f"{team1SpreadValues},")
                todaysGamesFile.write(f"{predictedTeam1SpreadResults},")
                todaysGamesFile.write(f"{overUnderValues},")
                todaysGamesFile.write(f"{predictedOverUnderResults}',\n")
                # todaysGamesFile.write(f"{predictedScores['team2'][0]},")
                # todaysGamesFile.write(f"{predictedScores['team1'][0]}',\n")

            else:
                todaysGamesFile.write(f"'{gameTime},")
                todaysGamesFile.write(f"{getTeam(str(team1))['fullName']},")
                todaysGamesFile.write(f"{getTeam(str(team2))['fullName']},")
                todaysGamesFile.write(f"{team2SpreadValues},")
                todaysGamesFile.write(f"{predictedTeam2SpreadResults},")
                todaysGamesFile.write(f"{overUnderValues},")
                todaysGamesFile.write(f"{predictedOverUnderResults}',\n")
                # todaysGamesFile.write(f"{predictedScores['team1'][0]},")
                # todaysGamesFile.write(f"{predictedScores['team2'][0]}',\n")
            
            

            gamesAlreadyPredicted.append(team1)
            gamesAlreadyPredicted.append(team2)

    todaysGamesFile.write(f"]")
    todaysGamesFile.close()

    print('All games today have been predicted!')


            
def updateDatabaseActualResults():
    #Connect to MySQL Database
    mydb = mysql.connector.connect(
        host='127.0.0.1',
        user='davidcarney',
        password='Sinorrabb1t',
        database='NBA'
        )
    mycursor = mydb.cursor()

    #Get all data from Database where the spread is recorded
    mycursor.execute(f"SELECT * FROM nbaStats where spreadCalculated is not NULL and isWin is not NULL and spreadActual is NULL;")
    teamData = mycursor.fetchall()
    allTeamsDF = pd.DataFrame(teamData, columns = ALL_COLUMNS)
    
    for row in allTeamsDF.values:
        id,gameNumber,teamNumber,isHome,oppTeamNumber,isWin,isOT,gameDayNumber,gameStartNumber,teamPoints,oppTeamPoints,teamWins,teamLosses,teamStreakCode,isInSeasonTournament,year,spread,spreadOdds,overUnder,overUnderOdds,moneyLine,gameTimeActual,spreadCalculated,overUnderCalculated,spreadActual,overUnderActual,gameDate = row
        
        #Calculate overUnder cover
        overUnderCalc = teamPoints + oppTeamPoints
        if overUnderCalc > float(overUnder):
            overUnderActual = 1
        else:
            overUnderActual = 0

        #Calculate the spread
        spreadFavored = spread[0]
        spreadValue = float(spread[1:])
        
        if spreadFavored == '-':
            spreadCalc = teamPoints - oppTeamPoints
            if spreadCalc > spreadValue:
                spreadActual = 1
            else:
                spreadActual = 0
        else:
            spreadCalc = oppTeamPoints - teamPoints
            if spreadCalc > spreadValue:
                spreadActual = 0
            else:
                spreadActual = 1

        updateData = (
            f"UPDATE nbaStats "
            f"SET spreadActual = {spreadActual}, "
            f"overUnderActual = {overUnderActual} "
            f"WHERE id = {id};"
        )
        mycursor.execute(updateData)
        mydb.commit()

    print('All actual results have been saved to database!')
    


def percentHelper(win, firstName, secondName):
    name = f'{firstName}_{secondName}'

    if win == True:
        ALL_PERCENTAGES[name] = [ALL_PERCENTAGES[name][0] + 100, ALL_PERCENTAGES[name][1] + 1] 
    else:
        ALL_PERCENTAGES[name] = [ALL_PERCENTAGES[name][0], ALL_PERCENTAGES[name][1] + 1]


def updatePercentages():
    #global variable
    overallName = 'overall'

    #Connect to MySQL Database
    mydb = mysql.connector.connect(
        host='127.0.0.1',
        user='davidcarney',
        password='Sinorrabb1t',
        database='NBA'
        )
    mycursor = mydb.cursor()

    #Get all data from Database where the spread is recorded
    mycursor.execute(f"SELECT * FROM nbaStats where spreadActual is not NULL;")
    data = mycursor.fetchall()
    df = pd.DataFrame(data, columns = ALL_COLUMNS)
    
    #Iterate over each team
    teams = getTeam(ALL_TEAMS)

    todaysDate = date.today()
    past1Day = int(todaysDate.strftime('%d')) - 1
    past1Date = todaysDate.replace(day=past1Day)
    past2Day = int(todaysDate.strftime('%d')) - 2
    past2Date = todaysDate.replace(day=past2Day)
    past3Day = int(todaysDate.strftime('%d')) - 3
    past3Date = todaysDate.replace(day=past3Day)
    past4Day = int(todaysDate.strftime('%d')) - 4
    past4Date = todaysDate.replace(day=past4Day)
    past5Day = int(todaysDate.strftime('%d')) - 5
    past5Date = todaysDate.replace(day=past5Day)
    
    past5Days = [past1Date.strftime('%m/%d/%y'), past2Date.strftime('%m/%d/%y'), past3Date.strftime('%m/%d/%y'), past4Date.strftime('%m/%d/%y'), past5Date.strftime('%m/%d/%y')]

    #Get todays date for overall last 5 days
    for row in df.sort_values(by=['gameNumber']).values[::-1]:
        id,gameNumber,teamNumber,isHome,oppTeamNumber,isWin,isOT,gameDayNumber,gameStartNumber,teamPoints,oppTeamPoints,teamWins,teamLosses,teamStreakCode,isInSeasonTournament,year,spread,spreadOdds,overUnder,overUnderOdds,moneyLine,gameTimeActual,spreadCalculated,overUnderCalculated,spreadActual,overUnderActual,gameDate = row
        teamShortName = getTeam(str(teamNumber))['shortName']
        teamWinSpread = spreadCalculated == spreadActual
        teamWinOverUnder = overUnderCalculated == overUnderActual
        teamWinParlay = teamWinSpread and teamWinOverUnder

        #Calculate team percents
        percentHelper(teamWinSpread, teamShortName, 'spread')
        percentHelper(teamWinOverUnder, teamShortName, 'overUnder')
        percentHelper(teamWinParlay, teamShortName, 'parlay')

        #Calculate team day percents
        if gameDayNumber == 0:
            #Sunday
            percentHelper(teamWinSpread, teamShortName, 'Sunday_spread')
            percentHelper(teamWinOverUnder, teamShortName, 'Sunday_overUnder')
            percentHelper(teamWinParlay, teamShortName, 'Sunday_parlay')
        elif gameDayNumber == 1:
            #Monday
            percentHelper(teamWinSpread, teamShortName, 'Monday_spread')
            percentHelper(teamWinOverUnder, teamShortName, 'Monday_overUnder')
            percentHelper(teamWinParlay, teamShortName, 'Monday_parlay')
        elif gameDayNumber == 2:
            #Tuesday
            percentHelper(teamWinSpread, teamShortName, 'Tuesday_spread')
            percentHelper(teamWinOverUnder, teamShortName, 'Tuesday_overUnder')
            percentHelper(teamWinParlay, teamShortName, 'Tuesday_parlay')
        elif gameDayNumber == 3:
            #Wednesday
            percentHelper(teamWinSpread, teamShortName, 'Wednesday_spread')
            percentHelper(teamWinOverUnder, teamShortName, 'Wednesday_overUnder')
            percentHelper(teamWinParlay, teamShortName, 'Wednesday_parlay')
        elif gameDayNumber == 4:
            #Thursday
            percentHelper(teamWinSpread, teamShortName, 'Thursday_spread')
            percentHelper(teamWinOverUnder, teamShortName, 'Thursday_overUnder')
            percentHelper(teamWinParlay, teamShortName, 'Thursday_parlay')
        elif gameDayNumber == 5:
            #Friday
            percentHelper(teamWinSpread, teamShortName, 'Friday_spread')
            percentHelper(teamWinOverUnder, teamShortName, 'Friday_overUnder')
            percentHelper(teamWinParlay, teamShortName, 'Friday_parlay')
        elif gameDayNumber == 6:
            #Saturday
            percentHelper(teamWinSpread, teamShortName, 'Saturday_spread')
            percentHelper(teamWinOverUnder, teamShortName, 'Saturday_overUnder')
            percentHelper(teamWinParlay, teamShortName, 'Saturday_parlay')

        #Calculate team time percents
        if (gameStartNumber == 0) or (gameStartNumber == 1):
            #12 - 12:59
            percentHelper(teamWinSpread, teamShortName, 'Time_12_1259_spread')
            percentHelper(teamWinOverUnder, teamShortName, 'Time_12_1259_overUnder')
            percentHelper(teamWinParlay, teamShortName, 'Time_12_1259_parlay')
        elif (gameStartNumber == 2) or (gameStartNumber == 3):
            #1 - 1:59
            percentHelper(teamWinSpread, teamShortName, 'Time_1_159_spread')
            percentHelper(teamWinOverUnder, teamShortName, 'Time_1_159_overUnder')
            percentHelper(teamWinParlay, teamShortName, 'Time_1_159_parlay')
        elif (gameStartNumber == 4) or (gameStartNumber == 5):
            #2 - 2:59
            percentHelper(teamWinSpread, teamShortName, 'Time_2_259_spread')
            percentHelper(teamWinOverUnder, teamShortName, 'Time_2_259_overUnder')
            percentHelper(teamWinParlay, teamShortName, 'Time_2_259_parlay')
        elif (gameStartNumber == 6) or (gameStartNumber == 7):
            #3 - 3:59
            percentHelper(teamWinSpread, teamShortName, 'Time_3_359_spread')
            percentHelper(teamWinOverUnder, teamShortName, 'Time_3_359_overUnder')
            percentHelper(teamWinParlay, teamShortName, 'Time_3_359_parlay')
        elif (gameStartNumber == 8) or (gameStartNumber == 9):
            #4 - 4:59
            percentHelper(teamWinSpread, teamShortName, 'Time_4_459_spread')
            percentHelper(teamWinOverUnder, teamShortName, 'Time_4_459_overUnder')
            percentHelper(teamWinParlay, teamShortName, 'Time_4_459_parlay')
        elif (gameStartNumber == 10) or (gameStartNumber == 11):
            #5 - 5:59
            percentHelper(teamWinSpread, teamShortName, 'Time_5_559_spread')
            percentHelper(teamWinOverUnder, teamShortName, 'Time_5_559_overUnder')
            percentHelper(teamWinParlay, teamShortName, 'Time_5_559_parlay')
        elif (gameStartNumber == 12) or (gameStartNumber == 13):
            #6 - 6:59
            percentHelper(teamWinSpread, teamShortName, 'Time_6_659_spread')
            percentHelper(teamWinOverUnder, teamShortName, 'Time_6_659_overUnder')
            percentHelper(teamWinParlay, teamShortName, 'Time_6_659_parlay')
        elif (gameStartNumber == 14) or (gameStartNumber == 15):
            #7 - 7:59
            percentHelper(teamWinSpread, teamShortName, 'Time_7_759_spread')
            percentHelper(teamWinOverUnder, teamShortName, 'Time_7_759_overUnder')
            percentHelper(teamWinParlay, teamShortName, 'Time_7_759_parlay')
        elif (gameStartNumber == 16) or (gameStartNumber == 17):
            #8 - 8:59
            percentHelper(teamWinSpread, teamShortName, 'Time_8_859_spread')
            percentHelper(teamWinOverUnder, teamShortName, 'Time_8_859_overUnder')
            percentHelper(teamWinParlay, teamShortName, 'Time_8_859_parlay')
        elif (gameStartNumber == 18) or (gameStartNumber == 19):
            #9 - 9:59
            percentHelper(teamWinSpread, teamShortName, 'Time_9_959_spread')
            percentHelper(teamWinOverUnder, teamShortName, 'Time_9_959_overUnder')
            percentHelper(teamWinParlay, teamShortName, 'Time_9_959_parlay')
        elif (gameStartNumber == 20) or (gameStartNumber == 21):
            #10 - 10:59
            percentHelper(teamWinSpread, teamShortName, 'Time_10_1059_spread')
            percentHelper(teamWinOverUnder, teamShortName, 'Time_10_1059_overUnder')
            percentHelper(teamWinParlay, teamShortName, 'Time_10_1059_parlay')
        elif (gameStartNumber == 22) or (gameStartNumber == 23):
            #11 - 11:59
            percentHelper(teamWinSpread, teamShortName, 'Time_11_1159_spread')
            percentHelper(teamWinOverUnder, teamShortName, 'Time_11_1159_overUnder')
            percentHelper(teamWinParlay, teamShortName, 'Time_11_1159_parlay')

        #Calculate team last 5 games
        teamCount = TEAM_LAST_5_GAME_COUNT[teamShortName]
        if teamCount < 5:
            if teamCount == 0:
                percentHelper(teamWinSpread,teamShortName,'last_games_spread_1')
                percentHelper(teamWinOverUnder,teamShortName,'last_games_overUnder_1')
                percentHelper(teamWinParlay,teamShortName,'last_games_parlay_1')
            elif teamCount == 1:
                percentHelper(teamWinSpread,teamShortName,'last_games_spread_2')
                percentHelper(teamWinOverUnder,teamShortName,'last_games_overUnder_2')
                percentHelper(teamWinParlay,teamShortName,'last_games_parlay_2')
            elif teamCount == 2:
                percentHelper(teamWinSpread,teamShortName,'last_games_spread_3')
                percentHelper(teamWinOverUnder,teamShortName,'last_games_overUnder_3')
                percentHelper(teamWinParlay,teamShortName,'last_games_parlay_3')
            elif teamCount == 3:
                percentHelper(teamWinSpread,teamShortName,'last_games_spread_4')
                percentHelper(teamWinOverUnder,teamShortName,'last_games_overUnder_4')
                percentHelper(teamWinParlay,teamShortName,'last_games_parlay_4')
            elif teamCount == 4:
                percentHelper(teamWinSpread,teamShortName,'last_games_spread_5')
                percentHelper(teamWinOverUnder,teamShortName,'last_games_overUnder_5')
                percentHelper(teamWinParlay,teamShortName,'last_games_parlay_5')

            TEAM_LAST_5_GAME_COUNT[teamShortName] = teamCount + 1

        #Calculate overall last 5 games
        if gameDate in past5Days:
            if gameDate == past5Days[0]:
                percentHelper(teamWinSpread,overallName,'last_games_spread_1')
                percentHelper(teamWinOverUnder,overallName,'last_games_overUnder_1')
                percentHelper(teamWinParlay,overallName,'last_games_parlay_1')
            elif gameDate == past5Days[1]:
                percentHelper(teamWinSpread,overallName,'last_games_spread_2')
                percentHelper(teamWinOverUnder,overallName,'last_games_overUnder_2')
                percentHelper(teamWinParlay,overallName,'last_games_parlay_2')
            elif gameDate == past5Days[2]:
                percentHelper(teamWinSpread,overallName,'last_games_spread_3')
                percentHelper(teamWinOverUnder,overallName,'last_games_overUnder_3')
                percentHelper(teamWinParlay,overallName,'last_games_parlay_3')
            elif gameDate == past5Days[3]:
                percentHelper(teamWinSpread,overallName,'last_games_spread_4')
                percentHelper(teamWinOverUnder,overallName,'last_games_overUnder_4')
                percentHelper(teamWinParlay,overallName,'last_games_parlay_4')
            elif gameDate == past5Days[4]:
                percentHelper(teamWinSpread,overallName,'last_games_spread_5')
                percentHelper(teamWinOverUnder,overallName,'last_games_overUnder_5')
                percentHelper(teamWinParlay,overallName,'last_games_parlay_5')


        #Calculate overall percents
        percentHelper(teamWinSpread, overallName, 'spread')
        percentHelper(teamWinOverUnder, overallName, 'overUnder')
        percentHelper(teamWinParlay, overallName, 'parlay')

        #Calculate overall day percents
        if gameDayNumber == 0:
            #Sunday
            percentHelper(teamWinSpread, overallName, 'Sunday_spread')
            percentHelper(teamWinOverUnder, overallName, 'Sunday_overUnder')
            percentHelper(teamWinParlay, overallName, 'Sunday_parlay')
        elif gameDayNumber == 1:
            #Monday
            percentHelper(teamWinSpread, overallName, 'Monday_spread')
            percentHelper(teamWinOverUnder, overallName, 'Monday_overUnder')
            percentHelper(teamWinParlay, overallName, 'Monday_parlay')
        elif gameDayNumber == 2:
            #Tuesday
            percentHelper(teamWinSpread, overallName, 'Tuesday_spread')
            percentHelper(teamWinOverUnder, overallName, 'Tuesday_overUnder')
            percentHelper(teamWinParlay, overallName, 'Tuesday_parlay')
        elif gameDayNumber == 3:
            #Wednesday
            percentHelper(teamWinSpread, overallName, 'Wednesday_spread')
            percentHelper(teamWinOverUnder, overallName, 'Wednesday_overUnder')
            percentHelper(teamWinParlay, overallName, 'Wednesday_parlay')
        elif gameDayNumber == 4:
            #Thursday
            percentHelper(teamWinSpread, overallName, 'Thursday_spread')
            percentHelper(teamWinOverUnder, overallName, 'Thursday_overUnder')
            percentHelper(teamWinParlay, overallName, 'Thursday_parlay')
        elif gameDayNumber == 5:
            #Friday
            percentHelper(teamWinSpread, overallName, 'Friday_spread')
            percentHelper(teamWinOverUnder, overallName, 'Friday_overUnder')
            percentHelper(teamWinParlay, overallName, 'Friday_parlay')
        elif gameDayNumber == 6:
            #Saturday
            percentHelper(teamWinSpread, overallName, 'Saturday_spread')
            percentHelper(teamWinOverUnder, overallName, 'Saturday_overUnder')
            percentHelper(teamWinParlay, overallName, 'Saturday_parlay')

        #Calculate overall time percents
        if (gameStartNumber == 0) or (gameStartNumber == 1):
            #12 - 12:59
            percentHelper(teamWinSpread, overallName, 'Time_12_1259_spread')
            percentHelper(teamWinOverUnder, overallName, 'Time_12_1259_overUnder')
            percentHelper(teamWinParlay, overallName, 'Time_12_1259_parlay')
        elif (gameStartNumber == 2) or (gameStartNumber == 3):
            #1 - 1:59
            percentHelper(teamWinSpread, overallName, 'Time_1_159_spread')
            percentHelper(teamWinOverUnder, overallName, 'Time_1_159_overUnder')
            percentHelper(teamWinParlay, overallName, 'Time_1_159_parlay')
        elif (gameStartNumber == 4) or (gameStartNumber == 5):
            #2 - 2:59
            percentHelper(teamWinSpread, overallName, 'Time_2_259_spread')
            percentHelper(teamWinOverUnder, overallName, 'Time_2_259_overUnder')
            percentHelper(teamWinParlay, overallName, 'Time_2_259_parlay')
        elif (gameStartNumber == 6) or (gameStartNumber == 7):
            #3 - 3:59
            percentHelper(teamWinSpread, overallName, 'Time_3_359_spread')
            percentHelper(teamWinOverUnder, overallName, 'Time_3_359_overUnder')
            percentHelper(teamWinParlay, overallName, 'Time_3_359_parlay')
        elif (gameStartNumber == 8) or (gameStartNumber == 9):
            #4 - 4:59
            percentHelper(teamWinSpread, overallName, 'Time_4_459_spread')
            percentHelper(teamWinOverUnder, overallName, 'Time_4_459_overUnder')
            percentHelper(teamWinParlay, overallName, 'Time_4_459_parlay')
        elif (gameStartNumber == 10) or (gameStartNumber == 11):
            #5 - 5:59
            percentHelper(teamWinSpread, overallName, 'Time_5_559_spread')
            percentHelper(teamWinOverUnder, overallName, 'Time_5_559_overUnder')
            percentHelper(teamWinParlay, overallName, 'Time_5_559_parlay')
        elif (gameStartNumber == 12) or (gameStartNumber == 13):
            #6 - 6:59
            percentHelper(teamWinSpread, overallName, 'Time_6_659_spread')
            percentHelper(teamWinOverUnder, overallName, 'Time_6_659_overUnder')
            percentHelper(teamWinParlay, overallName, 'Time_6_659_parlay')
        elif (gameStartNumber == 14) or (gameStartNumber == 15):
            #7 - 7:59
            percentHelper(teamWinSpread, overallName, 'Time_7_759_spread')
            percentHelper(teamWinOverUnder, overallName, 'Time_7_759_overUnder')
            percentHelper(teamWinParlay, overallName, 'Time_7_759_parlay')
        elif (gameStartNumber == 16) or (gameStartNumber == 17):
            #8 - 8:59
            percentHelper(teamWinSpread, overallName, 'Time_8_859_spread')
            percentHelper(teamWinOverUnder, overallName, 'Time_8_859_overUnder')
            percentHelper(teamWinParlay, overallName, 'Time_8_859_parlay')
        elif (gameStartNumber == 18) or (gameStartNumber == 19):
            #9 - 9:59
            percentHelper(teamWinSpread, overallName, 'Time_9_959_spread')
            percentHelper(teamWinOverUnder, overallName, 'Time_9_959_overUnder')
            percentHelper(teamWinParlay, overallName, 'Time_9_959_parlay')
        elif (gameStartNumber == 20) or (gameStartNumber == 21):
            #10 - 10:59
            percentHelper(teamWinSpread, overallName, 'Time_10_1059_spread')
            percentHelper(teamWinOverUnder, overallName, 'Time_10_1059_overUnder')
            percentHelper(teamWinParlay, overallName, 'Time_10_1059_parlay')
        elif (gameStartNumber == 22) or (gameStartNumber == 23):
            #11 - 11:59
            percentHelper(teamWinSpread, overallName, 'Time_11_1159_spread')
            percentHelper(teamWinOverUnder, overallName, 'Time_11_1159_overUnder')
            percentHelper(teamWinParlay, overallName, 'Time_11_1159_parlay')

    for percent in ALL_PERCENTAGES:
        if ALL_PERCENTAGES[percent][1] != 0:
            ALL_PERCENTAGES[percent] = round(ALL_PERCENTAGES[percent][0] / ALL_PERCENTAGES[percent][1], 2)
        else:
            ALL_PERCENTAGES[percent] = 'NA'

    #Open frontend file and write ALL_PERCENTAGES
    percentagesFilename = '../frontend/src/nbaPages/percentages.js'
    percentagesFile = open(percentagesFilename, 'w')
    percentagesFile.write('export const percentages = {\n')
    for percent in ALL_PERCENTAGES:
        value = ALL_PERCENTAGES[percent]
        if value == 'NA':
            percentagesFile.write(f"{percent} : 'NA',\n")
        else:
            percentagesFile.write(f"{percent} : {value},\n")
    percentagesFile.write('}')
    percentagesFile.close()

    print('All percentages have been sent to the frontend!')
 

def runParlays():
    #Initial variables
    teams = getTeam(ALL_TEAMS)
    columnsToPredict = ['spreadActual','overUnderActual']
    columnsToRemove = ['isWin','isOT','teamWins','teamLosses','teamStreakCode','gameTimeActual','date']
    gamblingColumns = ['spread','spreadOdds','overUnder','overUnderOdds','moneyLine']
    year = 2024


    #Connect to MySQL Database
    mydb = mysql.connector.connect(
        host='127.0.0.1',
        user='davidcarney',
        password='Sinorrabb1t',
        database='NBA'
        )
    mycursor = mydb.cursor()

    #Get all data from Database
    mycursor.execute(f"SELECT * FROM nbaStats;")
    teamData = mycursor.fetchall()
    allTeamsDF = pd.DataFrame(teamData, columns = ALL_COLUMNS)

    #create DF of games to predict
    gamesToBePredictedDF = allTeamsDF[(allTeamsDF['isWin'].isna()) & (allTeamsDF['spread'].notna())]
    gamesToBePredictedDFWoGD = gamesToBePredictedDF.drop(columns = columnsToRemove)
    gamesToBePredictedDFWoGD = gamesToBePredictedDFWoGD.drop(columns = columnsToPredict)
    
    #Create DF for training data
    df = allTeamsDF[(allTeamsDF['isWin'].notna()) & (allTeamsDF['spread'].notna())]
    df = df.drop(columns = columnsToRemove)
    df['spreadOdds'] = df['spreadOdds'].replace(to_replace='−', value='-', regex=True)
    df['overUnderOdds'] = df['overUnderOdds'].replace(to_replace='−', value='-', regex=True)
    df['moneyLine'] = df['moneyLine'].replace(to_replace='−', value='-', regex=True)
    df[gamblingColumns] = df[gamblingColumns].astype(float)

    print(df)

    featureSelection =  RFECV(estimator, step=1, cv=2)
    elasticNetGS = GridSearchCV(elasticNet, elasticNetParams, cv=2, scoring='neg_mean_absolute_error')
    elasticNetGS.fit(X_train, y_train)
    bestElasticNet2 = ElasticNet(alpha = elasticNetGS.best_params_['alpha'], random_state=19)
 

            
    # for column in columnsToPredict:
    #     y = df[column]
    #     X = df.drop(columns=columnsToPredict)

    #     X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.19, random_state = 19)
        
    #     #Scale training and testing data
    #     scalar = StandardScaler()
        
    #     scalar.fit(X_train)
    #     X_train = scalar.transform(X_train)
    #     X_test = scalar.transform(X_test)

    #     #Feature selection
    #     featureSelection = VarianceThreshold(threshold=(.8 * (1 - .8)))
    #     X_train = featureSelection.fit_transform(X_train)





    print('All parlays today have been predicted!')


  

updateNBAGames()
getGamblingData()
runML()
updateDatabaseActualResults()
updatePercentages()
# runParlays()
