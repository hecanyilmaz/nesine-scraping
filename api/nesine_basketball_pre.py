from api.nesine_basketball_scraper import NesineBasketballDriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, NoSuchElementException
from selenium.common.exceptions import WebDriverException
import pandas as pd

class PreMatchDriver(NesineBasketballDriver):

    URL = 'https://www.nesine.com/iddaa/basketbol'
    SYNC_SECOND = 2
    COLUMNS = ['match_id', 'match_time', 'team_1', 'team_2', 'ms_1', 'ms_x', 'ms_2', 'fh_1', 'fh_x', 'fh_2', 'p1_1', 'p1_x', 'p1_2', 'p2_1', 'p2_x', 'p2_2', 'p3_1','p3_x', 'p3_2', 'p4_1', 'p4_x', 'p4_2']

    def __init__(self, url=URL):
        super(PreMatchDriver, self).__init__()

        try:
            # Goes to the address given
            self.driver.get(url)
            # Pass entrance 
            self.pass_entrance()

        except WebDriverException:
            print("[INFO]: Web driver can not be reached out at the moment.")

    # Clears the configuration have been made
    def clear_configuration(self, sync_second = SYNC_SECOND):

        # Opens configuration window
        configure_date_button = self.find_element_until(By.XPATH, '//*[@id="date-league-btn"]', wait=sync_second)
        configure_date_button.click()

        # Clears configs
        clear_button = self.find_element_until(By.XPATH, ' //*[@id="d-btnDateLeagueClear"]', wait=sync_second)
        clear_button.click()

        # Applies filter
        configure_apply_filter_button = self.find_element_until(By.XPATH, '//*[@id="d-btnDateLeagueFilter"]', wait=sync_second)
        configure_apply_filter_button.click()
    
    # Filters for configuration options
    def filter_configuration(self, day, sync_second = SYNC_SECOND, bypass_clearing=False):

        # Clearing past configured options if exist
        if (bypass_clearing==True):
            self.clear_configuration()

        # Opens configuration window
        configure_date_button = self.find_element_until(By.XPATH, '//*[@id="date-league-btn"]', wait=sync_second)
        configure_date_button.click()

        # Filtering for DAYS
        match day:
            case 'today':
                day_xpath = '//*[@id="d-date-list"]/li[1]/div/label'
            case 'tomorrow': 
                day_xpath = '//*[@id="d-date-list"]/li[2]/div/label'
            case 'next-day':
                day_xpath = '//*[@id="d-date-list"]/li[3]/div/label'
                
        # Filters for day option
        configure_today_button = self.find_element_until(By.XPATH, day_xpath, wait=sync_second)
        configure_today_button.click()
        
        # Applies filter
        configure_apply_filter_button = self.find_element_until(By.XPATH, '//*[@id="d-btnDateLeagueFilter"]', wait=sync_second)
        configure_apply_filter_button.click()

    # Get list of matches
    def get_list_of_matches(self):
        try:
            return self.find_elements_until(By.CSS_SELECTOR, "div.odd-col.event-list.pre-event")
        except NoSuchElementException:
            return []
    
    # Get ID's of matches as list
    def get_ids_of_matches(self):
        try:
            return [[{'match_id': [match.get_attribute('data-code')]}] for match in self.get_list_of_matches()]
        except NoSuchElementException:
            return [[None] for match in self.get_list_of_matches()]
    
    # Get team names from ID
    def get_team_names(self, match_id):
        try:
            team_names = list(map(lambda team_name: team_name.strip(), self.find_element_until(By.XPATH, f'//*[@id="r_{match_id}"]/div[1]/div[3]/a').text.split(' - ')))
            return [{'team_names': team_names}]
        except NoSuchElementException: 
            return [{'team_names': [None, None]}]

    # Get match hour from ID
    def get_match_time(self, match_id):
        try:
            match_time = self.find_element_until(By.XPATH, f'//*[@id="r_{match_id}"]/div[1]/div[2]/span').text
            return [{'match_time': [match_time]}]
        except NoSuchElementException:
            return [{'match_time': [None]}]

    # Get bet for 'ms'
    def get_bet_ms(self, match_id):
        try:
            ms_1 = self.find_element_until(By.XPATH, f'//*[@id="collapse-{match_id}-all-0"]/div/div[1]/div[2]/div/div[2]/a[1]').text
            ms_x = self.find_element_until(By.XPATH, f'//*[@id="collapse-{match_id}-all-0"]/div/div[1]/div[2]/div/div[2]/a[2]').text
            ms_2 = self.find_element_until(By.XPATH, f'//*[@id="collapse-{match_id}-all-0"]/div/div[1]/div[2]/div/div[2]/a[3]').text
        
        # When XPATH can not be reached out of for the moment
        except NoSuchElementException:
            return [None, None, None]
            
        if ms_2 == '':
            ms_2 = ms_x
            ms_x = None

        return [val if val != '' else None for val in [ms_1, ms_x, ms_2]]
    
    # Get bet for 'first_half'
    def get_bet_fh(self, match_id):
        try:
            fh_1 = self.find_element_until(By.XPATH, f'//*[@id="collapse-{match_id}-all-2"]/div/div/div[2]/div/div[2]/a[1]').text
            fh_x = self.find_element_until(By.XPATH, f'//*[@id="collapse-{match_id}-all-2"]/div/div/div[2]/div/div[2]/a[2]').text
            fh_2 = self.find_element_until(By.XPATH, f'//*[@id="collapse-{match_id}-all-2"]/div/div/div[2]/div/div[2]/a[3]').text
        
        # When XPATH can not be reached out of for the moment
        except NoSuchElementException:
            return [None, None, None]
            
        return [val if val != '' else None for val in [fh_1, fh_x, fh_2]]
    
    # Get bet for 'x th period'
    def get_bet_period_x(self, match_id, period_number):
        try:
            p_1 = self.find_element_until(By.XPATH, f'//*[@id="collapse-{match_id}-all-4"]/div/div[{period_number}]/div[2]/div/div[2]/a[1]').text
            p_x = self.find_element_until(By.XPATH, f'//*[@id="collapse-{match_id}-all-4"]/div/div[{period_number}]/div[2]/div/div[2]/a[2]').text
            p_2 = self.find_element_until(By.XPATH, f'//*[@id="collapse-{match_id}-all-4"]/div/div[{period_number}]/div[2]/div/div[2]/a[3]').text
        
        # When XPATH can not be reached out of for the moment
        except NoSuchElementException:
            return [None, None, None]
            
        return [val if val != '' else None for val in [p_1, p_x, p_2]]

    ## Get bets
    # Returns list of dictionaries
    def get_detailed_bets(self, match_id, bets=['all_match', 'first_half', 'period_1', 'period_2', 'period_3', 'period_4']):
        # Expands detailed bet view
        match_expand_collapse_button = self.find_element_until(By.XPATH, f'//*[@id="{match_id}_m"]')
        match_expand_collapse_button.click()

        return_list = []

        for bet in bets:
            match bet:
                case 'all_match':
                    return_list.extend([{'all_match': self.get_bet_ms(match_id=match_id)}])
                case 'first_half':
                    return_list.extend([{'first_half': self.get_bet_fh(match_id=match_id)}])
                case 'period_1':
                    return_list.extend([{'period_1': self.get_bet_period_x(match_id=match_id, period_number=1)}])
                case 'period_2':
                    return_list.extend([{'period_2': self.get_bet_period_x(match_id=match_id, period_number=2)}])
                case 'period_3':
                    return_list.extend([{'period_3': self.get_bet_period_x(match_id=match_id, period_number=3)}])
                case 'period_4':
                    return_list.extend([{'period_4': self.get_bet_period_x(match_id=match_id, period_number=4)}])
        
        # Collapses detailed bet view
        #match_expand_collapse_button = self.find_element_until(By.XPATH, f'//*[@id="{match_id}_m"]/a')
        match_expand_collapse_button.click()

        return return_list

    # Converting a record to the row as Pandas Dataframe
    def record_to_row(self, record):

        # To create a dataframe for the specific row, we put used columns and values into to lists
        columns = []
        values = []

        for dic in record:
            
            key = list(dic.keys())[0]
            value = dic.values()
            
            values.extend(*value)
            
            # Match the case to add appropriate columns to the row
            match key:
                case 'match_id':
                    columns.extend(['match_id'])
                case 'match_time':
                    columns.extend(['match_time'])
                case 'team_names':
                    columns.extend(['team_1', 'team_2'])
                case 'all_match':
                    columns.extend(['ms_1', 'ms_x', 'ms_2'])
                case 'first_half':
                    columns.extend(['fh_1', 'fh_x', 'fh_2'])
                case 'period_1':
                    columns.extend(['p1_1', 'p1_x', 'p1_2'])
                case 'period_2':
                    columns.extend(['p2_1', 'p2_x', 'p2_2'])
                case 'period_3':
                    columns.extend(['p3_1', 'p3_x', 'p3_2'])
                case 'period_4':
                    columns.extend(['p4_1', 'p4_x', 'p4_2'])

        df = pd.DataFrame([values], columns=columns)

        return df
    
    # Concatenating rows and building a Pandas Dataframe
    def to_df(self, multiple_records, path=False, save_it=False):

        df = pd.DataFrame(columns=self.COLUMNS)

        for record in multiple_records:
            row = self.record_to_row(record)
            df = pd.concat([df, row], ignore_index=True)

        # Save the dataframe as csv file
        if (save_it==True):
            df.to_csv(path, index=False)

        return df