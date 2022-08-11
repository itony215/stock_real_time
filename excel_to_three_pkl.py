import pickle
import requests
from datetime import date
from io import StringIO
import pandas as pd
import json
from bs4 import BeautifulSoup
from datetime import datetime
import os
from tqdm import tqdm
def transform_ym(date):   #民國轉西元
        y, m, d = date.split('/')
        return str(int(y)+1911) + '-' + m + '-' + d

column = ['時間','買賣超(張)','外資持股比例','買賣超(張).1','投信持股比例','買賣超(張).2','自營商持股比例']
with os.scandir('/home/pineapple/Documents/stock/crawler/margin/data_0804/') as it:
    combine=pd.DataFrame([])
    for entry in tqdm(it):
        if entry.name.endswith(".xlsx") and entry.is_file():
            print(entry.name, entry.path)
            df=pd.read_excel(entry.path)
            df = pd.DataFrame(df,columns = column)
            target=[]
            stock_id = entry.name.split(".")[0]
            for i in df.index:
                if not(df.loc[i].isnull().values.any()): 
                    target.append(i)
            
            new_df = pd.DataFrame(df, index= target)
            new_df.insert(0, "stock_id",stock_id)
            new_df['外資買賣超%'] = new_df['外資持股比例'].diff(1)*100
            new_df['外資持股比例'] = new_df['外資持股比例']*100
            new_df['投信買賣超%'] = new_df['投信持股比例'].diff(1)*100
            new_df['投信持股比例'] = new_df['投信持股比例']*100
            new_df['自營商買賣超%'] = new_df['自營商持股比例'].diff(1)*100
            new_df['自營商持股比例'] = new_df['自營商持股比例']*100
            new_df=new_df[["stock_id","時間","買賣超(張).1","投信買賣超%","投信持股比例","買賣超(張)","外資買賣超%","外資持股比例","買賣超(張).2","自營商買賣超%","自營商持股比例"]]
            new_df.columns = ["stock_id","date","投信買賣超(張)","投信買賣超%","投信持股比例","外資買賣超(張)","外資買賣超%","外資持股比例","自營商買賣超(張)","自營商買賣超%","自營商持股比例"]
            new_df.set_index(keys = ["stock_id","date"],inplace=True)
            
        combine = pd.concat([combine,new_df],axis=0)
combine.to_pickle("./三大法人買賣超.pkl")        