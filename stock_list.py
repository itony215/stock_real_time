import pandas as pd
import requests
from io import StringIO
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
stock_list_df.index.name = 'stock_id'
stock_list_old = pd.read_pickle("./stock_list.pkl")
if(len(stock_list_df)> len(stock_list_old)):
    stock_list_df.to_pickle("/home/pineapple/Documents/stock/crawler/stock_list.pkl")