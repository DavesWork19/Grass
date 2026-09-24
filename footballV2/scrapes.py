from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
from bs4 import BeautifulSoup
import re
import time
import random
import pandas as pd
from datetime import datetime

from legends import getDay, getChannel, getWeatherCode
from constants import NFL_TEAMS

# Pro Football Reference now sits behind a Cloudflare "Just a moment..." JS
# challenge - plain `requests` (any User-Agent) and vanilla Selenium both get a
# 403. undetected-chromedriver clears it, as long as Selenium is told not to
# block forever on the challenge page's load event (page_load_strategy='eager').
# We keep a single browser alive for the whole run and pace requests with
# human-ish pauses + scrolling so we don't trip PFR's rate limiter.
_PFR_HREF_RE = re.compile(r'/teams/([a-z]{3})/')
PFR_CODE_TO_NAME = {team['pfr']: team['name'] for team in NFL_TEAMS}

_driver = None


def _installed_chrome_major_version():
    """undetected-chromedriver's own auto-detection has picked a chromedriver
    for the wrong major version before (e.g. grabbing 154 while the installed
    Chrome.app auto-updated to 153) - pin version_main from the actual binary
    instead of trusting it."""
    import subprocess

    for path in (
        '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
        '/Applications/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing',
    ):
        try:
            out = subprocess.check_output([path, '--version'], text=True)
            match = re.search(r'(\d+)\.', out)
            if match:
                return int(match.group(1))
        except (FileNotFoundError, subprocess.CalledProcessError):
            continue
    return None


def _new_driver():
    import undetected_chromedriver as uc

    opts = uc.ChromeOptions()
    opts.add_argument('--window-size=1366,900')
    opts.page_load_strategy = 'eager'
    drv = uc.Chrome(
        options=opts,
        version_main=_installed_chrome_major_version(),
        use_subprocess=True,
    )
    drv.set_page_load_timeout(35)
    return drv


def _get_driver():
    global _driver
    if _driver is None:
        _driver = _new_driver()
    return _driver


def close_driver():
    global _driver
    if _driver is not None:
        try:
            _driver.quit()
        except Exception:
            pass
        _driver = None


def _restart_driver():
    close_driver()
    return _get_driver()


def _human_pause(a=1.5, b=4.0):
    time.sleep(random.uniform(a, b))


def _page_source(driver):
    try:
        return driver.page_source
    except Exception:
        return ''


def _settled_soup(driver, max_wait):
    """Poll until the Cloudflare interstitial clears (or we run out of time)."""
    deadline = time.time() + max_wait
    html = _page_source(driver)
    while time.time() < deadline:
        try:
            title = (driver.title or '').lower()
        except Exception:
            title = ''
        if html and 'just a moment' not in html.lower() and 'moment' not in title:
            break
        time.sleep(random.uniform(2.0, 3.5))
        html = _page_source(driver)

    try:
        for _ in range(random.randint(2, 4)):
            driver.execute_script(f'window.scrollBy(0, {random.randint(200, 700)});')
            _human_pause(0.4, 1.1)
    except Exception:
        pass

    return BeautifulSoup(_page_source(driver) or html, 'lxml')


def _fetch_soup(url, max_wait=45, attempts=3):
    """GET `url` through the shared undetected-chromedriver browser, waiting out
    the Cloudflare challenge, and return a BeautifulSoup of the settled page.
    Chrome's renderer occasionally wedges on PFR; on any driver-level error we
    tear the browser down and start a fresh one before retrying."""
    for attempt in range(1, attempts + 1):
        driver = _get_driver()
        _human_pause(1.5, 3.5)
        try:
            try:
                driver.get(url)
            except Exception:
                # 'eager' strategy still times out on a stuck challenge page -
                # the poll below picks it up once Cloudflare releases it.
                pass
            return _settled_soup(driver, max_wait)
        except Exception as exc:
            print(f"  _fetch_soup {url} attempt {attempt}/{attempts} failed ({exc!r}); restarting browser")
            _restart_driver()
            _human_pause(3.0, 6.0)

    return BeautifulSoup('', 'lxml')


