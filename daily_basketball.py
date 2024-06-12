# Libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import os
import pandas as pd
from datetime import datetime

# Constants
DYNAMIC_URL = "https://www.nesine.com/iddaa/basketbol"
SYNC_SECOND = 1
DAILY_FETCH_DIR = os.path.join(os.path.curdir, "matches_daily_fetches")
FILE_PATH = os.path.join(DAILY_FETCH_DIR, f'b_daily_{datetime.now().strftime("%Y-%m-%d_%H:%M:%S")}.csv')
COLUMNS = ['match_id', 'ms_1', 'ms_2', 'y_1', 'y_x', 'y_2','1p_1','1p_x', '1p_2','2p_1','2p_x', '2p_2','3p_1','3p_x', '3p_2','4p_1', '4p_x', '4p_2']

# Returns XPATH text as string
def xpath_value(xpath):
    return driver.find_element(By.XPATH, xpath).text

# If variable doesn't exist take it as NULL value
def split_strip_func(xpath, entries):
    try: 
        text = xpath_value(xpath).split()
        if (len(text) == entries):
            return list(map(lambda val: val.strip(), text))
        else:
            return [None for i in range(entries)] 
    except NoSuchElementException:
        return [None for i in range(entries)]

    

# Opens a new web driver, goes to the given page
driver = webdriver.Chrome()
driver.get(DYNAMIC_URL)

## Skipping insturction view
# Waiting for to view skip instruction button
time.sleep(SYNC_SECOND)
# Skips instructions
button_instructions = driver.find_element(By.XPATH, '//*[@id="tutorial"]/div/div[1]/div[1]/button')
button_instructions.click()
time.sleep(SYNC_SECOND)

# Accept cookies and awaits for 2 seconds
button_cookies = driver.find_element(By.XPATH, '//*[@id="c-p-bn"]')
button_cookies.click()
time.sleep(SYNC_SECOND)

## See daily matches configuration
# Opens configuration
configure_date_button = driver.find_element(By.XPATH, '//*[@id="date-league-btn"]')
configure_date_button.click()
time.sleep(SYNC_SECOND)

# Filters for 'today' option
configure_today_button = driver.find_element(By.XPATH, '//*[@id="d-date-list"]/li[1]/div/label')
configure_today_button.click()
time.sleep(SYNC_SECOND)

# Applies filter
configure_apply_filter_button = driver.find_element(By.XPATH, '//*[@id="d-btnDateLeagueFilter"]')
configure_apply_filter_button.click()
time.sleep(SYNC_SECOND)

# Creating dataframe
daily_info_df = pd.DataFrame(columns=COLUMNS)

# Get list of matches
list_of_matches = driver.find_elements(By.CSS_SELECTOR, "div.odd-col.event-list.pre-event")

# Traverse through the list of matches
for match in list_of_matches:
    # Match ID
    match_code = match.get_attribute('data-code')

    # Expands and collapses a match's details.
    match_expand_collapse_button = driver.find_element(By.XPATH, f'//*[@id="{match_code}_m"]/a')
    match_expand_collapse_button.click()

    # Bets
    ms = split_strip_func(f'//*[@id="collapse-{match_code}-all-0"]/div/div[1]/div[2]/div/div[2]', entries= 2)
    first_half = split_strip_func(f'//*[@id="collapse-{match_code}-all-2"]/div/div/div[2]/div/div[2]', entries= 3)
    period_1 = split_strip_func(f'//*[@id="collapse-{match_code}-all-4"]/div/div[1]/div[2]/div/div[2]', entries= 3)
    period_2 = split_strip_func(f'//*[@id="collapse-{match_code}-all-4"]/div/div[2]/div[2]/div/div[2]', entries= 3)
    period_3 = split_strip_func(f'//*[@id="collapse-{match_code}-all-4"]/div/div[3]/div[2]/div/div[2]', entries= 3)
    period_4 = split_strip_func(f'//*[@id="collapse-{match_code}-all-4"]/div/div[4]/div[2]/div/div[2]', entries= 3)

    # Row
    df_temp = pd.DataFrame([[match_code, ms[0], ms[1],
        first_half[0], first_half[1], first_half[2],
        period_1[0], period_1[1], period_1[2],
        period_2[0], period_1[1], period_1[2],
        period_3[0], period_1[1], period_1[2],
        period_4[0], period_1[1], period_1[2]
    ]], columns=COLUMNS)

    # Concatenate new row with the main dataframe
    daily_info_df = pd.concat([daily_info_df, df_temp], ignore_index=True)

    match_expand_collapse_button.click()

# Save to csv file!
daily_info_df.to_csv(FILE_PATH)

print("INFO: Number of matches fetched: ", len(list_of_matches))










"""
while(True):
    ms_1 = xpath_value(f'//*[@id="collapse-{match_code}-all-0"]/div/div[1]/div[2]/div/div[2]/a[1]/span[1]')
    ms_2 = xpath_value(f'//*[@id="collapse-{match_code}-all-0"]/div/div[1]/div[2]/div/div[2]/a[2]/span[1]')

    first_half_1 = xpath_value(f'//*[@id="collapse-{match_code}-all-2"]/div/div/div[2]/div/div[2]/a[1]/span[2]')
    first_half_x = xpath_value(f'//*[@id="collapse-{match_code}-all-2"]/div/div/div[2]/div/div[2]/a[2]/span[2]')
    first_half_2 = xpath_value(f'//*[@id="collapse-{match_code}-all-2"]/div/div/div[2]/div/div[2]/a[3]/span[2]')

    print_xpath('//*[@id="r_1548765"]/div[2]/dl/dd[2]/div/div/div')
    print_xpath('//*[@id="r_1548765"]/div[1]/div[3]/a')
    print_xpath('//*[@id="r_1548765"]/div[1]/div[2]')
    print(i.get_attribute('data-code'))
    x = i.text.split("\n")
    print("Time: ", x[0])
    print("Teams and MS:")
    print(x[1].split('-')[0].strip(), x[2].split()[0])
    print(x[1].split('-')[1].strip(), x[2].split()[1])
    print("---------------")
    time.sleep(60)
"""