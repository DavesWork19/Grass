import sys
import requests
from bs4 import BeautifulSoup
import mysql.connector
import pandas as pd
import numpy as np
from datetime import datetime
import time
import random
import json

from selenium import webdriver
from selenium.webdriver.common.by import By

from theBBallBot import theBot
from Legends import *
from constants import *

#For each team
#Go to website and scrape all data for given team
#Find previous week if its not a by week
#Save weeks data to database
class storeTeamData:
    def __init__(self, table, week, year):
        self.teams = ['dal','tam','nor','atl','car','min','gnb','det','chi','ram','crd','sfo','sea','oti','clt','jax','kan','rai','sdg','den','phi','was','nyg','nyj','mia','nwe','buf','cin','pit','rav','cle','htx']
        self.table = table
        self.week = week - 1
        self.year = year

    def storeDataToMySQL(self, team, df):
        mydb = mysql.connector.connect(
        host='127.0.0.1',
        user='davidcarney',
        password='Sinorrabb1t',
        database='NFL'
        )

        mycursor = mydb.cursor()

        for index, row in df.iterrows():
            if row[6] != 0:
                yardsPerPoint = (row[10] + row[20]) / row[6]
            else:
                yardsPerPoint = 0

            if row[4] == 0:
                insertData = (
                    f"UPDATE {self.table} SET "
                    f"WinLoss = {row[2]},"
                    f"OT = {row[3]},"
                    f"At = {row[4]},"
                    f"OppTeam = {row[5]},"
                    f"Tm = {row[6]},"
                    f"Opp = {row[7]},"
                    f"Cmp = {row[8]},"
                    f"AttPassing = {row[9]},"
                    f"YdsPassing = {row[10]},"
                    f"TDPassing = {row[11]},"
                    f"interceptions = {row[12]},"
                    f"Sk = {row[13]},"
                    f"YdsLossFromSacks = {row[14]},"
                    f"YPerAPassing = {row[15]},"
                    f"NYPerA = {row[16]},"
                    f"CmpPerc = {row[17]},"
                    f"Rate = {row[18]},"
                    f"AttRushing = {row[19]},"
                    f"YdsRushing = {row[20]},"
                    f"YPerARushing = {row[21]},"
                    f"TDRushing = {row[22]},"
                    f"FGM = {row[23]},"
                    f"FGA = {row[24]},"
                    f"XPM = {row[25]},"
                    f"XPA = {row[26]},"
                    f"Pnt = {row[27]},"
                    f"YdsPunting = {row[28]},"
                    f"ThirdDConv = {row[29]},"
                    f"ThirdDAtt = {row[30]},"
                    f"FourthDConv = {row[31]},"
                    f"FourthDAtt = {row[32]},"
                    f"YardsPerPoint = {yardsPerPoint},"
                    f"HomeTeam = {row[5]},"
                    f"Top = {row[33]} WHERE Year = {self.year} and Week = {self.week} and Team = '{team}'"
                )
                mycursor.execute(insertData)
                mydb.commit()
            else:
                insertData = (
                    f"UPDATE {self.table} SET "
                    f"WinLoss = {row[2]},"
                    f"OT = {row[3]},"
                    f"At = {row[4]},"
                    f"OppTeam = {row[5]},"
                    f"Tm = {row[6]},"
                    f"Opp = {row[7]},"
                    f"Cmp = {row[8]},"
                    f"AttPassing = {row[9]},"
                    f"YdsPassing = {row[10]},"
                    f"TDPassing = {row[11]},"
                    f"interceptions = {row[12]},"
                    f"Sk = {row[13]},"
                    f"YdsLossFromSacks = {row[14]},"
                    f"YPerAPassing = {row[15]},"
                    f"NYPerA = {row[16]},"
                    f"CmpPerc = {row[17]},"
                    f"Rate = {row[18]},"
                    f"AttRushing = {row[19]},"
                    f"YdsRushing = {row[20]},"
                    f"YPerARushing = {row[21]},"
                    f"TDRushing = {row[22]},"
                    f"FGM = {row[23]},"
                    f"FGA = {row[24]},"
                    f"XPM = {row[25]},"
                    f"XPA = {row[26]},"
                    f"Pnt = {row[27]},"
                    f"YdsPunting = {row[28]},"
                    f"ThirdDConv = {row[29]},"
                    f"ThirdDAtt = {row[30]},"
                    f"FourthDConv = {row[31]},"
                    f"FourthDAtt = {row[32]},"
                    f"YardsPerPoint = {yardsPerPoint},"
                    f"HomeTeam = {getTeamFromSmallName(team)},"
                    f"Top = {row[33]} WHERE Year = {self.year} and Week = {self.week} and Team = '{team}'"
                )
                mycursor.execute(insertData)
                mydb.commit()

    def getLastWeekTeamData(self, team):

        URL = f'https://www.pro-football-reference.com/teams/{team}/{self.year}/gamelog/'
        # HEADERS = {
        #     'User-Agent': 'Safari/605.15',
        # }
        # page = requests.get(URL, headers=HEADERS)
        proxies = {
        'http': 'http://172.67.191.62:80'
        }
        time.sleep(47)
        page = requests.get(URL, proxies=proxies)
        #page = requests.get(URL)
        time.sleep(random.choice([15,19,23]))
        soup = BeautifulSoup(page.content, 'html.parser')
        time.sleep(random.choice([15,19,23]))
        moreSoup = soup.find('table', id=f'gamelog{self.year}')

        df = pd.read_html(str(moreSoup))[0]

        columns = []
        for col in df.columns:
            columns.append(col[1])
        df.columns = columns

        if (df['Week'] == self.week).any(): #If not a by week
            df = df.drop(columns=['Unnamed: 3_level_1','Date'])
            df = df.rename(columns={'Unnamed: 4_level_1': 'WinLoss', 'Unnamed: 6_level_1': 'At'})
            df.columns.values[5] = 'OppTeam'
            df = df.loc[df['Week'] == self.week]

            df['Day'] = getDay(df['Day'].values[0])
            df['WinLoss'] = getWinloss(df['WinLoss'].values[0])
            df['OT'] = getOT(df['OT'].values[0])
            df['At'] = getAt(df['At'].values[0])
            df['OppTeam'] = getTeam(df['OppTeam'].values[0])
            df['ToP'] = float(df['ToP'].values[0].replace(':','.'))

            self.storeDataToMySQL(team, df)


    def storeAllTeamsData(self):
        for num, team in enumerate(self.teams):
            teamDF = self.getLastWeekTeamData(team)

            print(f'{num}. {team} updated.')
        
        print('All teams have been saved to database!')



def updateCoveredValues():
    mydb = mysql.connector.connect(
        host='127.0.0.1',
        user='davidcarney',
        password='Sinorrabb1t',
        database='NFL'
        )
    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM productionNFL WHERE spread is not NULL and tm is not NULL and (totalCovered is NULL or spreadCovered is NULL)")

    teamData = mycursor.fetchall()
    nextGames = pd.DataFrame(teamData, columns = ALL_COLUMNS)
    for game in nextGames.iterrows():
        game = game[1]
        id = game['id']
        teamPoints = int(game['Tm'])
        oppTeamPoints = int(game['Opp'])
        spread = game['spread']
        total = float(game['total'])
        spreadSign = spread[0]
        spreadValue = None

        #OverUnder
        if teamPoints + oppTeamPoints >= total:
            mycursor.execute(f'UPDATE productionNFL SET totalCovered = 1 WHERE id = {id}')
            mydb.commit()
        else:
            mycursor.execute(f'UPDATE productionNFL SET totalCovered = 0 WHERE id = {id}')
            mydb.commit()


        #Spread
        if spread != 'pk':
            spreadValue = float(spread[1:])

        if spreadSign == '-':
            if teamPoints - oppTeamPoints >= spreadValue:
                mycursor.execute(f'UPDATE productionNFL SET spreadCovered = 1 WHERE id = {id}')
                mydb.commit()
            else:
                mycursor.execute(f'UPDATE productionNFL SET spreadCovered = 0 WHERE id = {id}')
                mydb.commit()

        elif spreadSign == '+':
            if -(teamPoints - oppTeamPoints) <= spreadValue:
                mycursor.execute(f'UPDATE productionNFL SET spreadCovered = 1 WHERE id = {id}')
                mydb.commit()
            else:
                mycursor.execute(f'UPDATE productionNFL SET spreadCovered = 0 WHERE id = {id}')
                mydb.commit()
        else:
            if teamPoints - oppTeamPoints >= 0:
                mycursor.execute(f'UPDATE productionNFL SET spreadCovered = 1 WHERE id = {id}')
                mydb.commit()
            else:
                mycursor.execute(f'UPDATE productionNFL SET spreadCovered = 0 WHERE id = {id}')
                mydb.commit()




#For each game in a week
#Go to website and scrape all data (all games in a week)
#Find all unqiue game data for each game that week
#Write data to frontend files and store in database

