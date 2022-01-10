from IPython.display import display, clear_output
from urllib.request import urlopen
import pandas as pd
import math
from datetime import datetime, timedelta
import requests
import sched
import time
import json
import os.path as path
from bs4 import BeautifulSoup
s2 = sched.scheduler(time.time, time.sleep)
import dataframe_image as dfi
import glob

def lineNotify(token, msg, picURI):
    url = "https://notify-api.line.me/api/notify"
    headers = {
        "Authorization": "Bearer " + token
    }
   
    payload = {'message': msg}
    files = {'imageFile': open(picURI, 'rb')}
    r = requests.post(url, headers = headers, params = payload, files = files)
    return r.status_code

def alert_checker():
    for file in glob.glob("./5K/*.csv"):
        name =  path.basename(file)
        df = pd.read_csv(file, header=0)
        get_time = datetime.strptime(df.iloc[-1][0], '%Y-%m-%d %H:%M:%S')
        time = datetime.now()
        notice = ''
        if(len(df.index)>=3 and get_time-time<timedelta(minutes = 5) and time-get_time<timedelta(minutes = 5)):
            if(df.iloc[-1]['漲幅']>df.iloc[-2]['漲幅'] and df.iloc[-2]['漲幅']>df.iloc[-3]['漲幅']):
                notice += '漲兩根!'
            if(df.iloc[-1]['漲幅']<df.iloc[-2]['漲幅'] and df.iloc[-2]['漲幅']<df.iloc[-3]['漲幅']):
                notice += '跌兩根!'
            if(df.iloc[-1]['當盤成交量']>3*df.iloc[-2]['當盤成交量'] or df.iloc[-1]['當盤成交量']>3*df.iloc[-3]['當盤成交量']):
                notice += '有大量!'
        if len(notice) >0:
            notice = '['+ name +'] 注意!!'+ notice
            df_filter = df.filter(["五分K", "當盤成交價", "當盤成交量","累積成交量"])
            dfi.export(df_filter[-3:], 'df_styled.png')
            
            lineNotify('EDC3C8i9dTQz6n5AUBiLCtHWJmpn3odYjr5gtdR1p7h', notice, 'df_styled.png')
            vp = name.split('_')[0]
            df2 = pd.read_csv("./price_volumn/"+vp+'.csv', header=0, index_col = 0)
            df2 = df2.fillna(0)
            df15 = df2.sort_values('ma30', ascending=False).head(15)
            df15 = df15.sort_index(ascending=False)
            dfi.export(df15, 'df15.png')
            print(notice)
            
            lineNotify('EDC3C8i9dTQz6n5AUBiLCtHWJmpn3odYjr5gtdR1p7h', notice, 'df15.png')
        
        
    time = datetime.now()  
    print("更新時間:" + str(time.hour)+":"+str(time.minute)+":"+str(time.second))
    start_time = datetime.strptime(str(time.date())+'9:00', '%Y-%m-%d%H:%M')
    end_time =  datetime.strptime(str(time.date())+'13:25', '%Y-%m-%d%H:%M')
    
    # 判斷爬蟲終止條件
    if time >= start_time and time <= end_time:
        s2.enter(299, 0, alert_checker)

# 每秒定時器
s2.enter(1, 0, alert_checker)
s2.run()