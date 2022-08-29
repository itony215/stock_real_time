import pandas as pd
import os
import requests

def lineNotify(token, msg):
    url = "https://notify-api.line.me/api/notify"
    headers = {
        "Authorization": "Bearer " + token
    }
   
    payload = {'message': msg}
    #files = {'imageFile': open(picURI, 'rb')}
    r = requests.post(url, headers = headers, params = payload)
    return r.status_code
notice = '過熱第四天找空點:\n'
stock_list = pd.read_pickle("/home/pineapple/Documents/stock/crawler/stock_list.pkl")
with os.scandir('/home/pineapple/Documents/stock/crawler/stock_over_bband/') as it:
    for entry in it:
        if entry.name.endswith(".csv") and entry.is_file():
            #print(entry.name, entry.path)
            df = pd.read_csv(entry.path, index_col="date")
            if(df.iloc[-1]['count']>2 and df.iloc[-1]['漲跌幅']>1 and df.iloc[-1]['收盤價']>20 and df.iloc[-1]['量']>1000):
                stock_id = entry.name.split('.')[0]
                notice += stock_id+stock_list[stock_list.index==stock_id]['name'].values[0]+': '+str(df.iloc[-1]['收盤價'])+'\n'
                print(stock_id,stock_list[stock_list.index==stock_id]['name'].values[0],df.iloc[-1]['收盤價'])
lineNotify('X57Kb4EhV6073WKCE9UU2eT3IBvxmY44LPtmdUwwS8O', notice)