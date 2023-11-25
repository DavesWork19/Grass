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



#Scenarios 
#1. Away team stats - win percentage of when model correctly predicts game when they play away
#2. Home team stats - how well team is predicted when they play at home
#3. Day stats - percentage of model accuracy of team when they play of specific day
#4. Conference stats
#5 Division stats


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







# matchups = []

# groups = {'AFC North': ['Ravens', 'Bengals', 'Browns', 'Steelers'], 'AFC South': ['Titans', 'Colts', 'Jaguars', 'Texans'], 'AFC East': ['Bills', 'Jets', 'Dolphins', 'Patriots'], 'AFC West': ['Cheifs', 'Chargers', 'Broncos', 'Raiders'], 'AFC': ['Ravens', 'Bengals', 'Browns', 'Steelers', 'Titans', 'Colts', 'Jaguars', 'Texans', 'Bills', 'Jets', 'Dolphins', 'Patriots', 'Cheifs', 'Chargers', 'Broncos', 'Raiders'], 'NFC North': ['Vikings', 'Packers', 'Bears', 'Lions'], 'NFC South': ['Buccaneers', 'Falcons', 'Saints', 'Panthers'], 'NFC East': ['Cowboys', 'Giants', 'Eagles', 'Washington'], 'NFC West': ['49ers', 'Rams', 'Seahawks', 'Cardinals'], 'NFC': ['Vikings', 'Packers', 'Bears', 'Lions', 'Buccaneers', 'Falcons', 'Saints', 'Panthers', 'Cowboys', 'Giants', 'Eagles', 'Washington', '49ers', 'Rams', 'Seahawks', 'Cardinals']}
# results = {'AFC':[0,0], 'AFC North':[0,0], 'AFC South':[0,0], 'AFC East':[0,0], 'AFC West':[0,0], 'NFC':[0,0], 'NFC North':[0,0], 'NFC South':[0,0], 'NFC East':[0,0], 'NFC West':[0,0]}
# week = 0
# year = 0

# for line in fileRead.readlines():
#     data = line.split(',')
#     dataLength = len(data)

#     if dataLength > 1:
#         predictedWinner = data[0]
#         predictedLoser = data[1]
#         outcome = data[2][0]

#         if outcome == '1':
#             if predictedWinner not in results:
#                 results[predictedWinner] = [100,1]
#             else:
#                 results[predictedWinner] = [results[predictedWinner][0] + 100, results[predictedWinner][1] + 1]

#             if predictedLoser not in results:
#                 results[predictedLoser] = [100,1]
#             else:
#                 results[predictedLoser] = [results[predictedLoser][0] + 100, results[predictedLoser][1] + 1]


#             if predictedWinner in groups['AFC']:
#                 results['AFC'] = [results['AFC'][0]  + 100, results['AFC'][1] + 1]

#                 if predictedWinner in groups['AFC North']:
#                     results['AFC North'] = [results['AFC North'][0]  + 100, results['AFC North'][1] + 1]
#                 elif predictedWinner in groups['AFC South']:
#                     results['AFC South'] = [results['AFC South'][0]  + 100, results['AFC South'][1] + 1]
#                 elif predictedWinner in groups['AFC East']:
#                     results['AFC East'] = [results['AFC East'][0]  + 100, results['AFC East'][1] + 1]
#                 elif predictedWinner in groups['AFC West']:
#                     results['AFC West'] = [results['AFC West'][0]  + 100, results['AFC West'][1] + 1]

#             elif predictedWinner in groups['NFC']:
#                 results['NFC'] = [results['NFC'][0]  + 100, results['NFC'][1] + 1]

#                 if predictedWinner in groups['NFC North']:
#                     results['NFC North'] = [results['NFC North'][0]  + 100, results['NFC North'][1] + 1]
#                 elif predictedWinner in groups['NFC South']:
#                     results['NFC South'] = [results['NFC South'][0]  + 100, results['NFC South'][1] + 1]
#                 elif predictedWinner in groups['NFC East']:
#                     results['NFC East'] = [results['NFC East'][0]  + 100, results['NFC East'][1] + 1]
#                 elif predictedWinner in groups['NFC West']:
#                     results['NFC West'] = [results['NFC West'][0]  + 100, results['NFC West'][1] + 1]

#             if predictedLoser in groups['AFC']:
#                 results['AFC'] = [results['AFC'][0]  + 100, results['AFC'][1] + 1]

#                 if predictedLoser in groups['AFC North']:
#                     results['AFC North'] = [results['AFC North'][0]  + 100, results['AFC North'][1] + 1]
#                 elif predictedLoser in groups['AFC South']:
#                     results['AFC South'] = [results['AFC South'][0]  + 100, results['AFC South'][1] + 1]
#                 elif predictedLoser in groups['AFC East']:
#                     results['AFC East'] = [results['AFC East'][0]  + 100, results['AFC East'][1] + 1]
#                 elif predictedLoser in groups['AFC West']:
#                     results['AFC West'] = [results['AFC West'][0]  + 100, results['AFC West'][1] + 1]

#             elif predictedLoser in groups['NFC']:
#                 results['NFC'] = [results['NFC'][0]  + 100, results['NFC'][1] + 1]