#Also go to website and scrapte all gambling data
#Including spread, spreadOdds, overunder, overunderOdds, and moneyline
class getUpcomingWeekData:
    def __init__(self, week, year):
        self.week = week
        self.year = year
  
    def getWeatherByWeek(self):
        teamDataFilename = 'teamDataHolder.txt'
        teamDataFile = open(teamDataFilename, 'w')

        mydb = mysql.connector.connect(
        host='127.0.0.1',
        user='davidcarney',
        password='Sinorrabb1t',
        database='NFL'
        )
        mycursor = mydb.cursor()


        URL = f'https://www.nflweather.com/week/{self.year}/week-{self.week}'
        HEADERS = {
            'User-Agent': 'Safari/537.36',
        }
        page = requests.get(URL, headers=HEADERS)
        soup = BeautifulSoup(page.content, 'html.parser')
        moreSoup = soup.find('div', class_='container-game-box')
        time.sleep(7)

        matchUp = moreSoup.div 
        while matchUp != None:
            matchUpData1 = matchUp.div
            dateAndTime = matchUpData1.div.text.strip()
            dateAndTime = dateAndTime.split(' ')
            day = datetime.strptime(dateAndTime[0], '%m/%d/%y')
            dayCode = getDay(day.strftime('%A')[:3])

            hour = int(dateAndTime[1].split(':')[0])
            am_pm = dateAndTime[2]
            timeCode = getTime(hour,am_pm)
            time.sleep(3)

            matchUpData2 = matchUpData1.next_sibling.next_sibling
            awayTeam, at, homeTeam = matchUpData2.find_all('span')
            awayTeam = awayTeam.text
            homeTeam = homeTeam.text
 
            time.sleep(3)
            
            matchUpData3 = matchUpData2.next_sibling.next_sibling
            weatherData = matchUpData3.div.div.next_sibling.next_sibling
            weatherInfo = weatherData.find_all('span')

            temp = None
            weather = None
            if len(weatherInfo) == 0:
                temp = 62
                weather = 'Cloudy'
                print('ERROR : WEATHER INFO LEN IS 0')
            elif len(weatherInfo) == 1:
                temp = int(weatherInfo[0].text.split(' ')[0])
                weather = 'Clear'
            else:
                temp, weather = weatherInfo
                temp = int(temp.text.split(' ')[0])
                weather = weather.text

            time.sleep(3)
            windDataContainer = weatherData.next_sibling.next_sibling
            windData = windDataContainer.find_all('span')
            windDataLength = len(windData)
            wind = 0
            if windDataLength == 3:
                wind = windData[1].text.split(' ')[0]

            time.sleep(3)
            channelData = windDataContainer.next_sibling.next_sibling
            channel = 0
            if channelData != None:
                channels = channelData.find_all('span')
                channelsLength = len(channels)
                if channelsLength > 1:
                    channel = channels[1].text
                    if ',' in channel:
                        channel = channel.split(',')[0]
                    elif ' ' in channel:
                        channel = channel.split(' ')[0]
                    channel = getChannel(channel)
            else:
                channel = 6

            if channel == None:
                channel = 5
            
            insertHomeData = (
                        f"INSERT INTO productionNFL "
                        f"("
                        f"DateTime, "
                        f"Week, "
                        f"Day, "
                        f"At, "
                        f"OppTeam, "
                        f"Year, "
                        f"Team, "
                        f"HomeTeam, "
                        f"Time, "
                        f"Channel, "
                        f"Temp, "
                        f"Weather, "
                        f"Wind "
                        f") "
                        f"VALUES ("
                        f"'{' '.join(dateAndTime)}',"
                        f"{self.week},"
                        f"{dayCode},"
                        f"{1},"
                        f"{getTeam(awayTeam)},"
                        f"{self.year},"
                        f"'{getTeamSmallNameFromTeam(getTeam(homeTeam))}',"
                        f"{getTeam(homeTeam)},"
                        f"{timeCode},"
                        f"{channel},"
                        f"{getTemp(temp)},"
                        f"{getWeather(weather)},"
                        f"{wind}"
                        f")"
                )
            print(insertHomeData)
            mycursor.execute(insertHomeData)
            mydb.commit()

            insertAwayData = (
                        f"INSERT INTO productionNFL "
                        f"("
                        f"DateTime, "
                        f"Week, "
                        f"Day, "
                        f"At, "
                        f"OppTeam, "
                        f"Year, "
                        f"Team, "
                        f"HomeTeam, "
                        f"Time, "
                        f"Channel, "
                        f"Temp, "
                        f"Weather, "
                        f"Wind "
                        f") "
                        f"VALUES ("
                        f"'{' '.join(dateAndTime)}',"
                        f"{self.week},"
                        f"{dayCode},"
                        f"{0},"
                        f"{getTeam(homeTeam)},"
                        f"{self.year},"
                        f"'{getTeamSmallNameFromTeam(getTeam(awayTeam))}',"
                        f"{getTeam(homeTeam)},"
                        f"{timeCode},"
                        f"{channel},"
                        f"{getTemp(temp)},"
                        f"{getWeather(weather)},"
                        f"{wind}"
                        f")"
                )
            mycursor.execute(insertAwayData)
            mydb.commit()

            teamDataFile.write(awayTeam)
            teamDataFile.write('_')
            teamDataFile.write(homeTeam)
            teamDataFile.write('_')
            teamDataFile.write(f'{timeCode}')
            teamDataFile.write('_')
            teamDataFile.write(f'{dayCode}')
            teamDataFile.write('_')
            teamDataFile.write(f'{getTemp(temp)}')
            teamDataFile.write('_')
            teamDataFile.write(f'{getWeather(weather)}')
            teamDataFile.write('_')
            teamDataFile.write(f'{wind}')
            teamDataFile.write('\n')

            matchUp = matchUp.next_sibling.next_sibling

        print(f'Essential Data has been saved!')


    def gamblingDataHelper(self, team):
        teamName = team.find('th').find('div', class_='event-cell__name-text').text
        spread, total, ML = team.find_all('td')
        spread, spreadOdds = spread.find_all('span')
        spread = spread.text
        spreadOdds = spreadOdds.text
        awayOU, blank, total, totalOdds = total.find_all('span')
        awayOU = awayOU.text
        total = total.text
        totalOdds = totalOdds.text
        ML = ML.text

        return [teamName, spread, spreadOdds, total, totalOdds, ML]


    def getGamblingData(self):
        mydb = mysql.connector.connect(
            host='127.0.0.1',
            user='davidcarney',
            password='Sinorrabb1t',
            database='NFL'
        )
        mycursor = mydb.cursor()


        #Get previous games from Database
        mycursor.execute(f"SELECT * FROM productionNFL WHERE WinLoss is Null;")

        teamData = mycursor.fetchall()
        nextGames = pd.DataFrame(teamData, columns = ALL_COLUMNS)

        sleepTimes = [3,7,13]

        #Start Selenium driver
        driver = webdriver.Chrome()
        driver.get("https://sportsbook.draftkings.com/leagues/football/nfl")
        time.sleep(random.choice(sleepTimes))

        container = driver.find_element(By.CLASS_NAME, 'sportsbook-responsive-card-container')
        time.sleep(random.choice(sleepTimes))
        allSections = driver.find_elements(By.CLASS_NAME, 'parlay-card-10-a')


        for row in allSections:
            todayGamesTableHTML = row.get_attribute('innerHTML')
            soup = BeautifulSoup(todayGamesTableHTML, 'html.parser')
            table = soup.find('table')

            originalDate = table.find('thead').find_all('th')[0].text
            originalDateList = originalDate.split(' ')
            originalDateListLen = len(originalDateList)


            thisWeek = False
            if(originalDateListLen == 3):
                weekday, month, day = originalDateList
                day = day[:-2]

                updatedDate = datetime.strptime(f'{month}/{day}', '%b/%d')

                start, end = ALL_WEEKS[self.week]
                startMonth, startDay = start.split('/')
                startMonth = int(startMonth)
                startDay = int(startDay)
                endMonth, endDay = end.split('/')
                endMonth = int(endMonth)
                endDay = int(endDay)

                if (startMonth <= updatedDate.month) and (endMonth >= updatedDate.month) and (startDay <= updatedDate.day) and (endDay >= updatedDate.day):
                    thisWeek = True

            elif (originalDateList[0] == 'Tomorrow') or (originalDateList[0] == 'Today'):
                thisWeek = True    

            
            if thisWeek:
                games = table.find('tbody').find_all('tr')
                if len(games) == 2:
                    awayTeam, homeTeam = games
                    awayTeamName, awaySpread, awaySpreadOdds, awayTotal, awayTotalOdds, awayML = self.gamblingDataHelper(awayTeam)
                    homeTeamName, homeSpread, homeSpreadOdds, homeTotal, homeTotalOdds, homeML = self.gamblingDataHelper(homeTeam)

                    awayData = (
                        f"UPDATE productionNFL "
                        f"SET spread = '{awaySpread}', "
                        f"spreadOdds = '{awaySpreadOdds}', "
                        f"total = '{awayTotal}', "
                        f"totalOdds = '{awayTotalOdds}', "
                        f"ML = '{awayML}' "
                        f"WHERE Week = {self.week} and Year = {self.year} and Team = '{getTeamSmallNameFromTeam(getTeam(awayTeamName))}';"
                    )
                    mycursor.execute(awayData)
                    mydb.commit()


                    homeData = (
                        f"UPDATE productionNFL "
                        f"SET spread = '{homeSpread}', "
                        f"spreadOdds = '{homeSpreadOdds}', "
                        f"total = '{homeTotal}', "
                        f"totalOdds = '{homeTotalOdds}', "
                        f"ML = '{homeML}' "
                        f"WHERE Week = {self.week} and Year = {self.year} and Team = '{getTeamSmallNameFromTeam(getTeam(homeTeamName))}';"
                    )
                    mycursor.execute(homeData)
                    mydb.commit()
                else:
                    matchUps = []
                    awayCounter = True
                    awayTeam = None
                    homeTeam = None

                    for game in games:

                        if awayCounter:
                            awayTeam = game
                            awayCounter = False
                        else: 
                            homeTeam = game
                            awayCounter = True

                        if awayTeam and homeTeam:
                            awayTeamName, awaySpread, awaySpreadOdds, awayTotal, awayTotalOdds, awayML = self.gamblingDataHelper(awayTeam)
                            homeTeamName, homeSpread, homeSpreadOdds, homeTotal, homeTotalOdds, homeML = self.gamblingDataHelper(homeTeam)

                            awayData = (
                                f"UPDATE productionNFL "
                                f"SET spread = '{awaySpread}', "
                                f"spreadOdds = '{awaySpreadOdds}', "
                                f"total = '{awayTotal}', "
                                f"totalOdds = '{awayTotalOdds}', "
                                f"ML = '{awayML}' "
                                f"WHERE Week = {self.week} and Year = {self.year} and Team = '{getTeamSmallNameFromTeam(getTeam(awayTeamName))}';"
                            )
                            mycursor.execute(awayData)
                            mydb.commit()


                            homeData = (
                                f"UPDATE productionNFL "
                                f"SET spread = '{homeSpread}', "
                                f"spreadOdds = '{homeSpreadOdds}', "
                                f"total = '{homeTotal}', "
                                f"totalOdds = '{homeTotalOdds}', "
                                f"ML = '{homeML}' "
                                f"WHERE Week = {self.week} and Year = {self.year} and Team = '{getTeamSmallNameFromTeam(getTeam(homeTeamName))}';"
                            )
                            mycursor.execute(homeData)
                            mydb.commit()


                            awayTeam = None
                            homeTeam = None

                

        driver.quit()

        print('All gambling data has been saved!')









