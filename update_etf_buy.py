import pandas as pd
import numpy as np
import requests
import datetime
import time
from io import StringIO
from bs4 import BeautifulSoup
import pickle
import os
import json
from datetime import date


today = date.today()
day = today.strftime("%m/%d")
datestr = today.strftime("%Y%m%d")
stock_list_df = pd.read_pickle("/home/pineapple/Documents/stock/crawler/stock_list.pkl")
#datestr = "20220811"
#day = "08/11"
result = []
for s in stock_list_df.index:
    print(s)
    r = requests.get('https://concords.moneydj.com/z/zc/zco/zco.djhtm?a='+str(s)+'&e='+datestr+'&f='+datestr)
    soup = BeautifulSoup(r.text, 'html.parser')
    data = soup.find_all("td", class_ = ["t4t1","t3n1"])
    date = soup.find("div", {"class": "t11"})
    try:
        if day in date.getText():
            result.append([s,stock_list_df[stock_list_df.index==s]['name'].values[0],\
                        data[0].getText(),data[3].getText(),data[4].getText(),\
                        data[10].getText(),data[13].getText(),data[14].getText(),\
                        data[20].getText(),data[23].getText(),data[24].getText(),\
                        data[5].getText(),'-'+data[8].getText(),'-'+data[9].getText(),\
                        data[15].getText(),'-'+data[18].getText(),'-'+data[19].getText(),\
                        data[25].getText(),'-'+data[28].getText(),'-'+data[29].getText(),\
                        int(data[-7].getText().replace(',', ''))-int(data[-5].getText().replace(',', ''))])
        else:
            print('No update ', s, stock_list_df[stock_list_df.index==s]['name'].values[0])
    except:
        print('Error ', s, stock_list_df[stock_list_df.index==s]['name'].values[0])
        pass
new_df = pd.DataFrame(result)
new_df.to_csv("/home/pineapple/Documents/stock/crawler/ETF_buy/隔日衝占比_"+datestr+".csv",encoding='utf_8_sig', index = False)
new_df.to_pickle("/home/pineapple/Documents/stock/crawler/ETF_buy_pkl/隔日衝占比_"+datestr+".pkl")