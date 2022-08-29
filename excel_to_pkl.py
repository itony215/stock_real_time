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

column = ['時間','融資(張)','差額(張)','使用率','融券(張)','差額(張).1']

with os.scandir('./data_0804/') as it:
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
            new_df['使用率'] = new_df['使用率']*100
            new_df['券資比'] = round(new_df['融券(張)']/new_df['融資(張)']*100,2)
            new_df=new_df[["stock_id","時間","融資(張)","差額(張)","使用率","融券(張)","差額(張).1","券資比"]]
            new_df.columns = ["stock_id","date","融資(張)","融資差額(張)","融資使用率","融券(張)","融券差額(張)","券資比"]
            new_df.set_index(keys = ["stock_id","date"],inplace=True)
            
        combine = pd.concat([combine,new_df],axis=0)
combine.to_pickle("./融資融券.pkl")