def _find_table(soup, table_id):
    """PFR hides some tables inside HTML comments; check both places."""
    table = soup.find('table', id=table_id)
    if table:
        return table
    for comment in soup.find_all(string=lambda t: isinstance(t, str) and table_id in t):
        if '<table' in comment:
            found = BeautifulSoup(comment, 'lxml').find('table', id=table_id)
            if found:
                return found
    return None


# PFR renamed the gamelog table and reworked its columns in 2026; every cell now
# carries a stable data-stat attribute, so we read by that instead of by
# position. Maps our column name -> PFR data-stat.
_GAMELOG_STATS = {
    'week': 'week_num',
    'game_result': 'team_game_result',
    'game_location': 'game_location',
    'pts_for': 'points',
    'pts_against': 'points_opp',
    'pass_yds': 'pass_yds',
    'pass_int': 'pass_int',
    'sacks_allowed': 'pass_sacked',
    'rush_yds': 'rush_yds',
    'third_down_conv': 'third_down_success',
    'third_down_att': 'third_down_att',
}
_GAMELOG_TABLE_ID = (
    'table_pfr_team-year_game-logs_team-year-regular-season-game-log'
)


def scrape_all_game_data_by_team(pfr_code, year):
    """
    Scrape every played-game row from a team's Pro Football Reference gamelog page.

    Args:
        pfr_code: Pro Football Reference's 3-letter team code (e.g. 'buf')
        year: season year

    Returns:
        pandas DataFrame, one row per played game, with named columns:
        week, game_result, game_location ('@' for away, '' for home),
        opp_name (full team name), pts_for, pts_against, pass_yds, pass_int,
        sacks_allowed, rush_yds, third_down_conv, third_down_att
    """
    url = f'https://www.pro-football-reference.com/teams/{pfr_code}/{year}/gamelog/'
    soup = _fetch_soup(url)

    table = _find_table(soup, _GAMELOG_TABLE_ID)
    if not table:
        print(f"Gamelog table not found for {pfr_code} ({year})!")
        return pd.DataFrame()

    tbody = table.find('tbody')
    if not tbody:
        return pd.DataFrame()

    rows = []
    for tr in tbody.find_all('tr'):
        if tr.get('class') and 'thead' in tr.get('class'):
            continue

        cells = {c.get('data-stat'): c for c in tr.find_all(['th', 'td'])}
        if 'week_num' not in cells:
            continue

        result = cells.get('team_game_result')
        result_txt = result.get_text(strip=True) if result else ''
        if result_txt not in ('W', 'L', 'T'):
            continue  # unplayed / bye row

        row = {}
        for name, stat in _GAMELOG_STATS.items():
            cell = cells.get(stat)
            row[name] = cell.get_text(strip=True) if cell is not None else ''

        opp_cell = cells.get('opp_name_abbr')
        opp_name = opp_cell.get_text(strip=True) if opp_cell else ''
        if opp_cell is not None and opp_cell.find('a'):
            m = _PFR_HREF_RE.search(opp_cell.find('a').get('href', ''))
            if m:
                opp_name = PFR_CODE_TO_NAME.get(m.group(1), opp_name)
        row['opp_name'] = opp_name

        rows.append(row)

    return pd.DataFrame(rows)


def scrape_upcoming_game_by_team(pfr_code, year):
    """
    Scrapes the full season schedule+results table from a team's PFR season page.

    Args:
        pfr_code: Pro Football Reference's 3-letter team code (e.g. 'buf')
        year: season year

    Returns:
        pandas DataFrame containing the season's games data
    """
    url = f'https://www.pro-football-reference.com/teams/{pfr_code}/{year}.htm'
    soup = _fetch_soup(url)

    table = _find_table(soup, 'games')
    if not table:
        raise ValueError("Table with id='games' not found on the page")

    column_headers = []
    thead = table.find('thead')
    if thead:
        header_row = thead.find_all('tr')[-1]
        for th in header_row.find_all('th'):
            column_headers.append(th.get('data-stat', th.text.strip()))

    data = []
    tbody = table.find('tbody')
    if tbody:
        for row in tbody.find_all('tr'):
            row_data = []
            for td in row.find_all(['td', 'th']):
                row_data.append(td.text.strip())

            if row_data and row_data[0] != 'Week':
                data.append(row_data)

    df = pd.DataFrame(data, columns=column_headers)

    return df