#Update all percentages for all weeks and years
def updatePercentages():
    #Data format:
    # awayTeam_homeTeam_timeCode_dayCode_temp_weather_wind_predWinner_predLoser_outcome
    filename = 'teamData.txt'
    theFile = open(filename, 'r')

    teamInfo = {
        'Bills': 'AFC East',
        'Dolphins': 'AFC East',
        'Patriots': 'AFC East',
        'Jets': 'AFC East',
        'Bengals': 'AFC North',
        'Browns': 'AFC North',
        'Steelers': 'AFC North',
        'Ravens': 'AFC North',
        'Colts': 'AFC South',
        'Texans': 'AFC South',
        'Jaguars': 'AFC South',
        'Titans': 'AFC South',
        'Broncos': 'AFC West',
        'Chiefs': 'AFC West',
        'Raiders': 'AFC West',
        'Chargers': 'AFC West',
        'Cowboys': 'NFC East',
        'Giants': 'NFC East',
        'Eagles': 'NFC East',
        'Washington': 'NFC East',
        'Bears': 'NFC North',
        'Lions': 'NFC North',
        'Packers': 'NFC North',
        'Vikings': 'NFC North',
        'Falcons': 'NFC South',
        'Panthers': 'NFC South',
        'Saints': 'NFC South',
        'Buccaneers': 'NFC South',
        'Cardinals': 'NFC West',
        'Rams': 'NFC West',
        'Seahawks': 'NFC West',
        '49ers': 'NFC West',
    }
    results = {
        'AFC': [0, 0],
        'AFC North': [0, 0],
        'AFC South': [0, 0],
        'AFC East': [0, 0],
        'AFC West': [0, 0],
        'NFC': [0, 0],
        'NFC North': [0, 0],
        'NFC South': [0, 0],
        'NFC East': [0, 0],
        'NFC West': [0, 0],
        'Bills': [0, 0],
        'Dolphins': [0, 0],
        'Patriots': [0, 0],
        'Jets': [0, 0],
        'Bengals': [0, 0],
        'Browns': [0, 0],
        'Steelers': [0, 0],
        'Ravens': [0, 0],
        'Colts': [0, 0],
        'Texans': [0, 0],
        'Jaguars': [0, 0],
        'Titans': [0, 0],
        'Broncos': [0, 0],
        'Chiefs': [0, 0],
        'Raiders': [0, 0],
        'Chargers': [0, 0],
        'Cowboys': [0, 0],
        'Giants': [0, 0],
        'Eagles': [0, 0],
        'Washington': [0, 0],
        'Bears': [0, 0],
        'Lions': [0, 0],
        'Packers': [0, 0],
        'Vikings': [0, 0],
        'Falcons': [0, 0],
        'Panthers': [0, 0],
        'Saints': [0, 0],
        'Buccaneers': [0, 0],
        'Cardinals': [0, 0],
        'Rams': [0, 0],
        'Seahawks': [0, 0],
        '49ers': [0, 0],
        'Bills_away': [0, 0],
        'Dolphins_away': [0, 0],
        'Patriots_away': [0, 0],
        'Jets_away': [0, 0],
        'Bengals_away': [0, 0],
        'Browns_away': [0, 0],
        'Steelers_away': [0, 0],
        'Ravens_away': [0, 0],
        'Colts_away': [0, 0],
        'Texans_away': [0, 0],
        'Jaguars_away': [0, 0],
        'Titans_away': [0, 0],
        'Broncos_away': [0, 0],
        'Chiefs_away': [0, 0],
        'Raiders_away': [0, 0],
        'Chargers_away': [0, 0],
        'Cowboys_away': [0, 0],
        'Giants_away': [0, 0],
        'Eagles_away': [0, 0],
        'Washington_away': [0, 0],
        'Bears_away': [0, 0],
        'Lions_away': [0, 0],
        'Packers_away': [0, 0],
        'Vikings_away': [0, 0],
        'Falcons_away': [0, 0],
        'Panthers_away': [0, 0],
        'Saints_away': [0, 0],
        'Buccaneers_away': [0, 0],
        'Cardinals_away': [0, 0],
        'Rams_away': [0, 0],
        'Seahawks_away': [0, 0],
        '49ers_away': [0, 0],
        'Bills_home': [0, 0],
        'Dolphins_home': [0, 0],
        'Patriots_home': [0, 0],
        'Jets_home': [0, 0],
        'Bengals_home': [0, 0],
        'Browns_home': [0, 0],
        'Steelers_home': [0, 0],
        'Ravens_home': [0, 0],
        'Colts_home': [0, 0],
        'Texans_home': [0, 0],
        'Jaguars_home': [0, 0],
        'Titans_home': [0, 0],
        'Broncos_home': [0, 0],
        'Chiefs_home': [0, 0],
        'Raiders_home': [0, 0],
        'Chargers_home': [0, 0],
        'Cowboys_home': [0, 0],
        'Giants_home': [0, 0],
        'Eagles_home': [0, 0],
        'Washington_home': [0, 0],
        'Bears_home': [0, 0],
        'Lions_home': [0, 0],
        'Packers_home': [0, 0],
        'Vikings_home': [0, 0],
        'Falcons_home': [0, 0],
        'Panthers_home': [0, 0],
        'Saints_home': [0, 0],
        'Buccaneers_home': [0, 0],
        'Cardinals_home': [0, 0],
        'Rams_home': [0, 0],
        'Seahawks_home': [0, 0],
        '49ers_home': [0, 0],
        'Bills_predictedWinner': [0, 0],
        'Dolphins_predictedWinner': [0, 0],
        'Patriots_predictedWinner': [0, 0],
        'Jets_predictedWinner': [0, 0],
        'Bengals_predictedWinner': [0, 0],
        'Browns_predictedWinner': [0, 0],
        'Steelers_predictedWinner': [0, 0],
        'Ravens_predictedWinner': [0, 0],
        'Colts_predictedWinner': [0, 0],
        'Texans_predictedWinner': [0, 0],
        'Jaguars_predictedWinner': [0, 0],
        'Titans_predictedWinner': [0, 0],
        'Broncos_predictedWinner': [0, 0],
        'Chiefs_predictedWinner': [0, 0],
        'Raiders_predictedWinner': [0, 0],
        'Chargers_predictedWinner': [0, 0],
        'Cowboys_predictedWinner': [0, 0],
        'Giants_predictedWinner': [0, 0],
        'Eagles_predictedWinner': [0, 0],
        'Washington_predictedWinner': [0, 0],
        'Bears_predictedWinner': [0, 0],
        'Lions_predictedWinner': [0, 0],
        'Packers_predictedWinner': [0, 0],
        'Vikings_predictedWinner': [0, 0],
        'Falcons_predictedWinner': [0, 0],
        'Panthers_predictedWinner': [0, 0],
        'Saints_predictedWinner': [0, 0],
        'Buccaneers_predictedWinner': [0, 0],
        'Cardinals_predictedWinner': [0, 0],
        'Rams_predictedWinner': [0, 0],
        'Seahawks_predictedWinner': [0, 0],
        '49ers_predictedWinner': [0, 0],
        'Bills_predictedLoser': [0, 0],
        'Dolphins_predictedLoser': [0, 0],
        'Patriots_predictedLoser': [0, 0],
        'Jets_predictedLoser': [0, 0],
        'Bengals_predictedLoser': [0, 0],
        'Browns_predictedLoser': [0, 0],
        'Steelers_predictedLoser': [0, 0],
        'Ravens_predictedLoser': [0, 0],
        'Colts_predictedLoser': [0, 0],
        'Texans_predictedLoser': [0, 0],
        'Jaguars_predictedLoser': [0, 0],
        'Titans_predictedLoser': [0, 0],
        'Broncos_predictedLoser': [0, 0],
        'Chiefs_predictedLoser': [0, 0],
        'Raiders_predictedLoser': [0, 0],
        'Chargers_predictedLoser': [0, 0],
        'Cowboys_predictedLoser': [0, 0],
        'Giants_predictedLoser': [0, 0],
        'Eagles_predictedLoser': [0, 0],
        'Washington_predictedLoser': [0, 0],
        'Bears_predictedLoser': [0, 0],
        'Lions_predictedLoser': [0, 0],
        'Packers_predictedLoser': [0, 0],
        'Vikings_predictedLoser': [0, 0],
        'Falcons_predictedLoser': [0, 0],
        'Panthers_predictedLoser': [0, 0],
        'Saints_predictedLoser': [0, 0],
        'Buccaneers_predictedLoser': [0, 0],
        'Cardinals_predictedLoser': [0, 0],
        'Rams_predictedLoser': [0, 0],
        'Seahawks_predictedLoser': [0, 0],
        '49ers_predictedLoser': [0, 0],
        'Bills_day_Wed': [0, 0],
        'Dolphins_day_Wed': [0, 0],
        'Patriots_day_Wed': [0, 0],
        'Jets_day_Wed': [0, 0],
        'Bengals_day_Wed': [0, 0],
        'Browns_day_Wed': [0, 0],
        'Steelers_day_Wed': [0, 0],
        'Ravens_day_Wed': [0, 0],
        'Colts_day_Wed': [0, 0],
        'Texans_day_Wed': [0, 0],
        'Jaguars_day_Wed': [0, 0],
        'Titans_day_Wed': [0, 0],
        'Broncos_day_Wed': [0, 0],
        'Chiefs_day_Wed': [0, 0],
        'Raiders_day_Wed': [0, 0],
        'Chargers_day_Wed': [0, 0],
        'Cowboys_day_Wed': [0, 0],
        'Giants_day_Wed': [0, 0],
        'Eagles_day_Wed': [0, 0],
        'Washington_day_Wed': [0, 0],
        'Bears_day_Wed': [0, 0],
        'Lions_day_Wed': [0, 0],
        'Packers_day_Wed': [0, 0],
        'Vikings_day_Wed': [0, 0],
        'Falcons_day_Wed': [0, 0],
        'Panthers_day_Wed': [0, 0],
        'Saints_day_Wed': [0, 0],
        'Buccaneers_day_Wed': [0, 0],
        'Cardinals_day_Wed': [0, 0],
        'Rams_day_Wed': [0, 0],
        'Seahawks_day_Wed': [0, 0],
        '49ers_day_Wed': [0, 0],
        'Bills_day_Thu': [0, 0],
        'Dolphins_day_Thu': [0, 0],
        'Patriots_day_Thu': [0, 0],
        'Jets_day_Thu': [0, 0],
        'Bengals_day_Thu': [0, 0],
        'Browns_day_Thu': [0, 0],
        'Steelers_day_Thu': [0, 0],
        'Ravens_day_Thu': [0, 0],
        'Colts_day_Thu': [0, 0],
        'Texans_day_Thu': [0, 0],
        'Jaguars_day_Thu': [0, 0],
        'Titans_day_Thu': [0, 0],
        'Broncos_day_Thu': [0, 0],
        'Chiefs_day_Thu': [0, 0],
        'Raiders_day_Thu': [0, 0],
        'Chargers_day_Thu': [0, 0],
        'Cowboys_day_Thu': [0, 0],
        'Giants_day_Thu': [0, 0],
        'Eagles_day_Thu': [0, 0],
        'Washington_day_Thu': [0, 0],
        'Bears_day_Thu': [0, 0],
        'Lions_day_Thu': [0, 0],
        'Packers_day_Thu': [0, 0],
        'Vikings_day_Thu': [0, 0],
        'Falcons_day_Thu': [0, 0],
        'Panthers_day_Thu': [0, 0],
        'Saints_day_Thu': [0, 0],
        'Buccaneers_day_Thu': [0, 0],
        'Cardinals_day_Thu': [0, 0],
        'Rams_day_Thu': [0, 0],
        'Seahawks_day_Thu': [0, 0],
        '49ers_day_Thu': [0, 0],
        'Bills_day_Fri': [0, 0],
        'Dolphins_day_Fri': [0, 0],
        'Patriots_day_Fri': [0, 0],
        'Jets_day_Fri': [0, 0],
        'Bengals_day_Fri': [0, 0],
        'Browns_day_Fri': [0, 0],
        'Steelers_day_Fri': [0, 0],
        'Ravens_day_Fri': [0, 0],
        'Colts_day_Fri': [0, 0],
        'Texans_day_Fri': [0, 0],
        'Jaguars_day_Fri': [0, 0],
        'Titans_day_Fri': [0, 0],
        'Broncos_day_Fri': [0, 0],
        'Chiefs_day_Fri': [0, 0],
        'Raiders_day_Fri': [0, 0],
        'Chargers_day_Fri': [0, 0],
        'Cowboys_day_Fri': [0, 0],
        'Giants_day_Fri': [0, 0],
        'Eagles_day_Fri': [0, 0],
        'Washington_day_Fri': [0, 0],
        'Bears_day_Fri': [0, 0],
        'Lions_day_Fri': [0, 0],
        'Packers_day_Fri': [0, 0],
        'Vikings_day_Fri': [0, 0],
        'Falcons_day_Fri': [0, 0],
        'Panthers_day_Fri': [0, 0],
        'Saints_day_Fri': [0, 0],
        'Buccaneers_day_Fri': [0, 0],
        'Cardinals_day_Fri': [0, 0],
        'Rams_day_Fri': [0, 0],
        'Seahawks_day_Fri': [0, 0],
        '49ers_day_Fri': [0, 0],
        'Bills_day_Sat': [0, 0],
        'Dolphins_day_Sat': [0, 0],
        'Patriots_day_Sat': [0, 0],
        'Jets_day_Sat': [0, 0],
        'Bengals_day_Sat': [0, 0],
        'Browns_day_Sat': [0, 0],
        'Steelers_day_Sat': [0, 0],
        'Ravens_day_Sat': [0, 0],
        'Colts_day_Sat': [0, 0],
        'Texans_day_Sat': [0, 0],
        'Jaguars_day_Sat': [0, 0],
        'Titans_day_Sat': [0, 0],
        'Broncos_day_Sat': [0, 0],
        'Chiefs_day_Sat': [0, 0],
        'Raiders_day_Sat': [0, 0],
        'Chargers_day_Sat': [0, 0],
        'Cowboys_day_Sat': [0, 0],
        'Giants_day_Sat': [0, 0],
        'Eagles_day_Sat': [0, 0],
        'Washington_day_Sat': [0, 0],
        'Bears_day_Sat': [0, 0],
        'Lions_day_Sat': [0, 0],
        'Packers_day_Sat': [0, 0],
        'Vikings_day_Sat': [0, 0],
        'Falcons_day_Sat': [0, 0],
        'Panthers_day_Sat': [0, 0],
        'Saints_day_Sat': [0, 0],
        'Buccaneers_day_Sat': [0, 0],
        'Cardinals_day_Sat': [0, 0],
        'Rams_day_Sat': [0, 0],
        'Seahawks_day_Sat': [0, 0],
        '49ers_day_Sat': [0, 0],
        'Bills_day_Sun': [0, 0],
        'Dolphins_day_Sun': [0, 0],
        'Patriots_day_Sun': [0, 0],
        'Jets_day_Sun': [0, 0],
        'Bengals_day_Sun': [0, 0],
        'Browns_day_Sun': [0, 0],
        'Steelers_day_Sun': [0, 0],
        'Ravens_day_Sun': [0, 0],
        'Colts_day_Sun': [0, 0],
        'Texans_day_Sun': [0, 0],
        'Jaguars_day_Sun': [0, 0],
        'Titans_day_Sun': [0, 0],
        'Broncos_day_Sun': [0, 0],
        'Chiefs_day_Sun': [0, 0],
        'Raiders_day_Sun': [0, 0],
        'Chargers_day_Sun': [0, 0],
        'Cowboys_day_Sun': [0, 0],
        'Giants_day_Sun': [0, 0],
        'Eagles_day_Sun': [0, 0],
        'Washington_day_Sun': [0, 0],
        'Bears_day_Sun': [0, 0],
        'Lions_day_Sun': [0, 0],
        'Packers_day_Sun': [0, 0],
        'Vikings_day_Sun': [0, 0],
        'Falcons_day_Sun': [0, 0],
        'Panthers_day_Sun': [0, 0],
        'Saints_day_Sun': [0, 0],
        'Buccaneers_day_Sun': [0, 0],
        'Cardinals_day_Sun': [0, 0],
        'Rams_day_Sun': [0, 0],
        'Seahawks_day_Sun': [0, 0],
        '49ers_day_Sun': [0, 0],
        'Bills_day_Mon': [0, 0],
        'Dolphins_day_Mon': [0, 0],
        'Patriots_day_Mon': [0, 0],
        'Jets_day_Mon': [0, 0],
        'Bengals_day_Mon': [0, 0],
        'Browns_day_Mon': [0, 0],
        'Steelers_day_Mon': [0, 0],
        'Ravens_day_Mon': [0, 0],
        'Colts_day_Mon': [0, 0],
        'Texans_day_Mon': [0, 0],
        'Jaguars_day_Mon': [0, 0],
        'Titans_day_Mon': [0, 0],
        'Broncos_day_Mon': [0, 0],
        'Chiefs_day_Mon': [0, 0],
        'Raiders_day_Mon': [0, 0],
        'Chargers_day_Mon': [0, 0],
        'Cowboys_day_Mon': [0, 0],
        'Giants_day_Mon': [0, 0],
        'Eagles_day_Mon': [0, 0],
        'Washington_day_Mon': [0, 0],
        'Bears_day_Mon': [0, 0],
        'Lions_day_Mon': [0, 0],
        'Packers_day_Mon': [0, 0],
        'Vikings_day_Mon': [0, 0],
        'Falcons_day_Mon': [0, 0],
        'Panthers_day_Mon': [0, 0],
        'Saints_day_Mon': [0, 0],
        'Buccaneers_day_Mon': [0, 0],
        'Cardinals_day_Mon': [0, 0],
        'Rams_day_Mon': [0, 0],
        'Seahawks_day_Mon': [0, 0],
        '49ers_day_Mon': [0, 0],
        'Bills_day_Tue': [0, 0],
        'Dolphins_day_Tue': [0, 0],
        'Patriots_day_Tue': [0, 0],
        'Jets_day_Tue': [0, 0],
        'Bengals_day_Tue': [0, 0],
        'Browns_day_Tue': [0, 0],
        'Steelers_day_Tue': [0, 0],
        'Ravens_day_Tue': [0, 0],
        'Colts_day_Tue': [0, 0],
        'Texans_day_Tue': [0, 0],
        'Jaguars_day_Tue': [0, 0],
        'Titans_day_Tue': [0, 0],
        'Broncos_day_Tue': [0, 0],
        'Chiefs_day_Tue': [0, 0],
        'Raiders_day_Tue': [0, 0],
        'Chargers_day_Tue': [0, 0],
        'Cowboys_day_Tue': [0, 0],
        'Giants_day_Tue': [0, 0],
        'Eagles_day_Tue': [0, 0],
        'Washington_day_Tue': [0, 0],
        'Bears_day_Tue': [0, 0],
        'Lions_day_Tue': [0, 0],
        'Packers_day_Tue': [0, 0],
        'Vikings_day_Tue': [0, 0],
        'Falcons_day_Tue': [0, 0],
        'Panthers_day_Tue': [0, 0],
        'Saints_day_Tue': [0, 0],
        'Buccaneers_day_Tue': [0, 0],
        'Cardinals_day_Tue': [0, 0],
        'Rams_day_Tue': [0, 0],
        'Seahawks_day_Tue': [0, 0],
        '49ers_day_Tue': [0, 0],
    }
    week = 0
    year = 0



    for line in theFile:
        data = line.rstrip().split('_')
        if len(data) != 1:
            awayTeam, homeTeam, timeCode, dayCode, temp, weather, wind, predWinner, predLoser, outcome = data

            awayTeamName = f'{awayTeam}_away'
            homeTeamName = f'{homeTeam}_home'
            predictedWinner = f'{predWinner}_predictedWinner'
            predictedLoser = f'{predLoser}_predictedLoser'
            awayDivision = teamInfo[awayTeam]
            awayConf = awayDivision.split(' ')[0]
            homeDivision = teamInfo[homeTeam]
            homeConf = homeDivision.split(' ')[0]
            awayTeamDay = f'{awayTeam}_day_{getDayFromCode(dayCode)}'
            homeTeamDay = f'{homeTeam}_day_{getDayFromCode(dayCode)}'

            if outcome == '1':
                results[awayTeam] = [results[awayTeam][0] + 100, results[awayTeam][1] + 1]
                results[awayTeamName] = [results[awayTeamName][0] + 100, results[awayTeamName][1] + 1]

                results[homeTeam] = [results[homeTeam][0] + 100, results[homeTeam][1] + 1]
                results[homeTeamName] = [results[homeTeamName][0] + 100, results[homeTeamName][1] + 1]

                results[predictedWinner] = [results[predictedWinner][0] + 100, results[predictedWinner][1] + 1]
                results[predictedLoser] = [results[predictedLoser][0] + 100, results[predictedLoser][1] + 1]

                results[awayConf] = [results[awayConf][0] + 100, results[awayConf][1] + 1]
                results[awayDivision] = [results[awayDivision][0] + 100, results[awayDivision][1] + 1]

                results[homeConf] = [results[homeConf][0] + 100, results[homeConf][1] + 1]
                results[homeDivision] = [results[homeDivision][0] + 100, results[homeDivision][1] + 1]

                results[awayTeamDay] = [results[awayTeamDay][0] + 100, results[awayTeamDay][1] + 1]
                results[homeTeamDay] = [results[homeTeamDay][0] + 100, results[homeTeamDay][1] + 1]


                results[f'{year} Week {week}'] = [results[f'{year} Week {week}'][0] + 100, results[f'{year} Week {week}'][1] + 1]

            
            else:
                results[awayTeam] = [results[awayTeam][0] + 0, results[awayTeam][1] + 1]
                results[awayTeamName] = [results[awayTeamName][0] + 0, results[awayTeamName][1] + 1]

                results[homeTeam] = [results[homeTeam][0] + 0, results[homeTeam][1] + 1]
                results[homeTeamName] = [results[homeTeamName][0] + 0, results[homeTeamName][1] + 1]

                results[predictedWinner] = [results[predictedWinner][0] + 0, results[predictedWinner][1] + 1]
                results[predictedLoser] = [results[predictedLoser][0] + 0, results[predictedLoser][1] + 1]

                results[awayConf] = [results[awayConf][0] + 0, results[awayConf][1] + 1]
                results[awayDivision] = [results[awayDivision][0] + 0, results[awayDivision][1] + 1]

                results[homeConf] = [results[homeConf][0] + 0, results[homeConf][1] + 1]
                results[homeDivision] = [results[homeDivision][0] + 0, results[homeDivision][1] + 1]

                results[awayTeamDay] = [results[awayTeamDay][0] + 0, results[awayTeamDay][1] + 1]
                results[homeTeamDay] = [results[homeTeamDay][0] + 0, results[homeTeamDay][1] + 1]

                results[f'{year} Week {week}'] = [results[f'{year} Week {week}'][0] + 0, results[f'{year} Week {week}'][1] + 1]
                    
        else:
            data = data[0]
            if data == '2022':
                year = 2022
            elif data == '2023':
                year = 2023
            elif data == '2024':
                year = 2024
            else:
                week = data
                results[f'{year} Week {week}'] = [0,0]
        
    finalResults = {}
    for team in results:
        if results[team][1] == 0:
            finalResults[team] = -1
        else:    
            finalResults[team] = round(results[team][0]/results[team][1],2)



    filenameWrite = '../frontend/src/nflPages/percentages.json'
    with open(filenameWrite, 'w') as outfile:
        json.dump(finalResults, outfile)

    theFile.close()
    print('All percentages have been updated!')


