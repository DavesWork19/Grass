import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import mysql.connector
from datetime import date, datetime, timedelta
import random
import matplotlib.pyplot as plt

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
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import SGDClassifier

from selenium import webdriver
from selenium.webdriver.common.by import By

from legends import *
from constants import *


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
        #ADD A CHECK FOR PK VALUES

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
    print('(2/8) All gambling data has been saved!')



def runML():
    #Initial variables
    teams = getTeam(ALL_TEAMS)
    columnsToPredict = ['teamPoints','oppTeamPoints']
    columnsToRemove = ['isWin','isOT','teamWins','teamLosses','teamStreakCode','spread','spreadOdds','overUnder','overUnderOdds','moneyLine','gameTimeActual','date']
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
                X_test = featureSelection.transform(X_test)

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

                team1DataToPredict = featureSelection.transform(team1DataToPredict)
                team2DataToPredict = featureSelection.transform(team2DataToPredict)

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

    print('(3/8) All games today have been predicted!')

            
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

    print('(4/8) All actual results have been saved to database!')
    


def percentHelper(win, firstName, secondName):
    name = f'{firstName}_{secondName}'

    if win == True:
        ALL_PERCENTAGES[name] = [ALL_PERCENTAGES[name][0] + 100, ALL_PERCENTAGES[name][1] + 1] 
    else:
        ALL_PERCENTAGES[name] = [ALL_PERCENTAGES[name][0], ALL_PERCENTAGES[name][1] + 1]


def updatePercentages(save = 'dont'):
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
    past1Date = todaysDate - timedelta(days=1)
    past2Date = todaysDate - timedelta(days=2)
    past3Date = todaysDate - timedelta(days=3)
    past4Date = todaysDate - timedelta(days=4)
    past5Date = todaysDate - timedelta(days=5)
    past5Days = [past1Date.strftime('%m/%d/%y'), past2Date.strftime('%m/%d/%y'), past3Date.strftime('%m/%d/%y'), past4Date.strftime('%m/%d/%y'), past5Date.strftime('%m/%d/%y')]

    #Get todays date for overall last 5 days
    for row in df.sort_values(by=['gameNumber']).values[::-1]:
        id,gameNumber,teamNumber,isHome,oppTeamNumber,isWin,isOT,gameDayNumber,gameStartNumber,teamPoints,oppTeamPoints,teamWins,teamLosses,teamStreakCode,isInSeasonTournament,year,spread,spreadOdds,overUnder,overUnderOdds,moneyLine,gameTimeActual,spreadCalculated,overUnderCalculated,spreadActual,overUnderActual,gameDate = row
        teamShortName = getTeam(str(teamNumber))['shortName']
        teamWinSpread = spreadCalculated == spreadActual
        teamWinOverUnder = overUnderCalculated == overUnderActual
        teamWinParlay = teamWinSpread and teamWinOverUnder

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

        #Calculate team percents
        percentHelper(teamWinSpread, teamShortName, 'spread')
        percentHelper(teamWinOverUnder, teamShortName, 'overUnder')
        percentHelper(teamWinParlay, teamShortName, 'parlay')

        #Calculate day percents
        if gameDayNumber == 0:
            #Sunday
            percentHelper(teamWinSpread, overallName, 'Sunday_spread')
            percentHelper(teamWinOverUnder, overallName, 'Sunday_overUnder')
            percentHelper(teamWinParlay, overallName, 'Sunday_parlay')

            percentHelper(teamWinSpread, teamShortName, 'Sunday_spread')
            percentHelper(teamWinOverUnder, teamShortName, 'Sunday_overUnder')
            percentHelper(teamWinParlay, teamShortName, 'Sunday_parlay')
        elif gameDayNumber == 1:
            #Monday
            percentHelper(teamWinSpread, overallName, 'Monday_spread')
            percentHelper(teamWinOverUnder, overallName, 'Monday_overUnder')
            percentHelper(teamWinParlay, overallName, 'Monday_parlay')

            percentHelper(teamWinSpread, teamShortName, 'Monday_spread')
            percentHelper(teamWinOverUnder, teamShortName, 'Monday_overUnder')
            percentHelper(teamWinParlay, teamShortName, 'Monday_parlay')
        elif gameDayNumber == 2:
            #Tuesday
            percentHelper(teamWinSpread, overallName, 'Tuesday_spread')
            percentHelper(teamWinOverUnder, overallName, 'Tuesday_overUnder')
            percentHelper(teamWinParlay, overallName, 'Tuesday_parlay')

            percentHelper(teamWinSpread, teamShortName, 'Tuesday_spread')
            percentHelper(teamWinOverUnder, teamShortName, 'Tuesday_overUnder')
            percentHelper(teamWinParlay, teamShortName, 'Tuesday_parlay')
        elif gameDayNumber == 3:
            #Wednesday
            percentHelper(teamWinSpread, overallName, 'Wednesday_spread')
            percentHelper(teamWinOverUnder, overallName, 'Wednesday_overUnder')
            percentHelper(teamWinParlay, overallName, 'Wednesday_parlay')

            percentHelper(teamWinSpread, teamShortName, 'Wednesday_spread')
            percentHelper(teamWinOverUnder, teamShortName, 'Wednesday_overUnder')
            percentHelper(teamWinParlay, teamShortName, 'Wednesday_parlay')
        elif gameDayNumber == 4:
            #Thursday
            percentHelper(teamWinSpread, overallName, 'Thursday_spread')
            percentHelper(teamWinOverUnder, overallName, 'Thursday_overUnder')
            percentHelper(teamWinParlay, overallName, 'Thursday_parlay')

            percentHelper(teamWinSpread, teamShortName, 'Thursday_spread')
            percentHelper(teamWinOverUnder, teamShortName, 'Thursday_overUnder')
            percentHelper(teamWinParlay, teamShortName, 'Thursday_parlay')
        elif gameDayNumber == 5:
            #Friday
            percentHelper(teamWinSpread, overallName, 'Friday_spread')
            percentHelper(teamWinOverUnder, overallName, 'Friday_overUnder')
            percentHelper(teamWinParlay, overallName, 'Friday_parlay')

            percentHelper(teamWinSpread, teamShortName, 'Friday_spread')
            percentHelper(teamWinOverUnder, teamShortName, 'Friday_overUnder')
            percentHelper(teamWinParlay, teamShortName, 'Friday_parlay')
        elif gameDayNumber == 6:
            #Saturday
            percentHelper(teamWinSpread, overallName, 'Saturday_spread')
            percentHelper(teamWinOverUnder, overallName, 'Saturday_overUnder')
            percentHelper(teamWinParlay, overallName, 'Saturday_parlay')

            percentHelper(teamWinSpread, teamShortName, 'Saturday_spread')
            percentHelper(teamWinOverUnder, teamShortName, 'Saturday_overUnder')
            percentHelper(teamWinParlay, teamShortName, 'Saturday_parlay')

        #Calculate time percents
        if (gameStartNumber == 0) or (gameStartNumber == 1):
            #12 - 12:59
            percentHelper(teamWinSpread, overallName, 'Time_12_1259_spread')
            percentHelper(teamWinOverUnder, overallName, 'Time_12_1259_overUnder')
            percentHelper(teamWinParlay, overallName, 'Time_12_1259_parlay')

            percentHelper(teamWinSpread, teamShortName, 'Time_12_1259_spread')
            percentHelper(teamWinOverUnder, teamShortName, 'Time_12_1259_overUnder')
            percentHelper(teamWinParlay, teamShortName, 'Time_12_1259_parlay')
        elif (gameStartNumber == 2) or (gameStartNumber == 3):
            #1 - 1:59
            percentHelper(teamWinSpread, overallName, 'Time_1_159_spread')
            percentHelper(teamWinOverUnder, overallName, 'Time_1_159_overUnder')
            percentHelper(teamWinParlay, overallName, 'Time_1_159_parlay')

            percentHelper(teamWinSpread, teamShortName, 'Time_1_159_spread')
            percentHelper(teamWinOverUnder, teamShortName, 'Time_1_159_overUnder')
            percentHelper(teamWinParlay, teamShortName, 'Time_1_159_parlay')
        elif (gameStartNumber == 4) or (gameStartNumber == 5):
            #2 - 2:59
            percentHelper(teamWinSpread, overallName, 'Time_2_259_spread')
            percentHelper(teamWinOverUnder, overallName, 'Time_2_259_overUnder')
            percentHelper(teamWinParlay, overallName, 'Time_2_259_parlay')

            percentHelper(teamWinSpread, teamShortName, 'Time_2_259_spread')
            percentHelper(teamWinOverUnder, teamShortName, 'Time_2_259_overUnder')
            percentHelper(teamWinParlay, teamShortName, 'Time_2_259_parlay')
        elif (gameStartNumber == 6) or (gameStartNumber == 7):
            #3 - 3:59
            percentHelper(teamWinSpread, overallName, 'Time_3_359_spread')
            percentHelper(teamWinOverUnder, overallName, 'Time_3_359_overUnder')
            percentHelper(teamWinParlay, overallName, 'Time_3_359_parlay')

            percentHelper(teamWinSpread, teamShortName, 'Time_3_359_spread')
            percentHelper(teamWinOverUnder, teamShortName, 'Time_3_359_overUnder')
            percentHelper(teamWinParlay, teamShortName, 'Time_3_359_parlay')
        elif (gameStartNumber == 8) or (gameStartNumber == 9):
            #4 - 4:59
            percentHelper(teamWinSpread, overallName, 'Time_4_459_spread')
            percentHelper(teamWinOverUnder, overallName, 'Time_4_459_overUnder')
            percentHelper(teamWinParlay, overallName, 'Time_4_459_parlay')

            percentHelper(teamWinSpread, teamShortName, 'Time_4_459_spread')
            percentHelper(teamWinOverUnder, teamShortName, 'Time_4_459_overUnder')
            percentHelper(teamWinParlay, teamShortName, 'Time_4_459_parlay')
        elif (gameStartNumber == 10) or (gameStartNumber == 11):
            #5 - 5:59
            percentHelper(teamWinSpread, overallName, 'Time_5_559_spread')
            percentHelper(teamWinOverUnder, overallName, 'Time_5_559_overUnder')
            percentHelper(teamWinParlay, overallName, 'Time_5_559_parlay')

            percentHelper(teamWinSpread, teamShortName, 'Time_5_559_spread')
            percentHelper(teamWinOverUnder, teamShortName, 'Time_5_559_overUnder')
            percentHelper(teamWinParlay, teamShortName, 'Time_5_559_parlay')
        elif (gameStartNumber == 12) or (gameStartNumber == 13):
            #6 - 6:59
            percentHelper(teamWinSpread, overallName, 'Time_6_659_spread')
            percentHelper(teamWinOverUnder, overallName, 'Time_6_659_overUnder')
            percentHelper(teamWinParlay, overallName, 'Time_6_659_parlay')

            percentHelper(teamWinSpread, teamShortName, 'Time_6_659_spread')
            percentHelper(teamWinOverUnder, teamShortName, 'Time_6_659_overUnder')
            percentHelper(teamWinParlay, teamShortName, 'Time_6_659_parlay')
        elif (gameStartNumber == 14) or (gameStartNumber == 15):
            #7 - 7:59
            percentHelper(teamWinSpread, overallName, 'Time_7_759_spread')
            percentHelper(teamWinOverUnder, overallName, 'Time_7_759_overUnder')
            percentHelper(teamWinParlay, overallName, 'Time_7_759_parlay')

            percentHelper(teamWinSpread, teamShortName, 'Time_7_759_spread')
            percentHelper(teamWinOverUnder, teamShortName, 'Time_7_759_overUnder')
            percentHelper(teamWinParlay, teamShortName, 'Time_7_759_parlay')
        elif (gameStartNumber == 16) or (gameStartNumber == 17):
            #8 - 8:59
            percentHelper(teamWinSpread, overallName, 'Time_8_859_spread')
            percentHelper(teamWinOverUnder, overallName, 'Time_8_859_overUnder')
            percentHelper(teamWinParlay, overallName, 'Time_8_859_parlay')

            percentHelper(teamWinSpread, teamShortName, 'Time_8_859_spread')
            percentHelper(teamWinOverUnder, teamShortName, 'Time_8_859_overUnder')
            percentHelper(teamWinParlay, teamShortName, 'Time_8_859_parlay')
        elif (gameStartNumber == 18) or (gameStartNumber == 19):
            #9 - 9:59
            percentHelper(teamWinSpread, overallName, 'Time_9_959_spread')
            percentHelper(teamWinOverUnder, overallName, 'Time_9_959_overUnder')
            percentHelper(teamWinParlay, overallName, 'Time_9_959_parlay')

            percentHelper(teamWinSpread, teamShortName, 'Time_9_959_spread')
            percentHelper(teamWinOverUnder, teamShortName, 'Time_9_959_overUnder')
            percentHelper(teamWinParlay, teamShortName, 'Time_9_959_parlay')
        elif (gameStartNumber == 20) or (gameStartNumber == 21):
            #10 - 10:59
            percentHelper(teamWinSpread, overallName, 'Time_10_1059_spread')
            percentHelper(teamWinOverUnder, overallName, 'Time_10_1059_overUnder')
            percentHelper(teamWinParlay, overallName, 'Time_10_1059_parlay')

            percentHelper(teamWinSpread, teamShortName, 'Time_10_1059_spread')
            percentHelper(teamWinOverUnder, teamShortName, 'Time_10_1059_overUnder')
            percentHelper(teamWinParlay, teamShortName, 'Time_10_1059_parlay')
        elif (gameStartNumber == 22) or (gameStartNumber == 23):
            #11 - 11:59
            percentHelper(teamWinSpread, overallName, 'Time_11_1159_spread')
            percentHelper(teamWinOverUnder, overallName, 'Time_11_1159_overUnder')
            percentHelper(teamWinParlay, overallName, 'Time_11_1159_parlay')

            percentHelper(teamWinSpread, teamShortName, 'Time_11_1159_spread')
            percentHelper(teamWinOverUnder, teamShortName, 'Time_11_1159_overUnder')
            percentHelper(teamWinParlay, teamShortName, 'Time_11_1159_parlay')

    for percent in ALL_PERCENTAGES:
        if ALL_PERCENTAGES[percent][1] != 0:
            ALL_PERCENTAGES[percent] = round(ALL_PERCENTAGES[percent][0] / ALL_PERCENTAGES[percent][1], 2)
        else:
            ALL_PERCENTAGES[percent] = 'NA'


    if save == 'save':
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

    print('(5/8) All percentages have been sent to the frontend!')
 


