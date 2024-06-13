from automation.scraper import NesineScrapper
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
import pandas as pd

class BasketballMatchDriver(NesineScrapper):

    # Base URL
    URL = 'https://www.nesine.com/iddaa/canli-iddaa-canli-bahis?code='
    # Number of seconds for waiting to synchronize
    SYNC_SECOND = 1
    COLUMNS = ['match_id', 'team_1', 'team_2', 'remaining_time', 'period', 'period_activity']
    
    def __init__(self,  match_id, url=URL):
        super(BasketballMatchDriver, self).__init__()
        
        try:
            self.match_id = match_id
            self.url = url + self.match_id

            # Goes to the given address
            self.driver.get(self.url)

            # Pass entrance 
            self.pass_entrance()

        except WebDriverException:
            print("[WEB_DRIVER_EXCEPTION]: Web driver can not be reached out at the moment.")
    
    # Get the team names in the match
    def get_team_names(self):
        try:
            team_1 = self.driver.find_element(By.XPATH, '//*[@id="live-match-detail"]/div/div[1]/div[2]/div/a/div/table/tbody/tr/td[1]').text
            team_2 = self.driver.find_element(By.XPATH, '//*[@id="live-match-detail"]/div/div[1]/div[2]/div/a/div/table/tbody/tr/td[3]').text
            return [{'team_names': [team_1, team_2]}]
        except NoSuchElementException:
            return [{'team_names': [None, None]}]

    # Get the current score
    def get_score(self):
        try: 
            scores = list(map(lambda score: score.strip(), self.driver.find_element(By.XPATH, '//*[@id="live-match-detail"]/div/div[1]/div[2]/div/a/div/table/tbody/tr/td[2]').text.split('-')))
            return [{'scores': scores}]
        except:
            return [{'scores': [None, None]}]
    
    # Get the remaining time in a period
    def get_remaining_time(self):
        try: 
            scores = list(map(lambda score: score.strip(), self.driver.find_element(By.XPATH, '//*[@id="live-match-detail"]/div/div[1]/div[2]/div/a/div/table/tbody/tr/td[2]').text.split('-')))
            return [{'scores': scores}]
        except:
            return [{'scores': [None, None]}]

    # Get the what period is being played
    def get_period_number(self):
        pass

    # Get the info about is the period is being played or break between the period
    def get_period_activity(self):
        pass

    ## Get bets
    # Returns list of dictionaries
    def get_detailed_bets(self, match_id, bets=['all_match', 'first_half', 'period_1', 'period_2', 'period_3', 'period_4']):
        match_id = match_id[0]

        # Expands detailed bet view
        match_expand_collapse_button = self.driver.find_element(By.XPATH, f'//*[@id="{match_id}_m"]/a')
        match_expand_collapse_button.click()

        return_list = []

        for bet in bets:
            match bet:
                case 'all_match':
                    return_list.extend([{'all_match': self.get_bet_ms(match_id=match_id)}])
                case 'first_half':
                    return_list.extend([{'first_half': self.get_bet_ms(match_id=match_id)}])
                case 'period_1':
                    return_list.extend([{'period_1': self.get_bet_period_x(match_id=match_id, period_number=1)}])
                case 'period_2':
                    return_list.extend([{'period_2': self.get_bet_period_x(match_id=match_id, period_number=2)}])
                case 'period_3':
                    return_list.extend([{'period_3': self.get_bet_period_x(match_id=match_id, period_number=3)}])
                case 'period_4':
                    return_list.extend([{'period_4': self.get_bet_period_x(match_id=match_id, period_number=4)}])
        
        # Collapses detailed bet view
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