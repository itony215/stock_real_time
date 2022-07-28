import pickle
import requests
import datetime
from io import StringIO
import pandas as pd
import json
from bs4 import BeautifulSoup

def transform_ym(date): 
        y, m = date.split('/')
        return str(int(y)+1911) + '/' + m

today = datetime.date.today()
first = today.replace(day=1)
lastMonth = first - datetime.timedelta(days=1)
lastMonth.strftime("%Y/%m")

earn = pd.read_pickle("/home/pineapple/Documents/stock/crawler/history/營收.pkl")
today = datetime.date.today()
first = today.replace(day=1)
lastMonth = first - datetime.timedelta(days=1)
lastMonth.strftime("%Y/%m")

for stock_id in earn.index.levels[0]:
    try:
        if(earn.loc[stock_id].iloc[-1].name<lastMonth.strftime("%Y/%m")):
            r = requests.get('https://concords.moneydj.com/z/zc/zch/zch.djhtm?a='+stock_id)
            soup = BeautifulSoup(r.text, 'html.parser')
            data = soup.find_all("td", class_ = ["t3n0","t3n1"])
            table = soup.find_all('table')
            df = pd.read_html(str(table))[-1]
            new_df = df[5:]
            new_df.columns = new_df.iloc[0]
            new_df = new_df.drop(new_df.index[0])
            date = transform_ym(new_df.iloc[0]['年/月'])
            print(stock_id)
            if(earn.loc[stock_id].iloc[-1].name<date):
                print('ok')
                print(stock_id)

                earn.loc[(stock_id,date),'營收(千)'] = new_df.iloc[0,1]
                earn.loc[(stock_id,date),'月增率%'] = new_df.iloc[0,2].replace('%','')
                earn.loc[(stock_id,date),'去年同期(千)'] = new_df.iloc[0,3]
                earn.loc[(stock_id,date),'年增率%'] = new_df.iloc[0,4].replace('%','')
                earn.loc[(stock_id,date),'累計營收(千)'] = new_df.iloc[0,5]
                earn.loc[(stock_id,date),'累計年增率%'] = new_df.iloc[0,6].replace('%','')
    except:
        print('no data: ', stock_id)
        continue
earn.to_pickle("/home/pineapple/Documents/stock/crawler/history/營收.pkl")