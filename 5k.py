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
def ceil_dt(dt, delta):
    return datetime.min + math.ceil((dt - datetime.min) / delta) * delta
def stock_crawler(targets):
    
    clear_output(wait=True)
    
    stock_list = "|".join("{}.tw".format(target) for target in targets) 
    
    query_url = "http://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch="+ stock_list

    try:
        data = json.loads(urlopen(query_url).read())
        for r in data['msgArray']:
            #print(r)
            path_file = './5K/'+str(r['c'])+'_'+str(r['n'])+'.csv'
            #print(path_file)
            columns = ['z','tv','v','o','h','l','y','t']
            each_five = ceil_dt(datetime.strptime(r['d']+' '+r['t'], '%Y%m%d %H:%M:%S'), timedelta(minutes=5))

            if (r['z'] == '-'):
                r['z'] = r['a'].split('_')[0]
            if (r['tv'] == '-'):
                r['tv'] = 0
            if path.exists(path_file):
                #print(r['a'].split('_'))
                df = pd.read_csv(path_file, header=0)

                if(each_five>datetime.strptime(df.iloc[-1]['五分K'],'%Y-%m-%d %H:%M:%S')):
                    print('new')
                    if (r['z'] != '-'):
                        new_data = [each_five]
                        for i in columns:
                            new_data.append(r[i])
                        new_data.append((float(r['z'])-float(r['y']))/float(r['y']) * 100)
                        df.loc[-1] =  new_data
                        print(new_data)
                elif(each_five==datetime.strptime(df.iloc[-1]['五分K'],'%Y-%m-%d %H:%M:%S')):
                    print('same')
                    if(df.iloc[-1]['累積成交量']<float(r['v'])):
                        print('same', datetime.strptime(df.iloc[-1]['五分K'],'%Y-%m-%d %H:%M:%S'))
                        new_data = [each_five]
                        for i in columns:
                            new_data.append(r[i])
                        new_data.append((float(r['z'])-float(r['y']))/float(r['y']) * 100)
                        df.iloc[-1] = new_data
                else:
                    print('error')
                #display(df)
                #print(df['累積成交量'].shift(-1))
                #print(df['累積成交量'])
                df['當盤成交量'] = df['累積成交量'].astype(int) - df['累積成交量'].shift(1,fill_value=df['累積成交量'][0]).astype(int) 
                #df['當盤成交量'] = df['當盤成交量'].apply(lambda x : x if (x > 0) else 0) 
                df.to_csv('./5K/'+str(r['c'])+'_'+str(r['n'])+'.csv',  encoding='utf_8_sig', index=False)

            else:
                #print([r])
                #print(data['msgArray'])
                df = pd.DataFrame([r], columns=columns)
                columns = ['z','tv','v','o','h','l','y','t']
                df.columns = ['當盤成交價','當盤成交量','累積成交量','開盤價','最高價','最低價','昨收價','成交時間']
                #print('r[z]', r['z'])
                df['當盤成交價'] = r['z']
                df['當盤成交量'] = 0
                df.iloc[0,:7] = df.iloc[0,:7].astype(float)

                df['漲幅'] = (df['當盤成交價'] - df['昨收價'])/df['昨收價'] * 100
                #each_five = ceil_dt(datetime.strptime(data['msgArray'][0]['d']+' '+data['msgArray'][0]['t'], '%Y%m%d %H:%M:%S'), timedelta(minutes=5))
                df.insert(0, "五分K", each_five)   
                df.to_csv('./5K/'+str(r['c'])+'_'+str(r['n'])+'.csv',  encoding='utf_8_sig', index=False)
    except Exception as e:
        print(e)
        # show table
        #df = df.style.applymap(tableColor, subset=['漲幅'])
    # 紀錄更新時間
    time = datetime.now()  
    print("更新時間:" + str(time.hour)+":"+str(time.minute)+":"+str(time.second))
    
    #display(df)
    
    start_time = datetime.strptime(str(time.date())+'9:00', '%Y-%m-%d%H:%M')
    end_time =  datetime.strptime(str(time.date())+'13:33', '%Y-%m-%d%H:%M')
    
    # 判斷爬蟲終止條件
    if time >= start_time and time <= end_time:
        s.enter(5, 0, stock_crawler, argument=(targets,))

stock_list = ['tse_2330','otc_8299','tse_1101','otc_3169']

# 每秒定時器
s.enter(1, 0, stock_crawler, argument=(stock_list,))
s.run()