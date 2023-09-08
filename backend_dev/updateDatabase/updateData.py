import sys
import requests
from bs4 import BeautifulSoup
import mysql.connector
import pandas as pd
import numpy as np
from datetime import datetime
import time

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
        host="127.0.0.1",
        user="davidcarney",
        password="Sinorrabb1t",
        database="NFL"
        )

        mycursor = mydb.cursor()

        for index, row in df.iterrows():
            if row[6] != 0:
                yardsPerPoint = (row[10] + row[20]) / row[6]
            else:
                yardsPerPoint = 0

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

        URL = f"https://www.pro-football-reference.com/teams/{team}/{self.year}/gamelog/"
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
        time.sleep(10)
        soup = BeautifulSoup(page.content, 'html.parser')
        time.sleep(10)
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

            print(f"{num}. {team} updated.")


#For each game in a week
#Go to website and scrape all data (all games in a week)
#Find all weather data for each game that week
#Save data to database
class updateWeatherData:

    def __init__(self, table, week, year):
        self.table = table
        self.week = week
        self.year = year

    def addData(self, data, homeTeam, awayTeam):
        mydb = mysql.connector.connect(
            host="127.0.0.1",
            user="davidcarney",
            password="Sinorrabb1t",
            database="NFL"
            )

        mycursor = mydb.cursor()

        for column in data:
            insertValues = (
                f"UPDATE {self.table} "
                f"SET {column} = {data[column]} "
                f"WHERE (HomeTeam = {getTeam(homeTeam)}) and (OppTeam = {getTeam(awayTeam)}) and (Year = {self.year})"
            )

            mycursor.execute(insertValues)
            mydb.commit()

            insertValues = (
                f"UPDATE {self.table} "
                f"SET {column} = {data[column]} "
                f"WHERE (HomeTeam = {getTeam(awayTeam)}) and (OppTeam = {getTeam(homeTeam)}) and (Year = {self.year})"
            )

            mycursor.execute(insertValues)
            mydb.commit()

    def getWeatherByWeek(self):
        URL = f"https://www.nflweather.com/week/{self.year}/week-{self.week}"
        HEADERS = {
            'User-Agent': 'Safari/537.36',
        }
        page = requests.get(URL, headers=HEADERS)
        soup = BeautifulSoup(page.content, 'html.parser')
        moreSoup = soup.find('div', class_='container-game-box')

        matchUp = moreSoup.div 
        while matchUp != None:
            matchUpData1 = matchUp.div
            #dateAndTime = matchUpData1.div.text.strip()

            matchUpData2 = matchUpData1.next_sibling.next_sibling
            awayTeam, at, homeTeam = matchUpData2.find_all('span')
            awayTeam = awayTeam.text
            homeTeam = homeTeam.text
            
            matchUpData3 = matchUpData2.next_sibling.next_sibling
            weatherData = matchUpData3.div.div.next_sibling.next_sibling
            temp, weather = weatherData.find_all('span')
            temp = getTemp(int(temp.text.split(' ')[0]))
            weather = getWeather(weather.text)

            windDataContainer = weatherData.next_sibling.next_sibling
            windData = windDataContainer.find_all('span')
            windDataLength = len(windData)
            wind = 0
            if windDataLength == 3:
                wind = windData[1].text.split(' ')[0]

            channelData = windDataContainer.next_sibling.next_sibling
            channels = channelData.find_all('span')
            channelsLength = len(channels)
            channel = 0
            if channelsLength == 2:
                channel = channels[1].text
                if ',' in channel:
                    channel = channel.split(',')[0]
                channel = getChannel(channel)


            data = {'Channel':channel,'Temp':temp,'Weather':weather,'Wind':wind}
            print(data)
            self.addData(data, homeTeam, awayTeam)

            matchUp = matchUp.next_sibling.next_sibling

    def doit(self):
        self.getWeatherByWeek()
        print(f"Saved Week: {self.week} for Year: {self.year}")


