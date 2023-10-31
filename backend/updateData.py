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

from theBot2 import theBot
from Legends import *


#For each team
#Go to website and scrape all data for given team
#Find previous week if its not a by week
#Save weeks data to database

class storeTeamData:
    def __init__(self, table, week, year):
        self.teams = ['dal','tam','nor','atl','car','min','gnb','det','chi','ram','crd','sfo','sea','oti','clt','jax','kan','rai','sdg','den','phi','was','nyg','nyj','mia','nwe','buf','cin','pit','rav','cle','htx']
        self.table = table
        self.week = week
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
                        f"INSERT INTO {self.table} "
                        f"("
                        f"Week, "
                        f"Day, "
                        f"WinLoss, "
                        f"OT, "
                        f"At, "
                        f"OppTeam, "
                        f"Tm, "
                        f"Opp, "
                        f"Cmp, "
                        f"AttPassing, "
                        f"YdsPassing, "
                        f"TDPassing, "
                        f"Interceptions, "
                        f"Sk, "
                        f"YdsLossFromSacks, "
                        f"YPerAPassing, "
                        f"NYPerA, "
                        f"CmpPerc, "
                        f"Rate, "
                        f"AttRushing, "
                        f"YdsRushing, "
                        f"YPerARushing, "
                        f"TDRushing, "
                        f"FGM, "
                        f"FGA, "
                        f"XPM, "
                        f"XPA, "
                        f"Pnt, "
                        f"YdsPunting, "
                        f"ThirdDConv, "
                        f"ThirdDAtt, "
                        f"FourthDConv, "
                        f"FourthDAtt, "
                        f"ToP, "
                        f"Year, "
                        f"Team, "
                        f"YardsPerPoint, "
                        f"HomeTeam "
                        f") "
                        f"VALUES ("
                        f"{row[0]},"
                        f"{row[1]},"
                        f"{row[2]},"
                        f"{row[3]},"
                        f"{row[4]},"
                        f"{row[5]},"
                        f"{row[6]},"
                        f"{row[7]},"
                        f"{row[8]},"
                        f"{row[9]},"
                        f"{row[10]},"
                        f"{row[11]},"
                        f"{row[12]},"
                        f"{row[13]},"
                        f"{row[14]},"
                        f"{row[15]},"
                        f"{row[16]},"
                        f"{row[17]},"
                        f"{row[18]},"
                        f"{row[19]},"
                        f"{row[20]},"
                        f"{row[21]},"
                        f"{row[22]},"
                        f"{row[23]},"
                        f"{row[24]},"
                        f"{row[25]},"
                        f"{row[26]},"
                        f"{row[27]},"
                        f"{row[28]},"
                        f"{row[29]},"
                        f"{row[30]},"
                        f"{row[31]},"
                        f"{row[32]},"
                        f"{row[33]},"
                        f"{self.year},"
                        f"'{team}',"
                        f"{yardsPerPoint},"
                        f"{row[5]}"
                        f")"
                )
                mycursor.execute(insertData)
                mydb.commit()
            else:
                insertData = (
                    f"INSERT INTO {self.table} "
                    f"("
                    f"Week, "
                    f"Day, "
                    f"WinLoss, "
                    f"OT, "
                    f"At, "
                    f"OppTeam, "
                    f"Tm, "
                    f"Opp, "
                    f"Cmp, "
                    f"AttPassing, "
                    f"YdsPassing, "
                    f"TDPassing, "
                    f"Interceptions, "
                    f"Sk, "
                    f"YdsLossFromSacks, "
                    f"YPerAPassing, "
                    f"NYPerA, "
                    f"CmpPerc, "
                    f"Rate, "
                    f"AttRushing, "
                    f"YdsRushing, "
                    f"YPerARushing, "
                    f"TDRushing, "
                    f"FGM, "
                    f"FGA, "
                    f"XPM, "
                    f"XPA, "
                    f"Pnt, "
                    f"YdsPunting, "
                    f"ThirdDConv, "
                    f"ThirdDAtt, "
                    f"FourthDConv, "
                    f"FourthDAtt, "
                    f"ToP, "
                    f"Year, "
                    f"Team, "
                    f"YardsPerPoint, "
                    f"HomeTeam "
                    f") "
                    f"VALUES ("
                    f"{row[0]},"
                    f"{row[1]},"
                    f"{row[2]},"
                    f"{row[3]},"
                    f"{row[4]},"
                    f"{row[5]},"
                    f"{row[6]},"
                    f"{row[7]},"
                    f"{row[8]},"
                    f"{row[9]},"
                    f"{row[10]},"
                    f"{row[11]},"
                    f"{row[12]},"
                    f"{row[13]},"
                    f"{row[14]},"
                    f"{row[15]},"
                    f"{row[16]},"
                    f"{row[17]},"
                    f"{row[18]},"
                    f"{row[19]},"
                    f"{row[20]},"
                    f"{row[21]},"
                    f"{row[22]},"
                    f"{row[23]},"
                    f"{row[24]},"
                    f"{row[25]},"
                    f"{row[26]},"
                    f"{row[27]},"
                    f"{row[28]},"
                    f"{row[29]},"
                    f"{row[30]},"
                    f"{row[31]},"
                    f"{row[32]},"
                    f"{row[33]},"
                    f"{self.year},"
                    f"'{team}',"
                    f"{yardsPerPoint},"
                    f"{getTeamFromSmallName(team)}"
                    f")"
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


#For each game in a week
#Go to website and scrape all data (all games in a week)
#Find all weather data for each game that week
#Save data to database
class updateWeatherData:

    def __init__(self, table, week, year):
        self.table = table
        self.week = week
        self.year = year

    def addData(self, data, awayTeam, homeTeam):
        mydb = mysql.connector.connect(
            host='127.0.0.1',
            user='davidcarney',
            password='Sinorrabb1t',
            database='NFL'
            )

        mycursor = mydb.cursor()
        for column in data:            
            insertValues = (
                f"UPDATE {self.table} "
                f"SET {column} = {data[column]} "
                f"WHERE (HomeTeam = {homeTeam}) and (OppTeam = {awayTeam}) and (Week = {self.week}) and (Year = {self.year})"
            )

            mycursor.execute(insertValues)
            mydb.commit()

            insertValues = (
                f"UPDATE {self.table} "
                f"SET {column} = {data[column]} "
                f"WHERE (Team = '{getTeamSmallNameFromTeam(awayTeam)}') and (HomeTeam = {homeTeam}) and (Week = {self.week}) and (Year = {self.year})"
                )

            mycursor.execute(insertValues)
            mydb.commit()

    def getWeatherByWeek(self):
        URL = f'https://www.nflweather.com/week/{self.year}/week-{self.week}'
        HEADERS = {
            'User-Agent': 'Safari/537.36',
        }
        page = requests.get(URL, headers=HEADERS)
        soup = BeautifulSoup(page.content, 'html.parser')
        time.sleep(3)
        moreSoup = soup.find('div', class_='container-game-box')
        dates = []

        matchUp = moreSoup.div 
        while matchUp != None:
            matchUpData1 = matchUp.div
            dateAndTime = matchUpData1.div.text.strip()
            dates.append(dateAndTime[0])
            dateAndTime = dateAndTime.split(' ')
            day = datetime.strptime(dateAndTime[0], '%m/%d/%y')
            dayCode = getDay(day.strftime('%A')[:3])

            hour = int(dateAndTime[1].split(':')[0])
            am_pm = dateAndTime[2]
            timeCode = getTime(hour,am_pm)
            time.sleep(3)

            matchUpData2 = matchUpData1.next_sibling.next_sibling
            awayTeam, at, homeTeam = matchUpData2.find_all('span')
            awayTeam = getTeam(awayTeam.text)
            homeTeam = getTeam(homeTeam.text)
 
            time.sleep(3)
            
            matchUpData3 = matchUpData2.next_sibling.next_sibling
            weatherData = matchUpData3.div.div.next_sibling.next_sibling
            weatherInfo = weatherData.find_all('span')

            temp = None
            weather = None
            weatherInfoLen = len(weatherInfo)
            if weatherInfoLen == 0:
                temp = 73
                weather = 'Overcast'
            elif weatherInfoLen == 1:
                temp = getTemp(73)
                weather = getWeather('Overcast')
            else:
                temp, weather = weatherInfo
                temp = getTemp(int(temp.text.split(' ')[0]))
                weather = getWeather(weather.text)

            time.sleep(3)
            windDataContainer = weatherData.next_sibling.next_sibling
            windData = windDataContainer.find_all('span')
            windDataLength = len(windData)
            wind = 0
            if windDataLength == 3:
                wind = windData[1].text.split(' ')[0]

            time.sleep(3)
            channelData = windDataContainer.next_sibling.next_sibling
            if channelData != None:
                channels = channelData.find_all('span')
                channelsLength = len(channels)
                channel = 0
                if channelsLength > 1:
                    channel = channels[1].text
                    if ',' in channel:
                        channel = channel.split(',')[0]
                    elif ' ' in channel:
                        channel = channel.split(' ')[0]
                    channel = getChannel(channel)
            else:
                channel = 6
            

            data = {'Time':timeCode,'Channel':channel,'Temp':temp,'Weather':weather,'Wind':wind}
            self.addData(data, awayTeam, homeTeam)
            
            matchUp = matchUp.next_sibling.next_sibling
        return dates[0]

    def doit(self):
        startOfWeek = self.getWeatherByWeek()
        print(f'Upcoming week (week : {self.week}) data has been saved to database!')
        return startOfWeek


#For each game after given date
#Go to website and store data from excel sheet into pandas df
#Find all gambling data for each game after week start
#Save data to database  
class updateGamblingData:

    def __init__(self, table, year):
        self.table = table
        self.year = year

    def saveData(self, column, data, awayTeam, homeTeam):
        mydb = mysql.connector.connect(
            host='127.0.0.1',
            user='davidcarney',
            password='Sinorrabb1t',
            database='NFL'
            )

        mycursor = mydb.cursor()
        homeTeamCode = getTeam(homeTeam)
        awayTeamCode = getTeam(awayTeam)

        insertValues = (
            f"UPDATE {self.table} "
            f"SET {column} = {data} "
            f"WHERE (HomeTeam = {homeTeamCode}) and (OppTeam = {awayTeamCode}) and (Year = {self.year})"
        )
        mycursor.execute(insertValues)
        mydb.commit()
        insertValues = (
            f"UPDATE {self.table} "
            f"SET {column} = {data} "
            f"WHERE (Team = '{getTeamSmallNameFromTeam(awayTeamCode)}') and (HomeTeam = {homeTeamCode}) and (Year = {self.year})"
        )
        mycursor.execute(insertValues)
        mydb.commit()

    def doit(self, startOfWeek):
        URL = f'https://www.aussportsbetting.com/data/historical-nfl-results-and-odds-data/'
        # HEADERS = {
        #     'User-Agent': 'Safari/537.36',
        # }
        # page = requests.get(URL, headers=HEADERS)
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser')

        table = soup.find('table')
        tableData = table.find('td')
        a = tableData.find('a')
        href = a.get('href')
        startUrl = 'https://www.aussportsbetting.com'
        excel = startUrl + href

        excelContent = requests.get(excel).content
        
        #Warning error -> read_excel is auto changing string datetimes to datetimes
        #String datetimes will stay strings instead of changing to datetimes
        #Update string datetimes to datetimes
        df = pd.read_excel(excelContent)

        df = df[df['Date'] > startOfWeek]
        df = df[['Date','Home Team','Away Team','Neutral Venue?','Home Line Open','Home Line Min','Home Line Max','Home Line Close','Total Score Open','Total Score Min','Total Score Max','Total Score Close']]

        df['Neutral Venue?'] = df['Neutral Venue?'].fillna(0)
        df['Neutral Venue?'] = df['Neutral Venue?'].replace('Y',1)

        
        mydb = mysql.connector.connect(
            host='127.0.0.1',
            user='davidcarney',
            password='Sinorrabb1t',
            database='NFL'
            )

        mycursor = mydb.cursor()

        for index, row in df.iterrows():
            date, homeTeam, awayTeam, neutralVenue, homeLineOpen, homeLineMin, homeLineMax, homeLineClose, totalScoreOpen, totalScoreMin, totalScoreMax, totalScoreClose = row
            date = date.strftime('%Y-%m-%d')
            date = date.split('-')[0]
            homeLineClose = float(homeLineClose)
            homeFavored = 0
            awayFavored = 0
            if homeLineClose < 0:
                homeFavored = 1
            elif homeLineClose > 0:
                awayFavored = 1

            gameLine = homeLineClose - float(homeLineOpen)
            minMaxLine = float(homeLineMax) - float(homeLineMin)
            if gameLine < 0:
                gameLine = -gameLine
            totalScoreLine = float(totalScoreClose) - float(totalScoreOpen)
            if totalScoreLine < 0:
                totalScoreLine = -totalScoreLine
            minMaxTotalScoreLine = float(totalScoreMax) - float(totalScoreMin)

            #Save gameLine
            self.saveData('gameLine', gameLine, awayTeam, homeTeam)
            
            #Save minMaxLine
            self.saveData('minMaxLine', minMaxLine, awayTeam, homeTeam)

            #Save totalScoreLine
            self.saveData('totalScoreLine', totalScoreLine, awayTeam, homeTeam)

            #Save minMaxTotalScoreLine
            self.saveData('minMaxTotalScoreLine', minMaxTotalScoreLine, awayTeam, homeTeam)

            homeTeamCode = getTeam(homeTeam)
            awayTeamCode = getTeam(awayTeam)
            #Save favored data
            insertValues = (
                f"UPDATE {self.table} "
                f"SET favored = {homeFavored} "
                f"WHERE (HomeTeam = {homeTeamCode}) and (OppTeam = {awayTeamCode}) and (Year = {self.year})"
            )
            mycursor.execute(insertValues)
            mydb.commit()
            insertValues = (
                f"UPDATE {self.table} "
                f"SET favored = {awayFavored} "
                f"WHERE (Team = '{getTeamSmallNameFromTeam(awayTeamCode)}') and (HomeTeam = {homeTeamCode}) and (Year = {self.year})"
            )
            mycursor.execute(insertValues)
            mydb.commit()
            
        print(f'Gambling data has been saved to database!')




#Update all percentages for all weeks and years
def updatePercentages():
    matchups = []
    filenameRead = './percentages.txt'
    fileRead = open(filenameRead, 'r')


    groups = {'AFCNorth': ['Ravens', 'Bengals', 'Browns', 'Steelers'], 'AFCSouth': ['Titans', 'Colts', 'Jaguars', 'Texans'], 'AFCEast': ['Bills', 'Jets', 'Dolphins', 'Patriots'], 'AFCWest': ['Cheifs', 'Chargers', 'Broncos', 'Raiders'], 'AFC': ['Ravens', 'Bengals', 'Browns', 'Steelers', 'Titans', 'Colts', 'Jaguars', 'Texans', 'Bills', 'Jets', 'Dolphins', 'Patriots', 'Cheifs', 'Chargers', 'Broncos', 'Raiders'], 'NFCNorth': ['Vikings', 'Packers', 'Bears', 'Lions'], 'NFCSouth': ['Buccaneers', 'Falcons', 'Saints', 'Panthers'], 'NFCEast': ['Cowboys', 'Giants', 'Eagles', 'Commanders'], 'NFCWest': ['49ers', 'Rams', 'Seahawks', 'Cardinals'], 'NFC': ['Vikings', 'Packers', 'Bears', 'Lions', 'Buccaneers', 'Falcons', 'Saints', 'Panthers', 'Cowboys', 'Giants', 'Eagles', 'Commanders', '49ers', 'Rams', 'Seahawks', 'Cardinals']}
    results = {'AFC':[0,0], 'AFCNorth':[0,0], 'AFCSouth':[0,0], 'AFCEast':[0,0], 'AFCWest':[0,0], 'NFC':[0,0], 'NFCNorth':[0,0], 'NFCSouth':[0,0], 'NFCEast':[0,0], 'NFCWest':[0,0]}
    week = 0
    year = 0

    for line in fileRead.readlines():
        data = line.split(',')
        dataLength = len(data)

        if dataLength > 1:
            predictedWinner = data[0]
            predictedLoser = data[1]
            outcome = data[2][0]

            if outcome == '1':
                if predictedWinner not in results:
                    results[predictedWinner] = [100,1]
                else:
                    results[predictedWinner] = [results[predictedWinner][0] + 100, results[predictedWinner][1] + 1]

                if predictedLoser not in results:
                    results[predictedLoser] = [100,1]
                else:
                    results[predictedLoser] = [results[predictedLoser][0] + 100, results[predictedLoser][1] + 1]


                if predictedWinner in groups['AFC']:
                    results['AFC'] = [results['AFC'][0]  + 100, results['AFC'][1] + 1]

                    if predictedWinner in groups['AFCNorth']:
                        results['AFCNorth'] = [results['AFCNorth'][0]  + 100, results['AFCNorth'][1] + 1]
                    elif predictedWinner in groups['AFCSouth']:
                        results['AFCSouth'] = [results['AFCSouth'][0]  + 100, results['AFCSouth'][1] + 1]
                    elif predictedWinner in groups['AFCEast']:
                        results['AFCEast'] = [results['AFCEast'][0]  + 100, results['AFCEast'][1] + 1]
                    elif predictedWinner in groups['AFCWest']:
                        results['AFCWest'] = [results['AFCWest'][0]  + 100, results['AFCWest'][1] + 1]

                elif predictedWinner in groups['NFC']:
                    results['NFC'] = [results['NFC'][0]  + 100, results['NFC'][1] + 1]

                    if predictedWinner in groups['NFCNorth']:
                        results['NFCNorth'] = [results['NFCNorth'][0]  + 100, results['NFCNorth'][1] + 1]
                    elif predictedWinner in groups['NFCSouth']:
                        results['NFCSouth'] = [results['NFCSouth'][0]  + 100, results['NFCSouth'][1] + 1]
                    elif predictedWinner in groups['NFCEast']:
                        results['NFCEast'] = [results['NFCEast'][0]  + 100, results['NFCEast'][1] + 1]
                    elif predictedWinner in groups['NFCWest']:
                        results['NFCWest'] = [results['NFCWest'][0]  + 100, results['NFCWest'][1] + 1]

                if predictedLoser in groups['AFC']:
                    results['AFC'] = [results['AFC'][0]  + 100, results['AFC'][1] + 1]

                    if predictedLoser in groups['AFCNorth']:
                        results['AFCNorth'] = [results['AFCNorth'][0]  + 100, results['AFCNorth'][1] + 1]
                    elif predictedLoser in groups['AFCSouth']:
                        results['AFCSouth'] = [results['AFCSouth'][0]  + 100, results['AFCSouth'][1] + 1]
                    elif predictedLoser in groups['AFCEast']:
                        results['AFCEast'] = [results['AFCEast'][0]  + 100, results['AFCEast'][1] + 1]
                    elif predictedLoser in groups['AFCWest']:
                        results['AFCWest'] = [results['AFCWest'][0]  + 100, results['AFCWest'][1] + 1]

                elif predictedLoser in groups['NFC']:
                    results['NFC'] = [results['NFC'][0]  + 100, results['NFC'][1] + 1]

                    if predictedLoser in groups['NFCNorth']:
                        results['NFCNorth'] = [results['NFCNorth'][0]  + 100, results['NFCNorth'][1] + 1]
                    elif predictedLoser in groups['NFCSouth']:
                        results['NFCSouth'] = [results['NFCSouth'][0]  + 100, results['NFCSouth'][1] + 1]
                    elif predictedLoser in groups['NFCEast']:
                        results['NFCEast'] = [results['NFCEast'][0]  + 100, results['NFCEast'][1] + 1]
                    elif predictedLoser in groups['NFCWest']:
                        results['NFCWest'] = [results['NFCWest'][0]  + 100, results['NFCWest'][1] + 1]

                results[f'{year} Week {week}'] = [results[f'{year} Week {week}'][0] + 100, results[f'{year} Week {week}'][1] + 1]

            else:
                if predictedWinner not in results:
                    results[predictedWinner] = [0,1]
                else:
                    results[predictedWinner] = [results[predictedWinner][0] + 0, results[predictedWinner][1] + 1]

                if predictedLoser not in results:
                    results[predictedLoser] = [0,1]
                else:
                    results[predictedLoser] = [results[predictedLoser][0] + 0, results[predictedLoser][1] + 1]


                if predictedWinner in groups['AFC']:
                    results['AFC'] = [results['AFC'][0]  + 0, results['AFC'][1] + 1]

                    if predictedWinner in groups['AFCNorth']:
                        results['AFCNorth'] = [results['AFCNorth'][0]  + 0, results['AFCNorth'][1] + 1]
                    elif predictedWinner in groups['AFCSouth']:
                        results['AFCSouth'] = [results['AFCSouth'][0]  + 0, results['AFCSouth'][1] + 1]
                    elif predictedWinner in groups['AFCEast']:
                        results['AFCEast'] = [results['AFCEast'][0]  + 0, results['AFCEast'][1] + 1]
                    elif predictedWinner in groups['AFCWest']:
                        results['AFCWest'] = [results['AFCWest'][0]  + 0, results['AFCWest'][1] + 1]

                elif predictedWinner in groups['NFC']:
                    results['NFC'] = [results['NFC'][0]  + 0, results['NFC'][1] + 1]

                    if predictedWinner in groups['NFCNorth']:
                        results['NFCNorth'] = [results['NFCNorth'][0]  + 0, results['NFCNorth'][1] + 1]
                    elif predictedWinner in groups['NFCSouth']:
                        results['NFCSouth'] = [results['NFCSouth'][0]  + 0, results['NFCSouth'][1] + 1]
                    elif predictedWinner in groups['NFCEast']:
                        results['NFCEast'] = [results['NFCEast'][0]  + 0, results['NFCEast'][1] + 1]
                    elif predictedWinner in groups['NFCWest']:
                        results['NFCWest'] = [results['NFCWest'][0]  + 0, results['NFCWest'][1] + 1]

                if predictedLoser in groups['AFC']:
                    results['AFC'] = [results['AFC'][0]  + 0, results['AFC'][1] + 1]

                    if predictedLoser in groups['AFCNorth']:
                        results['AFCNorth'] = [results['AFCNorth'][0]  + 0, results['AFCNorth'][1] + 1]
                    elif predictedLoser in groups['AFCSouth']:
                        results['AFCSouth'] = [results['AFCSouth'][0]  + 0, results['AFCSouth'][1] + 1]
                    elif predictedLoser in groups['AFCEast']:
                        results['AFCEast'] = [results['AFCEast'][0]  + 0, results['AFCEast'][1] + 1]
                    elif predictedLoser in groups['AFCWest']:
                        results['AFCWest'] = [results['AFCWest'][0]  + 0, results['AFCWest'][1] + 1]

                elif predictedLoser in groups['NFC']:
                    results['NFC'] = [results['NFC'][0]  + 0, results['NFC'][1] + 1]

                    if predictedLoser in groups['NFCNorth']:
                        results['NFCNorth'] = [results['NFCNorth'][0]  + 0, results['NFCNorth'][1] + 1]
                    elif predictedLoser in groups['NFCSouth']:
                        results['NFCSouth'] = [results['NFCSouth'][0]  + 0, results['NFCSouth'][1] + 1]
                    elif predictedLoser in groups['NFCEast']:
                        results['NFCEast'] = [results['NFCEast'][0]  + 0, results['NFCEast'][1] + 1]
                    elif predictedLoser in groups['NFCWest']:
                        results['NFCWest'] = [results['NFCWest'][0]  + 0, results['NFCWest'][1] + 1]

                results[f'{year} Week {week}'] = [results[f'{year} Week {week}'][0] + 0, results[f'{year} Week {week}'][1] + 1]

        elif dataLength == 1:
            weekOrYear = data[0][:-1]
            if weekOrYear == '2022':
                year = 2022
            elif weekOrYear == '2023':
                year = 2023
            else:
                week = weekOrYear
                results[f'{year} Week {week}'] = [0,0]




    finalResults = {}
    for team in results:
        finalResults[team] = round(results[team][0]/results[team][1],2)


    filenameWrite = '../frontend/src/nflPages/percentages.json'
    with open(filenameWrite, 'w') as outfile:
        json.dump(finalResults, outfile)

    fileRead.close()
    


#For each game in a week
#Go to website and scrape all data (all games in a week)
#Find all data for each game that week
#Write data to frontend and backend files
class getUpcomingWeekData:
    def __init__(self, week, year):
        self.week = week + 1
        self.year = year
  
    def getWeatherByWeek(self):
        upcomingWeekBackendFilename = 'upcomingWeekData.txt'
        upcomingWeekFrontendFilename = '../frontend/src/nflPages/upcomingWeekData.js'
        upcomingWeekBackendFile = open(upcomingWeekBackendFilename, 'w')
        upcomingWeekFrontendFile = open(upcomingWeekFrontendFilename, 'w')
        upcomingWeekFrontendFile.write('export const upcomingWeekData = [\n')
        upcomingWeekFrontendFile.write(f"'{self.week}',\n")

        URL = f'https://www.nflweather.com/week/{self.year}/week-{self.week}'
        HEADERS = {
            'User-Agent': 'Safari/537.36',
        }
        page = requests.get(URL, headers=HEADERS)
        soup = BeautifulSoup(page.content, 'html.parser')
        moreSoup = soup.find('div', class_='container-game-box')
        time.sleep(3)

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
                temp = 73
                weather = 'Overcast'
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
            if channelData != None:
                channels = channelData.find_all('span')
                channelsLength = len(channels)
                channel = 0
                if channelsLength > 1:
                    channel = channels[1].text
                    if ',' in channel:
                        channel = channel.split(',')[0]
                    elif ' ' in channel:
                        channel = channel.split(' ')[0]
                    channel = getChannel(channel)
            else:
                channel = 6
            

            upcomingWeekBackendFile.write(awayTeam)
            upcomingWeekBackendFile.write('_')
            upcomingWeekBackendFile.write(homeTeam)
            upcomingWeekBackendFile.write('_')
            upcomingWeekBackendFile.write(f'{timeCode}')
            upcomingWeekBackendFile.write('_')
            upcomingWeekBackendFile.write(f'{dayCode}')
            upcomingWeekBackendFile.write('_')
            upcomingWeekBackendFile.write(f'{channel}')
            upcomingWeekBackendFile.write('_')
            upcomingWeekBackendFile.write(f'{getTemp(temp)}')
            upcomingWeekBackendFile.write('_')
            upcomingWeekBackendFile.write(f'{getWeather(weather)}')
            upcomingWeekBackendFile.write('_')
            upcomingWeekBackendFile.write(f'{wind}')
            upcomingWeekBackendFile.write('\n')

            upcomingWeekFrontendFile.write("'")
            upcomingWeekFrontendFile.write(f'{dateAndTime[0]}')
            upcomingWeekFrontendFile.write('_')
            upcomingWeekFrontendFile.write(f'{dateAndTime[1]}')
            upcomingWeekFrontendFile.write('_')
            upcomingWeekFrontendFile.write(f'{dateAndTime[2]}')
            upcomingWeekFrontendFile.write('_')
            upcomingWeekFrontendFile.write(f'{dateAndTime[3]}')
            upcomingWeekFrontendFile.write('_')
            upcomingWeekFrontendFile.write(awayTeam)
            upcomingWeekFrontendFile.write('_')
            upcomingWeekFrontendFile.write(homeTeam)
            upcomingWeekFrontendFile.write('_')
            upcomingWeekFrontendFile.write(f'{temp}')
            upcomingWeekFrontendFile.write('_')
            upcomingWeekFrontendFile.write(weather)
            upcomingWeekFrontendFile.write('_')
            upcomingWeekFrontendFile.write(f'{wind}')
            upcomingWeekFrontendFile.write("',")
            upcomingWeekFrontendFile.write('\n')

            matchUp = matchUp.next_sibling.next_sibling

        upcomingWeekFrontendFile.write('];')
        upcomingWeekBackendFile.close()
        upcomingWeekFrontendFile.close()

        print(f'Upcoming week (week : {self.week}) data has been saved to upcomingWeekData file!')





#Predict winner loser and their scores
class getPredictions:
    def __init__(self, week, year):
        self.week = week
        self.year = year

    def teamService(self, columnName, teamNumber, time, day, at, oppTeamNumber, channel, temp, weather, wind):
        mydb = mysql.connector.connect(
            host='127.0.0.1',
            user='davidcarney',
            password='Sinorrabb1t',
            database='NFL'
            )

        mycursor = mydb.cursor()

        mycursor.execute(f"SELECT * FROM productionNFL WHERE Team = '{getTeamSmallNameFromTeam(teamNumber)}' and Year > 2016")

        teamData = mycursor.fetchall()
        dfColumns = ['id','Week','Day','WinLoss','OT','At','OppTeam','Tm','Opp','Cmp','AttPassing','YdsPassing','TDPassing','Interceptions','Sk','YdsLossFromSacks','YPerAPassing','NYPerA','CmpPerc','Rate','AttRushing','YdsRushing','YPerARushing','TDRushing','FGM','FGA','XPM','XPA','Pnt','YdsPunting','ThirdDConv','ThirdDAtt','FourthDConv','FourthDAtt','ToP','Year','Team','YardsPerPoint','HomeTeam','Time','Channel','Temp','Weather','Wind','gameLine','minMaxLine','totalScoreLine','minMaxTotalScoreLine','favored']
        teamDF = pd.DataFrame(teamData, columns = dfColumns)

        upcomingWeekData = None
        if at == 0:
            upcomingWeekData = [[self.week, time, day, at, oppTeamNumber, wind, temp, weather, channel, self.year]]
            
        else:
            upcomingWeekData = [[self.week, time, day, at, oppTeamNumber, wind, temp, weather, channel, self.year]]
        
        upcomingWeekColumns = ['Week','Time','Day','At','OppTeam','Wind','Temp','Weather','Channel','Year']
        upcomingWeekDF = pd.DataFrame(upcomingWeekData, columns = upcomingWeekColumns)

        model = theBot(teamDF, upcomingWeekDF, columnName)
        model.adjustDF()

        #Run theBot code 3 times to keep adding to existing upcoming week DF
        predictions1 = model.useCode()
        predictions2 = model.useCode()
        predictions3 = model.useCode()


        return predictions1,predictions2,predictions3

    def updateMatchup(self, awayTeamName, homeTeamName, time, day, channel, temp, weather, wind, resultsFile, percentFile):
        homeTeamNumber = getTeam(homeTeamName)
        awayTeamNumber = getTeam(awayTeamName)

        homeWinLossOutcome = 1
        awayWinLossOutcome = 1
        homePointsOutcomeTm = [1,2]
        awayPointsOutcomeTm = [1,2]
        homePointsOutcomeOpp = [1,2]
        awayPointsOutcomeOpp = [1,2]

        for i in range(12):

            homePredictions1WL, homePredictions2WL, homePredictions3WL = self.teamService('WinLoss', homeTeamNumber, time, day, 1, awayTeamNumber, channel, temp, weather, wind)
            awayPredictions1WL, awayPredictions2WL, awayPredictions3WL = self.teamService('WinLoss', awayTeamNumber, time, day, 0, homeTeamNumber, channel, temp, weather, wind)

            homeWinLossOutcome = homeWinLossOutcome + ((homePredictions1WL[0] + homePredictions1WL[1]) / 2) + ((homePredictions2WL[0] + homePredictions2WL[1]) / 2) + ((homePredictions3WL[0] + homePredictions3WL[1]) / 2)
            awayWinLossOutcome = awayWinLossOutcome + ((awayPredictions1WL[0] + awayPredictions1WL[1]) / 2) + ((awayPredictions2WL[0] + awayPredictions2WL[1]) / 2) + ((awayPredictions3WL[0] + awayPredictions3WL[1]) / 2)

        # for i in range(12):
        #     homePredictions1TM, homePredictions2TM, homePredictions3TM = self.teamService('Tm', homeTeamNumber, time, day, 1, awayTeamNumber, channel, temp, weather, wind)
        #     awayPredictions1TM, awayPredictions2TM, awayPredictions3TM = self.teamService('Tm', awayTeamNumber, time, day, 0, homeTeamNumber, channel, temp, weather, wind)

        #     homePointsOutcomeTm.append((homePredictions1TM[0] + homePredictions2TM[0] + homePredictions3TM[0]) / 3)
        #     awayPointsOutcomeTm.append((awayPredictions1TM[0] + awayPredictions2TM[0] + awayPredictions3TM[0]) / 3)
        
        # for i in range(12):  
        #     homePredictions1OPP, homePredictions2OPP, homePredictions3OPP = self.teamService('Opp', homeTeamNumber, time, day, 1, awayTeamNumber, channel, temp, weather, wind)
        #     awayPredictions1OPP, awayPredictions2OPP, awayPredictions3OPP = self.teamService('Opp', awayTeamNumber, time, day, 0, homeTeamNumber, channel, temp, weather, wind)

        #     homePointsOutcomeOpp.append((homePredictions1OPP[0] + homePredictions2OPP[0] + homePredictions3OPP[0]) / 3)
        #     awayPointsOutcomeOpp.append((awayPredictions1OPP[0] + awayPredictions2OPP[0] + awayPredictions3OPP[0]) / 3)

        
        homePointsOutcomeTmMax = max(homePointsOutcomeTm)
        awayPointsOutcomeTmMax = max(awayPointsOutcomeTm)
        homePointsOutcomeOppMax = max(homePointsOutcomeOpp)
        awayPointsOutcomeOppMax = max(awayPointsOutcomeOpp)

        homePointsOutcomeTmMin = min(homePointsOutcomeTm)
        awayPointsOutcomeTmMin = min(awayPointsOutcomeTm)
        homePointsOutcomeOppMin = min(homePointsOutcomeOpp)
        awayPointsOutcomeOppMin = min(awayPointsOutcomeOpp)

        # homePointsOutcomeTmAvg = sum(homePointsOutcomeTm) / len(homePointsOutcomeTm)
        # awayPointsOutcomeTmAvg = sum(awayPointsOutcomeTm) / len(awayPointsOutcomeTm)
        # homePointsOutcomeOppAvg = sum(homePointsOutcomeOpp) / len(homePointsOutcomeOpp)
        # awayPointsOutcomeOppAvg = sum(awayPointsOutcomeOpp) / len(awayPointsOutcomeOpp)


        # print('homePointsOutcomeTm',homePointsOutcomeTmMax,min(homePointsOutcomeTm),sum(homePointsOutcomeTm) / len(homePointsOutcomeTm))
        # print('awayPointsOutcomeTm',max(awayPointsOutcomeTm),min(awayPointsOutcomeTm),sum(awayPointsOutcomeTm) / len(awayPointsOutcomeTm))
        # print('homePointsOutcomeOpp',max(homePointsOutcomeOpp),min(homePointsOutcomeOpp),sum(homePointsOutcomeOpp) / len(homePointsOutcomeOpp))
        # print('awayPointsOutcomeOpp',max(awayPointsOutcomeOpp),min(awayPointsOutcomeOpp),sum(awayPointsOutcomeOpp) / len(awayPointsOutcomeOpp))


        # homePointsOutcomeAvg = int((homePointsOutcomeTmAvg + awayPointsOutcomeOppAvg) / 2)
        # awayPointsOutcomeAvg = int((awayPointsOutcomeTmAvg + homePointsOutcomeOppAvg) / 2) 
        

        if homeWinLossOutcome > awayWinLossOutcome:
            percent = (1 - (awayWinLossOutcome / homeWinLossOutcome)) * 100   
            resultsFile.write("'")         
            resultsFile.write(homeTeamName)
            resultsFile.write(',')
            resultsFile.write(f'{round((homePointsOutcomeTmMax + awayPointsOutcomeOppMax) / 2,2)}')
            resultsFile.write(',')
            resultsFile.write(awayTeamName)
            resultsFile.write(',')
            resultsFile.write(f'{round((awayPointsOutcomeTmMin + homePointsOutcomeOppMin) / 2,2)}')
            resultsFile.write(',')
            resultsFile.write(str(round(percent,2)))
            resultsFile.write("',")
            resultsFile.write('\n')

            percentFile.write(f'{homeTeamName},{awayTeamName},\n')
       

        else:
            percent = (1 - (homeWinLossOutcome / awayWinLossOutcome)) * 100
            resultsFile.write("'")
            resultsFile.write(awayTeamName)
            resultsFile.write(',')
            resultsFile.write(f'{round((awayPointsOutcomeTmMax + homePointsOutcomeOppMax) / 2,2)}')
            resultsFile.write(',')
            resultsFile.write(homeTeamName)
            resultsFile.write(',')
            resultsFile.write(f'{round((homePointsOutcomeTmMin + awayPointsOutcomeOppMin) / 2,2)}')
            resultsFile.write(',')
            resultsFile.write(str(round(percent,2)))
            resultsFile.write("',")
            resultsFile.write('\n')

            percentFile.write(f'{awayTeamName},{homeTeamName},\n')
    
    def doit(self):
        readFilename = 'upcomingWeekData.txt'
        resultFilename = '../frontend/src/nflPages/results.js'
        percentageFilename = './percentages.txt'

        readFile = open(readFilename, 'r')
        resultsFile = open(resultFilename, 'w')
        percentFile = open(percentageFilename, 'a')
        resultsFile.write('export const weeklyResults = [\n')
        percentFile.write(f'{self.week + 1}\n')

        for matchup in readFile.readlines():

            awayTeam, homeTeam, time, day, channel, temp, weather, wind = matchup.split('_')
            wind = wind.strip()

            self.updateMatchup(awayTeam, homeTeam, time, day, channel, temp, weather, wind, resultsFile, percentFile)
            

        resultsFile.write('];')
        readFile.close()
        resultsFile.close()

        print('All matchups have been predicted!')











week = int(sys.argv[1])
year = 2023
table = 'productionNFL'

# storeDataObj = storeTeamData(table, week, year)
# storeDataObj.storeAllTeamsData()

# storeWeatherObj = updateWeatherData(table, week, year)
# startOfWeek = storeWeatherObj.doit()
# print('broken start of week ===> ', startOfWeek)

# month, day, year = startOfWeek.split('/')
# if day == 1:
#     month = int(month) - 1
#     day = '28'
# else:
#     day = int(day) - 1
# year = '20' + year

# resetStartOfWeek = f'{year}-{month}-{day}'
# resetStartOfWeek = '2023-10-18'

# storeGamblingObj = updateGamblingData(table, year)
# storeGamblingObj.doit(resetStartOfWeek)

# updatePercentages()

# storeUpcomingWeekData = getUpcomingWeekData(week, year)
# storeUpcomingWeekData.getWeatherByWeek()

predictions = getPredictions(week, year)
predictions.doit()