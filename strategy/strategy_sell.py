import pickle
import requests
from datetime import date,timedelta
from io import StringIO
import pandas as pd
import json
from bs4 import BeautifulSoup
from tqdm import tqdm
from datetime import datetime
import os
from pandas import Timestamp
def three_handle(stock_id,day):
    try:
        df = three.loc[stock_id]
        df['三大買賣超'] = df['投信買賣超(張)']+df['外資買賣超(張)']+df['自營商買賣超(張)']
        df['投信5買N天'] =(df['投信買賣超(張)'].gt(0)).rolling(5,min_periods=1).sum()
        df['投信5買N天'] = df['投信5買N天'].fillna(0).astype(int)
        df['投信10買N天'] =(df['投信買賣超(張)'].gt(0)).rolling(10,min_periods=1).sum()
        df['投信10買N天'] = df['投信10買N天'].fillna(0).astype(int)
        df['投信20買N天'] =(df['投信買賣超(張)'].gt(0)).rolling(20,min_periods=1).sum()
        df['投信20買N天'] = df['投信20買N天'].fillna(0).astype(int)

        df['投信5買%'] =round(df['投信買賣超%'].rolling(5,min_periods=1).sum(),2)
        df['投信5買%'] = df['投信5買%'].fillna(0).astype(float)
        df['投信10買%'] =round(df['投信買賣超%'].rolling(10,min_periods=1).sum(),2)
        df['投信10買%'] = df['投信10買%'].fillna(0).astype(float)
        df['投信20買%'] =round(df['投信買賣超%'].rolling(20,min_periods=1).sum(),2)
        df['投信20買%'] = df['投信20買%'].fillna(0).astype(float)

        df['外資5買N天'] =(df['外資買賣超(張)'].gt(0)).rolling(5,min_periods=1).sum()
        df['外資5買N天'] = df['外資5買N天'].fillna(0).astype(int)
        df['外資10買N天'] =(df['外資買賣超(張)'].gt(0)).rolling(10,min_periods=1).sum()
        df['外資10買N天'] = df['外資10買N天'].fillna(0).astype(int)
        df['外資20買N天'] =(df['外資買賣超(張)'].gt(0)).rolling(20,min_periods=1).sum()
        df['外資20買N天'] = df['外資20買N天'].fillna(0).astype(int)

        df['外資5買%'] =round(df['外資買賣超%'].rolling(5,min_periods=1).sum(),2)
        df['外資5買%'] = df['外資5買%'].fillna(0).astype(float)
        df['外資10買%'] =round(df['外資買賣超%'].rolling(10,min_periods=1).sum(),2)
        df['外資10買%'] = df['外資10買%'].fillna(0).astype(float)
        df['外資20買%'] =round(df['外資買賣超%'].rolling(20,min_periods=1).sum(),2)
        df['外資20買%'] = df['外資20買%'].fillna(0).astype(float)
        return df.loc[day]
    except:
        return pd.Series(dtype='float64')
def main_handle(stock_id,day):
    try:
        df2 = main.loc[stock_id]
        df2['主力5買%'] = round(df2['主力今日%'].rolling(5,min_periods=1).sum(),2)
        df2['主力5買%'] = df2['主力5買%'].fillna(0).astype(float)
        df2['主力10買%'] =round(df2['主力今日%'].rolling(10,min_periods=1).sum(),2)
        df2['主力10買%'] = df2['主力10買%'].fillna(0).astype(float)
        df2['主力20買%'] =round(df2['主力今日%'].rolling(20,min_periods=1).sum(),2)
        df2['主力20買%'] = df2['主力20買%'].fillna(0).astype(float)
        return df2.loc[day]
    except:
        return pd.Series(dtype='float64')
        #return pd.Series()

def end_price_handle(stock_id,day):
    try:
        df0 = pd.DataFrame(end[stock_id])
        df0.columns=['收盤價']
        df0['漲跌幅'] = round(df0['收盤價'].pct_change()*100,2)
        df0['昨日收盤價'] = df0['收盤價'].shift(1)
        df0['昨日漲跌幅'] = round(df0['昨日收盤價'].pct_change()*100,2)
        df0['ma5']=df0["收盤價"].rolling(window=5).mean()
        df0['ma10']=df0["收盤價"].rolling(window=10).mean()
        df0['ma20']=df0["收盤價"].rolling(window=20).mean()
        df0['ma60']=df0["收盤價"].rolling(window=60).mean()
        df0['ma5距離'] = round((df0['收盤價'] - df0['ma5']),2)
        df0['ma10距離'] =round((df0['收盤價'] - df0['ma10']),2)
        df0['ma20距離'] =round((df0['收盤價'] - df0['ma20']),2)
        df0['ma60距離'] =round((df0['收盤價'] - df0['ma60']),2)
        return df0.loc[day]
    except:
        #return pd.Series(dtype='float64')
        return pd.Series(dtype='float64')
def start_price_handle(stock_id,day):
    try:
        df3 = pd.DataFrame(start[stock_id])
        df3.columns=['開盤價']
        df3['昨日開盤價'] = df3['開盤價'].shift(1)
        return df3.loc[day]
    except:
        #return pd.Series(dtype='float64')
        return pd.Series(dtype='float64')
