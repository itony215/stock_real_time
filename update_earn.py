import pickle
import requests
import datetime
from io import StringIO
import pandas as pd
import json
from bs4 import BeautifulSoup
def lineNotify(token, msg):
    url = "https://notify-api.line.me/api/notify"
    headers = {
        "Authorization": "Bearer " + token
    }
   
    payload = {'message': msg}
    #files = {'imageFile': open(picURI, 'rb')}
    r = requests.post(url, headers = headers, params = payload)
    return r.status_code
def transform_ym(date): 
        y, m = date.split('/')
        return str(int(y)+1911) + '/' + m

today = datetime.date.today()
first = today.replace(day=1)
lastMonth = first - datetime.timedelta(days=1)
lastMonth.strftime("%Y/%m")

earn = pd.read_pickle("/home/pineapple/Documents/stock/crawler/history/營收.pkl")
today = datetime.date.today()
first = today.replace(day=1)
lastMonth = first - datetime.timedelta(days=1)
lastMonth.strftime("%Y/%m")
notice = '月年營收增:\n'
good_stock_list=[]
for stock_id in earn.index.levels[0]:
    try:
        if(earn.loc[stock_id].iloc[-1].name<lastMonth.strftime("%Y/%m")):
            r = requests.get('https://concords.moneydj.com/z/zc/zch/zch.djhtm?a='+stock_id)
            soup = BeautifulSoup(r.text, 'html.parser')
            data = soup.find_all("td", class_ = ["t3n0","t3n1"])
            table = soup.find_all('table')
            df = pd.read_html(str(table))[-1]
            new_df = df[5:]
            new_df.columns = new_df.iloc[0]
            new_df = new_df.drop(new_df.index[0])
            date = transform_ym(new_df.iloc[0]['年/月'])
            #print(stock_id)
            if(earn.loc[stock_id].iloc[-1].name<date):
                #print('ok')
                if(float(earn.loc[stock_id].iloc[-1]['月增率%'])<float(new_df.iloc[0,2].replace('%',''))\
                    and float(earn.loc[stock_id].iloc[-1]['年增率%'])<float(new_df.iloc[0,4].replace('%',''))\
                    and float(earn.loc[stock_id].iloc[-1]['累計年增率%'])<float(new_df.iloc[0,6].replace('%',''))):
                    notice += stock_id+', '
                    good_stock_list.append(stock_id)     
                    print('月年營收增 ',stock_id,today)
                earn.loc[(stock_id,date),'營收(千)'] = new_df.iloc[0,1]
                earn.loc[(stock_id,date),'月增率%'] = new_df.iloc[0,2].replace('%','')
                earn.loc[(stock_id,date),'去年同期(千)'] = new_df.iloc[0,3]
                earn.loc[(stock_id,date),'年增率%'] = new_df.iloc[0,4].replace('%','')
                earn.loc[(stock_id,date),'累計營收(千)'] = new_df.iloc[0,5]
                earn.loc[(stock_id,date),'累計年增率%'] = new_df.iloc[0,6].replace('%','')
                
    except:
        #print('error: ', stock_id)
        continue
earn.to_pickle("/home/pineapple/Documents/stock/crawler/history/營收.pkl")
good_stock_list_df = pd.DataFrame(good_stock_list)
good_stock_list_df.to_csv("/home/pineapple/Documents/stock/crawler/strategy/good_earn_list.csv",encoding='utf_8_sig', index = False)
lineNotify('X57Kb4EhV6073WKCE9UU2eT3IBvxmY44LPtmdUwwS8O', notice)