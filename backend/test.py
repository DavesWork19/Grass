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
thisWeek = False
month = 'Oct'
day = 31
updatedDate = datetime.strptime(f'{month}/{day}/2024', '%b/%d/%Y')

start, end = ALL_WEEKS[9]
startMonth, startDay = start.split('/')
startDate = datetime.strptime(f'{startMonth}/{startDay}/2024', '%m/%d/%Y')
endMonth, endDay = end.split('/')
endDate = datetime.strptime(f'{endMonth}/{endDay}/2024', '%m/%d/%Y')

print(startDate, endDate)

if (startDate <= updatedDate) and (endDate >= updatedDate):
    thisWeek = True




print(thisWeek)





# mydb = mysql.connector.connect(
#     host='127.0.0.1',
#     user='davidcarney',
#     password='Sinorrabb1t',
#     database='NFL'
# )
# mycursor = mydb.cursor()

# mycursor.execute("SELECT DateTime, Week, At, OppTeam, Team, spread, total, spreadCalculated, totalCalculated, spreadCovered, totalCovered FROM productionNFL WHERE spreadCalculated is NOT NULL and spreadCovered is NOT NULL")
# columns = ['DateTime', 'Week', 'At', 'OppTeam', 'Team', 'spread', 'total', 'spreadCalculated', 'totalCalculated', 'spreadCovered', 'totalCovered']
# teamData = mycursor.fetchall()
# percentages = pd.DataFrame(teamData, columns = columns)

# percentData = {}
# for team in ALL_TEAMS:
#     team = getTeamName(getTeamFromSmallName(team))
#     percentData[f'{team}_spread'] = [0,0]
#     percentData[f'{team}_total'] = [0,0]

#     percentData[f'{team}_home_spread'] = [0,0]
#     percentData[f'{team}_away_spread'] = [0,0]
#     percentData[f'{team}_home_total'] = [0,0]
#     percentData[f'{team}_away_total'] = [0,0]

# for week in ALL_WEEKS:
#     percentData[f'Week_{week}_spread'] = [0,0]
#     percentData[f'Week_{week}_total'] = [0,0]

# percentData['home_spread'] = [0,0]
# percentData['away_spread'] = [0,0]
# percentData['home_total'] = [0,0]
# percentData['away_total'] = [0,0]

# percentData['overall_spread'] = [0,0]
# percentData['overall_total'] = [0,0]


# for stat in percentages.iterrows():
#     stat = stat[1]
#     dateTime, week, at, oppTeam, team, spread, total, spreadCalculated, totalCalculated, spreadCovered, totalCovered = stat
#     team = getTeamName(getTeamFromSmallName(team))

#     if spreadCalculated == spreadCovered:
#         percentData[f'{team}_spread'] = [percentData[f'{team}_spread'][0] + 100, percentData[f'{team}_spread'][1] + 1]
#         percentData[f'Week_{week}_spread'] = [percentData[f'Week_{week}_spread'][0] + 100, percentData[f'Week_{week}_spread'][1] + 1]
#         percentData['overall_spread'] = [percentData['overall_spread'][0] + 100, percentData['overall_spread'][1] + 1]

#         if at:
#             percentData[f'{team}_home_spread'] = [percentData[f'{team}_home_spread'][0] + 100, percentData[f'{team}_home_spread'][1] + 1]
#             percentData['home_spread'] = [percentData['home_spread'][0] + 100, percentData['home_spread'][1] + 1]
#         else:
#             percentData[f'{team}_away_spread'] = [percentData[f'{team}_away_spread'][0] + 100, percentData[f'{team}_away_spread'][1] + 1]
#             percentData['away_spread'] = [percentData['away_spread'][0] + 100, percentData['away_spread'][1] + 1]

#     else:
#         percentData[f'{team}_spread'] = [percentData[f'{team}_spread'][0], percentData[f'{team}_spread'][1] + 1]
#         percentData[f'Week_{week}_spread'] = [percentData[f'Week_{week}_spread'][0], percentData[f'Week_{week}_spread'][1] + 1]
#         percentData['overall_spread'] = [percentData['overall_spread'][0], percentData['overall_spread'][1] + 1]

#         if at:
#             percentData[f'{team}_home_spread'] = [percentData[f'{team}_home_spread'][0], percentData[f'{team}_home_spread'][1] + 1]
#             percentData['home_spread'] = [percentData['home_spread'][0], percentData['home_spread'][1] + 1]
#         else:
#             percentData[f'{team}_away_spread'] = [percentData[f'{team}_away_spread'][0], percentData[f'{team}_away_spread'][1] + 1]
#             percentData['away_spread'] = [percentData['away_spread'][0], percentData['away_spread'][1] + 1]

    
#     if totalCalculated == totalCovered:
#         percentData[f'{team}_total'] = [percentData[f'{team}_total'][0] + 100, percentData[f'{team}_total'][1] + 1]
#         percentData[f'Week_{week}_total'] = [percentData[f'Week_{week}_total'][0] + 100, percentData[f'Week_{week}_total'][1] + 1]
#         percentData['overall_total'] = [percentData['overall_total'][0] + 100, percentData['overall_total'][1] + 1]

#         if at:
#             percentData[f'{team}_home_total'] = [percentData[f'{team}_home_total'][0] + 100, percentData[f'{team}_home_total'][1] + 1]
#             percentData['home_total'] = [percentData['home_total'][0] + 100, percentData['home_total'][1] + 1]
#         else:
#             percentData[f'{team}_away_total'] = [percentData[f'{team}_away_total'][0] + 100, percentData[f'{team}_away_total'][1] + 1]
#             percentData['away_total'] = [percentData['away_total'][0] + 100, percentData['away_total'][1] + 1]


#     else:
#         percentData[f'{team}_total'] = [percentData[f'{team}_total'][0], percentData[f'{team}_total'][1] + 1]
#         percentData[f'Week_{week}_total'] = [percentData[f'Week_{week}_total'][0], percentData[f'Week_{week}_total'][1] + 1]
#         percentData['overall_total'] = [percentData['overall_total'][0], percentData['overall_total'][1] + 1]

#         if at:
#             percentData[f'{team}_home_total'] = [percentData[f'{team}_home_total'][0], percentData[f'{team}_home_total'][1] + 1]
#             percentData['home_total'] = [percentData['home_total'][0], percentData['home_total'][1] + 1]
#         else:
#             percentData[f'{team}_away_total'] = [percentData[f'{team}_away_total'][0], percentData[f'{team}_away_total'][1] + 1]
#             percentData['away_total'] = [percentData['away_total'][0], percentData['away_total'][1] + 1]


# for data in percentData:
#     try:
#         percentData[data] = round(percentData[data][0] / percentData[data][1], 2)
#     except:
#         percentData[data] = -1

    
# for data in percentData:
#     print(data,percentData[data])


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


    



