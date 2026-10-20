# NBA Teams data structure
NBA_TEAMS = [
    {"name": "Atlanta Hawks", "acronym": "ATL"},
    {"name": "Boston Celtics", "acronym": "BOS"},
    {"name": "Brooklyn Nets", "acronym": "BRK"},
    {"name": "Charlotte Hornets", "acronym": "CHO"},
    {"name": "Chicago Bulls", "acronym": "CHI"},
    {"name": "Cleveland Cavaliers", "acronym": "CLE"},
    {"name": "Dallas Mavericks", "acronym": "DAL"},
    {"name": "Denver Nuggets", "acronym": "DEN"},
    {"name": "Detroit Pistons", "acronym": "DET"},
    {"name": "Golden State Warriors", "acronym": "GSW"},
    {"name": "Houston Rockets", "acronym": "HOU"},
    {"name": "Indiana Pacers", "acronym": "IND"},
    {"name": "Los Angeles Clippers", "acronym": "LAC"},
    {"name": "Los Angeles Lakers", "acronym": "LAL"},
    {"name": "Memphis Grizzlies", "acronym": "MEM"},
    {"name": "Miami Heat", "acronym": "MIA"},
    {"name": "Milwaukee Bucks", "acronym": "MIL"},
    {"name": "Minnesota Timberwolves", "acronym": "MIN"},
    {"name": "New Orleans Pelicans", "acronym": "NOP"},
    {"name": "New York Knicks", "acronym": "NYK"},
    {"name": "Oklahoma City Thunder", "acronym": "OKC"},
    {"name": "Orlando Magic", "acronym": "ORL"},
    {"name": "Philadelphia 76ers", "acronym": "PHI"},
    {"name": "Phoenix Suns", "acronym": "PHO"},
    {"name": "Portland Trail Blazers", "acronym": "POR"},
    {"name": "Sacramento Kings", "acronym": "SAC"},
    {"name": "San Antonio Spurs", "acronym": "SAS"},
    {"name": "Toronto Raptors", "acronym": "TOR"},
    {"name": "Utah Jazz", "acronym": "UTA"},
    {"name": "Washington Wizards", "acronym": "WAS"}
]

# DraftKings' short team prefix -> Basketball Reference acronym, for the teams
# where they differ. 'LA' is ambiguous (Lakers/Clippers) and handled in
# saveBBallData.dk_to_bball_ref.
DK_TO_BBREF = {
    'BKN': 'BRK',
    'NO': 'NOP',
    'CHA': 'CHO',
    'NY': 'NYK',
    'GS': 'GSW',
    'SA': 'SAS',
    'PHX': 'PHO',
    'UTAH': 'UTA',
    'WSH': 'WAS',
}

# Never let an offseason gap (~190 days) into days_since_last_game - the
# longest in-season gap in the training data is the All-Star break (8-9 days).
MAX_DAYS_SINCE_LAST_GAME = 9


def current_season_year(today=None):
    """Basketball Reference names a season by the year it ends in: the
    2026-27 season (tipping off Oct 2026) is '2027'. Rolls over in August."""
    from datetime import date

    today = today or date.today()
    return today.year + 1 if today.month >= 8 else today.year
