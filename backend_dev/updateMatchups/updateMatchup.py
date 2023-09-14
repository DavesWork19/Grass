import requests
from bs4 import BeautifulSoup
import mysql.connector
import pandas as pd
from Legends import getDay, getTeam
from theBot2 import theBot


class getPredictions:
    def __init__(self, week, year):
        self.week = week
        self.year = year



    def teamService(self, teamNumber, time, day, at, oppTeamNumber, channel, temp, weather, wind):
        mydb = mysql.connector.connect(
            host="127.0.0.1",
            user="davidcarney",
            password="Sinorrabb1t",
            database="NFL"
            )

        mycursor = mydb.cursor()

        mycursor.execute(f"SELECT * FROM productionNFL WHERE HomeTeam = '{teamNumber}' and Year > 2017")

        teamData = mycursor.fetchall()
        dfColumns = ['id','Week','Day','WinLoss','OT','At','OppTeam','Tm','Opp','Cmp','AttPassing','YdsPassing','TDPassing','Interceptions','Sk','YdsLossFromSacks','YPerAPassing','NYPerA','CmpPerc','Rate','AttRushing','YdsRushing','YPerARushing','TDRushing','FGM','FGA','XPM','XPA','Pnt','YdsPunting','ThirdDConv','ThirdDAtt','FourthDConv','FourthDAtt','ToP','Year','Team','YardsPerPoint','HomeTeam','Time','Channel','Temp','Weather','Wind','gameLine','minMaxLine','totalScoreLine','minMaxTotalScoreLine','favored']
        teamDF = pd.DataFrame(teamData, columns = dfColumns)

        upcomingWeekData = [[self.week, time, day, at, oppTeamNumber, wind, temp, weather, channel, self.year]]
        upcomingWeekColumns = ['Week','Time','Day','At','OppTeam','Wind','Temp','Weather','Channel','Year']
        upcomingWeekDF = pd.DataFrame(upcomingWeekData, columns = upcomingWeekColumns)

        model = theBot(teamDF, upcomingWeekDF)
        model.adjustDF()

        #Run theBot code 3 times to keep adding to existing upcoming week DF
        predictions1 = model.useCode()
        predictions2 = model.useCode()
        predictions3 = model.useCode()


        return [predictions1,predictions2,predictions3]



    def updateMatchup(self, awayTeamName, homeTeamName, time, day, channel, temp, weather, wind, resultsFile):
        homeTeamNumber = getTeam(homeTeamName)
        awayTeamNumber = getTeam(awayTeamName)

        homeOutcome = 0
        awayOutcome = 0


        for i in range(12):

            homeTeamList = self.teamService(homeTeamNumber, time, day, 1, awayTeamNumber, channel, temp, weather, wind)
            awayTeamList = self.teamService(awayTeamNumber, time, day, 0, homeTeamNumber, channel, temp, weather, wind)

            homeOutcome = homeOutcome + ((homeTeamList[0][0][0] + homeTeamList[0][1][0]) / 2) + ((homeTeamList[1][0][0] + homeTeamList[1][1][0]) / 2) + ((homeTeamList[2][0][0] + homeTeamList[2][1][0]) / 2)
            awayOutcome = awayOutcome + ((awayTeamList[0][0][0] + awayTeamList[0][1][0]) / 2) + ((awayTeamList[1][0][0] + awayTeamList[1][1][0]) / 2) + ((awayTeamList[2][0][0] + awayTeamList[2][1][0]) / 2)

        if homeOutcome > awayOutcome:
            percent = (1 - (awayOutcome / homeOutcome)) * 100   
            resultsFile.write("'")         
            resultsFile.write(homeTeamName)
            resultsFile.write(',')
            resultsFile.write(awayTeamName)
            resultsFile.write(',')
            resultsFile.write(str(round(percent,2)))
            resultsFile.write("',")
            resultsFile.write('\n')

        else:
            percent = (1 - (homeOutcome / awayOutcome)) * 100
            resultsFile.write("'")
            resultsFile.write(awayTeamName)
            resultsFile.write(',')
            resultsFile.write(homeTeamName)
            resultsFile.write(',')
            resultsFile.write(str(round(percent,2)))
            resultsFile.write("',")
            resultsFile.write('\n')
        
        
        

    def doit(self):
        readFilename = "upcomingWeekData.txt"
        resultFilename = "../../frontend_production/src/pages/results.js"

        readFile = open(readFilename, "r")
        resultsFile = open(resultFilename, "w")
        resultsFile.write('export const weeklyResults = [\n')

        for matchup in readFile.readlines():

            awayTeam, homeTeam, time, day, channel, temp, weather, wind = matchup.split("_")
            wind = wind.strip()

            self.updateMatchup(awayTeam, homeTeam, time, day, channel, temp, weather, wind, resultsFile)

        resultsFile.write('];')
        readFile.close()
        resultsFile.close()


week = 1
year = 2023
obj = getPredictions(week, year)
obj.doit()
