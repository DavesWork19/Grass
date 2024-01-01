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

def getDayFromCode(day):
    if day == '0':
        return 'Wed'
    elif day == '1':
        return 'Thu'
    elif day == '2':
        return 'Fri'
    elif day == '3':
        return 'Sat'
    elif day == '4':
        return 'Sun'
    elif day == '5':
        return 'Mon'
    elif day == '6':
        return 'Tue'


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
        return 0
    else:
        return 1


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

def getTeamSmallNameFromTeam(team):
    if team == 0:
        return 'buf'
    elif team == 1:
        return 'mia'
    elif team == 2:
        return 'nwe'
    elif team == 3:
        return 'nyj'
    elif team == 4:
        return 'cin'
    elif team == 5:
        return 'cle'
    elif team == 6:
        return 'pit'
    elif team == 7:
        return 'rav'
    elif team == 8:
        return 'clt'
    elif team == 9:
        return 'htx'
    elif team == 10:
        return 'jax'
    elif team == 11:
        return 'oti'
    elif team == 12:
        return 'den'
    elif team == 13:
        return 'kan'
    elif team == 14:
        return 'rai'
    elif team == 15:
        return 'sdg'
    elif team == 16:
        return 'dal'
    elif team == 17:
        return 'nyg'
    elif team == 18:
        return 'phi'
    elif team == 19:
        return 'was'
    elif team == 20:
        return 'chi'
    elif team == 21:
        return 'det'
    elif team == 22:
        return 'gnb'
    elif team == 23:
        return 'min'
    elif team == 24:
        return 'atl'
    elif team == 25:
        return 'car'
    elif team == 26:
        return 'nor'
    elif team == 27:
        return 'tam'
    elif team == 28:
        return 'crd'
    elif team == 29:
        return 'ram'
    elif team == 30:
        return 'sea'
    elif team == 31:
        return 'sfo'



def getChannel(channel):
    if channel == 'tbd':
        return 0
    elif channel == 'ABC':
        return 1
    elif (channel == 'NBC') or (channel == 'nbc'):
        return 2
    elif (channel == 'CBS') or (channel == 'cbs'):
        return 3
    elif (channel == 'FOX') or (channel == 'fox'):
        return 4
    elif (channel == 'PRIME VIDEO') or (channel == 'AMAZON') or (channel == 'PRIME'):
        return 5
    elif (channel == 'ESPN') or (channel == 'espn') or (channel == 'ESPN+'):
        return 6
    elif (channel == 'NFL') or (channel == 'NFLN') or (channel == 'nfln') or (channel == 'NFLNetwork') or (channel == 'NFL NET') or (channel == 'nflnetwork') or (channel == 'NFL Network') or (channel == 'NFL NETWORK'):
        return 7
    elif (channel == 'Peacock'):
        return 8


def getTemp(temp):
    if temp < 33:
        return 0
    elif temp < 41:
        return 1
    elif temp < 56:
        return 2
    elif temp < 70:
        return 3
    elif temp < 86:
        return 4
    else:
        return 5

def getWeather(weather):
    if 'Dry' in weather:
        return 0
    elif ('Clear' in weather) or ('Sunny' in weather):
        return 1
    elif 'Humid' in weather:
        return 2
    elif ('Fog' in weather) or ('Foggy' in weather):
        return 3
    elif ('Overcast' in weather) or ('Cloudy' in weather) or ('Clouds' in weather):
        return 4
    elif ('Rain' in weather) or ('Drizzle' in weather) or ('Thunderstorms' in weather):
        return 5
    elif ('Snow' in weather) or ('Flurries' in weather) or ('Sleet' in weather):
        return 6
    else:
        return weather

def getTime(time, am_pm):
    if am_pm == 'AM':
        if time == 9:
            return 0
        elif time == 10:
            return 1
    else:
        if time == 12:
            return 2
        elif time == 1:
            return 3
        elif time == 2:
            return 4
        elif time == 3:
            return 5
        elif time == 4:
            return 6
        elif time == 5:
            return 7
        elif time == 7:
            return 8
        elif time == 8:
            return 9
        elif time == 9:
            return 10
        elif time == 10:
            return 11


