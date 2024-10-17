#Iterates over each column in upcomingWeek DF checking if any are correlated (with pvalue)
#to any other columns in the overall DF. If correlated (with pvalue) then send to
#linear regression, and if the linear regression score is greater than the score provided
#predict value in upcomingWeek DF

#Then predict winloss with upcomingWeek DF

#Feature selection for dataset
#Check spread data with confidence interval



import pandas as pd
import numpy as np
from scipy import stats



from sklearn import linear_model
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import VarianceThreshold
from sklearn.linear_model import ElasticNet
from sklearn.linear_model import Lasso
from sklearn.linear_model import SGDRegressor
from sklearn.linear_model import Ridge
from sklearn.model_selection import GridSearchCV, cross_val_predict
from sklearn.metrics import accuracy_score
from sklearn.metrics import mean_absolute_error
from sklearn.feature_selection import RFECV
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import SGDClassifier



#Takes a single team DF and the upcomingWeekData and columns and returns if they will win this week
class theBot:
    def __init__(self, teamDF, upcomingWeekDF, columnToPredict):
        self.columnToPredict = columnToPredict
        self.df = teamDF
        #Single row DF of the predicted values for the upcoming week
        self.upcomingWeek = upcomingWeekDF

    #Adjusts self.df to a DataFrame of floats and removes the team name
    def adjustDF(self):
        self.df = self.df.drop(columns=['Team', 'HomeTeam'])

        #Convert object types to floats
        for col in self.df:
            if self.df[col].dtypes == 'object':
                self.df[col] = self.df[col].astype('float')



    #Adds new linear columns to newLinearColumns by checking p value OR correlation
    def getCorrelatedColumns(self, corrColumn, pCutOff, corrCutOff):
        df = self.df.drop(columns=[self.columnToPredict])
        newLinearColumns = []

        for col in df:
            if (corrColumn != col) and (len(df[col].unique()) != 1) and (len(df[col]) >= 2) and (len(df[corrColumn]) >= 2):
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
    def predictLinearValues(self):
        linearList = self.upcomingWeek.columns.tolist()
        pCutOff = .05
        corrCutOff = .35
        scoreCutOff = .2


        for col in linearList:
            newColumnsToPredict = []
            newLinearColumns = self.getCorrelatedColumns(col, pCutOff, corrCutOff)


            for newLinearValue in newLinearColumns:
                if newLinearValue not in linearList:
                    linearList.append(newLinearValue)
                    newColumnsToPredict.append(newLinearValue)

            self.useLinR(newColumnsToPredict, scoreCutOff)



    def useCode(self):
        self.predictLinearValues()

        df = self.df
        X = df[self.upcomingWeek.columns]
        y = df[self.columnToPredict]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.19, random_state = 19)
        
        #Scale training and testing data
        scalar = StandardScaler()
        
        scalar.fit(X_train)
        X_train = scalar.transform(X_train)
        X_test = scalar.transform(X_test)

        #Feature selection
        # featureSelection =  RFECV(estimator, step=1, cv=2)
        featureSelection = VarianceThreshold(threshold=(.8 * (1 - .8)))
        X_train = featureSelection.fit_transform(X_train)
        X_test = featureSelection.transform(X_test)

        #Test models
        C = [0.00001, 0.0001, 0.001, 0.01, 0.1, 1.0, 10.0, 100.0, 1000.0]
        alphas = [0.000001, 0.00001, 0.0001, 0.001, 0.01, 0.1, 1.0, 10.0, 100.0, 1000.0]
        neighbors = [2,3,5,7]
        
        CParams = [{'C': C}]
        alphaParams = [{'alpha' : alphas}]
        KNNParams = [{'n_neighbors' : neighbors}]
        
        #Models
        SVCModel = SVC(probability=True, random_state=19)
        KNN = KNeighborsClassifier()
        LogReg = LogisticRegression(max_iter=7000, random_state=19)
        SGDCModel = SGDClassifier(loss='log', max_iter=7000, tol=1e-3, random_state=19)
        
        #CV 2 folds
        #Support Vector Machines
        SVCGS2 = GridSearchCV(SVCModel, CParams, cv=2)
        SVCGS2.fit(X_train, y_train)
        bestSVC2 = SVC(C = SVCGS2.best_params_['C'], probability=True, random_state=19)
        #K Nearest Neighbor
        KNNGS2 = GridSearchCV(KNN, KNNParams, cv=2)
        KNNGS2.fit(X_train, y_train)
        bestKNN2 = KNeighborsClassifier(n_neighbors = KNNGS2.best_params_['n_neighbors'])
        #Logistic Regression
        LRGS2 = GridSearchCV(LogReg, CParams, cv=2)
        LRGS2.fit(X_train, y_train)
        bestLR2 = LogisticRegression(C = LRGS2.best_params_['C'], max_iter=1000, random_state=19)
        #Stochastic Gradient Descent 
        SGDCGS2 = GridSearchCV(SGDCModel, alphaParams, cv=2)
        SGDCGS2.fit(X_train, y_train)
        bestSGDC2 = SGDClassifier(loss='log', alpha = SGDCGS2.best_params_['alpha'], max_iter=1000, tol=1e-3, random_state=19)

        #CV 3 folds
        #Support Vector Machines
        SVCGS3 = GridSearchCV(SVCModel, CParams, cv=3)
        SVCGS3.fit(X_train, y_train)
        bestSVC3 = SVC(C = SVCGS3.best_params_['C'], probability=True, random_state=19)
        #K Nearest Neighbor
        KNNGS3 = GridSearchCV(KNN, KNNParams, cv=3)
        KNNGS3.fit(X_train, y_train)
        bestKNN3 = KNeighborsClassifier(n_neighbors = KNNGS3.best_params_['n_neighbors'])
        #Logistic Regression
        LRGS3 = GridSearchCV(LogReg, CParams, cv=3)
        LRGS3.fit(X_train, y_train)
        bestLR3 = LogisticRegression(C = LRGS3.best_params_['C'], max_iter=1000, random_state=19)
        #Stochastic Gradient Descent 
        SGDCGS3 = GridSearchCV(SGDCModel, alphaParams, cv=3)
        SGDCGS3.fit(X_train, y_train)
        bestSGDC3 = SGDClassifier(loss='log', alpha = SGDCGS3.best_params_['alpha'], max_iter=1000, tol=1e-3, random_state=19)

        #CV 5 folds
        #Support Vector Machines
        SVCGS5 = GridSearchCV(SVCModel, CParams, cv=5)
        SVCGS5.fit(X_train, y_train)
        bestSVC5 = SVC(C = SVCGS5.best_params_['C'], probability=True, random_state=19)
        #K Nearest Neighbor
        KNNGS5 = GridSearchCV(KNN, KNNParams, cv=5)
        KNNGS5.fit(X_train, y_train)
        bestKNN5 = KNeighborsClassifier(n_neighbors = KNNGS5.best_params_['n_neighbors'])
        #Logistic Regression
        LRGS5 = GridSearchCV(LogReg, CParams, cv=5)
        LRGS5.fit(X_train, y_train)
        bestLR5 = LogisticRegression(C = LRGS5.best_params_['C'], max_iter=1000, random_state=19)
        #Stochastic Gradient Descent 
        SGDCGS5 = GridSearchCV(SGDCModel, alphaParams, cv=5)
        SGDCGS5.fit(X_train, y_train)
        bestSGDC5 = SGDClassifier(loss='log', alpha = SGDCGS5.best_params_['alpha'], max_iter=1000, tol=1e-3, random_state=19)

        #CV 7 folds
        #Support Vector Machines
        SVCGS7 = GridSearchCV(SVCModel, CParams, cv=7)
        SVCGS7.fit(X_train, y_train)
        bestSVC7 = SVC(C = SVCGS7.best_params_['C'], probability=True, random_state=19)
        #K Nearest Neighbor
        KNNGS7 = GridSearchCV(KNN, KNNParams, cv=7)
        KNNGS7.fit(X_train, y_train)
        bestKNN7 = KNeighborsClassifier(n_neighbors = KNNGS7.best_params_['n_neighbors'])
        #Logistic Regression
        LRGS7 = GridSearchCV(LogReg, CParams, cv=7)
        LRGS7.fit(X_train, y_train)
        bestLR7 = LogisticRegression(C = LRGS7.best_params_['C'], max_iter=1000, random_state=19)
        #Stochastic Gradient Descent 
        SGDCGS7 = GridSearchCV(SGDCModel, alphaParams, cv=7)
        SGDCGS7.fit(X_train, y_train)
        bestSGDC7 = SGDClassifier(loss='log', alpha = SGDCGS7.best_params_['alpha'], max_iter=1000, tol=1e-3, random_state=19)

        bestSVC2.fit(X_train, y_train)
        bestSVC2Score = accuracy_score(y_test, bestSVC2.predict(X_test))
        bestSVC3.fit(X_train, y_train)
        bestSVC3Score = accuracy_score(y_test, bestSVC3.predict(X_test))
        bestSVC5.fit(X_train, y_train)
        bestSVC5Score = accuracy_score(y_test, bestSVC5.predict(X_test))
        bestSVC7.fit(X_train, y_train)
        bestSVC7Score = accuracy_score(y_test, bestSVC7.predict(X_test))

        bestKNN2.fit(X_train, y_train)
        bestKNN2Score = accuracy_score(y_test, bestKNN2.predict(X_test))
        bestKNN3.fit(X_train, y_train)
        bestKNN3Score = accuracy_score(y_test, bestKNN3.predict(X_test))
        bestKNN5.fit(X_train, y_train)
        bestKNN5Score = accuracy_score(y_test, bestKNN5.predict(X_test))
        bestKNN7.fit(X_train, y_train)
        bestKNN7Score = accuracy_score(y_test, bestKNN7.predict(X_test))

        bestLR2.fit(X_train, y_train)
        bestLR2Score = accuracy_score(y_test, bestLR2.predict(X_test))
        bestLR3.fit(X_train, y_train)
        bestLR3Score = accuracy_score(y_test, bestLR3.predict(X_test))
        bestLR5.fit(X_train, y_train)
        bestLR5Score = accuracy_score(y_test, bestLR5.predict(X_test))
        bestLR7.fit(X_train, y_train)
        bestLR7Score = accuracy_score(y_test, bestLR7.predict(X_test))

        bestSGDC2.fit(X_train, y_train)
        bestSGDC2Score = accuracy_score(y_test, bestSGDC2.predict(X_test))
        bestSGDC3.fit(X_train, y_train)
        bestSGDC3Score = accuracy_score(y_test, bestSGDC3.predict(X_test))
        bestSGDC5.fit(X_train, y_train)
        bestSGDC5Score = accuracy_score(y_test, bestSGDC5.predict(X_test))
        bestSGDC7.fit(X_train, y_train)
        bestSGDC7Score = accuracy_score(y_test, bestSGDC7.predict(X_test))

        allScores = {'bestSVC2Score' : bestSVC2Score,'bestSVC3Score' : bestSVC3Score,'bestSVC5Score' : bestSVC5Score,'bestSVC7Score' : bestSVC7Score,'bestKNN2Score' : bestKNN2Score,'bestKNN3Score' : bestKNN3Score,'bestKNN5Score' : bestKNN5Score,'bestKNN7Score' : bestKNN7Score,'bestLR2Score' : bestLR2Score,'bestLR3Score' : bestLR3Score,'bestLR5Score' : bestLR5Score,'bestLR7Score' : bestLR7Score, 'bestSGDC2Score' : bestSGDC2Score, 'bestSGDC3Score' : bestSGDC3Score, 'bestSGDC5Score' : bestSGDC5Score, 'bestSGDC7Score' : bestSGDC7Score}
        allBestModels = {'bestSVC2Score' : bestSVC2,'bestSVC3Score' : bestSVC3,'bestSVC5Score' : bestSVC5,'bestSVC7Score' : bestSVC7,'bestKNN2Score' : bestKNN2,'bestKNN3Score' : bestKNN3,'bestKNN5Score' : bestKNN5,'bestKNN7Score' : bestKNN7,'bestLR2Score' : bestLR2,'bestLR3Score' : bestLR3,'bestLR5Score' : bestLR5,'bestLR7Score' : bestLR7, 'bestSGDC2Score' : bestSGDC2, 'bestSGDC3Score' : bestSGDC3, 'bestSGDC5Score' : bestSGDC5, 'bestSGDC7Score' : bestSGDC7}

        bestScore = max(allScores, key=allScores.get)
        bestModel = allBestModels[bestScore]

        scaledTeamDF = scalar.transform(self.upcomingWeek)
        scaledTeamDF = featureSelection.transform(scaledTeamDF)

        teamPrediction = bestModel.predict(scaledTeamDF)[0]
        teamPredictionProb = bestModel.predict_proba(scaledTeamDF)[0][0]

        return [teamPrediction, teamPredictionProb]