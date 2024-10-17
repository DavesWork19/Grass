import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import mysql.connector
from datetime import date
import random

from selenium import webdriver
from selenium.webdriver.common.by import By

from legends import *
from constants import ALL_TEAMS, ALL_YEARS, ALL_COLUMNS

sleepTimes = [7,13,17]


def saveAllData():
    print('ok')

    teams = getTeam(ALL_TEAMS)

    #Connect to mysql
    mydb = mysql.connector.connect(
        host='127.0.0.1',
        user='davidcarney',
        password='Sinorrabb1t',
        database='NBA'
        )
    mycursor = mydb.cursor()
    
    for year in ALL_YEARS:
        for team in teams:
            originalTeamNumber = getTeam(team)['number']

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
                    
                                    
            time.sleep(random.choice(sleepTimes))
            print(f"{getTeam(team)['number'] + 1}/30 {team} completed.")



# def addAllPercentages():
#     print(f'allPercentages =','{')
#     for team in getTeam(ALL_TEAMS):
#         print(f"'{team}_spread': 0,")
#         print(f"'{team}_overUnder': 0,")
#         print(f"'{team}_parlay': 0,")

#         print(f"'{team}_last5Games_spread': 0,")
#         print(f"'{team}_last5Games_overUnder': 0,")
#         print(f"'{team}_last5Games_parlay': 0,")

#         print(f"'{team}_Monday_spread': 0,")
#         print(f"'{team}_Monday_overUnder': 0,")
#         print(f"'{team}_Monday_parlay': 0,")
#         print(f"'{team}_Tuesday_spread': 0,")
#         print(f"'{team}_Tuesday_overUnder': 0,")
#         print(f"'{team}_Tuesday_parlay': 0,")
#         print(f"'{team}_Wednesday_spread': 0,")
#         print(f"'{team}_Wednesday_overUnder': 0,")
#         print(f"'{team}_Wednesday_parlay': 0,")
#         print(f"'{team}_Thursday_spread': 0,")
#         print(f"'{team}_Thursday_overUnder': 0,")
#         print(f"'{team}_Thursday_parlay': 0,")
#         print(f"'{team}_Friday_spread': 0,")
#         print(f"'{team}_Friday_overUnder': 0,")
#         print(f"'{team}_Friday_parlay': 0,")
#         print(f"'{team}_Saturday_spread': 0,")
#         print(f"'{team}_Saturday_overUnder': 0,")
#         print(f"'{team}_Saturday_parlay': 0,")
#         print(f"'{team}_Sunday_spread': 0,")
#         print(f"'{team}_Sunday_overUnder': 0,")
#         print(f"'{team}_Sunday_parlay': 0,")

#         print(f"'{team}_Time_12_1259_spread': 0,")
#         print(f"'{team}_Time_1_159_spread': 0,")
#         print(f"'{team}_Time_2_259_spread': 0,")
#         print(f"'{team}_Time_3_359_spread': 0,")
#         print(f"'{team}_Time_4_459_spread': 0,")
#         print(f"'{team}_Time_5_559_spread': 0,")
#         print(f"'{team}_Time_6_659_spread': 0,")
#         print(f"'{team}_Time_7_759_spread': 0,")
#         print(f"'{team}_Time_8_859_spread': 0,")
#         print(f"'{team}_Time_9_959_spread': 0,")
#         print(f"'{team}_Time_10_1059_spread': 0,")
#         print(f"'{team}_Time_11_1159_spread': 0,")
#         print(f"'{team}_Time_12_1259_overUnder': 0,")
#         print(f"'{team}_Time_1_159_overUnder': 0,")
#         print(f"'{team}_Time_2_259_overUnder': 0,")
#         print(f"'{team}_Time_3_359_overUnder': 0,")
#         print(f"'{team}_Time_4_459_overUnder': 0,")
#         print(f"'{team}_Time_5_559_overUnder': 0,")
#         print(f"'{team}_Time_6_659_overUnder': 0,")
#         print(f"'{team}_Time_7_759_overUnder': 0,")
#         print(f"'{team}_Time_8_859_overUnder': 0,")
#         print(f"'{team}_Time_9_959_overUnder': 0,")
#         print(f"'{team}_Time_10_1059_overUnder': 0,")
#         print(f"'{team}_Time_11_1159_overUnder': 0,")
#         print(f"'{team}_Time_12_1259_parlay': 0,")
#         print(f"'{team}_Time_1_159_parlay': 0,")
#         print(f"'{team}_Time_2_259_parlay': 0,")
#         print(f"'{team}_Time_3_359_parlay': 0,")
#         print(f"'{team}_Time_4_459_parlay': 0,")
#         print(f"'{team}_Time_5_559_parlay': 0,")
#         print(f"'{team}_Time_6_659_parlay': 0,")
#         print(f"'{team}_Time_7_759_parlay': 0,")
#         print(f"'{team}_Time_8_859_parlay': 0,")
#         print(f"'{team}_Time_9_959_parlay': 0,")
#         print(f"'{team}_Time_10_1059_parlay': 0,")
#         print(f"'{team}_Time_11_1159_parlay': 0,")

