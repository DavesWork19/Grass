import sys
from datetime import date

from saveNFLData import saveData
from updates import updateDBActuals, getPreviousPercentages
from bots import runDaBot, runDaParlays
from frontend import updateFrontendGames, updateFrontendParlays
from legends import get_current_week
from constants import WEEK_DATE_RANGES
from scrapes import close_driver


if __name__ == "__main__":
    week = int(sys.argv[1]) if len(sys.argv) > 1 else get_current_week(date.today(), WEEK_DATE_RANGES)

    if week is None:
        print("No active NFL week found for today - nothing to run. Pass a week number explicitly to override.")
        sys.exit(1)

    try:
        # Stage 1 - get new data for this week and backfill the previous week's results
        print('Starting... 0 / 7')
        saveData(week)

        # Stage 2 - Update actual results using new data
        print('1 / 7')
        updateDBActuals(week)
    finally:
        close_driver()

    # Stage 3 - Run the ML calculations and save into DB table
    print('2 / 7')
    confidenceScores = runDaBot(week)

    # Stage 4 - Update frontend games
    print('3 / 7')
    updateFrontendGames(week)

    # Stage 5 - update percentages
    print('4 / 7')
    percentTotals = getPreviousPercentages()

    # Stage 6 - Run them mf lays baby
    print('5 / 7')
    runDaParlays(confidenceScores, percentTotals)

    # Stage 7 - Update frontend with lays
    print('6 / 7')
    updateFrontendParlays(week)

    print('7 / 7 ...Finished!')
