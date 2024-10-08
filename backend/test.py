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

from theBot2 import theBot
from Legends import *
from constants import *



# mydb = mysql.connector.connect(
#     host='127.0.0.1',
#     user='davidcarney',
#     password='Sinorrabb1t',
#     database='NFL'
#     )
# mycursor = mydb.cursor()

# mycursor.execute("SELECT * FROM productionNFL WHERE spread is not NULL and tm is not NULL and (totalCovered is NULL or spreadCovered is NULL)")

# teamData = mycursor.fetchall()
# nextGames = pd.DataFrame(teamData, columns = ALL_COLUMNS)
# for game in nextGames.iterrows():
#     game = game[1]
#     id = game['id']
#     teamPoints = int(game['Tm'])
#     oppTeamPoints = int(game['Opp'])
#     spread = game['spread']
#     total = float(game['total'])
#     spreadSign = spread[0]
#     spreadValue = None

#     #OverUnder
#     if teamPoints + oppTeamPoints >= total:
#         mycursor.execute(f'UPDATE productionNFL SET totalCovered = 1 WHERE id = {id}')
#         mydb.commit()
#     else:
#         mycursor.execute(f'UPDATE productionNFL SET totalCovered = 0 WHERE id = {id}')
#         mydb.commit()


#     #Spread
#     if spread != 'pk':
#         spreadValue = float(spread[1:])

#     if spreadSign == '-':
#         if teamPoints - oppTeamPoints >= spreadValue:
#             mycursor.execute(f'UPDATE productionNFL SET spreadCovered = 1 WHERE id = {id}')
#             mydb.commit()
#         else:
#             mycursor.execute(f'UPDATE productionNFL SET spreadCovered = 0 WHERE id = {id}')
#             mydb.commit()

#     elif spreadSign == '+':
#         if -(teamPoints - oppTeamPoints) <= spreadValue:
#             mycursor.execute(f'UPDATE productionNFL SET spreadCovered = 1 WHERE id = {id}')
#             mydb.commit()
#         else:
#             mycursor.execute(f'UPDATE productionNFL SET spreadCovered = 0 WHERE id = {id}')
#             mydb.commit()
#     else:
#         if teamPoints - oppTeamPoints >= 0:
#             mycursor.execute(f'UPDATE productionNFL SET spreadCovered = 1 WHERE id = {id}')
#             mydb.commit()
#         else:
#             mycursor.execute(f'UPDATE productionNFL SET spreadCovered = 0 WHERE id = {id}')
#             mydb.commit()


week = 2














parlayCoin = [1,3]
parlayNumbers = [1,2,3,4,5,6,7,8,9,10]

mydb = mysql.connector.connect(
        host='127.0.0.1',
    user='davidcarney',
    password='Sinorrabb1t',
    database='NFL'
)
mycursor = mydb.cursor()

for team in ALL_TEAMS:
    mycursor.execute(f"SELECT Week, Day, Team, spread, spreadCalculated, spreadCovered, total, totalCalculated, totalCovered FROM productionNFL WHERE totalCovered is not NULL and totalCalculated is not NULL and team = '{team}'")
    columns = ['Week', 'Day', 'Team', 'spread', 'spreadCalculated', 'spreadCovered', 'total', 'totalCalculated', 'totalCovered']
    allDataDB = mycursor.fetchall()
    allData = pd.DataFrame(allDataDB, columns = columns)

    print(allData)

    break


# for parlay in range(1,5):
#     callsFileName = f'../frontend/src/nflPages/parlay{parlay}Calls.js'

#     callsFile = open(callsFileName, 'w')
#     resultsFile = open(resultsFileName, 'a')

#     for team in ALL_TEAMS:
#         mycursor.execute(f"SELECT Week, Day, Team, spread, spreadCalculated, spreadCovered, total, totalCalculated, totalCovered FROM productionNFL WHERE totalCovered is not NULL and totalCalculated is not NULL and team = '{team}'")
#         columns = ['Week', 'Day', 'Team', 'spread', 'spreadCalculated', 'spreadCovered', 'total', 'totalCalculated', 'totalCovered']
#         allDataDB = mycursor.fetchall()
#         allData = pd.DataFrame(allDataDB, columns = columns)

#         mycursor.execute(f"SELECT Week, Day, Team, spread, spreadCalculated, spreadCovered, total, totalCalculated, totalCovered FROM productionNFL WHERE winLoss is NULL and team = '{team}'")
#         columns = ['Week', 'Day', 'Team', 'spread', 'spreadCalculated', 'spreadCovered', 'total', 'totalCalculated', 'totalCovered']
#         allDataDB = mycursor.fetchall()
#         newData = pd.DataFrame(allDataDB, columns = columns)


#         totalCounter = [0,0]
#         spreadCounter = [0,0]

#         for row in range(len(allData['totalCovered'])):
#             if allData['totalCalculated'][row] == allData['totalCovered'][row]:
#                 totalCounter = [totalCounter[0] + 100, totalCounter[1] + 1]
#             elif allData['totalCalculated'][row] != allData['totalCovered'][row]:
#                 totalCounter = [totalCounter[0], totalCounter[1] + 1]
        
#             if allData['spreadCalculated'][row] == allData['spreadCovered'][row]:
#                 spreadCounter = [spreadCounter[0] + 100, spreadCounter[1] + 1]
#             elif allData['spreadCalculated'][row] != allData['spreadCovered'][row]:
#                 spreadCounter = [spreadCounter[0], spreadCounter[1] + 1]

#         totalCounted = totalCounter[0]/totalCounter[1]
#         spreadCounted = spreadCounter[0]/spreadCounter[1]

#         if parlay == 1:
            
        
#         elif parlay == 2:

#         elif parlay == 3:
#             if random.choice(parlayCoin) == 3:
#                 callsFile.write("'")
#                 callsFile.write(getTeamName(getTeamFromSmallName(team)))
#                 callsFile.write('_')
#                 callsFile.write(newData['spread'])
#                 callsFile.write('_')
#                 callsFile.write(awayTeam)
#                 callsFile.write('_')
#                 callsFile.write(homeTeam)
#                 callsFile.write('_')
#                 callsFile.write(teamName)
#                 callsFile.write('_')
#                 callsFile.write(spread)
#                 callsFile.write('_')
#                 callsFile.write(str(spreadCalculated))
#                 callsFile.write('_')
#                 callsFile.write(total)
#                 callsFile.write('_')
#                 callsFile.write(str(totalCalculated))
#                 callsFile.write("',")
#                 callsFile.write('\n')

#     callsFile.write('];')
#     callsFile.close()


    



