import pickle
import requests
from datetime import date,timedelta
from io import StringIO
import pandas as pd
import json
from bs4 import BeautifulSoup
from datetime import datetime
import os
from pandas import Timestamp

margin = pd.read_pickle("/home/pineapple/Documents/stock/crawler/margin/融資融券.pkl")
three = pd.read_pickle("/home/pineapple/Documents/stock/crawler/three/三大法人買賣超.pkl")
volumn = pd.read_pickle("/home/pineapple/Documents/stock/crawler/history/成交股數.pkl")
end = pd.read_pickle("/home/pineapple/Documents/stock/crawler/history/收盤價.pkl")
high = pd.read_pickle("/home/pineapple/Documents/stock/crawler/history/最高價.pkl")
low = pd.read_pickle("/home/pineapple/Documents/stock/crawler/history/最低價.pkl")
start = pd.read_pickle("/home/pineapple/Documents/stock/crawler/history/開盤價.pkl")
high=high.fillna(0)
low=low.fillna(0)
start=start.fillna(0)
end=end.fillna(0)
volumn=volumn.fillna(0)
three=three.fillna(0)
margin=margin.fillna(0)

today = datetime.today()
for i in start.columns:  #['2201']:
    result=[]
    date=[]
    startday_str = '01/4/21 8:00:00'
    startday = datetime.strptime(startday_str, '%m/%d/%y %H:%M:%S')
    startday_ymd = startday.strftime("%Y-%m-%d")
    
    df0 = pd.DataFrame(end[i])
    df0.columns=['收盤價']
    df0['ma5']=round(df0["收盤價"].rolling(window=5).mean(),2)
    df0['ma10']=round(df0["收盤價"].rolling(window=10).mean(),2)
    df0['ma20']=round(df0["收盤價"].rolling(window=20).mean(),2)
    df0['ma60']=round(df0["收盤價"].rolling(window=60).mean(),2)
    
    filepath = '/home/pineapple/Documents/stock/crawler/flat_viewer/json/data_'+i+'.json'
    if os.path.exists(filepath):
        with open(filepath, mode='r+') as f:
            data = json.load(f)
            lastupdate_str = data['date'][-1]+ ' 8:00:00'
            lastupdate = datetime.strptime(lastupdate_str, '%Y-%m-%d %H:%M:%S')
            lastupdate = lastupdate + timedelta(days=1)
            #lastupdate_ymd = data['date'][-1]
            lastupdate_ymd = lastupdate.strftime("%Y-%m-%d")
            #print('lastupdate',lastupdate)
            #print(lastupdate<start.index[-1]+ timedelta(days=1))
            #print(start.index[-1]+ timedelta(days=1))
            while lastupdate < (start.index[-1]+ timedelta(days=1)):
                # print('go')
                try:
                    timestr = float(lastupdate.timestamp())*1000
                    

                    if((i,lastupdate_ymd) in margin.index):
                        mar=margin.loc[i].loc[lastupdate_ymd]['融券差額(張)']
                    else:
                        mar=0

                    if((i,lastupdate_ymd) in three.index):
                        thr=three.loc[i].loc[lastupdate_ymd]['投信買賣超(張)']
                    else:
                        thr=0

                    data['stock_data'].append(
                        [timestr,start[i][lastupdate_ymd],high[i][lastupdate_ymd],low[i][lastupdate_ymd],end[i][lastupdate_ymd],
                         round(volumn[i][lastupdate_ymd]/1000,2),thr,mar,
                        df0.loc[lastupdate_ymd]['ma5'],df0.loc[lastupdate_ymd]['ma10'],df0.loc[lastupdate_ymd]['ma20'],df0.loc[lastupdate_ymd]['ma60']
                        ])
                    data['date'].append(lastupdate_ymd)
                        #date.append(lastupdate_ymd)
                except:
                    pass
                lastupdate = lastupdate + timedelta(days=1)
                #print(data['date'])

            f.seek(0) 
            json.dump(data, f,indent=2)
            f.truncate() 
    else:
        print(i)
        while startday < today:
            try:
                timestr = float(startday.timestamp())*1000
                startday_ymd = startday.strftime("%Y-%m-%d")

                if((i,startday_ymd) in margin.index):
                    mar=margin.loc[i].loc[startday_ymd]['融券差額(張)']
                else:
                    mar=0

                if((i,startday_ymd) in three.index):
                    thr=three.loc[i].loc[startday_ymd]['投信買賣超(張)']
                else:
                    thr=0
                
                result.append(
                    [timestr,start[i][startday_ymd],high[i][startday_ymd],low[i][startday_ymd],end[i][startday_ymd],
                     round(volumn[i][startday_ymd]/1000,2),thr,mar,
                    df0.loc[startday_ymd]['ma5'],df0.loc[startday_ymd]['ma10'],df0.loc[startday_ymd]['ma20'],df0.loc[startday_ymd]['ma60']
                    ])
                date.append(startday_ymd)
            except:
                pass


            startday = startday + timedelta(days=1)
        dictionary = {
                        "stock_id": i,
                        "date": date,
                        "stock_data": result,
                    }


        json_object = json.dumps(dictionary, indent=2)
        with open('/home/pineapple/Documents/stock/crawler/flat_viewer/json/data_'+str(i)+'.json', 'w') as json_file:
            json_file.write(json_object)