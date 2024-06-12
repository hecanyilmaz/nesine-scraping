from api.nesine_basketball_pre import PreMatchDriver
import pandas as pd
import os
from datetime import datetime, timedelta

DAILY_FETCH_DIR = os.path.join(os.path.curdir, "basketball_daily")
FILE_PATH = os.path.join(DAILY_FETCH_DIR, f'{(datetime.now()+timedelta(1)).strftime("%Y-%m-%d")}.csv')
COLUMNS = ['match_id', 'match_time', 'team_1', 'team_2', 'ms_1', 'ms_x', 'ms_2', 'fh_1', 'fh_x', 'fh_2', 'p1_1', 'p1_x', 'p1_2', 'p2_1', 'p2_x', 'p2_2', 'p3_1','p3_x', 'p3_2','p4_1', 'p4_x', 'p4_2']

nesine_driver = PreMatchDriver()
nesine_driver.filter_configuration(day='tomorrow')
ids_dic_list = nesine_driver.get_ids_of_matches()

records = []

for id_dic in ids_dic_list:
    record, match_id = list(), id_dic[0]['match_id'][0]
    
    match_team_names = nesine_driver.get_team_names(match_id)
    match_bets = nesine_driver.get_detailed_bets(match_id=match_id)
    match_time = nesine_driver.get_match_time(match_id)
    
    record.extend(match_bets)
    record.extend(id_dic)
    record.extend(match_team_names)
    record.extend(match_time)

    
    records.append(record)


x = nesine_driver.to_df(records, save_it=True, path=FILE_PATH)