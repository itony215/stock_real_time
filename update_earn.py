import pickle
import requests
import datetime
from io import StringIO
import pandas as pd
import json
from bs4 import BeautifulSoup
from tqdm import tqdm
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
stock_list = pd.read_pickle("/home/pineapple/Documents/stock/crawler/history/stock_list.pkl")
earn = pd.read_pickle("/home/pineapple/Documents/stock/crawler/history/營收.pkl")
today = datetime.date.today()
first = today.replace(day=1)
lastMonth = first - datetime.timedelta(days=1)
lastMonth.strftime("%Y/%m")
notice = '月年營收增:\n'
notice2 = '月年營收減:\n'
good_stock_list=[]
bad_stock_list=[]
for stock_id in tqdm(stock_list.index): #['1101','1102','1103','3661','6533'] earn.index.levels[0]
    try:
        print(stock_id)
        if(stock_id in earn.index.levels[0]):
            last_update = earn.loc[stock_id].iloc[-1].name
            if(earn.loc[stock_id].iloc[-1].name>=lastMonth.strftime("%Y/%m")):
                continue;
        else:
            last_update = ''
            print('new',stock_id)
        r = requests.get('https://concords.moneydj.com/z/zc/zch/zch.djhtm?a='+stock_id)
        soup = BeautifulSoup(r.text, 'html.parser')
        #data = soup.find_all("td", class_ = ["t3n0","t3n1"])
        table = soup.find_all('table')
        df = pd.read_html(str(table))[-1]
        new_df = df[5:]
        new_df.columns = new_df.iloc[0]
        new_df = new_df.drop(new_df.index[0])
#             #date = transform_ym(new_df.iloc[0]['年/月'])
#             #print(stock_id)
        new_df = new_df.fillna(0)

        if(last_update != '' and last_update<transform_ym(new_df.iloc[0]['年/月'])):
            month_g = earn.loc[stock_id].iloc[-1]['月增率%']
            year_g = earn.loc[stock_id].iloc[-1]['年增率%']
            year_t = earn.loc[stock_id].iloc[-1]['累計年增率%']
            if(any('' == c for c in [month_g,year_g,year_t])):
                print('資料不全 ',stock_id,today) 
            elif(float(month_g)<float(new_df.iloc[0,2].replace('%','').replace(',',''))\
                    and float(year_g)<float(new_df.iloc[0,4].replace('%','').replace(',',''))\
                    and float(year_t)<float(new_df.iloc[0,6].replace('%','').replace(',',''))):
                    notice += stock_id+', '
                    good_stock_list.append(stock_id)     
                    print('月年營收增 ',stock_id,today)    
            elif(float(month_g)>float(new_df.iloc[0,2].replace('%','').replace(',',''))\
                    and float(year_g)>float(new_df.iloc[0,4].replace('%','').replace(',',''))\
                    and float(year_t)>float(new_df.iloc[0,6].replace('%','').replace(',',''))):
                    notice2 += stock_id+', '
                    bad_stock_list.append(stock_id)     
                    print('月年營收減 ',stock_id,today) 
        for i in range(len(new_df)):
            date = transform_ym(new_df.iloc[i]['年/月'])
            if(last_update<=date):
                # print('ok')
                earn.loc[(stock_id,date),'營收(千)'] = new_df.iloc[i,1] if new_df.iloc[i,1] != 0 else 0
                earn.loc[(stock_id,date),'月增率%'] = new_df.iloc[i,2].replace('%','') if new_df.iloc[i,2] != 0 else 0
                earn.loc[(stock_id,date),'去年同期(千)'] = new_df.iloc[i,3] if new_df.iloc[i,3] != 0 else 0
                earn.loc[(stock_id,date),'年增率%'] = new_df.iloc[i,4].replace('%','') if new_df.iloc[i,4] != 0 else 0
                earn.loc[(stock_id,date),'累計營收(千)'] = new_df.iloc[i,5] if new_df.iloc[i,5] != 0 else 0
                earn.loc[(stock_id,date),'累計年增率%'] = new_df.iloc[i,6].replace('%','') if new_df.iloc[i,6] != 0 else 0
 
    except:
        print('error: ', stock_id)
        

earn = earn.sort_index()
earn.to_pickle("/home/pineapple/Documents/stock/crawler/history/營收.pkl")
good_stock_list_df = pd.DataFrame(good_stock_list)
good_stock_list_df.to_csv("/home/pineapple/Documents/stock/crawler/strategy/good_earn_list.csv",encoding='utf_8_sig', index = False)
bad_stock_list_df = pd.DataFrame(bad_stock_list)
bad_stock_list_df.to_csv("/home/pineapple/Documents/stock/crawler/strategy/bad_earn_list.csv",encoding='utf_8_sig', index = False)
lineNotify('X57Kb4EhV6073WKCE9UU2eT3IBvxmY44LPtmdUwwS8O', notice)
lineNotify('X57Kb4EhV6073WKCE9UU2eT3IBvxmY44LPtmdUwwS8O', notice2)