from datetime import datetime

from constants import NFL_TEAMS


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
    elif ('Washington' in team) or ('Commanders' in team):
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


def getTeamName(teamNumber):
    if teamNumber == 0:
        return 'Bills'
    elif teamNumber == 1:
        return 'Dolphins'
    elif teamNumber == 2:
        return 'Patriots'
    elif teamNumber == 3:
        return 'Jets'
    elif teamNumber == 4:
        return 'Bengals'
    elif teamNumber == 5:
        return 'Browns'
    elif teamNumber == 6:
        return 'Steelers'
    elif teamNumber == 7:
        return 'Ravens'
    elif teamNumber == 8:
        return 'Colts'
    elif teamNumber == 9:
        return 'Texans'
    elif teamNumber == 10:
        return 'Jaguars'
    elif teamNumber == 11:
        return 'Titans'
    elif teamNumber == 12:
        return 'Broncos'
    elif teamNumber == 13:
        return 'Chiefs'
    elif teamNumber == 14:
        return 'Raiders'
    elif teamNumber == 15:
        return 'Chargers'
    elif teamNumber == 16:
        return 'Cowboys'
    elif teamNumber == 17:
        return 'Giants'
    elif teamNumber == 18:
        return 'Eagles'
    elif teamNumber == 19:
        return 'Commanders'
    elif teamNumber == 20:
        return 'Bears'
    elif teamNumber == 21:
        return 'Lions'
    elif teamNumber == 22:
        return 'Packers'
    elif teamNumber == 23:
        return 'Vikings'
    elif teamNumber == 24:
        return 'Falcons'
    elif teamNumber == 25:
        return 'Panthers'
    elif teamNumber == 26:
        return 'Saints'
    elif teamNumber == 27:
        return 'Buccaneers'
    elif teamNumber == 28:
        return 'Cardinals'
    elif teamNumber == 29:
        return 'Rams'
    elif teamNumber == 30:
        return 'Seahawks'
    elif teamNumber == 31:
        return '49ers'


def getTeamNumberFromSmallName(team):
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


def getTeamSmallNameFromTeamNumber(team):
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


def getUUID(week, year, team):
    if week < 10:
        return int(f'{str(year)[:2]}0{week}{team}')
    else:
        return int(f'{str(year)[:2]}{week}{team}')


def getWeatherCode(weather):
    if ('Dry' in weather) or ('Clear' in weather) or ('Sunny' in weather):
        return 0
    elif ('Humid' in weather) or ('Fog' in weather) or ('Foggy' in weather) or ('Overcast' in weather) or ('Cloudy' in weather) or ('Clouds' in weather):
        return 1
    elif ('Rain' in weather) or ('Drizzle' in weather) or ('Thunderstorms' in weather):
        return 2
    elif ('Snow' in weather) or ('Flurries' in weather) or ('Sleet' in weather) or ('Frost' in weather):
        return 3
    else:
        return weather


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


def getChannel(channel):
    if channel is None:
        return 0
    channel = channel.strip()
    if channel.upper() in ('TBD', ''):
        return 0
    elif channel == 'ABC':
        return 1
    elif channel.upper() == 'NBC':
        return 2
    elif channel.upper() == 'CBS':
        return 3
    elif channel.upper() == 'FOX':
        return 4
    elif channel.upper() in ('PRIME VIDEO', 'AMAZON', 'PRIME'):
        return 5
    elif channel.upper() in ('ESPN', 'ESPN+'):
        return 6
    elif channel.upper() in ('NFL', 'NFLN', 'NFL NET', 'NFL NETWORK', 'NFLNETWORK'):
        return 7
    elif channel == 'Peacock':
        return 8
    else:
        return 0


def time_to_int(time_str):
    """
    Convert time string like '9:30p' or '2:15a' to integer (minutes since midnight).

    Args:
        time_str: Time string in format like '9:30p', '2:15a', '11:45pm', '3:00am'

    Returns:
        int: Minutes since midnight (0-1439)
    """
    time_str = time_str.lower().strip()
    is_pm = 'p' in time_str

    time_str = time_str.replace('am', '').replace('pm', '').replace('a', '').replace('p', '')

    parts = time_str.split(':')
    hours = int(parts[0])
    minutes = int(parts[1]) if len(parts) > 1 else 0

    if is_pm and hours != 12:
        hours += 12
    elif not is_pm and hours == 12:
        hours = 0

    return (hours * 60 + minutes) / 10


def get_team_acronym(team_name):
    """
    Convert an NFL team name to its acronym.

    Args:
        team_name (str): The full name of the NFL team (case-insensitive)

    Returns:
        str: The team's acronym, or None if not found
    """
    for team in NFL_TEAMS:
        if team["name"].lower() == team_name.lower():
            return team["acronym"]

    team_name_lower = team_name.lower()
    for team in NFL_TEAMS:
        if team_name_lower in team["name"].lower():
            return team["acronym"]

    return None


def get_current_week(today, week_ranges):
    """
    Find which NFL week (Wed-Tue window) `today` falls into.

    Args:
        today: a date object
        week_ranges: dict of {week_num: (start 'm/d', end 'm/d')}, e.g. constants.WEEK_DATE_RANGES

    Returns:
        int week number, or None if today falls outside every window (offseason)
    """
    year = today.year
    for week, (start, end) in week_ranges.items():
        start_month, start_day = (int(x) for x in start.split('/'))
        end_month, end_day = (int(x) for x in end.split('/'))

        start_year = year if start_month >= 8 else year
        end_year = start_year if end_month >= start_month else start_year + 1

        start_date = datetime(start_year, start_month, start_day).date()
        end_date = datetime(end_year, end_month, end_day).date()

        if start_date <= today <= end_date:
            return week

    return None
