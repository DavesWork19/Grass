import sys
import requests
from bs4 import BeautifulSoup
import mysql.connector
import pandas as pd
import numpy as np
from datetime import datetime
import time
import csv
import random
from Legends import *

class updateGamblingData:

    def __init__(self, table, year):
        self.table = table
        self.year = year

    def saveData(self, column, data, awayTeam, homeTeam):
        mydb = mysql.connector.connect(
            host="127.0.0.1",
            user="davidcarney",
            password="Sinorrabb1t",
            database="NFL"
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

    def doit(self):
        df = pd.read_csv('gamblingData.csv')
        df = df[['Date','Home Team','Away Team','Neutral Venue?','Home Line Open','Home Line Min','Home Line Max','Home Line Close','Total Score Open','Total Score Min','Total Score Max','Total Score Close']]

        df['Neutral Venue?'] = df['Neutral Venue?'].fillna(0)
        df['Neutral Venue?'] = df['Neutral Venue?'].replace('Y',1)
        
        mydb = mysql.connector.connect(
            host="127.0.0.1",
            user="davidcarney",
            password="Sinorrabb1t",
            database="NFL"
            )

        mycursor = mydb.cursor()

        for index, row in df.iterrows():
            date, homeTeam, awayTeam, neutralVenue, homeLineOpen, homeLineMin, homeLineMax, homeLineClose, totalScoreOpen, totalScoreMin, totalScoreMax, totalScoreClose = row
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

            #print(date, gameLine, minMaxLine, totalScoreLine, minMaxTotalScoreLine, homeFavored, awayFavored)
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
            
        print(f"Updated gambling data.")

   
year = 2022
table = 'productionNFL'
obj = updateGamblingData(table, year)
obj.doit()


# years = [2016,2017,2018,2019,2020,2021,2022]
# for year in years:
#     print(year)
#     weeks = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17]
#     if year > 2020:
#         weeks.append(18)

#     for week in weeks:
#         print(week)

