import os

from saveBBallData import saveData
from updates import updateDBActuals, getPreviousPercentages
from bots import runDaBot, runDaParlays
from frontend import updateFrontendGames, updateFrontendParlays



if __name__ == "__main__":
    # Frontend files are written relative to backendV2/.
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    #Stage 1 - get new data for new day and for the previous game for all teams
    print('Starting... 0 / 7')
    saveData()
    
    #Stage 2 - Update actual results using new data
    print('1 / 7')
    updateDBActuals()

    #Stage 3 - Run the ML calculations and save into DB table
    print('2 / 7')
    confidenceScores = runDaBot()

    #Stage 4 - Update frontend games
    print('3 / 7')
    updateFrontendGames()
    
    #Stage 5 - update percentages
    print('4 / 7')
    percentTotals = getPreviousPercentages()

    #Stage 6 - Run them mf lays baby
    print('5 / 7')
    runDaParlays(confidenceScores, percentTotals)

    #Stage 7 - Update frontend with lays
    print('6 / 7')
    updateFrontendParlays()

    print('7 / 7 ...Finished!')