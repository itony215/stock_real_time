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
    stock_list = "|".join("{}.tw".format(target) for target in targets) 
    query_url = "http://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch="+ stock_list

    data = json.loads(urlopen(query_url).read())    
    for r in data['msgArray']:
        notice=""
        ah = df.loc[df['股票代號'] == int(r['c'])].AH.item()
        nh = df.loc[df['股票代號'] == int(r['c'])].NH.item()
        nl = df.loc[df['股票代號'] == int(r['c'])].NL.item()
        al = df.loc[df['股票代號'] == int(r['c'])].AL.item()

        if (r['z'] == '-'):
            r['z'] = r['a'].split('_')[0]
        if(float(r['z'])>=ah):
            notice = 'AH'
        elif(float(r['z'])>=nh):
            notice = 'NH'
        elif(float(r['z'])<=nl):
            notice = 'NL'
        elif(float(r['z'])<=al):
            notice = 'AL'
        else:
            print('沒波動: ', r['z'])
            
        if(len(notice)>1):
            string = df.loc[df['股票代號'] == int(r['c'])].Notice.item()
            stock_no = int(r['c'])
            if(string == notice):
                pass
            else:
                df.loc[df.股票代號==stock_no,'Notice'] = notice
                notify = "{} {} {} {} (AH:{:.2f}, NH:{:.2f}, NL:{:.2f}, AL:{:.2f})".format(r['c'],r['n'],notice,r['z'],ah,nh,nl,al)
                lineNotify('rj5NDKeoYlTpHVbYryI8cAGgIS7J2vvstmEcvEZE4Rj', notify)
                df.to_csv('/home/pineapple/Documents/stock/CDP.csv',  encoding='utf_8_sig', index=False)
                
    time = datetime.now()  
    print("更新時間:" + str(time.hour)+":"+str(time.minute)+":"+str(time.second))

    start_time = datetime.strptime(str(time.date())+'8:50', '%Y-%m-%d%H:%M')
    end_time =  datetime.strptime(str(time.date())+'13:33', '%Y-%m-%d%H:%M')

    if time >= start_time and time <= end_time:
        s.enter(5, 0, stock_crawler, argument=(targets,))

stock_list = ['tse_2330','otc_8299','tse_1101','otc_3169','otc_3217','otc_6187','otc_8924','tse_3515','tse_8016','otc_3707','tse_2481','tse_3532', 'otc_3675','otc_3680','otc_3141','tse_6531','tse_6706','tse_6196','tse_4961','otc_6138','otc_3587','tse_3583','otc_3624','otc_3491','otc_8155','tse_8150','tse_3035','tse_3653','otc_6667','otc_6457','tse_3189','tse_6477','otc_6223','otc_3455','tse_2233','tse_3059']

s.enter(1, 0, stock_crawler, argument=(stock_list,))
s.run()