#                 if predictedLoser in groups['NFC North']:
#                     results['NFC North'] = [results['NFC North'][0]  + 100, results['NFC North'][1] + 1]
#                 elif predictedLoser in groups['NFC South']:
#                     results['NFC South'] = [results['NFC South'][0]  + 100, results['NFC South'][1] + 1]
#                 elif predictedLoser in groups['NFC East']:
#                     results['NFC East'] = [results['NFC East'][0]  + 100, results['NFC East'][1] + 1]
#                 elif predictedLoser in groups['NFC West']:
#                     results['NFC West'] = [results['NFC West'][0]  + 100, results['NFC West'][1] + 1]

#             results[f'{year} Week {week}'] = [results[f'{year} Week {week}'][0] + 100, results[f'{year} Week {week}'][1] + 1]

#         else:
#             if predictedWinner not in results:
#                 results[predictedWinner] = [0,1]
#             else:
#                 results[predictedWinner] = [results[predictedWinner][0] + 0, results[predictedWinner][1] + 1]

#             if predictedLoser not in results:
#                 results[predictedLoser] = [0,1]
#             else:
#                 results[predictedLoser] = [results[predictedLoser][0] + 0, results[predictedLoser][1] + 1]


#             if predictedWinner in groups['AFC']:
#                 results['AFC'] = [results['AFC'][0]  + 0, results['AFC'][1] + 1]

#                 if predictedWinner in groups['AFC North']:
#                     results['AFC North'] = [results['AFC North'][0]  + 0, results['AFC North'][1] + 1]
#                 elif predictedWinner in groups['AFC South']:
#                     results['AFC South'] = [results['AFC South'][0]  + 0, results['AFC South'][1] + 1]
#                 elif predictedWinner in groups['AFC East']:
#                     results['AFC East'] = [results['AFC East'][0]  + 0, results['AFC East'][1] + 1]
#                 elif predictedWinner in groups['AFC West']:
#                     results['AFC West'] = [results['AFC West'][0]  + 0, results['AFC West'][1] + 1]

#             elif predictedWinner in groups['NFC']:
#                 results['NFC'] = [results['NFC'][0]  + 0, results['NFC'][1] + 1]

#                 if predictedWinner in groups['NFC North']:
#                     results['NFC North'] = [results['NFC North'][0]  + 0, results['NFC North'][1] + 1]
#                 elif predictedWinner in groups['NFC South']:
#                     results['NFC South'] = [results['NFC South'][0]  + 0, results['NFC South'][1] + 1]
#                 elif predictedWinner in groups['NFC East']:
#                     results['NFC East'] = [results['NFC East'][0]  + 0, results['NFC East'][1] + 1]
#                 elif predictedWinner in groups['NFC West']:
#                     results['NFC West'] = [results['NFC West'][0]  + 0, results['NFC West'][1] + 1]

#             if predictedLoser in groups['AFC']:
#                 results['AFC'] = [results['AFC'][0]  + 0, results['AFC'][1] + 1]

#                 if predictedLoser in groups['AFC North']:
#                     results['AFC North'] = [results['AFC North'][0]  + 0, results['AFC North'][1] + 1]
#                 elif predictedLoser in groups['AFC South']:
#                     results['AFC South'] = [results['AFC South'][0]  + 0, results['AFC South'][1] + 1]
#                 elif predictedLoser in groups['AFC East']:
#                     results['AFC East'] = [results['AFC East'][0]  + 0, results['AFC East'][1] + 1]
#                 elif predictedLoser in groups['AFC West']:
#                     results['AFC West'] = [results['AFC West'][0]  + 0, results['AFC West'][1] + 1]

#             elif predictedLoser in groups['NFC']:
#                 results['NFC'] = [results['NFC'][0]  + 0, results['NFC'][1] + 1]

#                 if predictedLoser in groups['NFC North']:
#                     results['NFC North'] = [results['NFC North'][0]  + 0, results['NFC North'][1] + 1]
#                 elif predictedLoser in groups['NFC South']:
#                     results['NFC South'] = [results['NFC South'][0]  + 0, results['NFC South'][1] + 1]
#                 elif predictedLoser in groups['NFC East']:
#                     results['NFC East'] = [results['NFC East'][0]  + 0, results['NFC East'][1] + 1]
#                 elif predictedLoser in groups['NFC West']:
#                     results['NFC West'] = [results['NFC West'][0]  + 0, results['NFC West'][1] + 1]

#             results[f'{year} Week {week}'] = [results[f'{year} Week {week}'][0] + 0, results[f'{year} Week {week}'][1] + 1]

#     elif dataLength == 1:
#         weekOrYear = data[0][:-1]
#         if weekOrYear == '2022':
#             year = 2022
#         elif weekOrYear == '2023':
#             year = 2023
#         else:
#             week = weekOrYear
#             results[f'{year} Week {week}'] = [0,0]




# finalResults = {}
# for team in results:
#     finalResults[team] = round(results[team][0]/results[team][1],2)


# filenameWrite = '../frontend/src/nflPages/percentages.json'
# with open(filenameWrite, 'w') as outfile:
#     json.dump(finalResults, outfile)

# fileRead.close()