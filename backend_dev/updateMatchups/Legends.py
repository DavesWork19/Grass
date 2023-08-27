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


def getTeamNumber(team):
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
