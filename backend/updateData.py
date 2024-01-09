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


    def doit(self):
        self.getWeatherByWeek()
        print(f'Upcoming week (week : {self.week}) data has been saved to database!')



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
        teamDataFilename = 'teamDataHolder.txt'
        upcomingWeekBackendFile = open(upcomingWeekBackendFilename, 'w')
        upcomingWeekFrontendFile = open(upcomingWeekFrontendFilename, 'w')
        teamDataFile = open(teamDataFilename, 'w')
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
        #teamDF = teamDF.drop(columns=['favored'])
        #teamDF = teamDF.drop(columns=['Channel','Temp','Weather','Wind','favored'])

        #favoredTeams = ['pit', 'kan', 'rav', 'nor', 'cle','atl','htx','nwe','gnb','clt','phi', 'nyg','cin', 'sdg']

        # upcomingWeekData = None
        # if at == 0:
        #     # if getTeamSmallNameFromTeam(teamNumber) in favoredTeams:
        #     #     upcomingWeekData = [[self.week, time, day, at, oppTeamNumber, wind, temp, weather, channel, self.year, 1]]
        #     # else:
        #     upcomingWeekData = [[self.week, time, day, at, oppTeamNumber, wind, temp, weather, channel, self.year]]
            
        # else:
        #     # if getTeamSmallNameFromTeam(teamNumber) in favoredTeams:
        #     #     upcomingWeekData = [[self.week, time, day, at, oppTeamNumber, wind, temp, weather, channel, self.year, 1]]
        #     # else:
        upcomingWeekData = [[self.week, time, day, at, oppTeamNumber, wind, temp, weather, channel, self.year]]
        #upcomingWeekData = [[self.week, time, day, at, oppTeamNumber, self.year]]
        

        
        upcomingWeekColumns = ['Week','Time','Day','At','OppTeam', 'Wind', 'Temp', 'Weather', 'Channel','Year']
        #upcomingWeekColumns = ['Week','Time','Day','At','OppTeam','Year']
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
            resultsFile.write(f'{getDayFromCode(str(day))}')
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
            resultsFile.write(f'{getDayFromCode(str(day))}')
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




def updateTeamData(week):
    week = week + 1
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
            if weekOrYear == 2023:
                passedYear = True
            if (weekOrYear == week) and (passedYear == True):
                passedWeek = True
        elif (passedWeek == True) and (passedYear == True):
            predictions.append([line[0],line[1]])
    teamDataFile.write(f'{week}\n')
    for (teamDataLine, predLine) in zip(teamDataHolderFile, predictions):
        teamDataFile.write(f'{teamDataLine.rstrip()}_{predLine[0]}_{predLine[1]}_\n')








week = int(sys.argv[1])
year = 2023
table = 'productionNFL'

storeDataObj = storeTeamData(table, week, year)
storeDataObj.storeAllTeamsData()

storeWeatherObj = updateWeatherData(table, week, year)
storeWeatherObj.doit()

resetStartOfWeek = '2023-12-27'

storeGamblingObj = updateGamblingData(table, year)
storeGamblingObj.doit(resetStartOfWeek)

updatePercentages()

storeUpcomingWeekData = getUpcomingWeekData(week, year)
storeUpcomingWeekData.getWeatherByWeek()

predictions = getPredictions(week, year)
predictions.doit()

updateTeamData(week)