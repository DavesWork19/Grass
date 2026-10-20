from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
from bs4 import BeautifulSoup, Comment
import re
import time
import random
import pandas as pd


def scrape_misc_data_by_team(url):
    """
    Scrape Pace column with Team and Lg Rank rows from Basketball Reference
    
    Args:
        url: Basketball Reference team page URL
    
    Returns:
        Dictionary containing the scraped data
    """

    initial_delay = random.uniform(1.5, 3.5)
    time.sleep(initial_delay)
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    processing_delay = random.uniform(0.5, 1.5)
    time.sleep(processing_delay)
    
    soup = BeautifulSoup(response.content, 'lxml')
    
    team_misc_div = soup.find('div', id='div_team_misc')
    
    if not team_misc_div:
        html = response.text
        match = re.search(r'<!--\s*(<div[^>]*id="div_team_misc".*?</div>)\s*-->', html, re.DOTALL)
        
        if match:
            comment_html = match.group(1)
            team_misc_div = BeautifulSoup(comment_html, 'lxml')
        else:
            return None
    
    table = team_misc_div.find('table') if isinstance(team_misc_div, BeautifulSoup) else team_misc_div.find('table')
    
    if not table:
        return None
    
    data = {}
    stats_to_extract = ['pace', 'mov', 'srs', 'off_rtg', 'def_rtg']
    
    for row in table.find_all('tr'):
        th = row.find('th')
        
        row_label = th.get_text(strip=True)
        
        if row_label in ('Team', 'Lg Rank'):
            
            for stat in stats_to_extract:
                cell = row.find(attrs={'data-stat': stat})
                if cell:
                    data[f'{stat}_{row_label}'] = cell.get_text(strip=True)
            
            if len(data) == 2:
                break
    
    return pd.DataFrame.from_dict([data])


def scrape_all_game_data_by_team(url):
    """
    Scrape all rows and columns from team_game_log_reg table
    
    Args:
        url: Basketball Reference game log page URL
    
    Returns:
        pandas DataFrame containing all game log data
    """

    initial_delay = random.uniform(1.5, 3.5)
    time.sleep(initial_delay)
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    processing_delay = random.uniform(0.5, 1.5)
    time.sleep(processing_delay)
    
    soup = BeautifulSoup(response.content, 'lxml')

    table = soup.find('table', id='team_game_log_reg')
    
    # If not found, search in HTML comments
    if not table:
        html = response.text
        match = re.search(r'<!--\s*(<table[^>]*id="team_game_log_reg".*?</table>)\s*-->', html, re.DOTALL)
        
        if match:
            table_html = match.group(1)
            table = BeautifulSoup(table_html, 'lxml').find('table')
            if table:
                print(f"Found table in comments")
    
    if not table:
        print("Table with id='team_game_log_reg' not found!")
        return pd.DataFrame()
    
    columns = []
    
    thead = table.find('thead')
    if thead:
        header_rows = thead.find_all('tr')
        unblocked_header_rows = header_rows[1].find_all('th')

        for th in unblocked_header_rows:
            col_name = th.get('data-stat', th.get_text(strip=True))
            
            if col_name:
                columns.append(col_name)
                         
    else:
        print('No thead found for team_game_log_reg table!')


    tbody = table.find('tbody')
    
    if not tbody:
        return pd.DataFrame()
    
    data_rows = [
        [cell.get_text(strip=True) for cell in row.find_all(['th', 'td'])]
        for row in tbody.find_all('tr')
        if not (row.get('class') and 'thead' in row.get('class')) and row.find(['th', 'td'])
    ]
    
    if not (data_rows and columns):
        return pd.DataFrame()
    
    return pd.DataFrame(data_rows, columns=columns)


def _normalize_odds(text):
    """DraftKings renders minus signs as the unicode figure dash (U+2212); the
    frontend parseFloat()s spreads and updates.py parses a leading ASCII '-'."""
    return text.replace('\u2212', '-').replace('\u2013', '-').strip()


