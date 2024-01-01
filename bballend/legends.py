from constants import ALL_TEAMS, TEAM_STREAK_LEVEL

def getTeam(team):
    if (team == 'BOS') or (team == '0') or (team in 'Boston Celtics'):
        return {'fullName' : 'Boston Celtics', 'shortName' : 'BOS', 'number' : 0, 'division' : 'Atlantic', 'conference' : 'Eastern'}
    elif (team == 'NYK') or (team == '2') or (team in 'New York Knicks'):
        return {'fullName' : 'New York Knicks', 'shortName' : 'NYK', 'shortName2' : 'NY', 'number' : 2, 'division' : 'Atlantic', 'conference' : 'Eastern'}
    elif (team == 'BRK') or (team == '3') or (team in 'Brooklyn Nets'):
        return {'fullName' : 'Brooklyn Nets', 'shortName' : 'BRK', 'shortName2' : 'BKN', 'number' : 3, 'division' : 'Atlantic', 'conference' : 'Eastern'}
    elif (team == 'TOR') or (team == '4') or (team in 'Toronto Raptors'):
        return {'fullName' : 'Toronto Raptors', 'shortName' : 'TOR', 'number' : 4, 'division' : 'Atlantic', 'conference' : 'Eastern'}
    elif (team == 'MIL') or (team == '5') or (team in 'Milwaukee Bucks'):
        return {'fullName' : 'Milwaukee Bucks', 'shortName' : 'MIL', 'number' : 5, 'division' : 'Central', 'conference' : 'Eastern'}
    elif (team == 'IND') or (team == '6') or (team in 'Indiana Pacers'):
        return {'fullName' : 'Indiana Pacers', 'shortName' : 'IND', 'number' : 6, 'division' : 'Central', 'conference' : 'Eastern'}
    elif (team == 'CLE') or (team == '7') or (team in 'Cleveland Cavaliers'):
        return {'fullName' : 'Cleveland Cavaliers', 'shortName' : 'CLE', 'number' : 7, 'division' : 'Central', 'conference' : 'Eastern'}
    elif (team == 'PHI') or (team == '1') or (team in 'Philadelphia 76ers'):
        return {'fullName' : 'Philadelphia 76ers', 'shortName' : 'PHI', 'number' : 1, 'division' : 'Atlantic', 'conference' : 'Eastern'}
    elif (team == 'CHI') or (team == '8') or (team in 'Chicago Bulls'):
        return {'fullName' : 'Chicago Bulls', 'shortName' : 'CHI', 'number' : 8, 'division' : 'Central', 'conference' : 'Eastern'}
    elif (team == 'DET') or (team == '9') or (team in 'Detroit Pistons'):
        return {'fullName' : 'Detroit Pistons', 'shortName' : 'DET', 'number' : 9, 'division' : 'Central', 'conference' : 'Eastern'}
    elif (team == 'ORL') or (team == '10') or (team in 'Orlando Magic'):
        return {'fullName' : 'Orlando Magic', 'shortName' : 'ORL', 'number' : 10, 'division' : 'Southeast', 'conference' : 'Eastern'}
    elif (team == 'MIA') or (team == '11') or (team in 'Miami Heat'):
        return {'fullName' : 'Miami Heat', 'shortName' : 'MIA', 'number' : 11, 'division' : 'Southeast', 'conference' : 'Eastern'}
    elif (team == 'ATL') or (team == '12') or (team in 'Atlanta Hawks'):
        return {'fullName' : 'Atlanta Hawks', 'shortName' : 'ATL', 'number' : 12, 'division' : 'Southeast', 'conference' : 'Eastern'}
    elif (team == 'CHO') or (team == '13') or (team in 'Charlotte Hornets'):
        return {'fullName' : 'Charlotte Hornets', 'shortName' : 'CHO', 'shortName2' : 'CHA', 'number' : 13, 'division' : 'Southeast', 'conference' : 'Eastern'}
    elif (team == 'WAS') or (team == '14') or (team in 'Washington Wizards'):
        return {'fullName' : 'Washington Wizards', 'shortName' : 'WAS', 'number' : 14, 'division' : 'Southeast', 'conference' : 'Eastern'}
    elif (team == 'MIN') or (team == '15') or (team in 'Minnesota Timberwolves'):
        return {'fullName' : 'Minnesota Timberwolves', 'shortName' : 'MIN', 'number' : 15, 'division' : 'Northwest', 'conference' : 'Western'}
    elif (team == 'OKC') or (team == '16') or (team in 'Oklahoma City Thunder'):
        return {'fullName' : 'Oklahoma City Thunder', 'shortName' : 'OKC', 'number' : 16, 'division' : 'Northwest', 'conference' : 'Western'}
    elif (team == 'DEN') or (team == '17') or (team in 'Denver Nuggets'):
        return {'fullName' : 'Denver Nuggets', 'shortName' : 'DEN', 'number' : 17, 'division' : 'Northwest', 'conference' : 'Western'}
    elif (team == 'UTA') or (team == '18') or (team in 'Utah Jazz'):
        return {'fullName' : 'Utah Jazz', 'shortName' : 'UTA', 'number' : 18, 'division' : 'Northwest', 'conference' : 'Western'}
    elif (team == 'POR') or (team == '19') or (team in 'Portland Trail Blazers'):
        return {'fullName' : 'Portland Trail Blazers', 'shortName' : 'POR', 'number' : 19, 'division' : 'Northwest', 'conference' : 'Western'}
    elif (team == 'PHO') or (team == '20') or (team in 'Phoenix Suns'):
        return {'fullName' : 'Phoenix Suns', 'shortName' : 'PHO', 'number' : 20, 'division' : 'Pacific', 'conference' : 'Western'}
    elif (team == 'SAC') or (team == '21') or (team in 'Sacramento Kings'):
        return {'fullName' : 'Sacramento Kings', 'shortName' : 'SAC', 'number' : 21, 'division' : 'Pacific', 'conference' : 'Western'}
    elif (team == 'LAL') or (team == '22') or (team in 'Los Angeles Lakers'):
        return {'fullName' : 'Los Angeles Lakers', 'shortName' : 'LAL', 'shortName2' : 'LA Lakers', 'number' : 22, 'division' : 'Pacific', 'conference' : 'Western'}
    elif (team == 'GSW') or (team == '23') or (team in 'Golden State Warriors'):
        return {'fullName' : 'Golden State Warriors', 'shortName' : 'GSW', 'shortName2' : 'GS', 'number' : 23, 'division' : 'Pacific', 'conference' : 'Western'}
    elif (team == 'LAC') or (team == '24') or (team in 'Los Angeles Clippers'):
        return {'fullName' : 'Los Angeles Clippers', 'shortName' : 'LAC', 'number' : 24, 'division' : 'Pacific', 'conference' : 'Western'}
    elif (team == 'DAL') or (team == '25') or (team in 'Dallas Mavericks'):
        return {'fullName' : 'Dallas Mavericks', 'shortName' : 'DAL', 'number' : 25, 'division' : 'Southwest', 'conference' : 'Western'}
    elif (team == 'HOU') or (team == '26') or (team in 'Houston Rockets'):
        return {'fullName' : 'Houston Rockets', 'shortName' : 'HOU', 'number' : 26, 'division' : 'Southwest', 'conference' : 'Western'}
    elif (team == 'NOP') or (team == '27') or (team in 'New Orleans Pelicans'):
        return {'fullName' : 'New Orleans Pelicans', 'shortName' : 'NOP', 'shortName2' : 'NO', 'number' : 27, 'division' : 'Southwest', 'conference' : 'Western'}
    elif (team == 'MEM') or (team == '28') or (team in 'Memphis Grizzlies'):
        return {'fullName' : 'Memphis Grizzlies', 'shortName' : 'MEM', 'number' : 28, 'division' : 'Southwest', 'conference' : 'Western'}
    elif (team == 'SAS') or (team == '29') or (team in 'San Antonio Spurs'):
        return {'fullName' : 'San Antonio Spurs', 'shortName' : 'SAS', 'number' : 29, 'division' : 'Southwest', 'conference' : 'Western'}
    elif (team == ALL_TEAMS):
        return ['BOS','PHI','NYK','BRK','TOR','MIL','IND','CLE','CHI','DET','ORL','MIA','ATL','CHO','WAS','MIN','OKC','DEN','UTA','POR','PHO','SAC','LAL','GSW','LAC','DAL','HOU','NOP','MEM','SAS']