#     print(f"'overall_spread': 0,")
#     print(f"'overall_overUnder': 0,")
#     print(f"'overall_parlay': 0,")
#     print(f"'overall_last5Games_spread': 0,")
#     print(f"'overall_last5Games_overUnder': 0,")
#     print(f"'overall_last5Games_parlay': 0,")
#     print(f"'overall_Monday_spread': 0,")
#     print(f"'overall_Monday_overUnder': 0,")
#     print(f"'overall_Monday_parlay': 0,")
#     print(f"'overall_Tuesday_spread': 0,")
#     print(f"'overall_Tuesday_overUnder': 0,")
#     print(f"'overall_Tuesday_parlay': 0,")
#     print(f"'overall_Wednesday_spread': 0,")
#     print(f"'overall_Wednesday_overUnder': 0,")
#     print(f"'overall_Wednesday_parlay': 0,")
#     print(f"'overall_Thursday_spread': 0,")
#     print(f"'overall_Thursday_overUnder': 0,")
#     print(f"'overall_Thursday_parlay': 0,")
#     print(f"'overall_Friday_spread': 0,")
#     print(f"'overall_Friday_overUnder': 0,")
#     print(f"'overall_Friday_parlay': 0,")
#     print(f"'overall_Saturday_spread': 0,")
#     print(f"'overall_Saturday_overUnder': 0,")
#     print(f"'overall_Saturday_parlay': 0,")
#     print(f"'overall_Sunday_spread': 0,")
#     print(f"'overall_Sunday_overUnder': 0,")
#     print(f"'overall_Sunday_parlay': 0,")
#     print(f"'overall_Time_12_1259_spread': 0,")
#     print(f"'overall_Time_1_159_spread': 0,")
#     print(f"'overall_Time_2_259_spread': 0,")
#     print(f"'overall_Time_3_359_spread': 0,")
#     print(f"'overall_Time_4_459_spread': 0,")
#     print(f"'overall_Time_5_559_spread': 0,")
#     print(f"'overall_Time_6_659_spread': 0,")
#     print(f"'overall_Time_7_759_spread': 0,")
#     print(f"'overall_Time_8_859_spread': 0,")
#     print(f"'overall_Time_9_959_spread': 0,")
#     print(f"'overall_Time_10_1059_spread': 0,")
#     print(f"'overall_Time_11_1159_spread': 0,")
#     print(f"'overall_Time_12_1259_overUnder': 0,")
#     print(f"'overall_Time_1_159_overUnder': 0,")
#     print(f"'overall_Time_2_259_overUnder': 0,")
#     print(f"'overall_Time_3_359_overUnder': 0,")
#     print(f"'overall_Time_4_459_overUnder': 0,")
#     print(f"'overall_Time_5_559_overUnder': 0,")
#     print(f"'overall_Time_6_659_overUnder': 0,")
#     print(f"'overall_Time_7_759_overUnder': 0,")
#     print(f"'overall_Time_8_859_overUnder': 0,")
#     print(f"'overall_Time_9_959_overUnder': 0,")
#     print(f"'overall_Time_10_1059_overUnder': 0,")
#     print(f"'overall_Time_11_1159_overUnder': 0,")
#     print(f"'overall_Time_12_1259_parlay': 0,")
#     print(f"'overall_Time_1_159_parlay': 0,")
#     print(f"'overall_Time_2_259_parlay': 0,")
#     print(f"'overall_Time_3_359_parlay': 0,")
#     print(f"'overall_Time_4_459_parlay': 0,")
#     print(f"'overall_Time_5_559_parlay': 0,")
#     print(f"'overall_Time_6_659_parlay': 0,")
#     print(f"'overall_Time_7_759_parlay': 0,")
#     print(f"'overall_Time_8_859_parlay': 0,")
#     print(f"'overall_Time_9_959_parlay': 0,")
#     print(f"'overall_Time_10_1059_parlay': 0,")
#     print(f"'overall_Time_11_1159_parlay': 0,")
#     print('}')



saveAllData()





