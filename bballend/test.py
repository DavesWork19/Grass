import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import mysql.connector
from datetime import date
import random

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score

from selenium import webdriver
from selenium.webdriver.common.by import By

from legends import *
from constants import ALL_TEAMS, ALL_YEARS 


sleepTimes = [7,13,17]


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
   
                    gameDay = row.find('td', attrs={'data-stat': 'date_game'}).text.split(',')[0]
                    gameStart = row.find('td', attrs={'data-stat': 'game_start_time'}).text
                    gameLocation = row.find('td', attrs={'data-stat': 'game_location'}).text
                    gameOppTeam = row.find('td', attrs={'data-stat': 'opp_name'}).text
                    gameResult = row.find('td', attrs={'data-stat': 'game_result'}).text
                    inSeasonTournament = row.find('td', attrs={'data-stat': 'game_remarks'}).text
                    primaryKey = int(f'{gameNumber}0{originalTeamNumber}{str(year)[-2:]}')

                    oppTeamNumber = getTeam(gameOppTeam)['number']
                    gameDayNumber = getDay(gameDay)['dayNumber']
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
                                f"year "
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
                                f"{year}"
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
                                f"gameTimeActual "
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
                                f"'{gameStart}'"
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
    dfColumns = ['id','gameNumber','teamNumber','isHome','oppTeamNumber','isWin','isOT','gameDayNumber','gameStartNumber','teamPoints','oppTeamPoints','teamWins','teamLosses','teamStreakCode','isInSeasonTournament','year','spread','spreadOdds','overUnder','overUnderOdds','moneyLine','gameTimeActual']
    nextGames = pd.DataFrame(teamData, columns = dfColumns)

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
        time.sleep(3)

        moreOverUnder = someOverUnder.find('div', class_='sportsbook-outcome-body-wrapper')
        evenMoreOverUnder = moreOverUnder.find_all('span')
        overUnderOdds  = evenMoreOverUnder[-1]
        overUnder = evenMoreOverUnder[-2]
        overUnder = overUnder.text
        overUnderOdds = overUnderOdds.text
        time.sleep(3)

        moreML = someML.find('div', class_='sportsbook-outcome-body-wrapper')
        MLOdds = moreML.find('span')
        MLOdds = MLOdds.text
        time.sleep(3)

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
    #Connect to MySQL Database
    mydb = mysql.connector.connect(
        host='127.0.0.1',
        user='davidcarney',
        password='Sinorrabb1t',
        database='NBA'
        )
    mycursor = mydb.cursor()

    #Open frontend file
    todaysGamesFilename = '../frontend/src/nbaPages/todaysGames.js'
    todaysGamesFile = open(todaysGamesFilename, 'w')
    todaysGamesFile.write('export const todaysGames = [\n')
    todaysDate = date.today().strftime("%B %d, %Y")
    todaysGamesFile.write(f"'{todaysDate}',\n")

    #Get all data from Database
    mycursor.execute(f"SELECT * FROM nbaStats;")
    teamData = mycursor.fetchall()
    dfColumns = ['id','gameNumber','teamNumber','isHome','oppTeamNumber','isWin','isOT','gameDayNumber','gameStartNumber','teamPoints','oppTeamPoints','teamWins','teamLosses','teamStreakCode','isInSeasonTournament','year','spread','spreadOdds','overUnder','overUnderOdds','moneyLine','gameTimeActual']
    allTeamsDF = pd.DataFrame(teamData, columns = dfColumns)

    
    #Iterate over each team
    teams = getTeam(ALL_TEAMS)
    columnsToPredict = ['teamPoints','oppTeamPoints']
    columnsToRemove = ['isWin','isOT','teamWins','teamLosses','teamStreakCode','spread','spreadOdds','overUnder','overUnderOdds','moneyLine','gameTimeActual']
    gamblingColumns = ['spread','spreadOdds','overUnder','overUnderOdds','moneyLine']
    year = 2024

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
            modelScores = {'teamLogisticRegression' : [0,0]}
            predictedScores = {'team1' : 0, 'team2' : 0}
            
            #Predicts column from columnsToPredict from dataframe for team1 and team2
            for column in columnsToPredict:
                y = df[column]
                X = df.drop(columns=columnsToPredict)

                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.19, random_state = 19)

                # create a pipeline object
                pipe = make_pipeline(
                    StandardScaler(),
                    LogisticRegression()
                )
                pipe.fit(X_train, y_train)

                for predicted,actual in zip(pipe.predict(X_test), y_test):
                    if ((actual + 3) >= predicted) and ((actual - 3) <= predicted):
                        modelScores['teamLogisticRegression'][0] = modelScores['teamLogisticRegression'][0] + 100
                        modelScores['teamLogisticRegression'][1] = modelScores['teamLogisticRegression'][1] + 1
                    else:
                        modelScores['teamLogisticRegression'][1] = modelScores['teamLogisticRegression'][1] + 1
                    
                predictedAccuracyScore = accuracy_score(pipe.predict(X_test), y_test)*100
                #print(f'predictedAccuracyScore: {predictedAccuracyScore}% for {column}\n')

                if column == 'teamPoints':
                    predictedScores['team1'] = pipe.predict(gamesToBePredictedDFWoGD[gamesToBePredictedDFWoGD['teamNumber'] == team1])
                    predictedScores['team2'] = pipe.predict(gamesToBePredictedDFWoGD[gamesToBePredictedDFWoGD['teamNumber'] == team2])
                elif column == 'oppTeamPoints':
                    predictedScores['team2'] = predictedScores['team2'] + pipe.predict(gamesToBePredictedDFWoGD[gamesToBePredictedDFWoGD['teamNumber'] == team1])
                    predictedScores['team2'] = predictedScores['team2'] / 2
                    predictedScores['team1'] = predictedScores['team1'] + pipe.predict(gamesToBePredictedDFWoGD[gamesToBePredictedDFWoGD['teamNumber'] == team2])
                    predictedScores['team1'] = predictedScores['team1'] / 2

            
            team1GamblingData = gamesToBePredictedDF[gamesToBePredictedDF['teamNumber'] == team1]
            team2GamblingData = gamesToBePredictedDF[gamesToBePredictedDF['teamNumber'] == team2]

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
            
            
            
            
            adjustedPredictedScored = modelScores['teamLogisticRegression'][0]/modelScores['teamLogisticRegression'][1]   
            #print(f'adjustedPredictedScored: {adjustedPredictedScored} for {team1} and {team2}')


            gamesAlreadyPredicted.append(team1)
            gamesAlreadyPredicted.append(team2)

    todaysGamesFile.write(f"]")
    todaysGamesFile.close()

    print('ALl games today have been predicted!')


            



updateNBAGames()
getGamblingData()
runML()