def clearConsts():
    for percent in ALL_PERCENTAGES:
        ALL_PERCENTAGES[percent] = [0,0]

    for team in TEAM_LAST_5_GAME_COUNT:
        TEAM_LAST_5_GAME_COUNT[team] = 0

def updatePercentConstsForParlay():
    clearConsts()

    overallName = 'overall'
    teams = getTeam(ALL_TEAMS)
    datePercentDict = {}    
    
    #Connect to MySQL Database
    mydb = mysql.connector.connect(
        host='127.0.0.1',
        user='davidcarney',
        password='Sinorrabb1t',
        database='NBA'
        )
    mycursor = mydb.cursor()

    #Get all data from Database
    mycursor.execute(f"SELECT * FROM nbaStats WHERE date is not NULL and spreadActual is not NULL;")
    teamData = mycursor.fetchall()
    allTeamsDF = pd.DataFrame(teamData, columns = ALL_COLUMNS)
    allTeamsDF = allTeamsDF.sort_values(by=['date'])
    df = allTeamsDF.copy()

    for col in ALL_COLUMNS_EXT:
        df[col] = [0] * len(df)


    strDateColumn = [x for x in allTeamsDF['date'].unique()[5:]] 
    todaysDate = date.today().strftime('%m/%d/%y')
    strDateColumn.append(todaysDate)

    dateColumn = []
    for strDate in strDateColumn:
        dateColumn.append(datetime.strptime(strDate, '%m/%d/%y'))

    allTeamsDF['date'] = pd.to_datetime(allTeamsDF['date'], format='%m/%d/%y')
    
    for theDate in dateColumn:
        past1Date = theDate - timedelta(days=1)
        past2Date = theDate - timedelta(days=2)
        past3Date = theDate - timedelta(days=3)
        past4Date = theDate - timedelta(days=4)
        past5Date = theDate - timedelta(days=5)
        
        past5Days = [past1Date, past2Date, past3Date, past4Date, past5Date]

        #Get todays date for overall last 5 days
        for row in allTeamsDF[allTeamsDF['date'] < theDate].sort_values(by=['gameNumber']).values[::-1]:
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

        holder = {}
        for percent in ALL_PERCENTAGES:
            if ALL_PERCENTAGES[percent][1] != 0:
                holder[percent] = round(ALL_PERCENTAGES[percent][0] / ALL_PERCENTAGES[percent][1], 2)
            else:
                holder[percent] = 0
    
        datePercentDict[f"{theDate.strftime('%m/%d/%y')}"] = holder
        
        clearConsts()

    for row in df.values:
        id,gameNumber,teamNumber,isHome,oppTeamNumber,isWin,isOT,gameDayNumber,gameStartNumber,teamPoints,oppTeamPoints,teamWins,teamLosses,teamStreakCode,isInSeasonTournament,year,spread,spreadOdds,overUnder,overUnderOdds,moneyLine,gameTimeActual,spreadCalculated,overUnderCalculated,spreadActual,overUnderActual,gameDate,team_spread,team_overUnder,team_parlay,team_date_spread,team_date_overUnder,team_date_parlay,team_time_spread,team_time_overUnder,team_time_parlay,teamPast1DaySpread,teamPast1DayOverUnder,teamPast1DayParlay,teamPast2DaySpread,teamPast2DayOverUnder,teamPast2DayParlay,teamPast3DaySpread,teamPast3DayOverUnder,teamPast3DayParlay,teamPast4DaySpread,teamPast4DayOverUnder,teamPast4DayParlay,teamPast5DaySpread,teamPast5DayOverUnder,teamPast5DayParlay,overall_spread,overall_overUnder,overall_parlay,overall_date_spread,overall_date_overUnder,overall_date_parlay,overall_time_spread,overall_time_overUnder,overall_time_parlay,overallPast1DaySpread,overallPast1DayOverUnder,overallPast1DayParlay,overallPast2DaySpread,overallPast2DayOverUnder,overallPast2DayParlay,overallPast3DaySpread,overallPast3DayOverUnder,overallPast3DayParlay,overallPast4DaySpread,overallPast4DayOverUnder,overallPast4DayParlay,overallPast5DaySpread,overallPast5DayOverUnder,overallPast5DayParlay = row
        for theDate in datePercentDict:
            if theDate == gameDate:
                teamName = getTeam(str(teamNumber))['shortName']
                overallDaySpread = -1
                overallDayOverUnder = -1
                overallDayParlay = -1
                overallTimeSpread = -1
                overallTimeOverUnder = -1
                overallTimeParlay = -1

                teamDaySpread = -1
                teamDayOverUnder = -1
                teamDayParlay = -1
                teamTimeSpread = -1
                teamTimeOverUnder = -1
                teamTimeParlay = -1
                
                #Day Percentages
                if gameDayNumber == 0:
                    #Sunday
                    overallDaySpread = datePercentDict[theDate]['overall_Sunday_spread']
                    overallDayOverUnder = datePercentDict[theDate]['overall_Sunday_overUnder']
                    overallDayParlay = datePercentDict[theDate]['overall_Sunday_parlay']

                    teamDaySpread = datePercentDict[theDate][f'{teamName}_Sunday_spread']
                    teamDayOverUnder = datePercentDict[theDate][f'{teamName}_Sunday_overUnder']
                    teamDayParlay = datePercentDict[theDate][f'{teamName}_Sunday_parlay']
                elif gameDayNumber == 1:
                    #Monday
                    overallDaySpread = datePercentDict[theDate]['overall_Monday_spread']
                    overallDayOverUnder = datePercentDict[theDate]['overall_Monday_overUnder']
                    overallDayParlay = datePercentDict[theDate]['overall_Monday_parlay']

                    teamDaySpread = datePercentDict[theDate][f'{teamName}_Monday_spread']
                    teamDayOverUnder = datePercentDict[theDate][f'{teamName}_Monday_overUnder']
                    teamDayParlay = datePercentDict[theDate][f'{teamName}_Monday_parlay']
                elif gameDayNumber == 2:
                    #Tuesday
                    overallDaySpread = datePercentDict[theDate]['overall_Tuesday_spread']
                    overallDayOverUnder = datePercentDict[theDate]['overall_Tuesday_overUnder']
                    overallDayParlay = datePercentDict[theDate]['overall_Tuesday_parlay']

                    teamDaySpread = datePercentDict[theDate][f'{teamName}_Tuesday_spread']
                    teamDayOverUnder = datePercentDict[theDate][f'{teamName}_Tuesday_overUnder']
                    teamDayParlay = datePercentDict[theDate][f'{teamName}_Tuesday_parlay']
                elif gameDayNumber == 3:
                    #Wednesday
                    overallDaySpread = datePercentDict[theDate]['overall_Wednesday_spread']
                    overallDayOverUnder = datePercentDict[theDate]['overall_Wednesday_overUnder']
                    overallDayParlay = datePercentDict[theDate]['overall_Wednesday_parlay']

                    teamDaySpread = datePercentDict[theDate][f'{teamName}_Wednesday_spread']
                    teamDayOverUnder = datePercentDict[theDate][f'{teamName}_Wednesday_overUnder']
                    teamDayParlay = datePercentDict[theDate][f'{teamName}_Wednesday_parlay']
                elif gameDayNumber == 4:
                    #Thursday
                    overallDaySpread = datePercentDict[theDate]['overall_Thursday_spread']
                    overallDayOverUnder = datePercentDict[theDate]['overall_Thursday_overUnder']
                    overallDayParlay = datePercentDict[theDate]['overall_Thursday_parlay']

                    teamDaySpread = datePercentDict[theDate][f'{teamName}_Thursday_spread']
                    teamDayOverUnder = datePercentDict[theDate][f'{teamName}_Thursday_overUnder']
                    teamDayParlay = datePercentDict[theDate][f'{teamName}_Thursday_parlay']
                elif gameDayNumber == 5:
                    #Friday
                    overallDaySpread = datePercentDict[theDate]['overall_Friday_spread']
                    overallDayOverUnder = datePercentDict[theDate]['overall_Friday_overUnder']
                    overallDayParlay = datePercentDict[theDate]['overall_Friday_parlay']

                    teamDaySpread = datePercentDict[theDate][f'{teamName}_Friday_spread']
                    teamDayOverUnder = datePercentDict[theDate][f'{teamName}_Friday_overUnder']
                    teamDayParlay = datePercentDict[theDate][f'{teamName}_Friday_parlay']
                elif gameDayNumber == 6:
                    #Saturday
                    overallDaySpread = datePercentDict[theDate]['overall_Saturday_spread']
                    overallDayOverUnder = datePercentDict[theDate]['overall_Saturday_overUnder']
                    overallDayParlay = datePercentDict[theDate]['overall_Saturday_parlay']

                    teamDaySpread = datePercentDict[theDate][f'{teamName}_Saturday_spread']
                    teamDayOverUnder = datePercentDict[theDate][f'{teamName}_Saturday_overUnder']
                    teamDayParlay = datePercentDict[theDate][f'{teamName}_Saturday_parlay']
                
                #Time percents
                if (gameStartNumber == 0) or (gameStartNumber == 1):
                    #12 - 12:59
                    overallTimeSpread = datePercentDict[theDate]['overall_Time_12_1259_spread']
                    overallTimeOverUnder = datePercentDict[theDate]['overall_Time_12_1259_overUnder']
                    overallTimeParlay = datePercentDict[theDate]['overall_Time_12_1259_parlay']

                    teamTimeSpread = datePercentDict[theDate][f'{teamName}_Time_12_1259_spread']
                    teamTimeOverUnder = datePercentDict[theDate][f'{teamName}_Time_12_1259_overUnder']
                    teamTimeParlay = datePercentDict[theDate][f'{teamName}_Time_12_1259_parlay']
                elif (gameStartNumber == 2) or (gameStartNumber == 3):
                    #1 - 1:59
                    overallTimeSpread = datePercentDict[theDate]['overall_Time_1_159_spread']
                    overallTimeOverUnder = datePercentDict[theDate]['overall_Time_1_159_overUnder']
                    overallTimeParlay = datePercentDict[theDate]['overall_Time_1_159_parlay']

                    teamTimeSpread = datePercentDict[theDate][f'{teamName}_Time_1_159_spread']
                    teamTimeOverUnder = datePercentDict[theDate][f'{teamName}_Time_1_159_overUnder']
                    teamTimeParlay = datePercentDict[theDate][f'{teamName}_Time_1_159_parlay']
                elif (gameStartNumber == 4) or (gameStartNumber == 5):
                    #2 - 2:59
                    overallTimeSpread = datePercentDict[theDate]['overall_Time_2_259_spread']
                    overallTimeOverUnder = datePercentDict[theDate]['overall_Time_2_259_overUnder']
                    overallTimeParlay = datePercentDict[theDate]['overall_Time_2_259_parlay']

                    teamTimeSpread = datePercentDict[theDate][f'{teamName}_Time_2_259_spread']
                    teamTimeOverUnder = datePercentDict[theDate][f'{teamName}_Time_2_259_overUnder']
                    teamTimeParlay = datePercentDict[theDate][f'{teamName}_Time_2_259_parlay']
                elif (gameStartNumber == 6) or (gameStartNumber == 7):
                    #3 - 3:59
                    overallTimeSpread = datePercentDict[theDate]['overall_Time_3_359_spread']
                    overallTimeOverUnder = datePercentDict[theDate]['overall_Time_3_359_overUnder']
                    overallTimeParlay = datePercentDict[theDate]['overall_Time_3_359_parlay']

                    teamTimeSpread = datePercentDict[theDate][f'{teamName}_Time_3_359_spread']
                    teamTimeOverUnder = datePercentDict[theDate][f'{teamName}_Time_3_359_overUnder']
                    teamTimeParlay = datePercentDict[theDate][f'{teamName}_Time_3_359_parlay']
                elif (gameStartNumber == 8) or (gameStartNumber == 9):
                    #4 - 4:59
                    overallTimeSpread = datePercentDict[theDate]['overall_Time_4_459_spread']
                    overallTimeOverUnder = datePercentDict[theDate]['overall_Time_4_459_overUnder']
                    overallTimeParlay = datePercentDict[theDate]['overall_Time_4_459_parlay']

                    teamTimeSpread = datePercentDict[theDate][f'{teamName}_Time_4_459_spread']
                    teamTimeOverUnder = datePercentDict[theDate][f'{teamName}_Time_4_459_overUnder']
                    teamTimeParlay = datePercentDict[theDate][f'{teamName}_Time_4_459_parlay']
                elif (gameStartNumber == 10) or (gameStartNumber == 11):
                    #5 - 5:59
                    overallTimeSpread = datePercentDict[theDate]['overall_Time_5_559_spread']
                    overallTimeOverUnder = datePercentDict[theDate]['overall_Time_5_559_overUnder']
                    overallTimeParlay = datePercentDict[theDate]['overall_Time_5_559_parlay']

                    teamTimeSpread = datePercentDict[theDate][f'{teamName}_Time_5_559_spread']
                    teamTimeOverUnder = datePercentDict[theDate][f'{teamName}_Time_5_559_overUnder']
                    teamTimeParlay = datePercentDict[theDate][f'{teamName}_Time_5_559_parlay']
                elif (gameStartNumber == 12) or (gameStartNumber == 13):
                    #6 - 6:59
                    overallTimeSpread = datePercentDict[theDate]['overall_Time_6_659_spread']
                    overallTimeOverUnder = datePercentDict[theDate]['overall_Time_6_659_overUnder']
                    overallTimeParlay = datePercentDict[theDate]['overall_Time_6_659_parlay']

                    teamTimeSpread = datePercentDict[theDate][f'{teamName}_Time_6_659_spread']
                    teamTimeOverUnder = datePercentDict[theDate][f'{teamName}_Time_6_659_overUnder']
                    teamTimeParlay = datePercentDict[theDate][f'{teamName}_Time_6_659_parlay']
                elif (gameStartNumber == 14) or (gameStartNumber == 15):
                    #7 - 7:59
                    overallTimeSpread = datePercentDict[theDate]['overall_Time_7_759_spread']
                    overallTimeOverUnder = datePercentDict[theDate]['overall_Time_7_759_overUnder']
                    overallTimeParlay = datePercentDict[theDate]['overall_Time_7_759_parlay']

                    teamTimeSpread = datePercentDict[theDate][f'{teamName}_Time_7_759_spread']
                    teamTimeOverUnder = datePercentDict[theDate][f'{teamName}_Time_7_759_overUnder']
                    teamTimeParlay = datePercentDict[theDate][f'{teamName}_Time_7_759_parlay']
                elif (gameStartNumber == 16) or (gameStartNumber == 17):
                    #8 - 8:59
                    overallTimeSpread = datePercentDict[theDate]['overall_Time_8_859_spread']
                    overallTimeOverUnder = datePercentDict[theDate]['overall_Time_8_859_overUnder']
                    overallTimeParlay = datePercentDict[theDate]['overall_Time_8_859_parlay']

                    teamTimeSpread = datePercentDict[theDate][f'{teamName}_Time_8_859_spread']
                    teamTimeOverUnder = datePercentDict[theDate][f'{teamName}_Time_8_859_overUnder']
                    teamTimeParlay = datePercentDict[theDate][f'{teamName}_Time_8_859_parlay']
                elif (gameStartNumber == 18) or (gameStartNumber == 19):
                    #9 - 9:59
                    overallTimeSpread = datePercentDict[theDate]['overall_Time_9_959_spread']
                    overallTimeOverUnder = datePercentDict[theDate]['overall_Time_9_959_overUnder']
                    overallTimeParlay = datePercentDict[theDate]['overall_Time_9_959_parlay']

                    teamTimeSpread = datePercentDict[theDate][f'{teamName}_Time_9_959_spread']
                    teamTimeOverUnder = datePercentDict[theDate][f'{teamName}_Time_9_959_overUnder']
                    teamTimeParlay = datePercentDict[theDate][f'{teamName}_Time_9_959_parlay']
                elif (gameStartNumber == 20) or (gameStartNumber == 21):
                    #10 - 10:59
                    overallTimeSpread = datePercentDict[theDate]['overall_Time_10_1059_spread']
                    overallTimeOverUnder = datePercentDict[theDate]['overall_Time_10_1059_overUnder']
                    overallTimeParlay = datePercentDict[theDate]['overall_Time_10_1059_parlay']

                    teamTimeSpread = datePercentDict[theDate][f'{teamName}_Time_10_1059_spread']
                    teamTimeOverUnder = datePercentDict[theDate][f'{teamName}_Time_10_1059_overUnder']
                    teamTimeParlay = datePercentDict[theDate][f'{teamName}_Time_10_1059_parlay']
                elif (gameStartNumber == 22) or (gameStartNumber == 23):
                    #11 - 11:59
                    overallTimeSpread = datePercentDict[theDate]['overall_Time_11_1159_spread']
                    overallTimeOverUnder = datePercentDict[theDate]['overall_Time_11_1159_overUnder']
                    overallTimeParlay = datePercentDict[theDate]['overall_Time_11_1159_parlay']

                    teamTimeSpread = datePercentDict[theDate][f'{teamName}_Time_11_1159_spread']
                    teamTimeOverUnder = datePercentDict[theDate][f'{teamName}_Time_11_1159_overUnder']
                    teamTimeParlay = datePercentDict[theDate][f'{teamName}_Time_11_1159_parlay']
                
                df.loc[df['id'] == id] = id,gameNumber,teamNumber,isHome,oppTeamNumber,isWin,isOT,gameDayNumber,gameStartNumber,teamPoints,oppTeamPoints,teamWins,teamLosses,teamStreakCode,isInSeasonTournament,year,spread,spreadOdds,overUnder,overUnderOdds,moneyLine,gameTimeActual,spreadCalculated,overUnderCalculated,spreadActual,overUnderActual,gameDate,datePercentDict[theDate][f'{teamName}_spread'],datePercentDict[theDate][f'{teamName}_overUnder'],datePercentDict[theDate][f'{teamName}_parlay'],teamDaySpread,teamDayOverUnder,teamDayParlay,teamTimeSpread,teamTimeOverUnder,teamTimeParlay,datePercentDict[theDate][f'{teamName}_last_games_spread_1'],datePercentDict[theDate][f'{teamName}_last_games_overUnder_1'],datePercentDict[theDate][f'{teamName}_last_games_parlay_1'],datePercentDict[theDate][f'{teamName}_last_games_spread_2'],datePercentDict[theDate][f'{teamName}_last_games_overUnder_2'],datePercentDict[theDate][f'{teamName}_last_games_parlay_2'],datePercentDict[theDate][f'{teamName}_last_games_spread_3'],datePercentDict[theDate][f'{teamName}_last_games_overUnder_3'],datePercentDict[theDate][f'{teamName}_last_games_parlay_3'],datePercentDict[theDate][f'{teamName}_last_games_spread_4'],datePercentDict[theDate][f'{teamName}_last_games_overUnder_4'],datePercentDict[theDate][f'{teamName}_last_games_parlay_4'],datePercentDict[theDate][f'{teamName}_last_games_spread_5'],datePercentDict[theDate][f'{teamName}_last_games_overUnder_5'],datePercentDict[theDate][f'{teamName}_last_games_parlay_5'],datePercentDict[theDate]['overall_spread'],datePercentDict[theDate]['overall_overUnder'],datePercentDict[theDate]['overall_parlay'],overallDaySpread,overallDayOverUnder,overallDayParlay,overallTimeSpread,overallTimeOverUnder,overallTimeParlay,datePercentDict[theDate]['overall_last_games_spread_1'],datePercentDict[theDate]['overall_last_games_overUnder_1'],datePercentDict[theDate]['overall_last_games_parlay_1'],datePercentDict[theDate]['overall_last_games_spread_2'],datePercentDict[theDate]['overall_last_games_overUnder_2'],datePercentDict[theDate]['overall_last_games_parlay_2'],datePercentDict[theDate]['overall_last_games_spread_3'],datePercentDict[theDate]['overall_last_games_overUnder_3'],datePercentDict[theDate]['overall_last_games_parlay_3'],datePercentDict[theDate]['overall_last_games_spread_4'],datePercentDict[theDate]['overall_last_games_overUnder_4'],datePercentDict[theDate]['overall_last_games_parlay_4'],datePercentDict[theDate]['overall_last_games_spread_5'],datePercentDict[theDate]['overall_last_games_overUnder_5'],datePercentDict[theDate]['overall_last_games_parlay_5']

    
    return df

