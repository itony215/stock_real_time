import pickle
import requests
from datetime import date
from io import StringIO
import pandas as pd
import json
from bs4 import BeautifulSoup
from tqdm import tqdm
import datetime
import os
def transform_ym(date):   #民國轉西元
        y, m, d = date.split('/')
        return str(int(y)+1911) + '-' + m + '-' + d

main = pd.read_pickle("/home/pineapple/Documents/stock/crawler/main/主力買賣超.pkl")
stock_total_release = pd.read_pickle("/home/pineapple/Documents/stock/crawler/main/stock_total_release.pkl")
today = date.today()
day = datetime.timedelta(days=1)
#day = today.strftime("%m/%d")
#datestr = today.strftime("%Y-%m-%d")
#datestr = '2022-08-11'
for stock_id in tqdm(main.index.levels[0]):
    old_date = main.loc[stock_id].iloc[-1].name
    day1 = old_date + day
    while day1 <= today:
        daystr = day1.strftime('%Y-%m-%d')
        print(daystr,stock_id)
    #if(old_date<str(today)):
        #print(stock_id)
        try:
            r = requests.get('https://concords.moneydj.com/z/zc/zco/zco.djhtm?a='+str(stock_id)+'&e='+daystr+'&f='+daystr)
            #https://concords.moneydj.com/z/zc/zcl/zcl_1101.djhtm
            soup = BeautifulSoup(r.text, 'html.parser')
            data = soup.find_all("td", class_ = ["t4t1","t3n1"])
            new_data = float(data[-7].getText().replace(',', ''))-int(data[-5].getText().replace(',', ''))
            main.loc[(stock_id,daystr),'主力買賣超(張)'] = new_data
            main.loc[(stock_id,daystr),'主力持股(張)'] = main.loc[stock_id].iloc[-1]['主力持股(張)']+new_data

        except:
            print('no update: ', stock_id)
            pass
            
        try:
            total_release = float(stock_total_release.loc[stock_id]['total'])
            main.loc[(stock_id,daystr),'主力今日%'] = round(new_data/total_release*100,2)
            main.loc[(stock_id,daystr),'主力持有%'] = round((main.loc[stock_id].iloc[-1]['主力持股(張)']+new_data)/total_release*100,2)
        except:
            pass
        day1 = day1 + day
#     else:
#         print('no update')
main = main.sort_index()
main.to_pickle("/home/pineapple/Documents/stock/crawler/main/主力買賣超_0812.pkl")