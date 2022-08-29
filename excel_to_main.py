import pickle
import requests
from datetime import date
from io import StringIO
import pandas as pd
import json
from bs4 import BeautifulSoup
from tqdm import tqdm
from datetime import datetime
import os

column = ['時間','買賣超(張).3','主力持股(張)']
stock_total_release = pd.read_pickle("/home/pineapple/Documents/stock/crawler/stock_total_release.pkl")
with os.scandir('/home/pineapple/Documents/stock/crawler/margin/data_0804/') as it:
    combine=pd.DataFrame([])
    for entry in tqdm(it):
        if entry.name.endswith(".xlsx") and entry.is_file():
            #print(entry.name, entry.path)
            df=pd.read_excel(entry.path)
            df = pd.DataFrame(df,columns = column)
            target=[]
            stock_id = entry.name.split(".")[0]
            try:
                total_release = float(stock_total_release.loc[stock_id]['total'])
            except:
                total_release = 1
            for i in df.index:
                if not(df.loc[i].isnull().values.any()): 
                    target.append(i)
            
            new_df = pd.DataFrame(df, index= target)
            new_df.insert(0, "stock_id",stock_id)
            
            new_df['主力今日%'] = round(new_df['買賣超(張).3']/total_release*100,2) 
            new_df['主力持有%'] = round(new_df['主力持股(張)']/total_release*100,2)

            new_df=new_df[["stock_id","時間","買賣超(張).3","主力持股(張)","主力今日%","主力持有%"]]
            new_df.columns = ["stock_id","date","主力買賣超(張)","主力持股(張)","主力今日%","主力持有%"]
            new_df.set_index(keys = ["stock_id","date"],inplace=True)
            
        combine = pd.concat([combine,new_df],axis=0)
combine.to_pickle("./主力買賣超.pkl")