#For each game after given date
#Go to website and store data from excel sheet into pandas df
#Find all gambling data for each game after week start
#Save data to database
class updateGamblingData:

    def __init__(self, table, year):
        self.table = table
        self.year = year

    def saveData(self, column, data):
        insertValues = (
            f"UPDATE {self.table} "
            f"SET {column} = {data} "
            f"WHERE (HomeTeam = {getTeam(homeTeam)}) and (OppTeam = {getTeam(awayTeam)}) and (Year = {self.year})"
        )
        mycursor.execute(insertValues)
        mydb.commit()
        insertValues = (
            f"UPDATE {self.table} "
            f"SET {column} = {data} "
            f"WHERE (HomeTeam = {getTeam(homeTeam)}) and (OppTeam = {getTeam(homeTeam)}) and (Year = {self.year})"
        )
        mycursor.execute(insertValues)
        mydb.commit()

    def getDF(self, startOfWeek):
        URL = f"https://www.aussportsbetting.com/data/historical-nfl-results-and-odds-data/"
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

        df = df[df['Date'] > np.array(np.datetime64(startOfWeek))]
        df = df[['Home Team','Away Team','Neutral Venue?','Home Line Open','Home Line Min','Home Line Max','Home Line Close','Total Score Open','Total Score Min','Total Score Max','Total Score Close']]

        df['Neutral Venue?'] = df['Neutral Venue?'].fillna(0)
        df['Neutral Venue?'] = df['Neutral Venue?'].replace('Y',1)

        return df

    def doit(self, startWeek):
        df = self.getDF(startWeek)
        
        mydb = mysql.connector.connect(
            host="127.0.0.1",
            user="davidcarney",
            password="Sinorrabb1t",
            database="NFL"
            )

        mycursor = mydb.cursor()

        for index, row in df.iterrows():
            homeTeam, awayTeam, neutralVenue, homeLineOpen, homeLineMin, homeLineMax, homeLineClose, totalScoreOpen, totalScoreMin, totalScoreMax, totalScoreClose = row
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

            print(gameLine, minMaxLine, totalScoreLine, minMaxTotalScoreLine, homeFavored, awayFavored)
            #Save gameLine
            saveData('gameLine', gameLine)
            
            #Save minMaxLine
            saveData('minMaxLine', minMaxLine)

            #Save totalScoreLine
            saveData('totalScoreLine', totalScoreLine)

            #Save minMaxTotalScoreLine
            saveData('minMaxTotalScoreLine', minMaxTotalScoreLine)

            #Save favored data
            insertValues = (
                f"UPDATE {self.table} "
                f"SET favored = {homeFavored} "
                f"WHERE (HomeTeam = {getTeam(homeTeam)}) and (OppTeam = {getTeam(awayTeam)}) and (Year = {self.year})"
            )
            mycursor.execute(insertValues)
            mydb.commit()
            insertValues = (
                f"UPDATE {self.table} "
                f"SET favored = {awayFavored}"
                f"WHERE (HomeTeam = {getTeam(homeTeam)}) and (OppTeam = {getTeam(homeTeam)}) and (Year = {self.year})"
            )
            mycursor.execute(insertValues)
            mydb.commit()
            
        print(f"Updated gambling data.")

        



class getUpcomingWeekData:
    def __init__(self, week, year):
        self.week = week + 1
        self.year = year
  
    def getWeatherByWeek(self):
        upcomingWeekBackendFilename = "../updateMatchups/upcomingWeekData.txt"
        upcomingWeekFrontendFilename = '../../frontend_production/src/upcomingWeekData.js'
        upcomingWeekBackendFile = open(upcomingWeekBackendFilename, "w")
        upcomingWeekFrontendFile = open(upcomingWeekFrontendFilename, 'w')
        upcomingWeekFrontendFile.write('export const upcomingWeekData = [\n')

        URL = f"https://www.nflweather.com/week/{self.year}/week-{self.week}"
        HEADERS = {
            'User-Agent': 'Safari/537.36',
        }
        page = requests.get(URL, headers=HEADERS)
        soup = BeautifulSoup(page.content, 'html.parser')
        moreSoup = soup.find('div', class_='container-game-box')

        matchUp = moreSoup.div 
        while matchUp != None:
            matchUpData1 = matchUp.div
            dateAndTime = matchUpData1.div.text.strip()

            matchUpData2 = matchUpData1.next_sibling.next_sibling
            awayTeam, at, homeTeam = matchUpData2.find_all('span')
            awayTeam = awayTeam.text
            homeTeam = homeTeam.text
            
            matchUpData3 = matchUpData2.next_sibling.next_sibling
            weatherData = matchUpData3.div.div.next_sibling.next_sibling
            temp, weather = weatherData.find_all('span')
            temp = int(temp.text.split(' ')[0])
            weather = weather.text

            windDataContainer = weatherData.next_sibling.next_sibling
            windData = windDataContainer.find_all('span')
            windDataLength = len(windData)
            wind = 0
            if windDataLength == 3:
                wind = windData[1].text.split(' ')[0]

            channelData = windDataContainer.next_sibling.next_sibling
            channels = channelData.find_all('span')
            channelsLength = len(channels)
            channel = 0
            if channelsLength == 2:
                channel = channels[1].text
                if ',' in channel:
                    channel = channel.split(',')[0]
                channel = getChannel(channel)

            upcomingWeekBackendFile.write(homeTeam)
            upcomingWeekBackendFile.write("_")
            upcomingWeekBackendFile.write(awayTeam)
            upcomingWeekBackendFile.write("_")
            upcomingWeekBackendFile.write(dateAndTime)
            upcomingWeekBackendFile.write("_")
            upcomingWeekBackendFile.write(f'{channel}')
            upcomingWeekBackendFile.write("_")
            upcomingWeekBackendFile.write(f'{getTemp(temp)}')
            upcomingWeekBackendFile.write("_")
            upcomingWeekBackendFile.write(f'{getWeather(weather)}')
            upcomingWeekBackendFile.write("_")
            upcomingWeekBackendFile.write(f'{wind}')
            upcomingWeekBackendFile.write("\n")

            upcomingWeekFrontendFile.write("'")
            upcomingWeekFrontendFile.write(dateAndTime)
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


week = int(sys.argv[1])
year = 2023
table = "NFLRegularSeasons"
startOfWeek = '2022-11-30'

# storeDataObj = storeTeamData(table, week, year)
# storeDataObj.storeAllTeamsData()

# storeWeatherObj = updateWeatherData(table, week, year)
# storeWeatherObj.doit()

# storeGamblingObj = updateGamblingData(table, year)
# storeGamblingObj.doit(startOfWeek)

storeUpcomingWeekData = getUpcomingWeekData(week, year)
storeUpcomingWeekData.getWeatherByWeek()
