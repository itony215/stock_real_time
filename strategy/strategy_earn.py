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
        return pd.Series()
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

def price_handle(stock_id,day):
    try:
        df0 = pd.DataFrame(end[stock_id])
        df0.columns=['收盤價']
        df0['漲跌幅'] = round(df0['收盤價'].pct_change()*100,2)
        return df0.loc[day]
    except:
        #return pd.Series(dtype='float64')
        return pd.Series()

def earn_handle(stock_id):
    try:
        today = date.today()
        first = today.replace(day=1)
        lastMonth = first - timedelta(days=1)
        lastMonth_str=lastMonth.strftime("%Y/%m")
        return earn.loc[stock_id,lastMonth_str]
    except:
        return pd.Series(dtype='float64')


three = pd.read_pickle("/home/pineapple/Documents/stock/crawler/three/三大法人買賣超.pkl")
end = pd.read_pickle("/home/pineapple/Documents/stock/crawler/history/收盤價.pkl")
main = pd.read_pickle("/home/pineapple/Documents/stock/crawler/main/主力買賣超.pkl")
earn = pd.read_pickle("/home/pineapple/Documents/stock/crawler/history/營收.pkl")
stock_list = pd.read_pickle("/home/pineapple/Documents/stock/crawler/history/stock_list.pkl")
good_earn_list = pd.read_csv("/home/pineapple/Documents/stock/crawler/strategy/good_earn_list.csv")
bad_earn_list = pd.read_csv("/home/pineapple/Documents/stock/crawler/strategy/bad_earn_list.csv")

today = date.today()
yesterday = today - timedelta(days=1)
first = today.replace(day=1)
lastMonth = first - timedelta(days=1)
lastMonth_str=lastMonth.strftime("%Y/%m")

get_list = []
get_list_2 = []
#today = '2023-01-06'
# for stock_id in tqdm(three.index.levels[0]):
#     print(type(stock_id))
for i in (good_earn_list.index):
    stock_id = str(good_earn_list.iloc[i].values[0])
    #print(type(stock_id))
    try:
        df0 = price_handle(stock_id,str(today))
        df1 = three_handle(stock_id,str(today))
        df2 = main_handle(stock_id,str(today))
        df3 = earn_handle(stock_id)
        df4 = stock_list.loc[stock_id]
        df4['id'] = str(df4.name)
        combine = pd.concat([df0,df1,df2,df3,df4])
        get_list.append(combine)
    except:
        print('error: ',stock_id)
for i2 in (bad_earn_list.index):
    stock_id = str(bad_earn_list.iloc[i2].values[0])
    #print(type(stock_id))
    try:
        df0 = price_handle(stock_id,str(today))
        df1 = three_handle(stock_id,str(today))
        df2 = main_handle(stock_id,str(today))
        df3 = earn_handle(stock_id)
        df4 = stock_list.loc[stock_id]
        df4['id'] = str(df4.name)
        combine = pd.concat([df0,df1,df2,df3,df4])
        get_list_2.append(combine)
    except:
        print('error: ',stock_id)
#print()
result = pd.DataFrame(get_list,columns=['id','name','category','收盤價','漲跌幅','投信持股比例','投信買賣超%','投信買賣超(張)',\
                                         '投信5買%','投信10買%','投信20買%','投信5買N天','投信10買N天','投信20買N天',\
                                         "外資持股比例","外資買賣超(張)","外資買賣超%","外資5買%","外資10買%","外資20買%",'外資5買N天',\
                                         '外資10買N天','外資20買N天'"自營商買賣超(張)","自營商買賣超%","自營商持股比例",\
                                         "主力買賣超(張)","主力今日%",'主力5買%','主力10買%','主力20買%','月增率%','年增率%','累計年增率%'])

result.to_csv("/home/pineapple/Documents/stock/crawler/strategy/stock_data/data/年月營收增.csv",encoding='utf_8_sig', index = False)

result2 = pd.DataFrame(get_list_2,columns=['id','name','category','收盤價','漲跌幅','投信持股比例','投信買賣超%','投信買賣超(張)',\
                                         '投信5買%','投信10買%','投信20買%','投信5買N天','投信10買N天','投信20買N天',\
                                         "外資持股比例","外資買賣超(張)","外資買賣超%","外資5買%","外資10買%","外資20買%",'外資5買N天',\
                                         '外資10買N天','外資20買N天'"自營商買賣超(張)","自營商買賣超%","自營商持股比例",\
                                         "主力買賣超(張)","主力今日%",'主力5買%','主力10買%','主力20買%','月增率%','年增率%','累計年增率%'])

result2.to_csv("/home/pineapple/Documents/stock/crawler/strategy/stock_data/data/年月營收減.csv",encoding='utf_8_sig', index = False)