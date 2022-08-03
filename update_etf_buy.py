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
#datestr = '2022/08/02'
# 上市
r = requests.post('https://www.twse.com.tw/exchangeReport/MI_INDEX?response=csv&date=' + datestr + '&type=ALL')
df = pd.read_csv(StringIO(r.text.replace("=", "")), header=["證券代號" in l for l in r.text.split("\n")].index(True)-1, index_col=['證券代號'])
df=df[df.index.str.len() <5]
df1 = df.iloc[:, 0:1]
#上櫃
#r = requests.post('https://www.tpex.org.tw/web/stock/aftertrading/daily_close_quotes/stk_quote_result.php?l=zh-tw&d=' + datestr+'&s=0,asc,0')
r = requests.post('https://www.tpex.org.tw/web/stock/aftertrading/daily_close_quotes/stk_quote_result.php')
json_data = json.loads(r.text)
stock_json = json_data["aaData"]
df2 = pd.DataFrame(stock_json)
df2 = df2.set_index([0])
df2=df2[df2.index.str.len() <5]
df3 = df2.iloc[:, 0:1]
df3.columns = ['證券名稱']

stock_list_df = df1.append(df3)

result = []
for s in stock_list_df.index:
    print(s)
    r = requests.get('https://concords.moneydj.com/z/zc/zco/zco.djhtm?a='+str(s)+'&e='+datestr+'&f='+datestr)
    soup = BeautifulSoup(r.text, 'html.parser')
    data = soup.find_all("td", class_ = ["t4t1","t3n1"])
    date = soup.find("div", {"class": "t11"})
    try:
        if day in date.getText():
            result.append([s,stock_list_df[stock_list_df.index==s]['證券名稱'].values[0],\
                        data[0].getText(),data[3].getText(),data[4].getText(),\
                        data[10].getText(),data[13].getText(),data[14].getText(),\
                        data[20].getText(),data[23].getText(),data[24].getText(),\
                        data[5].getText(),'-'+data[8].getText(),'-'+data[9].getText(),\
                        data[15].getText(),'-'+data[18].getText(),'-'+data[19].getText(),\
                        data[25].getText(),'-'+data[28].getText(),'-'+data[29].getText(),\
                        int(data[-7].getText().replace(',', ''))-int(data[-5].getText().replace(',', ''))])
        else:
            print('No update ', s, stock_list_df[stock_list_df.index==s]['證券名稱'].values[0])
    except:
        print('Error ', s, stock_list_df[stock_list_df.index==s]['證券名稱'].values[0])
        pass
new_df = pd.DataFrame(result)
new_df.to_csv("./ETF_buy/隔日衝占比_"+datestr+".csv",encoding='utf_8_sig', index = False)