def getProbabilityRide(percent):
    numbers = [10,20,30,40,50,60,70,80,90,100]
    calculatedProb = random.choice(numbers)
    if percent > calculatedProb:
        return True
    else:
        return False 

def runParlays():
    #Initial variables
    teams = getTeam(ALL_TEAMS)
    columnsToPredict = ['spreadActual','overUnderActual']
    columnsToRemove = ['isWin','isOT','teamPoints','oppTeamPoints','teamWins','teamLosses','teamStreakCode','gameTimeActual','date']
    gamblingColumns = ['spread','spreadOdds','overUnder','overUnderOdds','moneyLine']
    year = 2024

    df = updatePercentConstsForParlay()

    #Connect to MySQL Database
    mydb = mysql.connector.connect(
        host='127.0.0.1',
        user='davidcarney',
        password='Sinorrabb1t',
        database='NBA'
        )
    mycursor = mydb.cursor()

    #Get all data from Database
    mycursor.execute(f"SELECT * FROM nbaStats WHERE isWin is NULL and spread is not NULL;")
    teamData = mycursor.fetchall()
    upcomingGames = pd.DataFrame(teamData, columns = ALL_COLUMNS)

    for col in ALL_COLUMNS_EXT:
        upcomingGames[col] = [0] * len(upcomingGames)


    #Need to add todays ALL_PERCENTAGES TO upcomingGames
    updatePercentages()
    
    for row in upcomingGames.values:
        id,gameNumber,teamNumber,isHome,oppTeamNumber,isWin,isOT,gameDayNumber,gameStartNumber,teamPoints,oppTeamPoints,teamWins,teamLosses,teamStreakCode,isInSeasonTournament,year,spread,spreadOdds,overUnder,overUnderOdds,moneyLine,gameTimeActual,spreadCalculated,overUnderCalculated,spreadActual,overUnderActual,gameDate,team_spread,team_overUnder,team_parlay,team_date_spread,team_date_overUnder,team_date_parlay,team_time_spread,team_time_overUnder,team_time_parlay,teamPast1DaySpread,teamPast1DayOverUnder,teamPast1DayParlay,teamPast2DaySpread,teamPast2DayOverUnder,teamPast2DayParlay,teamPast3DaySpread,teamPast3DayOverUnder,teamPast3DayParlay,teamPast4DaySpread,teamPast4DayOverUnder,teamPast4DayParlay,teamPast5DaySpread,teamPast5DayOverUnder,teamPast5DayParlay,overall_spread,overall_overUnder,overall_parlay,overall_date_spread,overall_date_overUnder,overall_date_parlay,overall_time_spread,overall_time_overUnder,overall_time_parlay,overallPast1DaySpread,overallPast1DayOverUnder,overallPast1DayParlay,overallPast2DaySpread,overallPast2DayOverUnder,overallPast2DayParlay,overallPast3DaySpread,overallPast3DayOverUnder,overallPast3DayParlay,overallPast4DaySpread,overallPast4DayOverUnder,overallPast4DayParlay,overallPast5DaySpread,overallPast5DayOverUnder,overallPast5DayParlay = row
        teamName = getTeam(str(teamNumber))['shortName']
        overallDaySpread = -1
        overallDayOverUnder = -1
        overallDayParlay = -1
        overallTimeSpread = -1
        overallTimeOverUnder = -1
        overallTimeParlay = -1

        teamDaySpread = -1
        teamDayOverUnder = -1
        teamDayParlay = -1
        teamTimeSpread = -1
        teamTimeOverUnder = -1
        teamTimeParlay = -1

        lastGameSpread1 = ALL_PERCENTAGES[f'{teamName}_last_games_spread_1']
        lastGameOverUnder1 = ALL_PERCENTAGES[f'{teamName}_last_games_overUnder_1']
        lastGameParlay1 = ALL_PERCENTAGES[f'{teamName}_last_games_parlay_1']
        lastGameSpread2 = ALL_PERCENTAGES[f'{teamName}_last_games_spread_2']
        lastGameOverUnder2 = ALL_PERCENTAGES[f'{teamName}_last_games_overUnder_2']
        lastGameParlay2 = ALL_PERCENTAGES[f'{teamName}_last_games_parlay_2']
        lastGameSpread3 = ALL_PERCENTAGES[f'{teamName}_last_games_spread_3']
        lastGameOverUnder3 = ALL_PERCENTAGES[f'{teamName}_last_games_overUnder_3']
        lastGameParlay3 = ALL_PERCENTAGES[f'{teamName}_last_games_parlay_3']
        lastGameSpread4 = ALL_PERCENTAGES[f'{teamName}_last_games_spread_4']
        lastGameOverUnder4 = ALL_PERCENTAGES[f'{teamName}_last_games_overUnder_4']
        lastGameParlay4 = ALL_PERCENTAGES[f'{teamName}_last_games_parlay_4']
        lastGameSpread5 = ALL_PERCENTAGES[f'{teamName}_last_games_spread_5']
        lastGameOverUnder5 = ALL_PERCENTAGES[f'{teamName}_last_games_overUnder_5']
        lastGameParlay5 = ALL_PERCENTAGES[f'{teamName}_last_games_parlay_5']

        overallLastGameSpread1 = ALL_PERCENTAGES['overall_last_games_spread_1']
        overallLastGameOverUnder1 = ALL_PERCENTAGES['overall_last_games_overUnder_1']
        overallLastGameParlay1 = ALL_PERCENTAGES['overall_last_games_parlay_1']
        overallLastGameSpread2 = ALL_PERCENTAGES['overall_last_games_spread_2']
        overallLastGameOverUnder2 = ALL_PERCENTAGES['overall_last_games_overUnder_2']
        overallLastGameParlay2 = ALL_PERCENTAGES['overall_last_games_parlay_2']
        overallLastGameSpread3 = ALL_PERCENTAGES['overall_last_games_spread_3']
        overallLastGameOverUnder3 = ALL_PERCENTAGES['overall_last_games_overUnder_3']
        overallLastGameParlay3 = ALL_PERCENTAGES['overall_last_games_parlay_3']
        overallLastGameSpread4 = ALL_PERCENTAGES['overall_last_games_spread_4']
        overallLastGameOverUnder4 = ALL_PERCENTAGES['overall_last_games_overUnder_4']
        overallLastGameParlay4 = ALL_PERCENTAGES['overall_last_games_parlay_4']
        overallLastGameSpread5 = ALL_PERCENTAGES['overall_last_games_spread_5']
        overallLastGameOverUnder5 = ALL_PERCENTAGES['overall_last_games_overUnder_5']
        overallLastGameParlay5 = ALL_PERCENTAGES['overall_last_games_parlay_5']
        
        #Day Percentages
        if gameDayNumber == 0:
            #Sunday
            overallDaySpread = ALL_PERCENTAGES['overall_Sunday_spread']
            overallDayOverUnder = ALL_PERCENTAGES['overall_Sunday_overUnder']
            overallDayParlay = ALL_PERCENTAGES['overall_Sunday_parlay']

            teamDaySpread = ALL_PERCENTAGES[f'{teamName}_Sunday_spread']
            teamDayOverUnder = ALL_PERCENTAGES[f'{teamName}_Sunday_overUnder']
            teamDayParlay = ALL_PERCENTAGES[f'{teamName}_Sunday_parlay']
        elif gameDayNumber == 1:
            #Monday
            overallDaySpread = ALL_PERCENTAGES['overall_Monday_spread']
            overallDayOverUnder = ALL_PERCENTAGES['overall_Monday_overUnder']
            overallDayParlay = ALL_PERCENTAGES['overall_Monday_parlay']

            teamDaySpread = ALL_PERCENTAGES[f'{teamName}_Monday_spread']
            teamDayOverUnder = ALL_PERCENTAGES[f'{teamName}_Monday_overUnder']
            teamDayParlay = ALL_PERCENTAGES[f'{teamName}_Monday_parlay']
        elif gameDayNumber == 2:
            #Tuesday
            overallDaySpread = ALL_PERCENTAGES['overall_Tuesday_spread']
            overallDayOverUnder = ALL_PERCENTAGES['overall_Tuesday_overUnder']
            overallDayParlay = ALL_PERCENTAGES['overall_Tuesday_parlay']

            teamDaySpread = ALL_PERCENTAGES[f'{teamName}_Tuesday_spread']
            teamDayOverUnder = ALL_PERCENTAGES[f'{teamName}_Tuesday_overUnder']
            teamDayParlay = ALL_PERCENTAGES[f'{teamName}_Tuesday_parlay']
        elif gameDayNumber == 3:
            #Wednesday
            overallDaySpread = ALL_PERCENTAGES['overall_Wednesday_spread']
            overallDayOverUnder = ALL_PERCENTAGES['overall_Wednesday_overUnder']
            overallDayParlay = ALL_PERCENTAGES['overall_Wednesday_parlay']

            teamDaySpread = ALL_PERCENTAGES[f'{teamName}_Wednesday_spread']
            teamDayOverUnder = ALL_PERCENTAGES[f'{teamName}_Wednesday_overUnder']
            teamDayParlay = ALL_PERCENTAGES[f'{teamName}_Wednesday_parlay']
        elif gameDayNumber == 4:
            #Thursday
            overallDaySpread = ALL_PERCENTAGES['overall_Thursday_spread']
            overallDayOverUnder = ALL_PERCENTAGES['overall_Thursday_overUnder']
            overallDayParlay = ALL_PERCENTAGES['overall_Thursday_parlay']

            teamDaySpread = ALL_PERCENTAGES[f'{teamName}_Thursday_spread']
            teamDayOverUnder = ALL_PERCENTAGES[f'{teamName}_Thursday_overUnder']
            teamDayParlay = ALL_PERCENTAGES[f'{teamName}_Thursday_parlay']
        elif gameDayNumber == 5:
            #Friday
            overallDaySpread = ALL_PERCENTAGES['overall_Friday_spread']
            overallDayOverUnder = ALL_PERCENTAGES['overall_Friday_overUnder']
            overallDayParlay = ALL_PERCENTAGES['overall_Friday_parlay']

            teamDaySpread = ALL_PERCENTAGES[f'{teamName}_Friday_spread']
            teamDayOverUnder = ALL_PERCENTAGES[f'{teamName}_Friday_overUnder']
            teamDayParlay = ALL_PERCENTAGES[f'{teamName}_Friday_parlay']
        elif gameDayNumber == 6:
            #Saturday
            overallDaySpread = ALL_PERCENTAGES['overall_Saturday_spread']
            overallDayOverUnder = ALL_PERCENTAGES['overall_Saturday_overUnder']
            overallDayParlay = ALL_PERCENTAGES['overall_Saturday_parlay']

            teamDaySpread = ALL_PERCENTAGES[f'{teamName}_Saturday_spread']
            teamDayOverUnder = ALL_PERCENTAGES[f'{teamName}_Saturday_overUnder']
            teamDayParlay = ALL_PERCENTAGES[f'{teamName}_Saturday_parlay']
        
        #Time percents
        if (gameStartNumber == 0) or (gameStartNumber == 1):
            #12 - 12:59
            overallTimeSpread = ALL_PERCENTAGES['overall_Time_12_1259_spread']
            overallTimeOverUnder = ALL_PERCENTAGES['overall_Time_12_1259_overUnder']
            overallTimeParlay = ALL_PERCENTAGES['overall_Time_12_1259_parlay']

            teamTimeSpread = ALL_PERCENTAGES[f'{teamName}_Time_12_1259_spread']
            teamTimeOverUnder = ALL_PERCENTAGES[f'{teamName}_Time_12_1259_overUnder']
            teamTimeParlay = ALL_PERCENTAGES[f'{teamName}_Time_12_1259_parlay']
        elif (gameStartNumber == 2) or (gameStartNumber == 3):
            #1 - 1:59
            overallTimeSpread = ALL_PERCENTAGES['overall_Time_1_159_spread']
            overallTimeOverUnder = ALL_PERCENTAGES['overall_Time_1_159_overUnder']
            overallTimeParlay = ALL_PERCENTAGES['overall_Time_1_159_parlay']

            teamTimeSpread = ALL_PERCENTAGES[f'{teamName}_Time_1_159_spread']
            teamTimeOverUnder = ALL_PERCENTAGES[f'{teamName}_Time_1_159_overUnder']
            teamTimeParlay = ALL_PERCENTAGES[f'{teamName}_Time_1_159_parlay']
        elif (gameStartNumber == 4) or (gameStartNumber == 5):
            #2 - 2:59
            overallTimeSpread = ALL_PERCENTAGES['overall_Time_2_259_spread']
            overallTimeOverUnder = ALL_PERCENTAGES['overall_Time_2_259_overUnder']
            overallTimeParlay = ALL_PERCENTAGES['overall_Time_2_259_parlay']

            teamTimeSpread = ALL_PERCENTAGES[f'{teamName}_Time_2_259_spread']
            teamTimeOverUnder = ALL_PERCENTAGES[f'{teamName}_Time_2_259_overUnder']
            teamTimeParlay = ALL_PERCENTAGES[f'{teamName}_Time_2_259_parlay']
        elif (gameStartNumber == 6) or (gameStartNumber == 7):
            #3 - 3:59
            overallTimeSpread = ALL_PERCENTAGES['overall_Time_3_359_spread']
            overallTimeOverUnder = ALL_PERCENTAGES['overall_Time_3_359_overUnder']
            overallTimeParlay = ALL_PERCENTAGES['overall_Time_3_359_parlay']

            teamTimeSpread = ALL_PERCENTAGES[f'{teamName}_Time_3_359_spread']
            teamTimeOverUnder = ALL_PERCENTAGES[f'{teamName}_Time_3_359_overUnder']
            teamTimeParlay = ALL_PERCENTAGES[f'{teamName}_Time_3_359_parlay']
        elif (gameStartNumber == 8) or (gameStartNumber == 9):
            #4 - 4:59
            overallTimeSpread = ALL_PERCENTAGES['overall_Time_4_459_spread']
            overallTimeOverUnder = ALL_PERCENTAGES['overall_Time_4_459_overUnder']
            overallTimeParlay = ALL_PERCENTAGES['overall_Time_4_459_parlay']

            teamTimeSpread = ALL_PERCENTAGES[f'{teamName}_Time_4_459_spread']
            teamTimeOverUnder = ALL_PERCENTAGES[f'{teamName}_Time_4_459_overUnder']
            teamTimeParlay = ALL_PERCENTAGES[f'{teamName}_Time_4_459_parlay']
        elif (gameStartNumber == 10) or (gameStartNumber == 11):
            #5 - 5:59
            overallTimeSpread = ALL_PERCENTAGES['overall_Time_5_559_spread']
            overallTimeOverUnder = ALL_PERCENTAGES['overall_Time_5_559_overUnder']
            overallTimeParlay = ALL_PERCENTAGES['overall_Time_5_559_parlay']

            teamTimeSpread = ALL_PERCENTAGES[f'{teamName}_Time_5_559_spread']
            teamTimeOverUnder = ALL_PERCENTAGES[f'{teamName}_Time_5_559_overUnder']
            teamTimeParlay = ALL_PERCENTAGES[f'{teamName}_Time_5_559_parlay']
        elif (gameStartNumber == 12) or (gameStartNumber == 13):
            #6 - 6:59
            overallTimeSpread = ALL_PERCENTAGES['overall_Time_6_659_spread']
            overallTimeOverUnder = ALL_PERCENTAGES['overall_Time_6_659_overUnder']
            overallTimeParlay = ALL_PERCENTAGES['overall_Time_6_659_parlay']

            teamTimeSpread = ALL_PERCENTAGES[f'{teamName}_Time_6_659_spread']
            teamTimeOverUnder = ALL_PERCENTAGES[f'{teamName}_Time_6_659_overUnder']
            teamTimeParlay = ALL_PERCENTAGES[f'{teamName}_Time_6_659_parlay']
        elif (gameStartNumber == 14) or (gameStartNumber == 15):
            #7 - 7:59
            overallTimeSpread = ALL_PERCENTAGES['overall_Time_7_759_spread']
            overallTimeOverUnder = ALL_PERCENTAGES['overall_Time_7_759_overUnder']
            overallTimeParlay = ALL_PERCENTAGES['overall_Time_7_759_parlay']

            teamTimeSpread = ALL_PERCENTAGES[f'{teamName}_Time_7_759_spread']
            teamTimeOverUnder = ALL_PERCENTAGES[f'{teamName}_Time_7_759_overUnder']
            teamTimeParlay = ALL_PERCENTAGES[f'{teamName}_Time_7_759_parlay']
        elif (gameStartNumber == 16) or (gameStartNumber == 17):
            #8 - 8:59
            overallTimeSpread = ALL_PERCENTAGES['overall_Time_8_859_spread']
            overallTimeOverUnder = ALL_PERCENTAGES['overall_Time_8_859_overUnder']
            overallTimeParlay = ALL_PERCENTAGES['overall_Time_8_859_parlay']

            teamTimeSpread = ALL_PERCENTAGES[f'{teamName}_Time_8_859_spread']
            teamTimeOverUnder = ALL_PERCENTAGES[f'{teamName}_Time_8_859_overUnder']
            teamTimeParlay = ALL_PERCENTAGES[f'{teamName}_Time_8_859_parlay']
        elif (gameStartNumber == 18) or (gameStartNumber == 19):
            #9 - 9:59
            overallTimeSpread = ALL_PERCENTAGES['overall_Time_9_959_spread']
            overallTimeOverUnder = ALL_PERCENTAGES['overall_Time_9_959_overUnder']
            overallTimeParlay = ALL_PERCENTAGES['overall_Time_9_959_parlay']

            teamTimeSpread = ALL_PERCENTAGES[f'{teamName}_Time_9_959_spread']
            teamTimeOverUnder = ALL_PERCENTAGES[f'{teamName}_Time_9_959_overUnder']
            teamTimeParlay = ALL_PERCENTAGES[f'{teamName}_Time_9_959_parlay']
        elif (gameStartNumber == 20) or (gameStartNumber == 21):
            #10 - 10:59
            overallTimeSpread = ALL_PERCENTAGES['overall_Time_10_1059_spread']
            overallTimeOverUnder = ALL_PERCENTAGES['overall_Time_10_1059_overUnder']
            overallTimeParlay = ALL_PERCENTAGES['overall_Time_10_1059_parlay']

            teamTimeSpread = ALL_PERCENTAGES[f'{teamName}_Time_10_1059_spread']
            teamTimeOverUnder = ALL_PERCENTAGES[f'{teamName}_Time_10_1059_overUnder']
            teamTimeParlay = ALL_PERCENTAGES[f'{teamName}_Time_10_1059_parlay']
        elif (gameStartNumber == 22) or (gameStartNumber == 23):
            #11 - 11:59
            overallTimeSpread = ALL_PERCENTAGES['overall_Time_11_1159_spread']
            overallTimeOverUnder = ALL_PERCENTAGES['overall_Time_11_1159_overUnder']
            overallTimeParlay = ALL_PERCENTAGES['overall_Time_11_1159_parlay']

            teamTimeSpread = ALL_PERCENTAGES[f'{teamName}_Time_11_1159_spread']
            teamTimeOverUnder = ALL_PERCENTAGES[f'{teamName}_Time_11_1159_overUnder']
            teamTimeParlay = ALL_PERCENTAGES[f'{teamName}_Time_11_1159_parlay']
        

        if overallDaySpread == 'NA':
            overallDaySpread = 0
        if overallDayOverUnder == 'NA':
            overallDayOverUnder = 0
        if overallDayParlay == 'NA':
            overallDayParlay = 0
        if overallTimeSpread == 'NA':
            overallTimeSpread = 0
        if overallTimeOverUnder == 'NA':
            overallTimeOverUnder = 0
        if overallTimeParlay == 'NA':
            overallTimeParlay = 0

        if teamDaySpread == 'NA':
            teamDaySpread = 0
        if teamDayOverUnder == 'NA':
            teamDayOverUnder = 0
        if teamDayParlay == 'NA':
            teamDayParlay = 0
        if teamTimeSpread == 'NA':
            teamTimeSpread = 0
        if teamTimeOverUnder == 'NA':
            teamTimeOverUnder = 0
        if teamTimeParlay == 'NA':
            teamTimeParlay = 0

        if lastGameSpread1 == 'NA':
            lastGameSpread1 = 0
        if lastGameOverUnder1 == 'NA':
            lastGameOverUnder1 = 0
        if lastGameParlay1 == 'NA':
            lastGameParlay1 = 0
        if lastGameSpread2 == 'NA':
            lastGameSpread2 = 0
        if lastGameOverUnder2 == 'NA':
            lastGameOverUnder2 = 0
        if lastGameParlay2 == 'NA':
            lastGameParlay2 = 0
        if lastGameSpread3 == 'NA':
            lastGameSpread3 = 0
        if lastGameOverUnder3 == 'NA':
            lastGameOverUnder3 = 0
        if lastGameParlay3 == 'NA':
            lastGameParlay3 = 0
        if lastGameSpread4 == 'NA':
            lastGameSpread4 = 0
        if lastGameOverUnder4 == 'NA':
            lastGameOverUnder4 = 0
        if lastGameParlay4 == 'NA':
            lastGameParlay4 = 0
        if lastGameSpread5 == 'NA':
            lastGameSpread5 = 0
        if lastGameOverUnder5 == 'NA':
            lastGameOverUnder5 = 0
        if lastGameParlay5 == 'NA':
            lastGameParlay5 = 0

        if overallLastGameSpread1 == 'NA':
            overallLastGameSpread1 = 0
        if overallLastGameOverUnder1 == 'NA':
            overallLastGameOverUnder1 = 0
        if overallLastGameParlay1 == 'NA':
            overallLastGameParlay1 = 0
        if overallLastGameSpread2 == 'NA':
            overallLastGameSpread2 = 0
        if overallLastGameOverUnder2 == 'NA':
            overallLastGameOverUnder2 = 0
        if overallLastGameParlay2 == 'NA':
            overallLastGameParlay2 = 0
        if overallLastGameSpread3 == 'NA':
            overallLastGameSpread3 = 0
        if overallLastGameOverUnder3 == 'NA':
            overallLastGameOverUnder3 = 0
        if overallLastGameParlay3 == 'NA':
            overallLastGameParlay3 = 0
        if overallLastGameSpread4 == 'NA':
            overallLastGameSpread4 = 0
        if overallLastGameOverUnder4 == 'NA':
            overallLastGameOverUnder4 = 0
        if overallLastGameParlay4 == 'NA':
            overallLastGameParlay4 = 0
        if overallLastGameSpread5 == 'NA':
            overallLastGameSpread5 = 0
        if overallLastGameOverUnder5 == 'NA':
            overallLastGameOverUnder5 = 0
        if overallLastGameParlay5 == 'NA':
            overallLastGameParlay5 = 0


        upcomingGames.loc[upcomingGames['id'] == id] = id,gameNumber,teamNumber,isHome,oppTeamNumber,isWin,isOT,gameDayNumber,gameStartNumber,teamPoints,oppTeamPoints,teamWins,teamLosses,teamStreakCode,isInSeasonTournament,year,spread,spreadOdds,overUnder,overUnderOdds,moneyLine,gameTimeActual,spreadCalculated,overUnderCalculated,spreadActual,overUnderActual,gameDate,ALL_PERCENTAGES[f'{teamName}_spread'],ALL_PERCENTAGES[f'{teamName}_overUnder'],ALL_PERCENTAGES[f'{teamName}_parlay'],teamDaySpread,teamDayOverUnder,teamDayParlay,teamTimeSpread,teamTimeOverUnder,teamTimeParlay,lastGameSpread1,lastGameOverUnder1,lastGameParlay1,lastGameSpread2,lastGameOverUnder2,lastGameParlay2,lastGameSpread3,lastGameOverUnder3,lastGameParlay3,lastGameSpread4,lastGameOverUnder4,lastGameParlay4,lastGameSpread5,lastGameOverUnder5,lastGameParlay5,ALL_PERCENTAGES['overall_spread'],ALL_PERCENTAGES['overall_overUnder'],ALL_PERCENTAGES['overall_parlay'],overallDaySpread,overallDayOverUnder,overallDayParlay,overallTimeSpread,overallTimeOverUnder,overallTimeParlay,overallLastGameSpread1,overallLastGameOverUnder1,overallLastGameParlay1,overallLastGameSpread2,overallLastGameOverUnder2,overallLastGameParlay2,overallLastGameSpread3,overallLastGameOverUnder3,overallLastGameParlay3,overallLastGameSpread4,overallLastGameOverUnder4,overallLastGameParlay4,overallLastGameSpread5,overallLastGameOverUnder5,overallLastGameParlay5


    #remove columns from DFs of columns with None values
    df = df.drop(columns = columnsToRemove)
    upcomingGames = upcomingGames.drop(columns = columnsToRemove)
    upcomingGames = upcomingGames.drop(columns = columnsToPredict)
    
    #Update training data
    df['spreadOdds'] = df['spreadOdds'].replace(to_replace='−', value='-', regex=True)
    df['overUnderOdds'] = df['overUnderOdds'].replace(to_replace='−', value='-', regex=True)
    df['moneyLine'] = df['moneyLine'].replace(to_replace='−', value='-', regex=True)
    df[gamblingColumns] = df[gamblingColumns].astype(float)

    upcomingGames['spreadOdds'] = upcomingGames['spreadOdds'].replace(to_replace='−', value='-', regex=True)
    upcomingGames['overUnderOdds'] = upcomingGames['overUnderOdds'].replace(to_replace='−', value='-', regex=True)
    upcomingGames['moneyLine'] = upcomingGames['moneyLine'].replace(to_replace='−', value='-', regex=True)
    upcomingGames[gamblingColumns] = upcomingGames[gamblingColumns].astype(float) 

    gamesAlreadyPredicted = []
    allParlays = []
    massiveP = []
    largeP = []
    decentP = []
    smallP = []

    for eachGame in upcomingGames.sort_values(by=['gameStartNumber'])[['teamNumber','oppTeamNumber']].values:        
        team1, team2 = list(eachGame)
        
        if (team1 not in gamesAlreadyPredicted) or (team2 not in gamesAlreadyPredicted):
            
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
                # featureSelection =  RFECV(estimator, step=1, cv=2)
                featureSelection = VarianceThreshold(threshold=(.8 * (1 - .8)))
                X_train = featureSelection.fit_transform(X_train)
                X_test = featureSelection.transform(X_test)

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
                SGDCModel = SGDClassifier(loss='log', max_iter=7000, tol=1e-3, random_state=19)
                
                #CV 2 folds
                #Support Vector Machines
                SVCGS2 = GridSearchCV(SVCModel, CParams, cv=2)
                SVCGS2.fit(X_train, y_train)
                bestSVC2 = SVC(C = SVCGS2.best_params_['C'], probability=True, random_state=19)
                #K Nearest Neighbor
                KNNGS2 = GridSearchCV(KNN, KNNParams, cv=2)
                KNNGS2.fit(X_train, y_train)
                bestKNN2 = KNeighborsClassifier(n_neighbors = KNNGS2.best_params_['n_neighbors'])
                #Logistic Regression
                LRGS2 = GridSearchCV(LogReg, CParams, cv=2)
                LRGS2.fit(X_train, y_train)
                bestLR2 = LogisticRegression(C = LRGS2.best_params_['C'], max_iter=1000, random_state=19)
                #Stochastic Gradient Descent 
                SGDCGS2 = GridSearchCV(SGDCModel, alphaParams, cv=2)
                SGDCGS2.fit(X_train, y_train)
                bestSGDC2 = SGDClassifier(loss='log', alpha = SGDCGS2.best_params_['alpha'], max_iter=1000, tol=1e-3, random_state=19)

                #CV 3 folds
                #Support Vector Machines
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
                bestSGDC3 = SGDClassifier(loss='log', alpha = SGDCGS3.best_params_['alpha'], max_iter=1000, tol=1e-3, random_state=19)

                #CV 5 folds
                #Support Vector Machines
                SVCGS5 = GridSearchCV(SVCModel, CParams, cv=5)
                SVCGS5.fit(X_train, y_train)
                bestSVC5 = SVC(C = SVCGS5.best_params_['C'], probability=True, random_state=19)
                #K Nearest Neighbor
                KNNGS5 = GridSearchCV(KNN, KNNParams, cv=5)
                KNNGS5.fit(X_train, y_train)
                bestKNN5 = KNeighborsClassifier(n_neighbors = KNNGS5.best_params_['n_neighbors'])
                #Logistic Regression
                LRGS5 = GridSearchCV(LogReg, CParams, cv=5)
                LRGS5.fit(X_train, y_train)
                bestLR5 = LogisticRegression(C = LRGS5.best_params_['C'], max_iter=1000, random_state=19)
                #Stochastic Gradient Descent 
                SGDCGS5 = GridSearchCV(SGDCModel, alphaParams, cv=5)
                SGDCGS5.fit(X_train, y_train)
                bestSGDC5 = SGDClassifier(loss='log', alpha = SGDCGS5.best_params_['alpha'], max_iter=1000, tol=1e-3, random_state=19)

                #CV 7 folds
                #Support Vector Machines
                SVCGS7 = GridSearchCV(SVCModel, CParams, cv=7)
                SVCGS7.fit(X_train, y_train)
                bestSVC7 = SVC(C = SVCGS7.best_params_['C'], probability=True, random_state=19)
                #K Nearest Neighbor
                KNNGS7 = GridSearchCV(KNN, KNNParams, cv=7)
                KNNGS7.fit(X_train, y_train)
                bestKNN7 = KNeighborsClassifier(n_neighbors = KNNGS7.best_params_['n_neighbors'])
                #Logistic Regression
                LRGS7 = GridSearchCV(LogReg, CParams, cv=7)
                LRGS7.fit(X_train, y_train)
                bestLR7 = LogisticRegression(C = LRGS7.best_params_['C'], max_iter=1000, random_state=19)
                #Stochastic Gradient Descent 
                SGDCGS7 = GridSearchCV(SGDCModel, alphaParams, cv=7)
                SGDCGS7.fit(X_train, y_train)
                bestSGDC7 = SGDClassifier(loss='log', alpha = SGDCGS7.best_params_['alpha'], max_iter=1000, tol=1e-3, random_state=19)

                bestSVC2.fit(X_train, y_train)
                bestSVC2Score = accuracy_score(y_test, bestSVC2.predict(X_test))
                bestSVC3.fit(X_train, y_train)
                bestSVC3Score = accuracy_score(y_test, bestSVC3.predict(X_test))
                bestSVC5.fit(X_train, y_train)
                bestSVC5Score = accuracy_score(y_test, bestSVC5.predict(X_test))
                bestSVC7.fit(X_train, y_train)
                bestSVC7Score = accuracy_score(y_test, bestSVC7.predict(X_test))

                bestKNN2.fit(X_train, y_train)
                bestKNN2Score = accuracy_score(y_test, bestKNN2.predict(X_test))
                bestKNN3.fit(X_train, y_train)
                bestKNN3Score = accuracy_score(y_test, bestKNN3.predict(X_test))
                bestKNN5.fit(X_train, y_train)
                bestKNN5Score = accuracy_score(y_test, bestKNN5.predict(X_test))
                bestKNN7.fit(X_train, y_train)
                bestKNN7Score = accuracy_score(y_test, bestKNN7.predict(X_test))

                bestLR2.fit(X_train, y_train)
                bestLR2Score = accuracy_score(y_test, bestLR2.predict(X_test))
                bestLR3.fit(X_train, y_train)
                bestLR3Score = accuracy_score(y_test, bestLR3.predict(X_test))
                bestLR5.fit(X_train, y_train)
                bestLR5Score = accuracy_score(y_test, bestLR5.predict(X_test))
                bestLR7.fit(X_train, y_train)
                bestLR7Score = accuracy_score(y_test, bestLR7.predict(X_test))

                bestSGDC2.fit(X_train, y_train)
                bestSGDC2Score = accuracy_score(y_test, bestSGDC2.predict(X_test))
                bestSGDC3.fit(X_train, y_train)
                bestSGDC3Score = accuracy_score(y_test, bestSGDC3.predict(X_test))
                bestSGDC5.fit(X_train, y_train)
                bestSGDC5Score = accuracy_score(y_test, bestSGDC5.predict(X_test))
                bestSGDC7.fit(X_train, y_train)
                bestSGDC7Score = accuracy_score(y_test, bestSGDC7.predict(X_test))

                allScores = {'bestSVC2Score' : bestSVC2Score,'bestSVC3Score' : bestSVC3Score,'bestSVC5Score' : bestSVC5Score,'bestSVC7Score' : bestSVC7Score,'bestKNN2Score' : bestKNN2Score,'bestKNN3Score' : bestKNN3Score,'bestKNN5Score' : bestKNN5Score,'bestKNN7Score' : bestKNN7Score,'bestLR2Score' : bestLR2Score,'bestLR3Score' : bestLR3Score,'bestLR5Score' : bestLR5Score,'bestLR7Score' : bestLR7Score, 'bestSGDC2Score' : bestSGDC2Score, 'bestSGDC3Score' : bestSGDC3Score, 'bestSGDC5Score' : bestSGDC5Score, 'bestSGDC7Score' : bestSGDC7Score}
                allBestModels = {'bestSVC2Score' : bestSVC2,'bestSVC3Score' : bestSVC3,'bestSVC5Score' : bestSVC5,'bestSVC7Score' : bestSVC7,'bestKNN2Score' : bestKNN2,'bestKNN3Score' : bestKNN3,'bestKNN5Score' : bestKNN5,'bestKNN7Score' : bestKNN7,'bestLR2Score' : bestLR2,'bestLR3Score' : bestLR3,'bestLR5Score' : bestLR5,'bestLR7Score' : bestLR7, 'bestSGDC2Score' : bestSGDC2, 'bestSGDC3Score' : bestSGDC3, 'bestSGDC5Score' : bestSGDC5, 'bestSGDC7Score' : bestSGDC7}

                bestScore = max(allScores, key=allScores.get)
                bestModel = allBestModels[bestScore]
                firstClass, secondClass = bestModel.classes_

                #Scale todays games
                team1DF = upcomingGames[upcomingGames['teamNumber'] == team1]
                team2DF = upcomingGames[upcomingGames['teamNumber'] == team2]
   
                scaledteam1DF = scalar.transform(team1DF)
                scaledteam1DF = featureSelection.transform(scaledteam1DF)
                scaledteam2DF = scalar.transform(team2DF)
                scaledteam2DF = featureSelection.transform(scaledteam2DF)

                if column == 'spreadActual':
                    team1Prediction = bestModel.predict(scaledteam1DF)[0]
                    team1PredictionProb = bestModel.predict_proba(scaledteam1DF)
                    team2Prediction = bestModel.predict(scaledteam2DF)[0]
                    team2PredictionProb = bestModel.predict_proba(scaledteam2DF)

                    team1PredictionProbFor0Class = -1
                    team1PredictionProbFor1Class = -1
                    team2PredictionProbFor0Class = -1
                    team2PredictionProbFor1Class = -1

                    if firstClass == 0:
                        team1PredictionProbFor0Class = team1PredictionProb[0][0]
                        team1PredictionProbFor1Class = team1PredictionProb[0][1]
                        team2PredictionProbFor0Class = team2PredictionProb[0][0]
                        team2PredictionProbFor1Class = team2PredictionProb[0][1]
                    else:
                        team1PredictionProbFor0Class = team1PredictionProb[0][1]
                        team1PredictionProbFor1Class = team1PredictionProb[0][0]
                        team2PredictionProbFor0Class = team2PredictionProb[0][1]
                        team2PredictionProbFor1Class = team2PredictionProb[0][0]


                    if (team1DF['spreadCalculated'].values[0] == team1Prediction) and (team2DF['spreadCalculated'].values[0] == team2Prediction):
                        if (team1Prediction == 0) and (team2Prediction == 1):
                            if (team2PredictionProbFor1Class > LARGE_PARLAY_THRESHOLD) and (team1PredictionProbFor0Class > LARGE_PARLAY_THRESHOLD):
                                largeP.append(f"1_{getTeam(str(team1))['fullName']}_{getTeam(str(team2))['fullName']}_{column.split('A')[0]}")
                            elif (team2PredictionProbFor1Class > DECENT_PARLAY_THRESHOLD) and (team1PredictionProbFor0Class > DECENT_PARLAY_THRESHOLD):
                                decentP.append(f"1_{getTeam(str(team1))['fullName']}_{getTeam(str(team2))['fullName']}_{column.split('A')[0]}")
                            else:
                                smallP.append(f"1_{getTeam(str(team1))['fullName']}_{getTeam(str(team2))['fullName']}_{column.split('A')[0]}")
                            
                        elif (team1Prediction == 1) and (team2Prediction == 0):
                            if (team2PredictionProbFor0Class > LARGE_PARLAY_THRESHOLD) and (team1PredictionProbFor1Class > LARGE_PARLAY_THRESHOLD):
                                largeP.append(f"1_{getTeam(str(team1))['fullName']}_{getTeam(str(team2))['fullName']}_{column.split('A')[0]}")
                            elif (team2PredictionProbFor0Class > DECENT_PARLAY_THRESHOLD) and (team1PredictionProbFor1Class > DECENT_PARLAY_THRESHOLD):
                                decentP.append(f"1_{getTeam(str(team1))['fullName']}_{getTeam(str(team2))['fullName']}_{column.split('A')[0]}")
                            else:
                                smallP.append(f"1_{getTeam(str(team1))['fullName']}_{getTeam(str(team2))['fullName']}_{column.split('A')[0]}")
                        
                        allParlays.append(f"1_{getTeam(str(team1))['fullName']}_{getTeam(str(team2))['fullName']}_{column.split('A')[0]}")
                    
                    elif (team1DF['spreadCalculated'].values[0] == team2Prediction) and (team2DF['spreadCalculated'].values[0] == team1Prediction):
                        if (team1Prediction == 0) and (team2Prediction == 1):
                            if (team2PredictionProbFor1Class > LARGE_PARLAY_THRESHOLD) and (team1PredictionProbFor0Class > LARGE_PARLAY_THRESHOLD):
                                largeP.append(f"0_{getTeam(str(team1))['fullName']}_{getTeam(str(team2))['fullName']}_{column.split('A')[0]}")
                            elif (team2PredictionProbFor1Class > DECENT_PARLAY_THRESHOLD) and (team1PredictionProbFor0Class > DECENT_PARLAY_THRESHOLD):
                                decentP.append(f"0_{getTeam(str(team1))['fullName']}_{getTeam(str(team2))['fullName']}_{column.split('A')[0]}")
                            else:
                                smallP.append(f"0_{getTeam(str(team1))['fullName']}_{getTeam(str(team2))['fullName']}_{column.split('A')[0]}")
                            
                        elif (team1Prediction == 1) and (team2Prediction == 0):
                            if (team2PredictionProbFor0Class > LARGE_PARLAY_THRESHOLD) and (team1PredictionProbFor1Class > LARGE_PARLAY_THRESHOLD):
                                largeP.append(f"0_{getTeam(str(team1))['fullName']}_{getTeam(str(team2))['fullName']}_{column.split('A')[0]}")
                            elif (team2PredictionProbFor0Class > DECENT_PARLAY_THRESHOLD) and (team1PredictionProbFor1Class > DECENT_PARLAY_THRESHOLD):
                                decentP.append(f"0_{getTeam(str(team1))['fullName']}_{getTeam(str(team2))['fullName']}_{column.split('A')[0]}")
                            else:
                                smallP.append(f"0_{getTeam(str(team1))['fullName']}_{getTeam(str(team2))['fullName']}_{column.split('A')[0]}")

                        allParlays.append(f"0_{getTeam(str(team1))['fullName']}_{getTeam(str(team2))['fullName']}_{column.split('A')[0]}")


                elif column == 'overUnderActual':
                    team1Prediction = bestModel.predict(scaledteam1DF)[0]
                    team1PredictionProb = bestModel.predict_proba(scaledteam1DF)
                    team2Prediction = bestModel.predict(scaledteam2DF)[0]
                    team2PredictionProb = bestModel.predict_proba(scaledteam2DF)

                    team1PredictionProbFor0Class = -1
                    team1PredictionProbFor1Class = -1
                    team2PredictionProbFor0Class = -1
                    team2PredictionProbFor1Class = -1

                    if firstClass == 0:
                        team1PredictionProbFor0Class = team1PredictionProb[0][0]
                        team1PredictionProbFor1Class = team1PredictionProb[0][1]
                        team2PredictionProbFor0Class = team2PredictionProb[0][0]
                        team2PredictionProbFor1Class = team2PredictionProb[0][1]
                    else:
                        team1PredictionProbFor0Class = team1PredictionProb[0][1]
                        team1PredictionProbFor1Class = team1PredictionProb[0][0]
                        team2PredictionProbFor0Class = team2PredictionProb[0][1]
                        team2PredictionProbFor1Class = team2PredictionProb[0][0]

                    if (team1DF['overUnderCalculated'].values[0] == team1Prediction) and (team2DF['overUnderCalculated'].values[0] == team2Prediction):
                        if (team1Prediction == 0) and (team2Prediction == 0):
                            if (team2PredictionProbFor0Class > LARGE_PARLAY_THRESHOLD) and (team1PredictionProbFor0Class > LARGE_PARLAY_THRESHOLD):
                                largeP.append(f"1_{getTeam(str(team1))['fullName']}_{getTeam(str(team2))['fullName']}_{column.split('A')[0]}")
                            elif (team2PredictionProbFor0Class > DECENT_PARLAY_THRESHOLD) and (team1PredictionProbFor0Class > DECENT_PARLAY_THRESHOLD):
                                decentP.append(f"1_{getTeam(str(team1))['fullName']}_{getTeam(str(team2))['fullName']}_{column.split('A')[0]}")
                            else:
                                smallP.append(f"1_{getTeam(str(team1))['fullName']}_{getTeam(str(team2))['fullName']}_{column.split('A')[0]}")

                        elif (team1Prediction == 1) and (team2Prediction == 1):
                            if (team2PredictionProbFor1Class > LARGE_PARLAY_THRESHOLD) and (team1PredictionProbFor1Class > LARGE_PARLAY_THRESHOLD):
                                largeP.append(f"1_{getTeam(str(team1))['fullName']}_{getTeam(str(team2))['fullName']}_{column.split('A')[0]}")
                            elif (team2PredictionProbFor1Class > DECENT_PARLAY_THRESHOLD) and (team1PredictionProbFor1Class > DECENT_PARLAY_THRESHOLD):
                                decentP.append(f"1_{getTeam(str(team1))['fullName']}_{getTeam(str(team2))['fullName']}_{column.split('A')[0]}")
                            else:
                                smallP.append(f"1_{getTeam(str(team1))['fullName']}_{getTeam(str(team2))['fullName']}_{column.split('A')[0]}")

                        allParlays.append(f"1_{getTeam(str(team1))['fullName']}_{getTeam(str(team2))['fullName']}_{column.split('A')[0]}")

                    elif ((1 - team1DF['overUnderCalculated'].values[0]) == team1Prediction) and ((1 - team2DF['overUnderCalculated'].values[0]) == team2Prediction):
                        if (team1Prediction == 0) and (team2Prediction == 0):
                            if (team2PredictionProbFor0Class > LARGE_PARLAY_THRESHOLD) and (team1PredictionProbFor0Class > LARGE_PARLAY_THRESHOLD):
                                largeP.append(f"0_{getTeam(str(team1))['fullName']}_{getTeam(str(team2))['fullName']}_{column.split('A')[0]}")
                            elif (team2PredictionProbFor0Class > DECENT_PARLAY_THRESHOLD) and (team1PredictionProbFor0Class > DECENT_PARLAY_THRESHOLD):
                                decentP.append(f"0_{getTeam(str(team1))['fullName']}_{getTeam(str(team2))['fullName']}_{column.split('A')[0]}")
                            else:
                                smallP.append(f"0_{getTeam(str(team1))['fullName']}_{getTeam(str(team2))['fullName']}_{column.split('A')[0]}")

                        elif (team1Prediction == 1) and (team2Prediction == 1):
                            if (team2PredictionProbFor1Class > LARGE_PARLAY_THRESHOLD) and (team1PredictionProbFor1Class > LARGE_PARLAY_THRESHOLD):
                                largeP.append(f"0_{getTeam(str(team1))['fullName']}_{getTeam(str(team2))['fullName']}_{column.split('A')[0]}")
                            elif (team2PredictionProbFor1Class > DECENT_PARLAY_THRESHOLD) and (team1PredictionProbFor1Class > DECENT_PARLAY_THRESHOLD):
                                decentP.append(f"0_{getTeam(str(team1))['fullName']}_{getTeam(str(team2))['fullName']}_{column.split('A')[0]}")
                            else:
                                smallP.append(f"0_{getTeam(str(team1))['fullName']}_{getTeam(str(team2))['fullName']}_{column.split('A')[0]}")

                        allParlays.append(f"0_{getTeam(str(team1))['fullName']}_{getTeam(str(team2))['fullName']}_{column.split('A')[0]}")
                    

            gamesAlreadyPredicted.append(team1)
            gamesAlreadyPredicted.append(team2)
    
    
    todaysDate = date.today().strftime("%B %d %Y")

    
    #Update database and file with small parlay
    smallParlayFilename = '../frontend/src/nbaPages/smallParlay.js'
    smallParlayFile = open(smallParlayFilename, 'w')
    smallParlayFile.write('export const smallParlay = [\n')

    for game in smallP:
        rideCalculated, team1, team2, category = game.split('_')

        insertData = (
            f"INSERT INTO nbaParlay1 "
            f"("
            f"date, "
            f"team1, "
            f"team2, "
            f"category, "
            f"rideCalculated "
            f") "
            f"VALUES ("
            f"'{todaysDate}',"
            f"'{team1}',"
            f"'{team2}',"
            f"'{category}',"
            f"{rideCalculated}"
            f")"
        )
        mycursor.execute(insertData)
        mydb.commit()

        
        smallParlayFile.write(f"'{team1},")
        smallParlayFile.write(f"{team2},")
        smallParlayFile.write(f"{category},")
        smallParlayFile.write(f"{rideCalculated}',\n")

    smallParlayFile.write('];')

    #Update database and file with decent parlay
    decentParlayFilename = '../frontend/src/nbaPages/decentParlay.js'
    decentParlayFile = open(decentParlayFilename, 'w')
    decentParlayFile.write('export const decentParlay = [\n')

    for game in decentP:
        rideCalculated, team1, team2, category = game.split('_')

        insertData = (
            f"INSERT INTO nbaParlay2 "
            f"("
            f"date, "
            f"team1, "
            f"team2, "
            f"category, "
            f"rideCalculated "
            f") "
            f"VALUES ("
            f"'{todaysDate}',"
            f"'{team1}',"
            f"'{team2}',"
            f"'{category}',"
            f"{rideCalculated}"
            f")"
        )
        mycursor.execute(insertData)
        mydb.commit()

        
        decentParlayFile.write(f"'{team1},")
        decentParlayFile.write(f"{team2},")
        decentParlayFile.write(f"{category},")
        decentParlayFile.write(f"{rideCalculated}',\n")

    decentParlayFile.write('];')


    #Update database and file with large parlay
    largeParlayFilename = '../frontend/src/nbaPages/largeParlay.js'
    largeParlayFile = open(largeParlayFilename, 'w')
    largeParlayFile.write('export const largeParlay = [\n')

    for game in largeP:
        rideCalculated, team1, team2, category = game.split('_')

        insertData = (
            f"INSERT INTO nbaParlay3 "
            f"("
            f"date, "
            f"team1, "
            f"team2, "
            f"category, "
            f"rideCalculated "
            f") "
            f"VALUES ("
            f"'{todaysDate}',"
            f"'{team1}',"
            f"'{team2}',"
            f"'{category}',"
            f"{rideCalculated}"
            f")"
        )
        mycursor.execute(insertData)
        mydb.commit()

        
        largeParlayFile.write(f"'{team1},")
        largeParlayFile.write(f"{team2},")
        largeParlayFile.write(f"{category},")
        largeParlayFile.write(f"{rideCalculated}',\n")

    largeParlayFile.write('];')

 

    for parlay in allParlays:
        rideCalculated, team1, team2, category = parlay.split('_')
        team1Name = getTeam(team1)['shortName']
        team2Name = getTeam(team2)['shortName']
        if getProbabilityRide(ALL_PERCENTAGES[f'{team1Name}_{category}']) and getProbabilityRide(ALL_PERCENTAGES[f'{team2Name}_{category}']):
            massiveP.append(f"{rideCalculated}_{team1}_{team2}_{category}")
    


    #Update database and file with massive parlay
    massiveParlayFilename = '../frontend/src/nbaPages/massiveParlay.js'
    massiveParlayFile = open(massiveParlayFilename, 'w')
    massiveParlayFile.write('export const massiveParlay = [\n')

    for game in massiveP:
        rideCalculated, team1, team2, category = game.split('_')

        insertData = (
            f"INSERT INTO nbaParlay4 "
            f"("
            f"date, "
            f"team1, "
            f"team2, "
            f"category, "
            f"rideCalculated "
            f") "
            f"VALUES ("
            f"'{todaysDate}',"
            f"'{team1}',"
            f"'{team2}',"
            f"'{category}',"
            f"{rideCalculated}"
            f")"
        )
        mycursor.execute(insertData)
        mydb.commit()

        
        massiveParlayFile.write(f"'{team1},")
        massiveParlayFile.write(f"{team2},")
        massiveParlayFile.write(f"{category},")
        massiveParlayFile.write(f"{rideCalculated}',\n")

    massiveParlayFile.write('];')

    print('(6/8) All parlays today have been predicted!')


