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
s = sched.scheduler(time.time, time.sleep)
a=0
def lineNotify(token, msg):
    url = "https://notify-api.line.me/api/notify"
    headers = {
        "Authorization": "Bearer " + token
    }
   
    payload = {'message': msg}
    #files = {'imageFile': open(picURI, 'rb')}
    r = requests.post(url, headers = headers, params = payload)
    return r.status_code
def stock_crawler(a):   
    clear_output(wait=True)
    try:
        url = requests.get("https://www.taifex.com.tw/mCht/quotesApi/getQuotes?objId=12")
        text = url.text

        data = json.loads(text)
        tx = data[0]
        print(tx['price'],tx['updown'])
        diff = abs(a-int(tx['updown']))
        a = int(tx['updown'])
        #print('a',a )
        print('diff', diff)
        notice = '\n台指期: '+tx['price']+', 漲跌: '+tx['updown']+', 差距: '+str(diff)
        if diff >5:
            lineNotify('X57Kb4EhV6073WKCE9UU2eT3IBvxmY44LPtmdUwwS8O', notice)
        if diff >20:     
            lineNotify('OBv21vIdKofMJ7MzL5Pwf6Y8iS9lOsoDbhTocAs6668', notice)
    except Exception as e:
        print(e)
    # 紀錄更新時間
    time = datetime.now()  
    print("更新時間:" + str(time.hour)+":"+str(time.minute)+":"+str(time.second))
    
    #display(df)
    
    start_time = datetime.strptime(str(time.date())+'14:01', '%Y-%m-%d%H:%M')
    end_time =  datetime.strptime(str(time.date())+'23:59', '%Y-%m-%d%H:%M')
    
    # 判斷爬蟲終止條件
    s.enter(300, 0, stock_crawler,argument=(a,))


# 每秒定時器
s.enter(1, 0, stock_crawler,argument=(a,))
s.run()