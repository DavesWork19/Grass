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


from sklearn.feature_selection import VarianceThreshold
from sklearn import svm
from sklearn import tree
from sklearn import neighbors
from sklearn import linear_model
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import f_classif
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score




def bot3(upcomingWeekDF, allDataDF, columnToPredict, teamNumber, oppTeamNumber):
    allDataDF = allDataDF.drop(columns=['HomeTeam'])
    teamName = getTeamSmallNameFromTeam(teamNumber)
    oppTeamName = getTeamSmallNameFromTeam(oppTeamNumber)

    teamsDF = allDataDF[(allDataDF['Team'] == teamName) | (allDataDF['Team'] == oppTeamName)]
    teamsDF = teamsDF.drop(columns=['Team'])

    print(upcomingWeekDF)
    

    y = teamsDF[columnToPredict]
    X = teamsDF.drop(columns=[columnToPredict])

    for col in X:
        if X[col].dtypes == 'object':
            X[col] = X[col].astype('float')

    

    # featSelection = SelectKBest(f_classif, k=7)
    # X_new = featSelection.fit_transform(X_upcomingWeek1,y_upcomingWeek1)
    # print(featSelection.get_feature_names_out())
    dfColumns = ['Tm','Opp','Cmp','AttPassing','YdsPassing','TDPassing','Interceptions','Sk','YdsLossFromSacks','YPerAPassing','NYPerA','CmpPerc','Rate','AttRushing','YdsRushing','YPerARushing','TDRushing','FGM','FGA','XPM','XPA','Pnt','YdsPunting','ThirdDConv','ThirdDAtt','FourthDConv','FourthDAtt','ToP','Year','YardsPerPoint','Time','gameLine','minMaxLine','totalScoreLine','minMaxTotalScoreLine','favored']


    # create a pipeline object
    # pipe = make_pipeline(
    #     StandardScaler(),
    #     LogisticRegression()
    # )
    X_upcomingWeek1 = X[['Week','Time','Day','At','OppTeam','Year']]
    for col in dfColumns:
        y_upcomingWeek1 = X[col]
        print()
        print()
        print() 
        print(col)


        X_train, X_test, y_train, y_test = train_test_split(X_upcomingWeek1.to_numpy(), y_upcomingWeek1, random_state=0)

        if (y_upcomingWeek1.dtype != 'float64'):

            regression = svm.SVC()
            regression.fit(X_train, y_train)

            rR = accuracy_score(regression.predict(X_test), y_test)*100

            print('accurary score', rR)


            model = tree.DecisionTreeClassifier()
            model.fit(X_train, y_train)

            print('accuracy_score =>> ',accuracy_score(model.predict(X_test), y_test)*100)

            model = make_pipeline(StandardScaler(), neighbors.KNeighborsClassifier(3))
            model.fit(X_train, y_train)
            print('accuracy_score =>> ',accuracy_score(model.predict(X_test), y_test)*100)


        regr = svm.SVR()
        regr.fit(X_train, y_train)
        print('reg score' , regr.score(X_test, y_test))

        regression = tree.DecisionTreeRegressor()
        regression = regression.fit(X_train, y_train)
        print(regression.score(X_test, y_test))

        regression = neighbors.KNeighborsRegressor(3)
        regression = regression.fit(X_train, y_train)

        print(regression.score(X_test, y_test))
    







def teamService(columnName, teamNumber, time, day, at, oppTeamNumber):
    mydb = mysql.connector.connect(
        host='127.0.0.1',
        user='davidcarney',
        password='Sinorrabb1t',
        database='NFL'
        )

    week = 5
    year = 2023

    mycursor = mydb.cursor()

    mycursor.execute(f"SELECT * FROM productionNFL WHERE Year > 2016")
    allData = mycursor.fetchall()

    dfColumns = ['id','Week','Day','WinLoss','OT','At','OppTeam','Tm','Opp','Cmp','AttPassing','YdsPassing','TDPassing','Interceptions','Sk','YdsLossFromSacks','YPerAPassing','NYPerA','CmpPerc','Rate','AttRushing','YdsRushing','YPerARushing','TDRushing','FGM','FGA','XPM','XPA','Pnt','YdsPunting','ThirdDConv','ThirdDAtt','FourthDConv','FourthDAtt','ToP','Year','Team','YardsPerPoint','HomeTeam','Time','Channel','Temp','Weather','Wind','gameLine','minMaxLine','totalScoreLine','minMaxTotalScoreLine','favored']
    allDataDF = pd.DataFrame(allData, columns = dfColumns)

    allDataDF = allDataDF.drop(columns=['id','Channel','Wind','Weather','Temp'])

    upcomingWeekData = None
    if at == 0:
        upcomingWeekData = [[week, time, day, at, oppTeamNumber, year]]
        
    else:
        upcomingWeekData = [[week, time, day, at, oppTeamNumber, year]]
    
    upcomingWeekColumns = ['Week','Time','Day','At','OppTeam','Year']
    upcomingWeekDF = pd.DataFrame(upcomingWeekData, columns = upcomingWeekColumns)

    result = bot3(upcomingWeekDF, allDataDF, columnName, teamNumber, oppTeamNumber)

    return result










def updateMatchup(awayTeamName, homeTeamName, time, day):
        homeTeamNumber = getTeam(homeTeamName)
        awayTeamNumber = getTeam(awayTeamName)

        homeWinLossOutcome = teamService('WinLoss', homeTeamNumber, time, day, 1, awayTeamNumber)
        awayWinLossOutcome = teamService('WinLoss', awayTeamNumber, time, day, 0, homeTeamNumber)



        if homeWinLossOutcome > awayWinLossOutcome:
            print(homeWinLossOutcome, awayWinLossOutcome)
            percent = (1 - (awayWinLossOutcome / homeWinLossOutcome)) * 100
            print(f'Winner: {homeTeam} and loser: {awayTeam}')  
                   

        else:
            print(awayWinLossOutcome, homeWinLossOutcome)
            percent = (1 - (homeWinLossOutcome / awayWinLossOutcome)) * 100
            print(f'Winner: {awayTeam} and loser: {homeTeam}')












readFilename = 'upcomingWeekData.txt'
readFile = open(readFilename, 'r')


for matchup in readFile.readlines():

    awayTeam, homeTeam, time, day, channel, temp, weather, wind = matchup.split('_')
    wind = wind.strip()

    updateMatchup(awayTeam, homeTeam, time, day)
    

readFile.close()

print('All matchups have been predicted!')