def updateDatabaseParlays():
    todaysDate = date.today()
    yesterdaysDate = todaysDate - timedelta(days=1)
    yesterdayParlayDate = yesterdaysDate.strftime('%B %d %Y')
    yesterdayStatsDate = yesterdaysDate.strftime('%m/%d/%y')

    #Connect to MySQL Database
    mydb = mysql.connector.connect(
        host='127.0.0.1',
        user='davidcarney',
        password='Sinorrabb1t',
        database='NBA'
        )
    mycursor = mydb.cursor()

    #Get all data from Database
    mycursor.execute(f"SELECT * FROM nbaStats WHERE date = '{yesterdayStatsDate}';")
    teamData = mycursor.fetchall()
    teamsDF = pd.DataFrame(teamData, columns = ALL_COLUMNS)

    for parlayNumber in PARLAY_NUMBERS:

        mycursor.execute(f"SELECT * FROM nbaParlay{parlayNumber} WHERE date = '{yesterdayParlayDate}';")
        parlayData = mycursor.fetchall()
        parlayDF = pd.DataFrame(parlayData, columns = PARLAY_COLUMNS)

        for values in parlayDF.values:
            id, gameDate, team1, team2, category, rideCalculated, rideActual = values
            team1Number = getTeam(team1)['number']
            team2Number = getTeam(team2)['number']

            updatedTeamsDF = teamsDF[(teamsDF['teamNumber'] == team1Number) | (teamsDF['teamNumber'] == team2Number)]

            if category == 'spread':
                if list(updatedTeamsDF['spreadCalculated'].values == updatedTeamsDF['spreadActual'].values) == [True, True]:
                    #rideActual = 1
                    updateData = (
                        f"UPDATE nbaParlay{parlayNumber} "
                        f"SET rideActual = 1 "
                        f"WHERE id = {id};"
                    )
                    mycursor.execute(updateData)
                    mydb.commit()
                else:
                    #rideActual = 0
                    updateData = (
                        f"UPDATE nbaParlay{parlayNumber} "
                        f"SET rideActual = 0 "
                        f"WHERE id = {id};"
                    )
                    mycursor.execute(updateData)
                    mydb.commit()
                
            else:
                #OverUnder
                if list(updatedTeamsDF['overUnderCalculated'].values == updatedTeamsDF['overUnderActual'].values) == [True, True]:
                    #rideActual = 1
                    updateData = (
                        f"UPDATE nbaParlay{parlayNumber} "
                        f"SET rideActual = 1 "
                        f"WHERE id = {id};"
                    )
                    mycursor.execute(updateData)
                    mydb.commit()
                else:
                    #rideActual = 0
                    updateData = (
                        f"UPDATE nbaParlay{parlayNumber} "
                        f"SET rideActual = 0 "
                        f"WHERE id = {id};"
                    )
                    mycursor.execute(updateData)
                    mydb.commit()


    print('(7/8) All parlays have been updated to the database!')


