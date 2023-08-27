import requests
from bs4 import BeautifulSoup
import mysql.connector
import pandas as pd
from Legends import getDay, getTeamNumber
from theBot2 import theBot


class getPredictions:
    def __init__(self, week, year):
        self.week = week
        self.year = year



    def teamService(self, teamNumber, day, at, oppTeamNumber, channel, temp, sky, wind):
        mydb = mysql.connector.connect(
            host="127.0.0.1",
            user="davidcarney",
            password="Sinorrabb1t",
            database="NFL"
            )

        mycursor = mydb.cursor()

        mycursor.execute(f"SELECT * FROM NFLRegularSeasons WHERE HomeTeam = '{teamNumber}'")

        teamData = mycursor.fetchall()

        dfColumns = ['ID','Week','Day','WinLoss','OT','At','OppTeam','Tm','Opp','Cmp','AttPassing','YdsPassing','TDPassing','Interceptions','Sk','YdsLossFromSacks','YPerAPassing','NYPerA','CmpPerc','Rate','AttRushing','YdsRushing','YPerARushing','TDRushing','FGM','FGA','XPM','XPA','Pnt','YdsPunting','ThirdDConv','ThirdDAtt','FourthDConv','FourthDAtt','ToP','Year','Team','YardsPerPoint','HomeTeam','Wind','Temp','Sky','Channel','GameLines','NeutralVenue','TotalScore']
        upcomingWeekColumns = ['Week','Day','At','OppTeam','Wind','Temp','Sky','Channel','Year']
        upcomingWeekData = [[self.week, day, at, oppTeamNumber, wind, temp, sky, channel, self.year]]

        teamDF = pd.DataFrame(teamData, columns = dfColumns)
        upcomingWeekDF = pd.DataFrame(upcomingWeekData, columns = upcomingWeekColumns)

        model = theBot(teamDF, upcomingWeekDF)
        model.adjustDF()

        #Run theBot code 3 times to keep adding to existing upcoming week DF
        predictions1 = model.useCode()
        predictions2 = model.useCode()
        predictions3 = model.useCode()


        return [predictions1,predictions2,predictions3]



    def updateMatchup(self, homeTeamName, awayTeamName, day, channel, temp, sky, wind, resultsFile):
        homeTeamNumber = getTeamNumber(homeTeamName)
        awayTeamNumber = getTeamNumber(awayTeamName)
        dayNumber = getDay(day)

        homeOutcome = 0
        awayOutcome = 0


        for i in range(12):

            homeTeamList = self.teamService(homeTeamNumber, dayNumber, 1, awayTeamNumber, channel, temp, sky, wind)
            awayTeamList = self.teamService(awayTeamNumber, dayNumber, 0, homeTeamNumber, channel, temp, sky, wind)

            homeOutcome = homeOutcome + ((homeTeamList[0][0][0] + homeTeamList[0][1][0]) / 2) + ((homeTeamList[1][0][0] + homeTeamList[1][1][0]) / 2) + ((homeTeamList[2][0][0] + homeTeamList[2][1][0]) / 2)
            awayOutcome = awayOutcome + ((awayTeamList[0][0][0] + awayTeamList[0][1][0]) / 2) + ((awayTeamList[1][0][0] + awayTeamList[1][1][0]) / 2) + ((awayTeamList[2][0][0] + awayTeamList[2][1][0]) / 2)



        if homeOutcome > awayOutcome:
            percent = (1 - (awayOutcome / homeOutcome)) * 100

            resultsFile.write(homeTeamName)
            resultsFile.write(',')
            resultsFile.write(awayTeamName)
            resultsFile.write(',')
            resultsFile.write(str(round(percent,2)))
            resultsFile.write('\n')
        else:
            percent = (1 - (homeOutcome / awayOutcome)) * 100

            resultsFile.write(awayTeamName)
            resultsFile.write(',')
            resultsFile.write(homeTeamName)
            resultsFile.write(',')
            resultsFile.write(str(round(percent,2)))
            resultsFile.write('\n')



    def doit(self):
        readFilename = "upcomingWeekData.txt"
        resultFilename = "../frontend/src/pages/results.txt"

        readFile = open(readFilename, "r")
        resultsFile = open(resultFilename, "w")

        for matchup in readFile.readlines():

            homeTeam, awayTeam, day, channel, temp, sky, wind = matchup.split("_")
            wind = wind.strip()

            self.updateMatchup(homeTeam, awayTeam, day, channel, temp, sky, wind, resultsFile)


        readFile.close()
        resultsFile.close()


week = 14
year = 2022
obj = getPredictions(week, year)
obj.doit()
