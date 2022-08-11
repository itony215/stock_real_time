import pandas as pd
import numpy as np
import requests
import datetime
import time

from io import StringIO
from bs4 import BeautifulSoup
from tqdm import tqdm
import pickle
import os
import json
from datetime import date
from tqdm import tqdm

today = date.today()
day = today.strftime("%m/%d")
stock_list_df = pd.read_pickle("./stock_list.pkl")

date2 = datetime.date(2022, 8, 10)
day = datetime.timedelta(days=1)

for s in tqdm(stock_list_df.index):
    date1 = datetime.date(2018, 1, 2)
    result = []
    while date1 <= date2:
        try:
            daystr = date1.strftime('%Y-%m-%d')
            r = requests.get('https://concords.moneydj.com/z/zc/zco/zco.djhtm?a='+str(s)+'&e='+daystr+'&f='+daystr)
            soup = BeautifulSoup(r.text, 'html.parser')
            data = soup.find_all("td", class_ = ["t4t1","t3n1"])
            print(s,daystr)
            data_by_date = [daystr,s,stock_list_df[stock_list_df.index==s]['證券名稱'].values[0]]
            
            for item in range(0,int(len(data)-8),10):
                if(data[item].getText()==""):
                    continue
                else:
                    data_by_date.append(data[item].getText())
                    data_by_date.append(float(data[item+3].getText().replace(',','')))
                    data_by_date.append(float(data[item+4].getText().replace('%','')))

            for item in range(5,int(len(data)-8),10):
                if(data[item].getText()==""):
                    continue
                else:
                    data_by_date.append(data[item].getText())
                    data_by_date.append(-float(data[item+3].getText().replace(',','')))
                    data_by_date.append(-float(data[item+4].getText().replace('%','')))
                    
            result.append(data_by_date)   
        except:
            print('error: ',s,date1)
            pass       
        date1 = date1 + day
    

    new_df = pd.DataFrame(result)
    #new_df.to_csv("/home/pineapple/Documents/stock/crawler/ETF_buy/隔日衝占比_"+datestr+".csv",encoding='utf_8_sig', index = False)
    new_df.to_pickle("./main_force_buy/主力券商買賣超_"+str(s)+".pkl")