def scrape_weekly_weather_and_schedule(year, week):
    """
    Scrapes nflweather.com's per-week schedule page for game time, weather,
    wind, and broadcast channel. This is the most fragile scraper in the
    pipeline - nflweather.com has no stable CSS classes on the inner elements,
    so it's parsed by DOM position (next_sibling chains) and will likely need
    manual fixes each season if the site's markup shifts.

    Args:
        year: season year
        week: NFL week number

    Returns:
        pandas DataFrame, one row per game with columns:
        away_team_full, home_team_full, day_code, time_code, temp_f,
        weather_code, wind_mph, channel_code
    """
    url = f'https://www.nflweather.com/week/{year}/week-{week}'
    headers = {'User-Agent': 'Safari/537.36'}

    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    container = soup.find('div', class_='container-game-box')

    rows = []
    if not container:
        return pd.DataFrame(rows)

    matchup = container.div
    while matchup is not None:
        try:
            matchup_data1 = matchup.div
            date_and_time = matchup_data1.div.text.strip().split(' ')
            day_code = getDay(datetime.strptime(date_and_time[0], '%m/%d/%y').strftime('%A')[:3])

            hour = int(date_and_time[1].split(':')[0])
            am_pm = date_and_time[2]
            time_code = hour if am_pm.upper().startswith('A') else hour + 12

            matchup_data2 = matchup_data1.next_sibling.next_sibling
            away_team, _, home_team = matchup_data2.find_all('span')
            away_team = away_team.text
            home_team = home_team.text

            matchup_data3 = matchup_data2.next_sibling.next_sibling
            weather_data = matchup_data3.div.div.next_sibling.next_sibling
            weather_info = weather_data.find_all('span')

            if len(weather_info) == 0:
                temp = 62
                weather = 'Cloudy'
            elif len(weather_info) == 1:
                temp = int(weather_info[0].text.split(' ')[0])
                weather = 'Clear'
            else:
                temp_el, weather_el = weather_info
                temp = int(temp_el.text.split(' ')[0])
                weather = weather_el.text

            wind_container = weather_data.next_sibling.next_sibling
            wind_data = wind_container.find_all('span')
            wind = 0
            if len(wind_data) == 3:
                wind_text = wind_data[1].text.split(' ')[0]
                wind = int(wind_text) if wind_text.isdigit() else 0

            channel_data = wind_container.next_sibling.next_sibling
            channel_code = 0
            if channel_data is not None:
                channels = channel_data.find_all('span')
                if len(channels) > 1:
                    channel_text = channels[1].text
                    if ',' in channel_text:
                        channel_text = channel_text.split(',')[0]
                    elif ' ' in channel_text:
                        channel_text = channel_text.split(' ')[0]
                    channel_code = getChannel(channel_text)

            rows.append({
                'away_team_full': away_team,
                'home_team_full': home_team,
                'day_code': day_code,
                'time_code': time_code,
                'temp_f': temp,
                'weather_code': getWeatherCode(weather),
                'wind_mph': wind,
                'channel_code': channel_code,
            })
        except (AttributeError, ValueError, IndexError):
            pass

        matchup = matchup.next_sibling.next_sibling if matchup.next_sibling else None

    return pd.DataFrame(rows)


def _normalize_odds(text):
    """DraftKings renders minus signs as the unicode figure dash (U+2212);
    downstream parsing (updates.py, saveNFLData.py) expects an ASCII '-'."""
    return text.replace('−', '-').replace('–', '-').strip()