def updateFavored():
    mydb = mysql.connector.connect(
        host='127.0.0.1',
        user='davidcarney',
        password='Sinorrabb1t',
        database='NFL'
    )
    mycursor = mydb.cursor()

    insertData = f"UPDATE productionNFL SET favored = 1 WHERE favored is NULL and spread LIKE '%-%'"
    mycursor.execute(insertData)
    mydb.commit()

    insertData = f"UPDATE productionNFL SET favored = 0 WHERE favored is NULL and spread LIKE '%+%'"
    mycursor.execute(insertData)
    mydb.commit()

    insertData = f"UPDATE productionNFL SET favored = 0 WHERE favored is NULL and spread = 'pk'"
    mycursor.execute(insertData)
    mydb.commit()

    insertData = f"UPDATE productionNFL SET spread = 0 WHERE spread = 'pk'"
    mycursor.execute(insertData)
    mydb.commit()

    print('Favored Column has been updated!')








#Predict winner loser and their scores
class getPredictions:
    def __init__(self, week, year):
        self.week = week
        self.year = year
                                
    def teamService(self, teamDataList):
        columnName,day,at,oppTeamNumber,teamName,time,channel,temp,weather,wind,spread,total = teamDataList

        mydb = mysql.connector.connect(
            host='127.0.0.1',
            user='davidcarney',
            password='Sinorrabb1t',
            database='NFL'
            )
        mycursor = mydb.cursor()
        mycursor.execute(f"SELECT * FROM productionNFL WHERE Team = '{teamName}' and Year > 2021 and WinLoss is not NULL")
        teamData = mycursor.fetchall()
        teamDF = pd.DataFrame(teamData, columns = ALL_COLUMNS)
        teamDF = teamDF.drop(columns=['DateTime','spreadOdds','totalOdds','ML','gameLine','minMaxLine','totalScoreLine','minMaxTotalScoreLine','spreadCalculated','totalCalculated'])
 
        upcomingWeekData = [[self.year, self.week, day, at, oppTeamNumber, time, channel, temp, weather, wind, spread, total]]
        upcomingWeekColumns = ['Year','Week','Day', 'At', 'OppTeam', 'Time', 'Channel', 'Temp', 'Weather', 'Wind', 'spread', 'total']
        upcomingWeekDF = pd.DataFrame(upcomingWeekData, columns = upcomingWeekColumns)

        model = theBot(teamDF, upcomingWeekDF, columnName)
        model.adjustDF()

        #Run theBot code 3 times to keep adding to existing upcoming week DF
        predictions1 = model.useCode()
        predictions2 = model.useCode()
        predictions3 = model.useCode()

        #Each prediction is a list of [Prediction result, Prediction probability]
        return predictions1,predictions2,predictions3

    def doit(self):
        mydb = mysql.connector.connect(
            host='127.0.0.1',
            user='davidcarney',
            password='Sinorrabb1t',
            database='NFL'
        )
        mycursor = mydb.cursor()

        mycursor.execute(f"SELECT * FROM productionNFL WHERE WinLoss is NULL")
        upcomingGamesData = mycursor.fetchall()
        upcomingGames = pd.DataFrame(upcomingGamesData, columns = ALL_COLUMNS)

        resultFilename = '../frontend/src/nflPages/results.js'
        percentageFilename = './percentages.txt'

        resultsFile = open(resultFilename, 'w')
        percentFile = open(percentageFilename, 'a')
        resultsFile.write('export const weeklyResults = [\n')
        percentFile.write(f'{self.week}\n')

        matchUpCounter = True
        homeTeamID = -1
        homeTeamName = ''
        awayTeamName = -1
        awayTeamName = ''
        matchUpHolder = {}
        for matchUp in upcomingGames.iterrows():
            matchUp = matchUp[1]
            id = matchUp['id']
            week = matchUp['Week']
            day = matchUp['Day']
            at = matchUp['At']
            oppTeam = matchUp['OppTeam']
            year = matchUp['Year']
            team = matchUp['Team']
            homeTeam = matchUp['HomeTeam']
            time = matchUp['Time']
            channel = matchUp['Channel']
            temp = matchUp['Temp']
            weather = matchUp['Weather']
            wind = matchUp['Wind']
            spread = matchUp['spread']
            total = matchUp['total']


            if matchUpCounter:
                if at == 1:
                    homeTeamID = id
                    homeTeamName = team
                    matchUpHolder['HomeSpread'] = ['spreadCovered',day,at,oppTeam,team,time,channel,temp,weather,wind,spread,total]
                    matchUpHolder['HomeTotal'] = ['totalCovered',day,at,oppTeam,team,time,channel,temp,weather,wind,spread,total]
                else:
                    awayTeamID = id
                    awayTeamName = team
                    matchUpHolder['AwaySpread'] = ['spreadCovered',day,at,oppTeam,team,time,channel,temp,weather,wind,spread,total]
                    matchUpHolder['AwayTotal'] = ['totalCovered',day,at,oppTeam,team,time,channel,temp,weather,wind,spread,total]

                matchUpCounter = False

            else:
                if at == 1:
                    homeTeamID = id
                    homeTeamName = team
                    matchUpHolder['HomeSpread'] = ['spreadCovered',day,at,oppTeam,team,time,channel,temp,weather,wind,spread,total]
                    matchUpHolder['HomeTotal'] = ['totalCovered',day,at,oppTeam,team,time,channel,temp,weather,wind,spread,total]

                else:
                    awayTeamID = id
                    awayTeamName = team
                    matchUpHolder['AwaySpread'] = ['spreadCovered',day,at,oppTeam,team,time,channel,temp,weather,wind,spread,total]
                    matchUpHolder['AwayTotal'] = ['totalCovered',day,at,oppTeam,team,time,channel,temp,weather,wind,spread,total]

                #Spread
                homeSpreadOutcome = 1
                awaySpreadOutcome = 1

                for i in range(3):
                    homePredictions1WL, homePredictions2WL, homePredictions3WL = self.teamService(matchUpHolder['HomeSpread'])
                    awayPredictions1WL, awayPredictions2WL, awayPredictions3WL = self.teamService(matchUpHolder['AwaySpread'])
                    
                    homeSpreadOutcome = homeSpreadOutcome + (homePredictions1WL[0] * convertProbZero(homePredictions1WL[1])) + (homePredictions2WL[0] * convertProbZero(homePredictions2WL[1])) + (homePredictions3WL[0] * convertProbZero(homePredictions3WL[1]))
                    awaySpreadOutcome = awaySpreadOutcome + (awayPredictions1WL[0] * convertProbZero(awayPredictions1WL[1])) + (awayPredictions2WL[0] * convertProbZero(awayPredictions2WL[1])) + (awayPredictions3WL[0] * convertProbZero(awayPredictions3WL[1]))
                
                if homeSpreadOutcome > awaySpreadOutcome:
                    resultsFile.write("'")         
                    resultsFile.write(homeTeamName)
                    resultsFile.write(',Covers Spread,')
                    resultsFile.write(f'{getDayFromCode(str(day))}')
                    resultsFile.write("',")
                    resultsFile.write('\n')

                    percentFile.write(f'{homeTeamName},cover Spread,{awayTeamName},not cover Spread,\n')

                    mycursor.execute(f'UPDATE productionNFL SET spreadCalculated = 1 WHERE id = {homeTeamID}')
                    mydb.commit()
                    mycursor.execute(f'UPDATE productionNFL SET spreadCalculated = 0 WHERE id = {awayTeamID}')
                    mydb.commit()
            

                else:
                    resultsFile.write("'")
                    resultsFile.write(awayTeamName)
                    resultsFile.write(',Covers Spread,')
                    resultsFile.write(f'{getDayFromCode(str(day))}')
                    resultsFile.write("',")
                    resultsFile.write('\n')

                    percentFile.write(f'{awayTeamName},cover Spread,{homeTeamName},not cover Spread,\n')

                    mycursor.execute(f'UPDATE productionNFL SET spreadCalculated = 1 WHERE id = {awayTeamID}')
                    mydb.commit()
                    mycursor.execute(f'UPDATE productionNFL SET spreadCalculated = 0 WHERE id = {homeTeamID}')
                    mydb.commit()
                
                
                #OverUnder
                homeOverUnderOutcome = 0
                awayOverUnderOutcome = 0

                for i in range(3):
                    homePredictions1WL, homePredictions2WL, homePredictions3WL = self.teamService(matchUpHolder['HomeTotal'])
                    awayPredictions1WL, awayPredictions2WL, awayPredictions3WL = self.teamService(matchUpHolder['AwayTotal'])
                    
                    homeOverUnderOutcome = homeOverUnderOutcome + homePredictions1WL[0] + homePredictions2WL[0] + homePredictions3WL[0]
                    awayOverUnderOutcome = awayOverUnderOutcome + awayPredictions1WL[0] + awayPredictions2WL[0] + awayPredictions3WL[0]

                if homeOverUnderOutcome + awayOverUnderOutcome > 9:
                    resultsFile.write("'")         
                    resultsFile.write(homeTeamName)
                    resultsFile.write(',Over,')
                    resultsFile.write(f'{getDayFromCode(str(day))}')
                    resultsFile.write("',")
                    resultsFile.write('\n')

                    percentFile.write(f'{homeTeamName},cover OverUnder,{awayTeamName},cover OverUnder,\n')

                    mycursor.execute(f'UPDATE productionNFL SET totalCalculated = 1 WHERE id = {homeTeamID}')
                    mydb.commit()
                    mycursor.execute(f'UPDATE productionNFL SET totalCalculated = 1 WHERE id = {awayTeamID}')
                    mydb.commit()
            

                else:
                    resultsFile.write("'")
                    resultsFile.write(awayTeamName)
                    resultsFile.write(',Under,')
                    resultsFile.write(f'{getDayFromCode(str(day))}')
                    resultsFile.write("',")
                    resultsFile.write('\n')

                    percentFile.write(f'{awayTeamName},not cover OverUnder,{homeTeamName},not cover OverUnder,\n')

                    mycursor.execute(f'UPDATE productionNFL SET totalCalculated = 0 WHERE id = {awayTeamID}')
                    mydb.commit()
                    mycursor.execute(f'UPDATE productionNFL SET totalCalculated = 0 WHERE id = {homeTeamID}')
                    mydb.commit()
                
                
                matchUpHolder = {}    
                homeTeamID = -1
                homeTeamName = ''
                awayTeamName = -1
                awayTeamName = ''
                matchUpCounter = True

                

        resultsFile.write('];')
        resultsFile.close()

        print('All matchups have been predicted!')