def getDay(day):
    if (day == 'Sun') or (day == '0'):
        return {'dayName' : 'Sunday', 'dayNumber' : 0}
    elif (day == 'Mon') or (day == '1'):
        return {'dayName' : 'Monday', 'dayNumber' : 1}
    elif (day == 'Tue') or (day == '2'):
        return {'dayName' : 'Tuesday', 'dayNumber' : 2}
    elif (day == 'Wed') or (day == '3'):
        return {'dayName' : 'Wednesday', 'dayNumber' : 3}
    elif (day == 'Thu') or (day == '4'):
        return {'dayName' : 'Thursday', 'dayNumber' : 4}
    elif (day == 'Fri') or (day == '5'):
        return {'dayName' : 'Friday', 'dayNumber' : 5}
    elif (day == 'Sat') or (day == '6'):
        return {'dayName' : 'Saturday', 'dayNumber' : 6}


def getTimeCode(time):
    hour, minutes = time.split(':')
    minutes = minutes[:-1]
    hour = int(hour)
    minutes = int(minutes)
    if time[-1] == 'p':
        if (hour == 12) and (minutes < 29):
            return 0
        elif (hour == 12):
            return 1
        elif (hour == 1) and (minutes < 29):
            return 2
        elif (hour == 1):
            return 3
        elif (hour == 2) and (minutes < 29):
            return 4
        elif (hour == 2):
            return 5
        elif (hour == 3) and (minutes < 29):
            return 6
        elif (hour == 3):
            return 7
        elif (hour == 4) and (minutes < 29):
            return 8
        elif (hour == 4):
            return 9
        elif (hour == 5) and (minutes < 29):
            return 10
        elif (hour == 5):
            return 11
        elif (hour == 6) and (minutes < 29):
            return 12
        elif (hour == 6):
            return 13
        elif (hour == 7) and (minutes < 29):
            return 14
        elif (hour == 7):
            return 15
        elif (hour == 8) and (minutes < 29):
            return 16
        elif (hour == 8):
            return 17
        elif (hour == 9) and (minutes < 29):
            return 18
        elif (hour == 9):
            return 19
        elif (hour == 10) and (minutes < 29):
            return 20
        elif (hour == 10):
            return 21
        elif (hour == 11) and (minutes < 29):
            return 22
        elif (hour == 11):
            return 23


def getIsWin(gameResult):
    if gameResult == 'W':
        return 1
    else:
        return 0

def getIsOT(gameOT):
    if gameOT == 'OT':
        return 1
    else:
        return 0

def getIsInSeasonT(inSeasonTournament):
    if inSeasonTournament == 'In-Season Tournament':
        return 1
    else:
        return 0


def getTeamStreakCode(teamStreak):
    winLoss, streakCount = teamStreak.split(' ')
    streakCount = int(streakCount)
    if winLoss == 'W':
        return TEAM_STREAK_LEVEL + streakCount
    else:
        return TEAM_STREAK_LEVEL - streakCount
