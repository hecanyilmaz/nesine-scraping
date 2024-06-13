from automation.football import FootballDriver

import sys
import os
from datetime import datetime, timedelta


# arg1 represents the day: today, tomorrow, next-day
def main(arg1):
    DIR = os.path.join(os.path.curdir, "football_daily")
    match arg1:
        case 'today':
            FILE_PATH = os.path.join(DIR, f'{(datetime.now()+timedelta(0)).strftime("%Y-%m-%d")}.csv')
        case 'tomorrow':
            FILE_PATH = os.path.join(DIR, f'{(datetime.now()+timedelta(1)).strftime("%Y-%m-%d")}.csv')
        case 'next-day':
            FILE_PATH = os.path.join(DIR, f'{(datetime.now()+timedelta(2)).strftime("%Y-%m-%d")}.csv')
    
    # Call Nesine.com Basketball driver and fetch specified days matches
    nesine_driver = FootballDriver()
    nesine_driver.filter_configuration(day=arg1)
    ids_list = nesine_driver.get_ids()

    records = []

    for match_id in ids_list:
        record = list()
        
        match_team_names = nesine_driver.get_team_names(match_id)
        match_bets = nesine_driver.get_detailed_bets(match_id=match_id)
        match_time = nesine_driver.get_match_time(match_id)
        
        record.extend([{'match_id': [match_id]}])
        record.extend(match_bets)
        record.extend(match_team_names)
        record.extend(match_time)

        records.append(record)

    nesine_driver.to_df(records, save=True, path=FILE_PATH)

if __name__ == "__main__":
    main(sys.argv[1])