# def getParlays():
#     mydb = mysql.connector.connect(
#         host='127.0.0.1',
#         user='davidcarney',
#         password='Sinorrabb1t',
#         database='NFL'
#     )
#     mycursor = mydb.cursor()

#     insertData = f"UPDATE productionNFL SET favored = 1 WHERE favored is NULL and spread LIKE '%-%'"
#     mycursor.execute(insertData)
#     mydb.commit()








def updateTeamData(week):
    teamDataFilename = 'teamData.txt'
    percentFilename = 'percentages.txt'
    teamDataHolderFilename = 'teamDataHolder.txt'
    teamDataFile = open(teamDataFilename, 'a')
    percentFile = open(percentFilename, 'r')
    teamDataHolderFile = open(teamDataHolderFilename, 'r')
    passedYear = False
    passedWeek = False
    predictions = []

    for line in percentFile:
        line = line.split(',')
        if len(line) == 1:
            weekOrYear = int(line[0].rstrip())
            if weekOrYear == 2024:
                passedYear = True
            if (weekOrYear == week) and (passedYear == True):
                passedWeek = True
        elif (passedWeek == True) and (passedYear == True):
            predictions.append([line[0],line[1]])
    teamDataFile.write(f'{week}\n')
    for (teamDataLine, predLine) in zip(teamDataHolderFile, predictions):
        teamDataFile.write(f'{teamDataLine.rstrip()}_{predLine[0]}_{predLine[1]}_\n')




