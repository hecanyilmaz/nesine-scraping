# Librarires
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import sys

# Match code
match_code = sys.argv[1] #1551676 1549698


# Opening a new driver and goes to the match page
dynamic_url = f"https://www.nesine.com/iddaa/canli-iddaa-canli-bahis?code={match_code}"
driver = webdriver.Chrome()
driver.get(dynamic_url)


## Skipping insturction page
# Waiting for to view skip instruction button
time.sleep(2)

# Skips instructions
button = driver.find_element(By.XPATH, '//*[@id="tutorial"]/div/div[1]/div[1]/button')
button.click()


# Getting new information
while(True):
    print(driver.find_element(By.XPATH, f'//*[@id="collapse-{match_code}-all-0"]/div/div[1]/div[2]/div/div[2]/a[3]/span').text)
    time.sleep(20)