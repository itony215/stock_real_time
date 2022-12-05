import pickle
import requests
from datetime import date
from io import StringIO
import pandas as pd
import json
from bs4 import BeautifulSoup
from datetime import datetime

eps = pd.read_pickle("/home/pineapple/Documents/stock/crawler/history/eps.pkl")

for stock_id in eps.columns:
    #print(stock_id)
    last_update = eps[stock_id].index[-1]
    r = requests.get('https://concords.moneydj.com/z/zc/zcd/zcd_'+stock_id+'.djhtm')
    soup = BeautifulSoup(r.text, 'html.parser')
    #data = soup.find_all("td", class_ = ["t3n0","t3n1"])
    table = soup.find_all('table')
    df = pd.read_html(str(table))[2]
    new_df = df[1:]
    new_df.columns = new_df.iloc[0]
    new_df = new_df.drop(new_df.index[0])
    
    for i in range(len(new_df)):
        if(last_update<=new_df.iloc[i]['季別']):
            #print('true')
            season = new_df.iloc[i]['季別']
            eps.loc[season,stock_id] = new_df.iloc[i]['稅後每股盈餘(元)']
        else:
            #print('false')
            break
eps = eps.sort_index()
eps.to_pickle("/home/pineapple/Documents/stock/crawler/history/eps.pkl")