def parlayPercentHelper(win, parlayPercents, name):
    if win == True:
        parlayPercents[name] = [parlayPercents[name][0] + 100, parlayPercents[name][1] + 1] 
    else:
        parlayPercents[name] = [parlayPercents[name][0], parlayPercents[name][1] + 1]


def updateParlayPercentages():
    parlayPercents = {}


    #Connect to MySQL Database
    mydb = mysql.connector.connect(
        host='127.0.0.1',
        user='davidcarney',
        password='Sinorrabb1t',
        database='NBA'
        )
    mycursor = mydb.cursor()


    for parlayNumber in PARLAY_NUMBERS:
        parlayName = f'Parlay {parlayNumber}'
        overallName = 'Overall'

        mycursor.execute(f"SELECT * FROM nbaParlay{parlayNumber} WHERE rideActual is not NULL;")
        parlayData = mycursor.fetchall()
        parlayDF = pd.DataFrame(parlayData, columns = PARLAY_COLUMNS)

        storedValues = []

        for row in parlayDF.sort_values(by=['date']).values:
            id, date, team1, team2, category, rideCalculated, rideActual = row
            parlayFullName = f'{parlayName}_{date}_{overallName}'
            parlayCategoryName = ''
            if category == 'spread':
                parlayCategoryName = f'{parlayName}_{date}_Spreads'
                if parlayCategoryName not in storedValues:
                    parlayPercents[parlayCategoryName] = [0,0]
                    storedValues.append(parlayCategoryName)
            elif category == 'overUnder':
                parlayCategoryName = f'{parlayName}_{date}_Over Unders'
                if parlayCategoryName not in storedValues:
                    parlayPercents[parlayCategoryName] = [0,0]
                    storedValues.append(parlayCategoryName)

            

            
            if date in storedValues:
                #same date
                parlayPercentHelper(rideCalculated == rideActual, parlayPercents, parlayCategoryName)
                parlayPercentHelper(rideCalculated == rideActual, parlayPercents, parlayFullName)
            else:
                #first date
                parlayPercents[parlayFullName] = [0,0]

                parlayPercentHelper(rideCalculated == rideActual, parlayPercents, parlayCategoryName)
                parlayPercentHelper(rideCalculated == rideActual, parlayPercents, parlayFullName)
                
                storedValues.append(date)

    finalParlayPercents = {}
    for percent in parlayPercents:
        if parlayPercents[percent][1] != 0:
            finalParlayPercents[percent] = round(parlayPercents[percent][0] / parlayPercents[percent][1], 2)
        else:
            finalParlayPercents[percent] = 'NA'


    #Update file with parlay percentages
    parlayPercentsFilename = '../frontend/src/nbaPages/parlayPercentages.js'
    parlayPercentsFile = open(parlayPercentsFilename, 'w')
    
    for parlayNumber in PARLAY_NUMBERS:
        parlayPercentsFile.write(f'export const parlay{parlayNumber}Percentages = [\n')
        for percent in finalParlayPercents:
            parlay, parlayDate, parlayCategory = percent.split('_')
            if parlay == f'Parlay {parlayNumber}':
                percentCorrect = finalParlayPercents[percent]
                if percentCorrect == 100:
                    
                    parlayTotalCalls = parlayPercents[percent][1]

                    parlayPercentsFile.write(f"'{parlay},")
                    parlayPercentsFile.write(f"{parlayCategory},")
                    parlayPercentsFile.write(f"{parlayDate},")
                    parlayPercentsFile.write(f"{parlayTotalCalls}',\n")

        parlayPercentsFile.write('];\n')
    
    
    parlayPercentsFile.close()

    print('(8/8) All parlays have been updated to the frontend file!')


            

        









updateNBAGames()
getGamblingData()                   #2/8
runML()                             #3/8
updateDatabaseActualResults()       #4/8
updatePercentages('save')           #5/8
runParlays()                        #6/8
updateDatabaseParlays()             #7/8
updateParlayPercentages()           #8/8