def scrape_todays_gambling_data():
    """
    Scrapes DraftKings' NBA page for the spread, over/under and moneyline of
    every listed game. Each game is a `cb-static-parlay__content--inner` block
    with a fixed 6-button grid: away spread, over, away ML, home spread, under,
    home ML. Blocks lazy-render on scroll, so we page down before parsing.

    The board can run past today into tomorrow's games - saveData drops any
    team whose next Basketball Reference game isn't today.
    """
    sleepTimes = [5, 9, 13]

    driver = webdriver.Chrome()
    driver.get("https://sportsbook.draftkings.com/leagues/basketball/nba")
    time.sleep(random.choice(sleepTimes))

    driver.find_element(By.CLASS_NAME, 'cb-static-parlay__event-wrapper')
    for y in range(0, 9000, 600):
        driver.execute_script(f'window.scrollTo(0, {y});')
        time.sleep(0.4)
    time.sleep(random.choice(sleepTimes))

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

    data_rows = []
    seen_teams = set()

    for div in soup.find_all('div', {'class': 'cb-static-parlay__content--inner'}):
        nextDiv = div.find('div', {'class': 'cb-market__template cb-market__template--2-columns'})
        if not nextDiv:
            continue
        leftData = nextDiv.find('div', {'class': 'cb-side-column__left'})
        rightData = nextDiv.find('div', {'class': 'cb-side-column__right cb-side-column__right--vertical'})
        if not leftData or not rightData:
            continue
        teamNames = leftData.find_all('div', {'class': 'cb-market__label-wrapper'})
        gamblingDataButtons = rightData.find_all('button')
        if len(teamNames) < 2 or len(gamblingDataButtons) < 6:
            continue

        awayTeam = teamNames[0].get_text(strip=True)
        homeTeam = teamNames[1].get_text(strip=True)

        # A team plays at most once a day; a repeat means the board has moved
        # on to a later day's slate.
        if awayTeam in seen_teams or homeTeam in seen_teams:
            break
        seen_teams.update([awayTeam, homeTeam])

        vals = []
        for gamblingData in gamblingDataButtons:
            points = gamblingData.find('div', {'class': 'cb-market__button-text-container'})
            odds = gamblingData.find('span', {'class': 'cb-market__button-odds'})
            vals.append((
                _normalize_odds(points.get_text(strip=True)) if points else '',
                _normalize_odds(odds.get_text(strip=True)) if odds else '',
            ))

        data_rows.append({
                'awayTeam': awayTeam,
                'homeTeam': homeTeam,
                'awaySpread': vals[0][0],
                'overUnder': vals[1][0].lstrip('OoUu').strip(),
                'awayMoneyLine': vals[2][1],
                'homeSpread': vals[3][0],
                'homeMoneyLine': vals[5][1]
                })

    return pd.DataFrame(data_rows)



def scrape_upcoming_game_by_team(url):
    """
    Scrapes the games table from Basketball Reference and returns a pandas DataFrame.
    
    Args:
        url: The URL of the Basketball Reference games page
        
    Returns:
        pandas DataFrame containing the games data
    """
    initial_delay = random.uniform(1.5, 3.5)
    time.sleep(initial_delay)

    # Send GET request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    initial_delay = random.uniform(1.5, 3.5)
    time.sleep(initial_delay)
    
    # Parse HTML
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table', {'id': 'games'})
    
    if not table:
        raise ValueError("Table with id='games' not found on the page")
    
    headers = []
    thead = table.find('thead')
    if thead:
        header_row = thead.find_all('tr')[-1]  # Get last row in case of multi-row headers
        for th in header_row.find_all('th'):
            headers.append(th.get('data-stat', th.text.strip()))
    
    data = []
    tbody = table.find('tbody')
    if tbody:
        for row in tbody.find_all('tr'):
                
            row_data = []
            for td in row.find_all(['td', 'th']):
                row_data.append(td.text.strip())
            
            if row_data[0] != 'G':  
                data.append(row_data)
    
    df = pd.DataFrame(data, columns=headers)
    
    return df


