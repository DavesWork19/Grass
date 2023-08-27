#Iterates over each column in upcomingWeek DF checking if any are correlated (with pvalue)
#to any other columns in the overall DF. If correlated (with pvalue) then send to
#linear regression, and if the linear regression score is greater than the score provided
#predict value in upcomingWeek DF

#Then predict winloss with upcomingWeek DF




import pandas as pd
import numpy as np
from scipy import stats


from sklearn import svm
from sklearn import tree
from sklearn import neighbors
from sklearn import linear_model
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler



#Takes a single team DF and the upcomingWeekData and columns and returns if they will win this week
class theBot:
    def __init__(self, teamDF, upcomingWeekDF):
        self.df = teamDF
        #Single row DF of the predicted values for the upcoming week
        self.upcomingWeek = upcomingWeekDF

    #Adjusts self.df to a DataFrame of floats and removes the team name
    def adjustDF(self):
        self.df = self.df.drop(columns=['Team'])

        #Convert object types to floats
        for col in self.df:
            if self.df[col].dtypes == 'object':
                self.df[col] = self.df[col].astype('float')



    #Adds new linear columns to newLinearColumns by checking p value OR correlation
    def getCorrelatedColumns(self, corrColumn, pCutOff, corrCutOff, columnToPredict):
        df = self.df.drop(columns=[columnToPredict])
        newLinearColumns = []

        for col in df:
            if (corrColumn != col) and (len(df[col].unique()) != 1):
                corr, pValue = stats.pearsonr(df[corrColumn], df[col])

                #Check P Values or correlations
                if (pValue <= pCutOff) or ((corr >= corrCutOff) or (corr <= -corrCutOff)) or ():
                    newLinearColumns.append(col)

        return newLinearColumns

    #Use Linear Regression to predict next weeks linear columns values if they have a score higher than scoreCutOff
    def useLinR(self, columnsToPredict, scoreCutOff):
        df = self.df

        for col in columnsToPredict:
            X = df[self.upcomingWeek.columns]
            y = df[col]

            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.19)

            model = linear_model.LinearRegression()
            model.fit(X_train, y_train)
            score = model.score(X_test,y_test)

            if score >= scoreCutOff:
                value = model.predict(self.upcomingWeek)
                if col not in self.upcomingWeek.columns:
                    self.upcomingWeek[col] = np.round(value,1)

    #Predict all linearly correlated columns
    def predictLinearValues(self, columnToPredict):
        linearList = self.upcomingWeek.columns.tolist()
        pCutOff = .05
        corrCutOff = .35
        scoreCutOff = .2


        for col in linearList:
            newColumnsToPredict = []
            newLinearColumns = self.getCorrelatedColumns(col, pCutOff, corrCutOff, columnToPredict)


            for newLinearValue in newLinearColumns:
                if newLinearValue not in linearList:
                    linearList.append(newLinearValue)
                    newColumnsToPredict.append(newLinearValue)

            self.useLinR(newColumnsToPredict, scoreCutOff)






#Iterates over each column in upcomingWeek DF checking if any are correlated (with pvalue)
#to any other columns in the overall DF. If correlated (with pvalue) then send to
#linear regression, and if the linear regression score is greater than the score provided
#predict value in upcomingWeek DF

#Then predict winloss with upcomingWeek DF

    #Use SVM model on predicted values from Linear Regression
    def scoreSVM(self, columnName):
        df = self.df
        X = df[self.upcomingWeek.columns]
        y = df[columnName]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.19)

        model = svm.SVC()
        model.fit(X_train, y_train)

        return model.score(X_test, y_test)

    #Use DT model
    def scoreDT(self, columnName):
        df = self.df

        X = df[self.upcomingWeek.columns]
        y = df[columnName]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.19)

        model = tree.DecisionTreeClassifier()
        model.fit(X_train, y_train)

        return model.score(X_test, y_test)

    #Use KNN model
    def scoreKNN(self, columnName):
        df = self.df
        X = df[self.upcomingWeek.columns]
        y = df[columnName]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.19)

        n_neighbors = 3
        # highScore = 0
        # highNeighbor = 0
        # for n_neighbors in [3,7,12]:
        #     model = make_pipeline(StandardScaler(), neighbors.KNeighborsClassifier(n_neighbors))
        #     model.fit(X_train, y_train)
        #     score = model.score(X_test, y_test)
        #
        #     if score > highScore:
        #         highScore = score
        #         highNeighbor = n_neighbors

        model = make_pipeline(StandardScaler(), neighbors.KNeighborsClassifier(n_neighbors))
        model.fit(X_train, y_train)
        return model.score(X_test, y_test)

    #Find higest model score
    def findScores(self, columnName):

        svmScore = self.scoreSVM(columnName)
        dtScore = self.scoreDT(columnName)
        knnScore = self.scoreKNN(columnName)

        if (svmScore >= dtScore) and (svmScore >= knnScore):
            return 'SVM'
        elif (knnScore >= svmScore) and (knnScore >= dtScore):
            return 'KNN'
        else:
            return 'DT'




    #Predict SVM model
    def predictSVM(self):
        columnName = 'WinLoss'
        df = self.df
        X = df[self.upcomingWeek.columns]
        y = df[columnName]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.19)

        classification = svm.SVC()
        classification.fit(X_train, y_train)

        regression = svm.SVR()
        regression.fit(X_train, y_train)

        return [classification.predict(self.upcomingWeek),regression.predict(self.upcomingWeek)]

    #Predict DT model
    def predictDT(self):
        columnName = 'WinLoss'
        df = self.df
        X = df[self.upcomingWeek.columns]
        y = df[columnName]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.19)

        classification = tree.DecisionTreeClassifier()
        classification = classification.fit(X_train, y_train)

        regression = tree.DecisionTreeRegressor()
        regression = regression.fit(X_train, y_train)


        return [classification.predict(self.upcomingWeek),regression.predict(self.upcomingWeek)]

    #Predict KNN model
    def predictKNN(self):
        columnName = 'WinLoss'
        n_neighbors = 3
        df = self.df
        X = df[self.upcomingWeek.columns]
        y = df[columnName]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.19)

        classification = neighbors.KNeighborsClassifier(n_neighbors)
        classification = classification.fit(X_train, y_train)

        regression = neighbors.KNeighborsRegressor(n_neighbors)
        regression = regression.fit(X_train, y_train)

        return [classification.predict(self.upcomingWeek),regression.predict(self.upcomingWeek)]

    #Find model prediction
    def findPrediction(self, model):
        if model == 'SVM':
            return self.predictSVM()
        elif model == 'DT':
            return self.predictDT()
        elif model == 'KNN':
            return self.predictKNN()




    def useCode(self):
        columnToPredict = 'WinLoss'

        self.predictLinearValues(columnToPredict)

        highestModel = self.findScores(columnToPredict)

        return self.findPrediction(highestModel)
