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
s = sched.scheduler(time.time, time.sleep)
import string
df = pd.read_csv("/home/pineapple/Documents/stock/CDP.csv", header=0)
def lineNotify(token, msg):
    url = "https://notify-api.line.me/api/notify"
    headers = {
        "Authorization": "Bearer " + token
    }
   
    payload = {'message': msg}
    r = requests.post(url, headers = headers, params = payload)
    return r.status_code

def stock_crawler(targets):
    clear_output(wait=True)
    stock_list = "|".join("{}".format(target) for target in targets) 
    query_url = "http://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch="+ stock_list
    try:
        data = json.loads(urlopen(query_url).read())    
        for r in data['msgArray']:
            if (r['z'] == '-'):
                if(r['a'] == '-'):
                    r['z'] = r['b'].split('_')[0]
                else:
                    r['z'] = r['a'].split('_')[0]
            notice=""
            ah = df.loc[df['股票代號'] == int(r['c'])].AH.item()
            nh = df.loc[df['股票代號'] == int(r['c'])].NH.item()
            nl = df.loc[df['股票代號'] == int(r['c'])].NL.item()
            al = df.loc[df['股票代號'] == int(r['c'])].AL.item()

            #print(r['z'])
            #print(ah)
            if(float(r['z'])>=ah):
                notice = 'AH'
            elif(float(r['z'])>=nh):
                notice = 'NH'
            elif(float(r['z'])<=nl):
                notice = 'NL'
            elif(float(r['z'])<=al):
                notice = 'AL'
            else:
                #print('沒波動: ', r['z'])
                pass

            if(len(notice)>1):
                string = df.loc[df['股票代號'] == int(r['c'])].Notice.item()
                stock_no = int(r['c'])
                if(string == notice):
                    pass
                elif(string == 'AH' and notice == 'NH'):
                    pass
                elif(string == 'AL' and notice == 'NL'):
                    pass
                else:
                    df.loc[df.股票代號==stock_no,'Notice'] = notice
                    notify = "{} {} {} {} (AH:{:.2f}, NH:{:.2f}, NL:{:.2f}, AL:{:.2f})".format(r['c'],r['n'],notice,r['z'],ah,nh,nl,al)
                    lineNotify('rj5NDKeoYlTpHVbYryI8cAGgIS7J2vvstmEcvEZE4Rj', notify)
                    df.to_csv('/home/pineapple/Documents/stock/CDP.csv',  encoding='utf_8_sig', index=False)
    except Exception as e:    
        print(e)
        print(r)                 
    time = datetime.now()  
    print("更新時間:" + str(time.hour)+":"+str(time.minute)+":"+str(time.second))

    start_time = datetime.strptime(str(time.date())+'8:50', '%Y-%m-%d%H:%M')
    end_time =  datetime.strptime(str(time.date())+'13:26', '%Y-%m-%d%H:%M')

    if time >= start_time and time <= end_time:
        s.enter(5, 0, stock_crawler, argument=(targets,))

stock_list = df['ID'].to_numpy()

s.enter(1, 0, stock_crawler, argument=(stock_list,))
s.run()
