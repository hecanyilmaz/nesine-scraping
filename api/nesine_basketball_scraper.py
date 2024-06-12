# Libraries
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
import time

class NesineBasketballDriver:

    # Constants
    SYNC_SECOND = 2
    driver = webdriver.Chrome()
    
    def __init__(self):
        pass

    # Skipping insturction view
    def pass_entrance(self, sync_second=SYNC_SECOND):

        # Waiting for to view skip instruction button

        # Skips instructions
        button_instructions = self.find_element_until(By.XPATH, '//*[@id="tutorial"]/div/div[1]/div[1]/button', wait=sync_second)
        button_instructions.click()

        time.sleep(1)    

        # Accept cookies and awaits for SYNC_SECOND
        button_cookies = self.find_element_until(By.XPATH, '//*[@id="c-p-bn"]', wait=sync_second)
        button_cookies.click()

    # Tries to find element between a time interval
    def find_element_until(self, strategy, locator, wait=0, poll_frequency=0):
        try: 
            return WebDriverWait(self.driver, wait, poll_frequency=poll_frequency).until(lambda x: x.find_element(strategy, locator))
        except TimeoutException:
            raise NoSuchElementException
    
    # Tries to find elements between a time interval
    def find_elements_until(self, strategy, locator, wait=0, poll_frequency=0):
        try: 
            return WebDriverWait(self.driver, wait, poll_frequency=poll_frequency).until(lambda x: x.find_elements(strategy, locator))
        except TimeoutException:
            return NoSuchElementException