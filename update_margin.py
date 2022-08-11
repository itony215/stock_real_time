import pickle
import requests
from datetime import date
import pandas as pd
from bs4 import BeautifulSoup
import datetime

def transform_ym(date):   #民國轉西元
        y, m, d = date.split('/')
        return str(int(y)+1911) + '-' + m + '-' + d


margin = pd.read_pickle("./融資融券.pkl")

day = datetime.timedelta(days=1)
today = date.today()
#day = today.strftime("%m/%d")


#datestr = '2022-08-08'
for stock_id in margin.index.levels[0]:
    datestr = margin.loc[stock_id].iloc[-1].name.strftime("%Y-%m-%d")
    if(datestr<str(today)):
        #print(stock_id)
        try:
            r = requests.get('https://concords.moneydj.com/z/zc/zcn/zcn.djhtm?a='+stock_id+'&c='+datestr+'&d='+str(today))
            soup = BeautifulSoup(r.text, 'html.parser')
            data = soup.find_all("td", class_ = ["t3n0","t3n1"])
            for i in range(1,int(len(data)-4),15):
                if(transform_ym(data[i].getText())!= datestr):
                    print('update: ', data[i].getText(), stock_id)
                    date=transform_ym(data[i].getText())
                    margin.loc[(stock_id,date),'融資(張)'] = float(data[i+4].getText().replace(',',''))
                    margin.loc[(stock_id,date),'融資差額(張)'] = float(data[i+5].getText().replace(',',''))
                    margin.loc[(stock_id,date),'融資使用率'] = float(data[i+7].getText().replace('%',''))

                    margin.loc[(stock_id,date),'融券(張)'] = float(data[i+11].getText().replace(',',''))
                    margin.loc[(stock_id,date),'融券差額(張)'] = float(data[i+12].getText().replace(',',''))
                    margin.loc[(stock_id,date),'券資比'] = float(data[i+13].getText().replace('%',''))
        except:
            print('error: ', stock_id)
            continue
#     else:
#         print('no update')
margin = margin.sort_index()
margin.to_pickle("./融資融券_0810.pkl")