def updateFrontend(week):
    upcomingWeekFrontendFilename = '../frontend/src/nflPages/upcomingWeekData.js'
    upcomingWeekFrontendFile = open(upcomingWeekFrontendFilename, 'w')
    upcomingWeekFrontendFile.write('export const upcomingWeekData = [\n')
    upcomingWeekFrontendFile.write(f"'{week}',\n")

    mydb = mysql.connector.connect(
        host='127.0.0.1',
        user='davidcarney',
        password='Sinorrabb1t',
        database='NFL'
        )
    mycursor = mydb.cursor()

    mycursor.execute("SELECT DateTime, At, OppTeam, Team, spread, total, spreadCalculated, totalCalculated FROM productionNFL WHERE winLoss is NULL")
    columns = ['DateTime', 'At', 'OppTeam', 'Team', 'spread', 'total', 'spreadCalculated', 'totalCalculated']
    teamData = mycursor.fetchall()
    nextGames = pd.DataFrame(teamData, columns = columns)

    matchUps = []
    for game in nextGames.iterrows():
        game = game[1]
        dateTime, At, OppTeam, Team, spread, total, spreadCalculated, totalCalculated = game
        teamName = getTeamName(getTeamFromSmallName(Team))
        oppTeamName = getTeamName(OppTeam)

        dateTimeStr = dateTime.split(' ')[0]
        dateTimeObj = datetime.strptime(dateTimeStr,'%m/%d/%y')
        weekDay = dateTimeObj.strftime('%A')
        abbrevMonth = dateTimeObj.strftime('%b')
        actualDay = dateTimeObj.strftime('%d')
        actualTime = ' '.join(dateTime.split(' ')[1:])

        if teamName not in matchUps:
            homeTeam = ''
            awayTeam = ''

            if At == 1:
                homeTeam = teamName
                awayTeam = oppTeamName

            else:
                homeTeam = oppTeamName
                awayTeam = teamName
                
            upcomingWeekFrontendFile.write("'")
            upcomingWeekFrontendFile.write(f'{weekDay}, {abbrevMonth} {actualDay}')
            upcomingWeekFrontendFile.write('_')
            upcomingWeekFrontendFile.write(str(actualTime))
            upcomingWeekFrontendFile.write('_')
            upcomingWeekFrontendFile.write(awayTeam)
            upcomingWeekFrontendFile.write('_')
            upcomingWeekFrontendFile.write(homeTeam)
            upcomingWeekFrontendFile.write('_')
            upcomingWeekFrontendFile.write(teamName)
            upcomingWeekFrontendFile.write('_')
            upcomingWeekFrontendFile.write(spread)
            upcomingWeekFrontendFile.write('_')
            upcomingWeekFrontendFile.write(str(spreadCalculated))
            upcomingWeekFrontendFile.write('_')
            upcomingWeekFrontendFile.write(total)
            upcomingWeekFrontendFile.write('_')
            upcomingWeekFrontendFile.write(str(totalCalculated))
            upcomingWeekFrontendFile.write("',")
            upcomingWeekFrontendFile.write('\n')


            matchUps.append(teamName)
            matchUps.append(oppTeamName)


    upcomingWeekFrontendFile.write('];')
    upcomingWeekFrontendFile.close()

    print('Fontend has been updated!')


