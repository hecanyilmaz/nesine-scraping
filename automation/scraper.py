# Libraries
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
import time

class NesineScrapper:

    # Constants
    SYNC_SECOND = 2

    def __init__(self):
        self.driver = webdriver.Chrome()
        pass

    # Skipping insturction view
    def pass_entrance(self, sync_second=SYNC_SECOND):

        # Skips instructions
        button_instructions = self.find_element_until(By.XPATH, '//*[@id="tutorial"]/div/div[1]/div[1]/button', wait=sync_second)
        button_instructions.click()

        time.sleep(1)    

        # Accept cookies and awaits for SYNC_SECOND
        button_cookies = self.find_element_until(By.XPATH, '//*[@id="c-p-bn"]', wait=sync_second)
        button_cookies.click()

        time.sleep(1)    

        # Closes summer advertisement and awaits for SYNC_SECOND
        button_cookies = self.find_element_until(By.XPATH, '//*[@id="mod-base"]/div/div/div[1]/a', wait=sync_second)
        button_cookies.click()

        time.sleep(1)   

    # Tries to find ELEMENT between a time interval
    def find_element_until(self, strategy, locator, wait=0, poll_frequency=0):
        try: 
            return WebDriverWait(self.driver, wait, poll_frequency=poll_frequency).until(lambda x: x.find_element(strategy, locator))
        except TimeoutException:
            raise NoSuchElementException
    
    # Tries to find ELEMENTS between a time interval
    def find_elements_until(self, strategy, locator, wait=0, poll_frequency=0):
        try: 
            return WebDriverWait(self.driver, wait, poll_frequency=poll_frequency).until(lambda x: x.find_elements(strategy, locator))
        except TimeoutException:
            return NoSuchElementException