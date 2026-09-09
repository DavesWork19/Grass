"""
Resume a weekly run from stage 2 onward, reusing the NFL1 rows main.py's
stage 1 (saveData) already inserted for this week - so a crash after stage 1
doesn't force a re-scrape and a duplicate insert.

    python3 resume_week.py <week> [--skip-actuals]

--skip-actuals skips updateDBActuals (pointless for a week whose games haven't
been played yet, and it re-scrapes every team's gamelog).
"""

import sys

from updates import updateDBActuals, getPreviousPercentages
from bots import runDaBot, runDaParlays
from frontend import updateFrontendGames, updateFrontendParlays
from scrapes import close_driver


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    week = int(sys.argv[1])
    skip_actuals = '--skip-actuals' in sys.argv

    try:
        if not skip_actuals:
            print('1 / 7  updateDBActuals')
            updateDBActuals(week)
        else:
            print('1 / 7  updateDBActuals (skipped)')
    finally:
        close_driver()

    print('2 / 7  runDaBot')
    confidence_scores = runDaBot(week)

    print('3 / 7  updateFrontendGames')
    updateFrontendGames(week)

    print('4 / 7  getPreviousPercentages')
    percent_totals = getPreviousPercentages()

    print('5 / 7  runDaParlays')
    runDaParlays(confidence_scores, percent_totals)

    print('6 / 7  updateFrontendParlays')
    updateFrontendParlays(week)

    print('7 / 7  ...Finished!')


if __name__ == '__main__':
    main()