def high_price_handle(stock_id,day):
    try:
        df4 = pd.DataFrame(high[stock_id])
        df4.columns=['最高價']
        return df4.loc[day]
    except:
        #return pd.Series(dtype='float64')
        return pd.Series(dtype='float64')
def volumn_handle(stock_id,day):
    try:
        df5 = pd.DataFrame(volumn[stock_id])
        df5.columns=['成交量']
        df5['成交量'] = round(df5['成交量']/1000,2)
        return df5.loc[day]
    except:
        #return pd.Series(dtype='float64')
        return pd.Series(dtype='float64')

def earn_handle(stock_id):
    try:
        today = date.today()
        first = today.replace(day=1)
        lastMonth = first - timedelta(days=1)
        lastMonth_str=lastMonth.strftime("%Y/%m")
        return earn.loc[stock_id,lastMonth_str]
    except:
        #return pd.Series(dtype='float64')
        return pd.Series(dtype='float64')
def margin_handle(stock_id,day):
    try:
        df10 = margin.loc[stock_id]
        df10['昨日融券'] = df10['融券差額(張)'].shift(1)
        df10['融券5N']=(df10['融券差額(張)'].gt(0)).rolling(5,min_periods=1).sum()
        df10['融券5N'] = df10['融券5N'].fillna(0).astype(int)
        df10['融券增加'] = round((df10['融券差額(張)']-df10['昨日融券'])/df10['昨日融券']*100,2)
        return df10.loc[day]
    except:
        return pd.Series(dtype='float64')
margin = pd.read_pickle("/home/pineapple/Documents/stock/crawler/margin/融資融券.pkl")
three = pd.read_pickle("/home/pineapple/Documents/stock/crawler/three/三大法人買賣超.pkl")
volumn = pd.read_pickle("/home/pineapple/Documents/stock/crawler/history/成交股數.pkl")
end = pd.read_pickle("/home/pineapple/Documents/stock/crawler/history/收盤價.pkl")
high = pd.read_pickle("/home/pineapple/Documents/stock/crawler/history/最高價.pkl")
low = pd.read_pickle("/home/pineapple/Documents/stock/crawler/history/最低價.pkl")
start = pd.read_pickle("/home/pineapple/Documents/stock/crawler/history/開盤價.pkl")
main = pd.read_pickle("/home/pineapple/Documents/stock/crawler/main/主力買賣超.pkl")
earn = pd.read_pickle("/home/pineapple/Documents/stock/crawler/history/營收.pkl")
stock_list = pd.read_pickle("/home/pineapple/Documents/stock/crawler/stock_list.pkl")

today = date.today()
yesterday = today - timedelta(days=1)
first = today.replace(day=1)
lastMonth = first - timedelta(days=1)
lastMonth_str=lastMonth.strftime("%Y/%m")

get_list = []
#yesterday = '2022-08-26'
for stock_id in tqdm(three.index.levels[0]):
    try:
        df0 = end_price_handle(stock_id,str(today))
        df1 = three_handle(stock_id,str(today))
        df2 = main_handle(stock_id,str(today))
        df3 = earn_handle(stock_id)
        df4 = stock_list.loc[stock_id]
        df4['id'] = str(df4.name)
        df5 = start_price_handle(stock_id,str(today))
        df6 = high_price_handle(stock_id,str(today))
        df7 = volumn_handle(stock_id,str(today))
        df10 = margin_handle(stock_id,str(today))
        combine = pd.concat([df0,df1,df2,df3,df4,df5,df6,df7,df10])
        combine['開盤位置']=round((combine['開盤價']-combine['昨日收盤價'])/combine['昨日收盤價']*100,2)
        combine['A轉跌幅']=round((combine['收盤價']-combine['最高價'])/combine['最高價']*100,2)
        get_list.append(combine)
    except:
        print('error: ',stock_id)
#print()
result = pd.DataFrame(get_list,columns=['id','name','category','昨日收盤價','昨日漲跌幅','開盤位置','開盤價','收盤價','漲跌幅','A轉跌幅','成交量','三大買賣超','投信買賣超(張)','投信買賣超%','投信持股比例',\
                                         "外資買賣超(張)","外資買賣超%","外資持股比例","自營商買賣超(張)","自營商買賣超%","自營商持股比例", "主力買賣超(張)","主力今日%",'投信5買%','投信10買%','投信20買%','投信5買N天','投信10買N天','投信20買N天',\
                                         "外資5買%","外資10買%","外資20買%",'外資5買N天','外資10買N天','外資20買N天',\
                                         '主力5買%','主力10買%','主力20買%','月增率%','年增率%','累計年增率%',\
                                         'ma5距離','ma10距離','ma20距離','ma60距離','融券5N','昨日融券','融券差額(張)','融券增加'])

result.to_csv("/home/pineapple/Documents/stock/crawler/strategy/stock_data/data/所有股票資訊_sell.csv",encoding='utf_8_sig', index = False)