def updatePercentagesFrontend():
    percentFrontendFilename = '../frontend/src/nflPages/percentages.json'
    percentFrontendFile = open(percentFrontendFilename, 'w')
    percentFrontendFile.write('{')

    mydb = mysql.connector.connect(
        host='127.0.0.1',
        user='davidcarney',
        password='Sinorrabb1t',
        database='NFL'
    )
    mycursor = mydb.cursor()

    mycursor.execute("SELECT DateTime, Week, Day, At, OppTeam, Team, spread, total, spreadCalculated, totalCalculated, spreadCovered, totalCovered FROM productionNFL WHERE spreadCalculated is NOT NULL and spreadCovered is NOT NULL")
    columns = ['DateTime', 'Week', 'Day', 'At', 'OppTeam', 'Team', 'spread', 'total', 'spreadCalculated', 'totalCalculated', 'spreadCovered', 'totalCovered']
    teamData = mycursor.fetchall()
    percentages = pd.DataFrame(teamData, columns = columns)

    percentData = {}
    for team in ALL_TEAMS:
        team = getTeamName(getTeamFromSmallName(team))
        percentData[f'{team}_spread'] = [0,0]
        percentData[f'{team}_total'] = [0,0]
        percentData[f'{team}_parlay'] = [0,0]

        percentData[f'{team}_home_spread'] = [0,0]
        percentData[f'{team}_away_spread'] = [0,0]
        percentData[f'{team}_home_total'] = [0,0]
        percentData[f'{team}_away_total'] = [0,0]
        percentData[f'{team}_home_parlay'] = [0,0]
        percentData[f'{team}_away_parlay'] = [0,0]

        percentData[f'{team}_Mon_spread'] = [0,0]
        percentData[f'{team}_Tue_spread'] = [0,0]
        percentData[f'{team}_Wed_spread'] = [0,0]
        percentData[f'{team}_Thu_spread'] = [0,0]
        percentData[f'{team}_Fri_spread'] = [0,0]
        percentData[f'{team}_Sat_spread'] = [0,0]
        percentData[f'{team}_Sun_spread'] = [0,0]
        percentData[f'{team}_Mon_total'] = [0,0]
        percentData[f'{team}_Tue_total'] = [0,0]
        percentData[f'{team}_Wed_total'] = [0,0]
        percentData[f'{team}_Thu_total'] = [0,0]
        percentData[f'{team}_Fri_total'] = [0,0]
        percentData[f'{team}_Sat_total'] = [0,0]
        percentData[f'{team}_Sun_total'] = [0,0]
        percentData[f'{team}_Mon_parlay'] = [0,0]
        percentData[f'{team}_Tue_parlay'] = [0,0]
        percentData[f'{team}_Wed_parlay'] = [0,0]
        percentData[f'{team}_Thu_parlay'] = [0,0]
        percentData[f'{team}_Fri_parlay'] = [0,0]
        percentData[f'{team}_Sat_parlay'] = [0,0]
        percentData[f'{team}_Sun_parlay'] = [0,0]

        percentData[f'{team}_8_spread'] = [0,0]
        percentData[f'{team}_9_spread'] = [0,0]
        percentData[f'{team}_10_spread'] = [0,0]
        percentData[f'{team}_11_spread'] = [0,0]
        percentData[f'{team}_12_spread'] = [0,0]
        percentData[f'{team}_13_spread'] = [0,0]
        percentData[f'{team}_14_spread'] = [0,0]
        percentData[f'{team}_15_spread'] = [0,0]
        percentData[f'{team}_16_spread'] = [0,0]
        percentData[f'{team}_17_spread'] = [0,0]
        percentData[f'{team}_18_spread'] = [0,0]
        percentData[f'{team}_19_spread'] = [0,0]
        percentData[f'{team}_20_spread'] = [0,0]
        percentData[f'{team}_21_spread'] = [0,0]
        percentData[f'{team}_22_spread'] = [0,0]
        percentData[f'{team}_23_spread'] = [0,0]
        percentData[f'{team}_24_spread'] = [0,0]
        percentData[f'{team}_8_total'] = [0,0]
        percentData[f'{team}_9_total'] = [0,0]
        percentData[f'{team}_10_total'] = [0,0]
        percentData[f'{team}_11_total'] = [0,0]
        percentData[f'{team}_12_total'] = [0,0]
        percentData[f'{team}_13_total'] = [0,0]
        percentData[f'{team}_14_total'] = [0,0]
        percentData[f'{team}_15_total'] = [0,0]
        percentData[f'{team}_16_total'] = [0,0]
        percentData[f'{team}_17_total'] = [0,0]
        percentData[f'{team}_18_total'] = [0,0]
        percentData[f'{team}_19_total'] = [0,0]
        percentData[f'{team}_20_total'] = [0,0]
        percentData[f'{team}_21_total'] = [0,0]
        percentData[f'{team}_22_total'] = [0,0]
        percentData[f'{team}_23_total'] = [0,0]
        percentData[f'{team}_24_total'] = [0,0]
        percentData[f'{team}_8_parlay'] = [0,0]
        percentData[f'{team}_9_parlay'] = [0,0]
        percentData[f'{team}_10_parlay'] = [0,0]
        percentData[f'{team}_11_parlay'] = [0,0]
        percentData[f'{team}_12_parlay'] = [0,0]
        percentData[f'{team}_13_parlay'] = [0,0]
        percentData[f'{team}_14_parlay'] = [0,0]
        percentData[f'{team}_15_parlay'] = [0,0]
        percentData[f'{team}_16_parlay'] = [0,0]
        percentData[f'{team}_17_parlay'] = [0,0]
        percentData[f'{team}_18_parlay'] = [0,0]
        percentData[f'{team}_19_parlay'] = [0,0]
        percentData[f'{team}_20_parlay'] = [0,0]
        percentData[f'{team}_21_parlay'] = [0,0]
        percentData[f'{team}_22_parlay'] = [0,0]
        percentData[f'{team}_23_parlay'] = [0,0]
        percentData[f'{team}_24_parlay'] = [0,0]


    for week in ALL_WEEKS:
        percentData[f'Week_{week}_spread'] = [0,0]
        percentData[f'Week_{week}_total'] = [0,0]
        percentData[f'Week_{week}_parlay'] = [0,0]

    percentData['home_spread'] = [0,0]
    percentData['away_spread'] = [0,0]
    percentData['home_total'] = [0,0]
    percentData['away_total'] = [0,0]
    percentData['home_parlay'] = [0,0]
    percentData['away_parlay'] = [0,0]
    percentData['overall_spread'] = [0,0]
    percentData['overall_total'] = [0,0]
    percentData['overall_parlay'] = [0,0]

    percentData['overall_Mon_spread'] = [0,0]
    percentData['overall_Tue_spread'] = [0,0]
    percentData['overall_Wed_spread'] = [0,0]
    percentData['overall_Thu_spread'] = [0,0]
    percentData['overall_Fri_spread'] = [0,0]
    percentData['overall_Sat_spread'] = [0,0]
    percentData['overall_Sun_spread'] = [0,0]
    percentData['overall_Mon_total'] = [0,0]
    percentData['overall_Tue_total'] = [0,0]
    percentData['overall_Wed_total'] = [0,0]
    percentData['overall_Thu_total'] = [0,0]
    percentData['overall_Fri_total'] = [0,0]
    percentData['overall_Sat_total'] = [0,0]
    percentData['overall_Sun_total'] = [0,0]
    percentData['overall_Mon_parlay'] = [0,0]
    percentData['overall_Tue_parlay'] = [0,0]
    percentData['overall_Wed_parlay'] = [0,0]
    percentData['overall_Thu_parlay'] = [0,0]
    percentData['overall_Fri_parlay'] = [0,0]
    percentData['overall_Sat_parlay'] = [0,0]
    percentData['overall_Sun_parlay'] = [0,0]

    percentData['overall_8_spread'] = [0,0]
    percentData['overall_9_spread'] = [0,0]
    percentData['overall_10_spread'] = [0,0]
    percentData['overall_11_spread'] = [0,0]
    percentData['overall_12_spread'] = [0,0]
    percentData['overall_13_spread'] = [0,0]
    percentData['overall_14_spread'] = [0,0]
    percentData['overall_15_spread'] = [0,0]
    percentData['overall_16_spread'] = [0,0]
    percentData['overall_17_spread'] = [0,0]
    percentData['overall_18_spread'] = [0,0]
    percentData['overall_19_spread'] = [0,0]
    percentData['overall_20_spread'] = [0,0]
    percentData['overall_21_spread'] = [0,0]
    percentData['overall_22_spread'] = [0,0]
    percentData['overall_23_spread'] = [0,0]
    percentData['overall_24_spread'] = [0,0]
    percentData['overall_8_total'] = [0,0]
    percentData['overall_9_total'] = [0,0]
    percentData['overall_10_total'] = [0,0]
    percentData['overall_11_total'] = [0,0]
    percentData['overall_12_total'] = [0,0]
    percentData['overall_13_total'] = [0,0]
    percentData['overall_14_total'] = [0,0]
    percentData['overall_15_total'] = [0,0]
    percentData['overall_16_total'] = [0,0]
    percentData['overall_17_total'] = [0,0]
    percentData['overall_18_total'] = [0,0]
    percentData['overall_19_total'] = [0,0]
    percentData['overall_20_total'] = [0,0]
    percentData['overall_21_total'] = [0,0]
    percentData['overall_22_total'] = [0,0]
    percentData['overall_23_total'] = [0,0]
    percentData['overall_24_total'] = [0,0]
    percentData['overall_8_parlay'] = [0,0]
    percentData['overall_9_parlay'] = [0,0]
    percentData['overall_10_parlay'] = [0,0]
    percentData['overall_11_parlay'] = [0,0]
    percentData['overall_12_parlay'] = [0,0]
    percentData['overall_13_parlay'] = [0,0]
    percentData['overall_14_parlay'] = [0,0]
    percentData['overall_15_parlay'] = [0,0]
    percentData['overall_16_parlay'] = [0,0]
    percentData['overall_17_parlay'] = [0,0]
    percentData['overall_18_parlay'] = [0,0]
    percentData['overall_19_parlay'] = [0,0]
    percentData['overall_20_parlay'] = [0,0]
    percentData['overall_21_parlay'] = [0,0]
    percentData['overall_22_parlay'] = [0,0]
    percentData['overall_23_parlay'] = [0,0]
    percentData['overall_24_parlay'] = [0,0]


    for stat in percentages.iterrows():
        stat = stat[1]
        dateTime, week, day, at, oppTeam, team, spread, total, spreadCalculated, totalCalculated, spreadCovered, totalCovered = stat
        team = getTeamName(getTeamFromSmallName(team))
        day = str(day)

        updatedTime = datetime.strptime(' '.join(dateTime.split(' ')[1:3]), '%I:%M %p')
        updatedHour = int(updatedTime.strftime('%H:%M').split(':')[0])

        teamSpread = f'{team}_spread'
        teamTotal = f'{team}_total'
        teamParlay = f'{team}_parlay'
        teamDaySpread = f'{team}_{getDayFromCode(day)}_spread'
        teamDayTotal = f'{team}_{getDayFromCode(day)}_total'
        teamDayParlay = f'{team}_{getDayFromCode(day)}_parlay'
        teamTimeSpread = f'{team}_{updatedHour}_spread'
        teamTimeTotal = f'{team}_{updatedHour}_total'
        teamTimeParlay = f'{team}_{updatedHour}_parlay'

        teamHomeSpread = f'{team}_home_spread'
        teamHomeTotal = f'{team}_home_total'
        teamHomeParlay = f'{team}_home_parlay'
        teamAwaySpread = f'{team}_away_spread'
        teamAwayTotal = f'{team}_away_total'
        teamAwayParlay = f'{team}_away_parlay'

        homeSpread = 'home_spread'
        homeTotal = 'home_total'
        homeParlay = 'home_parlay'
        awaySpread = 'away_spread'
        awayTotal = 'away_total'
        awayParlay = 'away_parlay'

        weekSpread = f'Week_{week}_spread'
        weekTotal = f'Week_{week}_total'
        weekParlay = f'Week_{week}_parlay'

        overallSpread = 'overall_spread'
        overallTotal = 'overall_total'
        overallParlay = 'overall_parlay'
        overallDaySpread = f'overall_{getDayFromCode(day)}_spread'
        overallDayTotal = f'overall_{getDayFromCode(day)}_total'
        overallDayParlay = f'overall_{getDayFromCode(day)}_parlay'
        overallTimeSpread = f'overall_{updatedHour}_spread'
        overallTimeTotal = f'overall_{updatedHour}_total'
        overallTimeParlay = f'overall_{updatedHour}_parlay'

        if spreadCalculated == spreadCovered:
            percentData[teamSpread] = [percentData[teamSpread][0] + 100, percentData[teamSpread][1] + 1]
            percentData[teamDaySpread] = [percentData[teamDaySpread][0] + 100, percentData[teamDaySpread][1] + 1]
            percentData[teamTimeSpread] = [percentData[teamTimeSpread][0] + 100, percentData[teamTimeSpread][1] + 1]
            percentData[weekSpread] = [percentData[weekSpread][0] + 100, percentData[weekSpread][1] + 1]
            percentData[overallSpread] = [percentData[overallSpread][0] + 100, percentData[overallSpread][1] + 1]
            percentData[overallDaySpread] = [percentData[overallDaySpread][0] + 100, percentData[overallDaySpread][1] + 1]
            percentData[overallTimeSpread] = [percentData[overallTimeSpread][0] + 100, percentData[overallTimeSpread][1] + 1]

            if at:
                percentData[teamHomeSpread] = [percentData[teamHomeSpread][0] + 100, percentData[teamHomeSpread][1] + 1]
                percentData[homeSpread] = [percentData[homeSpread][0] + 100, percentData[homeSpread][1] + 1]
            else:
                percentData[teamAwaySpread] = [percentData[teamAwaySpread][0] + 100, percentData[teamAwaySpread][1] + 1]
                percentData[awaySpread] = [percentData[awaySpread][0] + 100, percentData[awaySpread][1] + 1]

        else:
            percentData[teamSpread] = [percentData[teamSpread][0], percentData[teamSpread][1] + 1]
            percentData[teamDaySpread] = [percentData[teamDaySpread][0], percentData[teamDaySpread][1] + 1]
            percentData[teamTimeSpread] = [percentData[teamTimeSpread][0], percentData[teamTimeSpread][1] + 1]            
            percentData[weekSpread] = [percentData[weekSpread][0], percentData[weekSpread][1] + 1]
            percentData[overallSpread] = [percentData[overallSpread][0], percentData[overallSpread][1] + 1]
            percentData[overallDaySpread] = [percentData[overallDaySpread][0], percentData[overallDaySpread][1] + 1]
            percentData[overallTimeSpread] = [percentData[overallTimeSpread][0], percentData[overallTimeSpread][1] + 1]

            if at:
                percentData[teamHomeSpread] = [percentData[teamHomeSpread][0], percentData[teamHomeSpread][1] + 1]
                percentData[homeSpread] = [percentData[homeSpread][0], percentData[homeSpread][1] + 1]
            else:
                percentData[teamAwaySpread] = [percentData[teamAwaySpread][0], percentData[teamAwaySpread][1] + 1]
                percentData[awaySpread] = [percentData[awaySpread][0], percentData[awaySpread][1] + 1]

        
        if totalCalculated == totalCovered:
            percentData[teamTotal] = [percentData[teamTotal][0] + 100, percentData[teamTotal][1] + 1]
            percentData[teamDayTotal] = [percentData[teamDayTotal][0] + 100, percentData[teamDayTotal][1] + 1]            
            percentData[teamTimeTotal] = [percentData[teamTimeTotal][0] + 100, percentData[teamTimeTotal][1] + 1]
            percentData[weekTotal] = [percentData[weekTotal][0] + 100, percentData[weekTotal][1] + 1]
            percentData[overallTotal] = [percentData[overallTotal][0] + 100, percentData[overallTotal][1] + 1]
            percentData[overallDayTotal] = [percentData[overallDayTotal][0] + 100, percentData[overallDayTotal][1] + 1]
            percentData[overallTimeTotal] = [percentData[overallTimeTotal][0] + 100, percentData[overallTimeTotal][1] + 1]

            if at:
                percentData[teamHomeTotal] = [percentData[teamHomeTotal][0] + 100, percentData[teamHomeTotal][1] + 1]
                percentData[homeTotal] = [percentData[homeTotal][0] + 100, percentData[homeTotal][1] + 1]
            else:
                percentData[teamAwayTotal] = [percentData[teamAwayTotal][0] + 100, percentData[teamAwayTotal][1] + 1]
                percentData[awayTotal] = [percentData[awayTotal][0] + 100, percentData[awayTotal][1] + 1]

        else:
            percentData[teamTotal] = [percentData[teamTotal][0], percentData[teamTotal][1] + 1]
            percentData[teamDayTotal] = [percentData[teamDayTotal][0], percentData[teamDayTotal][1] + 1]            
            percentData[teamTimeTotal] = [percentData[teamTimeTotal][0], percentData[teamTimeTotal][1] + 1]
            percentData[weekTotal] = [percentData[weekTotal][0], percentData[weekTotal][1] + 1]
            percentData[overallTotal] = [percentData[overallTotal][0], percentData[overallTotal][1] + 1]
            percentData[overallDayTotal] = [percentData[overallDayTotal][0], percentData[overallDayTotal][1] + 1]
            percentData[overallTimeTotal] = [percentData[overallTimeTotal][0], percentData[overallTimeTotal][1] + 1]

            if at:
                percentData[teamHomeTotal] = [percentData[teamHomeTotal][0], percentData[teamHomeTotal][1] + 1]
                percentData[homeTotal] = [percentData[homeTotal][0], percentData[homeTotal][1] + 1]
            else:
                percentData[teamAwayTotal] = [percentData[teamAwayTotal][0], percentData[teamAwayTotal][1] + 1]
                percentData[awayTotal] = [percentData[awayTotal][0], percentData[awayTotal][1] + 1]


        if (spreadCalculated == spreadCovered) and (totalCalculated == totalCovered):
            percentData[teamParlay] = [percentData[teamParlay][0] + 100, percentData[teamParlay][1] + 1]
            percentData[teamDayParlay] = [percentData[teamDayParlay][0] + 100, percentData[teamDayParlay][1] + 1]            
            percentData[teamTimeParlay] = [percentData[teamTimeParlay][0] + 100, percentData[teamTimeParlay][1] + 1]
            percentData[weekParlay] = [percentData[weekParlay][0] + 100, percentData[weekParlay][1] + 1]
            percentData[overallParlay] = [percentData[overallParlay][0] + 100, percentData[overallParlay][1] + 1]
            percentData[overallDayParlay] = [percentData[overallDayParlay][0] + 100, percentData[overallDayParlay][1] + 1]
            percentData[overallTimeParlay] = [percentData[overallTimeParlay][0] + 100, percentData[overallTimeParlay][1] + 1]

            if at:
                percentData[teamHomeParlay] = [percentData[teamHomeParlay][0] + 100, percentData[teamHomeParlay][1] + 1]
                percentData[homeParlay] = [percentData[homeParlay][0] + 100, percentData[homeParlay][1] + 1]
            else:
                percentData[teamAwayParlay] = [percentData[teamAwayParlay][0] + 100, percentData[teamAwayParlay][1] + 1]
                percentData[awayParlay] = [percentData[awayParlay][0] + 100, percentData[awayParlay][1] + 1]

        else:
            percentData[teamParlay] = [percentData[teamParlay][0], percentData[teamParlay][1] + 1]
            percentData[teamDayParlay] = [percentData[teamDayParlay][0], percentData[teamDayParlay][1] + 1]            
            percentData[teamTimeParlay] = [percentData[teamTimeParlay][0], percentData[teamTimeParlay][1] + 1]
            percentData[weekParlay] = [percentData[weekParlay][0], percentData[weekParlay][1] + 1]
            percentData[overallParlay] = [percentData[overallParlay][0], percentData[overallParlay][1] + 1]
            percentData[overallDayParlay] = [percentData[overallDayParlay][0], percentData[overallDayParlay][1] + 1]
            percentData[overallTimeParlay] = [percentData[overallTimeParlay][0], percentData[overallTimeParlay][1] + 1]

            if at:
                percentData[teamHomeParlay] = [percentData[teamHomeParlay][0], percentData[teamHomeParlay][1] + 1]
                percentData[homeParlay] = [percentData[homeParlay][0], percentData[homeParlay][1] + 1]
            else:
                percentData[teamAwayParlay] = [percentData[teamAwayParlay][0], percentData[teamAwayParlay][1] + 1]
                percentData[awayParlay] = [percentData[awayParlay][0], percentData[awayParlay][1] + 1]


    for data in percentData:
        try:
            percentData[data] = round(percentData[data][0] / percentData[data][1], 2)
        except:
            percentData[data] = -1

    count = 1
    for data in percentData:
        if count == len(percentData):
            percentFrontendFile.write(f'"{data}" : {percentData[data]}')
        else:
            percentFrontendFile.write(f'"{data}" : {percentData[data]},')

        count = count + 1


    percentFrontendFile.write('}')
    percentFrontendFile.close()

    print('Percentages on the fontend have been updated!')










week = int(sys.argv[1])
year = 2024
table = 'productionNFL'

print(f'Start Time : {time.localtime()}')

# 1/4
#Store old game data
storeDataObj = storeTeamData(table, week, year)
storeDataObj.storeAllTeamsData()
updateCoveredValues()

# 2/4
#Store new game data
storeUpcomingWeekData = getUpcomingWeekData(week, year)
storeUpcomingWeekData.getWeatherByWeek()
storeUpcomingWeekData.getGamblingData()

# 3/4
updatePercentages()
updateFavored()


# 4/4
#Get predictions
predictions = getPredictions(week, year)
predictions.doit()

updateTeamData(week)

# getParlays()

# Update frontend
updateFrontend(week)
updatePercentagesFrontend()


print(f'End time : {time.localtime()}')