def scrape_weekly_gambling_data(week, year, week_date_ranges):
    """
    Scrapes DraftKings' NFL page (Selenium) for this week's spread, over/under,
    and moneyline for every matchup currently listed.

    DraftKings rebuilt its sportsbook frontend in 2026; the old
    `sportsbook-responsive-card-container` / `parlay-card-10-a` table markup is
    gone. The current page renders each game as a `cb-static-parlay__content--inner`
    block (2-column market template - team labels on the left, a fixed 6-button
    grid on the right: away spread, over, away ML, home spread, under, home ML).
    The blocks lazy-render on scroll, so we page down before parsing. This
    mirrors backendV2/scrapes.py's `scrape_todays_gambling_data`.

    Args:
        week: NFL week number (unused now - the DK slate widget only lists the
            immediate upcoming week; kept for call-site compatibility)
        year: season year (unused, kept for call-site compatibility)
        week_date_ranges: constants.WEEK_DATE_RANGES (unused, kept for
            call-site compatibility)

    Returns:
        pandas DataFrame with columns: awayTeam, homeTeam, awaySpread,
        overUnder, awayMoneyLine, homeSpread, homeMoneyLine
    """
    sleep_times = [3, 7, 13]

    driver = webdriver.Chrome()
    driver.get('https://sportsbook.draftkings.com/leagues/football/nfl')
    time.sleep(random.choice(sleep_times))

    # The market board lazy-renders game rows as they scroll into view.
    driver.find_element(By.CLASS_NAME, 'cb-static-parlay__event-wrapper')
    for y in range(0, 9000, 600):
        driver.execute_script(f'window.scrollTo(0, {y});')
        time.sleep(0.4)
    time.sleep(random.choice(sleep_times))

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

    data_rows = []
    seen = set()
    seen_teams = set()

    for block in soup.find_all('div', class_='cb-static-parlay__content--inner'):
        template = block.find(
            'div', class_='cb-market__template cb-market__template--2-columns'
        )
        if not template:
            continue

        left = template.find('div', class_='cb-side-column__left')
        right = template.find(
            'div', class_='cb-side-column__right cb-side-column__right--vertical'
        )
        if not left or not right:
            continue

        team_labels = left.find_all('div', class_='cb-market__label-wrapper')
        buttons = right.find_all('button')
        if len(team_labels) < 2 or len(buttons) < 6:
            continue

        away_team = team_labels[0].get_text(strip=True)
        home_team = team_labels[1].get_text(strip=True)

        vals = []
        for btn in buttons:
            points_el = btn.find('div', class_='cb-market__button-text-container')
            odds_el = btn.find('span', class_='cb-market__button-odds')
            points = points_el.get_text(strip=True) if points_el else ''
            odds = odds_el.get_text(strip=True) if odds_el else ''
            vals.append((points, odds))

        # Button order: 0 away spread, 1 over, 2 away ML, 3 home spread,
        # 4 under, 5 home ML.
        away_spread = _normalize_odds(vals[0][0])
        over_under = _normalize_odds(vals[1][0]).lstrip('OoUu')
        away_ml = _normalize_odds(vals[2][1])
        home_spread = _normalize_odds(vals[3][0])
        home_ml = _normalize_odds(vals[5][1])

        key = (away_team, home_team)
        if key in seen or not away_team or not home_team:
            continue

        # The widget lists the upcoming slate's games followed immediately by
        # the week after that (no header/date separates them). Each team
        # plays once a week, so the first repeated team marks the boundary -
        # stop there rather than blending two weeks' games together.
        if away_team in seen_teams or home_team in seen_teams:
            break
        seen_teams.add(away_team)
        seen_teams.add(home_team)
        seen.add(key)

        data_rows.append({
            'awayTeam': away_team,
            'homeTeam': home_team,
            'awaySpread': away_spread,
            'overUnder': over_under,
            'awayMoneyLine': away_ml,
            'homeSpread': home_spread,
            'homeMoneyLine': home_ml,
        })

    return pd.DataFrame(data_rows)
