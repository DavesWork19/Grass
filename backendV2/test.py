"""
TradingView US Stock Gainers Scraper
======================================
Scrapes div[data-query-type="media"] > table from:
https://www.tradingview.com/markets/stocks-usa/market-movers-gainers/

Requirements:
    pip install selenium pandas webdriver-manager

Usage:
    python tradingview_gainers_scraper.py

Output:
    gainers.csv
"""

import re
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

URL = "https://www.tradingview.com/markets/stocks-usa/market-movers-gainers/"


def clean(text: str) -> str:
    """Strip whitespace, newlines, and non-breaking spaces."""
    text = text.replace('\xa0', ' ')
    return re.sub(r'\s+', ' ', text).strip()


def clean_company(text: str) -> str:
    """Clean company name: remove commas and all quote characters."""
    text = clean(text)
    # Remove commas
    text = text.replace(',', '')
    # Remove all quote variants (straight + curly)
    text = text.replace('"', '')
    text = text.replace("'", '')
    text = text.replace('\u2018', '')   # left single quotation mark '
    text = text.replace('\u2019', '')   # right single quotation mark '
    text = text.replace('\u201c', '')   # left double quotation mark "
    text = text.replace('\u201d', '')   # right double quotation mark "
    return text.strip()


def build_driver() -> webdriver.Chrome:
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    )
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)


def get_headers(driver) -> list[str]:
    """
    Read column names from <th> elements in the scrollable (non-sticky) thead.
    Replaces the first 'Symbol' header with two columns: 'Ticker' and 'Company'.
    """
    ths = driver.find_elements(
        By.CSS_SELECTOR,
        'div[data-query-type="media"] div.tableWrap-kuYuZ1id thead th'
    )
    headers = []
    for th in ths:
        label = clean(th.text)
        if not label:
            label = th.get_attribute("data-field") or "—"
        headers.append(label)

    if headers:
        headers = ["Ticker", "Company"] + headers[1:]

    return headers


def parse_ticker_cell(td) -> tuple[str, str]:
    """Extract ticker symbol and company name from the first <td>."""
    try:
        ticker = clean(td.find_element(By.CSS_SELECTOR, "a.tickerName-ixuo49jq").text)
    except Exception:
        ticker = ""
    try:
        company = clean_company(td.find_element(By.CSS_SELECTOR, "a.tickerDescription-ixuo49jq").text)
    except Exception:
        company = ""
    return ticker, company


def parse_rows(driver, headers: list[str]) -> list[dict]:
    """Parse all visible <tr> rows from tbody into a list of dicts."""
    rows_data = []
    tbody = driver.find_element(
        By.CSS_SELECTOR,
        'div[data-query-type="media"] '
        'div.tableWrap-kuYuZ1id '
        'tbody[data-testid="selectable-rows-table-body"]'
    )
    rows = tbody.find_elements(By.TAG_NAME, "tr")

    for row in rows:
        tds = row.find_elements(By.TAG_NAME, "td")
        if not tds:
            continue

        ticker, company = parse_ticker_cell(tds[0])
        cells = [ticker, company]

        for td in tds[1:]:
            cells.append(clean(td.text))

        while len(cells) < len(headers):
            cells.append("")
        cells = cells[: len(headers)]

        rows_data.append(dict(zip(headers, cells)))

    return rows_data


def scrape_gainers() -> pd.DataFrame:
    print("[+] Launching browser ...")
    driver = build_driver()
    all_rows: list[dict] = []

    try:
        print(f"[+] Opening {URL}")
        driver.get(URL)

        print("[+] Waiting for table body ...")
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR,
                'tbody[data-testid="selectable-rows-table-body"] tr[data-rowkey]'
            ))
        )
        time.sleep(2)

        headers = get_headers(driver)
        print(f"[+] Columns ({len(headers)}): {headers}")

        all_rows = parse_rows(driver, headers)
        print(f"[+] Initial rows: {len(all_rows)}")

        last_count = len(all_rows)
        for scroll_n in range(1, 20):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            all_rows = parse_rows(driver, headers)
            if len(all_rows) == last_count:
                print(f"[+] No new rows after scroll #{scroll_n}. Done.")
                break
            last_count = len(all_rows)
            print(f"    Scroll #{scroll_n}: {last_count} rows ...")

    finally:
        driver.quit()

    return pd.DataFrame(all_rows)


def main():
    df = scrape_gainers()

    print("\n── Preview (first 10 rows) ───────────────────────────────────────")
    print(df.head(10).to_string(index=False))
    print(f"\nTotal rows : {len(df)}")
    print(f"Columns    : {list(df.columns)}")

    df.to_csv("gainers.csv", index=False)
    print("\n[✓] Saved to 'gainers.csv'")


if __name__ == "__main__":
    main()