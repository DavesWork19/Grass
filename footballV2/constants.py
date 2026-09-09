# NFL Teams data structure
# Ordered to match legends.py's 0-31 numeric team codes (Bills=0 ... 49ers=31)
NFL_TEAMS = [
    {"name": "Buffalo Bills", "acronym": "BUF", "pfr": "buf"},
    {"name": "Miami Dolphins", "acronym": "MIA", "pfr": "mia"},
    {"name": "New England Patriots", "acronym": "NE", "pfr": "nwe"},
    {"name": "New York Jets", "acronym": "NYJ", "pfr": "nyj"},
    {"name": "Cincinnati Bengals", "acronym": "CIN", "pfr": "cin"},
    {"name": "Cleveland Browns", "acronym": "CLE", "pfr": "cle"},
    {"name": "Pittsburgh Steelers", "acronym": "PIT", "pfr": "pit"},
    {"name": "Baltimore Ravens", "acronym": "BAL", "pfr": "rav"},
    {"name": "Indianapolis Colts", "acronym": "IND", "pfr": "clt"},
    {"name": "Houston Texans", "acronym": "HOU", "pfr": "htx"},
    {"name": "Jacksonville Jaguars", "acronym": "JAX", "pfr": "jax"},
    {"name": "Tennessee Titans", "acronym": "TEN", "pfr": "oti"},
    {"name": "Denver Broncos", "acronym": "DEN", "pfr": "den"},
    {"name": "Kansas City Chiefs", "acronym": "KC", "pfr": "kan"},
    {"name": "Las Vegas Raiders", "acronym": "LV", "pfr": "rai"},
    {"name": "Los Angeles Chargers", "acronym": "LAC", "pfr": "sdg"},
    {"name": "Dallas Cowboys", "acronym": "DAL", "pfr": "dal"},
    {"name": "New York Giants", "acronym": "NYG", "pfr": "nyg"},
    {"name": "Philadelphia Eagles", "acronym": "PHI", "pfr": "phi"},
    {"name": "Washington Commanders", "acronym": "WAS", "pfr": "was"},
    {"name": "Chicago Bears", "acronym": "CHI", "pfr": "chi"},
    {"name": "Detroit Lions", "acronym": "DET", "pfr": "det"},
    {"name": "Green Bay Packers", "acronym": "GB", "pfr": "gnb"},
    {"name": "Minnesota Vikings", "acronym": "MIN", "pfr": "min"},
    {"name": "Atlanta Falcons", "acronym": "ATL", "pfr": "atl"},
    {"name": "Carolina Panthers", "acronym": "CAR", "pfr": "car"},
    {"name": "New Orleans Saints", "acronym": "NO", "pfr": "nor"},
    {"name": "Tampa Bay Buccaneers", "acronym": "TB", "pfr": "tam"},
    {"name": "Arizona Cardinals", "acronym": "ARI", "pfr": "crd"},
    {"name": "Los Angeles Rams", "acronym": "LAR", "pfr": "ram"},
    {"name": "Seattle Seahawks", "acronym": "SEA", "pfr": "sea"},
    {"name": "San Francisco 49ers", "acronym": "SF", "pfr": "sfo"},
]

SEASON_YEAR = 2026

# NFL "weeks" run Wed-Tue. Needs a manual once-a-year recalibration to the
# actual season schedule (the old backend/constants.py's ALL_WEEKS required
# the same yearly upkeep) - these are best-effort dates for the 2026 season.
WEEK_DATE_RANGES = {
    1: ('9/9', '9/15'),
    2: ('9/16', '9/22'),
    3: ('9/23', '9/29'),
    4: ('9/30', '10/6'),
    5: ('10/7', '10/13'),
    6: ('10/14', '10/20'),
    7: ('10/21', '10/27'),
    8: ('10/28', '11/3'),
    9: ('11/4', '11/10'),
    10: ('11/11', '11/17'),
    11: ('11/18', '11/24'),
    12: ('11/25', '12/1'),
    13: ('12/2', '12/8'),
    14: ('12/9', '12/15'),
    15: ('12/16', '12/22'),
    16: ('12/23', '12/29'),
    17: ('12/30', '1/5'),
    18: ('1/6', '1/12'),
}
