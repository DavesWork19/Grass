def getDay(day):
    if day == 'Wed':
        return 0
    elif day == 'Thu':
        return 1
    elif day == 'Fri':
        return 2
    elif day == 'Sat':
        return 3
    elif day == 'Sun':
        return 4
    elif day == 'Mon':
        return 5
    elif day == 'Tue':
        return 6


def getWinloss(result):
    if result == 'W':
        return 1
    else:
        return 0


def getOT(ot):
    if ot == 'OT':
        return 1
    else:
        return 0


def getAt(at):
    if at == '@':
        return 1
    else:
        return 0


def getTeam(team):
    if 'Bills' in team:
        return 0
    elif 'Dolphins' in team:
        return 1
    elif 'Patriots' in team:
        return 2
    elif 'Jets' in team:
        return 3
    elif 'Bengals' in team:
        return 4
    elif 'Browns' in team:
        return 5
    elif 'Steelers' in team:
        return 6
    elif 'Ravens' in team:
        return 7
    elif 'Colts' in team:
        return 8
    elif 'Texans' in team:
        return 9
    elif 'Jaguars' in team:
        return 10
    elif 'Titans' in team:
        return 11
    elif 'Broncos' in team:
        return 12
    elif 'Chiefs' in team:
        return 13
    elif 'Raiders' in team:
        return 14
    elif 'Chargers' in team:
        return 15
    elif 'Cowboys' in team:
        return 16
    elif 'Giants' in team:
        return 17
    elif 'Eagles' in team:
        return 18
    elif 'Washington' in team:
        return 19
    elif 'Bears' in team:
        return 20
    elif 'Lions' in team:
        return 21
    elif 'Packers' in team:
        return 22
    elif 'Vikings' in team:
        return 23
    elif 'Falcons' in team:
        return 24
    elif 'Panthers' in team:
        return 25
    elif 'Saints' in team:
        return 26
    elif 'Buccaneers' in team:
        return 27
    elif 'Cardinals' in team:
        return 28
    elif 'Rams' in team:
        return 29
    elif 'Seahawks' in team:
        return 30
    elif '49ers' in team:
        return 31


def getTeamFromSmallName(team):
    if 'buf' == team:
        return 0
    elif 'mia' == team:
        return 1
    elif 'nwe' == team:
        return 2
    elif 'nyj' == team:
        return 3
    elif 'cin' == team:
        return 4
    elif 'cle' == team:
        return 5
    elif 'pit' == team:
        return 6
    elif 'rav' == team:
        return 7
    elif 'clt' == team:
        return 8
    elif 'htx' == team:
        return 9
    elif 'jax' == team:
        return 10
    elif 'oti' == team:
        return 11
    elif 'den' == team:
        return 12
    elif 'kan' == team:
        return 13
    elif 'rai' == team:
        return 14
    elif 'sdg' == team:
        return 15
    elif 'dal' == team:
        return 16
    elif 'nyg' == team:
        return 17
    elif 'phi' == team:
        return 18
    elif 'was' == team:
        return 19
    elif 'chi' == team:
        return 20
    elif 'det' == team:
        return 21
    elif 'gnb' == team:
        return 22
    elif 'min' == team:
        return 23
    elif 'atl' == team:
        return 24
    elif 'car' == team:
        return 25
    elif 'nor' == team:
        return 26
    elif 'tam' == team:
        return 27
    elif 'crd' == team:
        return 28
    elif 'ram' == team:
        return 29
    elif 'sea' == team:
        return 30
    elif 'sfo' == team:
        return 31


def getChannel(channel):
    if channel == 'ESPN':
        return 0
    elif channel == 'CBS':
        return 1
    elif channel == 'NBC':
        return 2
    elif channel == 'NBC':
        return 3
    elif channel == 'FOX':
        return 4
    elif (channel == 'PRIME VIDEO') or (channel == 'AMAZON'):
        return 5
    else:
        return 6


def getTemp(temp):
    if temp == 'DOME':
        return 0
    elif temp < 40:
        return 1
    elif (temp >= 40) and (temp < 80):
        return 2
    elif temp >= 80:
        return 3
    else:
        return 4

def getSky(sky):
    if sky == 'DOME':
        return 0
    elif sky == 'Clear':
        return 1
    elif sky == 'Cloudy':
        return 2
    elif sky == 'Foggy':
        return 3
    elif sky == 'Rain':
        return 4
    elif sky == 'Overcast':
        return 5
    elif sky == 'Snow':
        return 6
    elif sky == 'Drizzle':
        return 7
    elif sky == 'Dry':
        return 8
    elif sky == 'Flurries':
        return 9
    elif sky == 'Humid':
        return 10
    elif sky == 'Sleet':
        return 11
    elif sky == 'Windy':
        return 12
    else:
        return 13
