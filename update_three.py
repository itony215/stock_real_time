import pickle
import requests
from datetime import date
from io import StringIO
import pandas as pd
import json
from bs4 import BeautifulSoup
from tqdm import tqdm
from datetime import datetime
import os
def transform_ym(date):   #民國轉西元
        y, m, d = date.split('/')
        return str(int(y)+1911) + '-' + m + '-' + d
stock_list = pd.read_pickle("/home/pineapple/Documents/stock/crawler/history/stock_list.pkl")
three = pd.read_pickle("/home/pineapple/Documents/stock/crawler/three/三大法人買賣超.pkl")
stock_total_release = pd.read_pickle("/home/pineapple/Documents/stock/crawler/stock_total_release.pkl")
today = date.today()
#day = today.strftime("%m/%d")
#datestr = today.strftime("%Y-%m-%d")
#datestr = '2022-08-11'
for stock_id in tqdm(['1101','6830']):#stock_list.index
    if(stock_id in three.index.levels[0]):
        old_date = three.loc[stock_id].iloc[-1].name.strftime("%Y-%m-%d")
    else:
        old_date = str(today)
    if(old_date<=str(today) or three.loc[(stock_id,old_date)].isna().any()):
        #print(stock_id)
        #print(stock_id in three.index.levels[0])
        try:
            r = requests.get('https://concords.moneydj.com/z/zc/zcl/zcl.djhtm?a='+stock_id+'&c='+old_date+'&d='+str(today))#
            #https://concords.moneydj.com/z/zc/zcl/zcl_1101.djhtm
            soup = BeautifulSoup(r.text, 'html.parser')
            data = soup.find_all("td", class_ = ["t3n0","t3r1","t3n1"])
            date = transform_ym(data[1].getText())
            total_release = float(stock_total_release.loc[stock_id]['total'])
            for i in range(1,int(len(data)-7),11):
                date = transform_ym(data[i].getText()) 
                try:
                    if(old_date<date):
                        three.loc[(stock_id,date),'投信買賣超(張)'] = float(data[i+2].getText().replace(',',''))
                        three.loc[(stock_id,date),'投信買賣超%'] = round(float(data[i+2].getText().replace(',',''))/total_release*100,2)
                        three.loc[(stock_id,date),'投信持股比例'] = round(float(data[i+6].getText().replace(',',''))/total_release*100,2)
                        print('投信 update: ',stock_id,data[i].getText(),data[i+2].getText(),data[i+6].getText())
                except:
                    print('no new data 投信',stock_id,i)
                    pass
                try:
                    # print('old_date',old_date)
                    # print('date', date)
                    #print(three.loc[(stock_id,date)].isna().any())
                    if(old_date<=date):
                        if(stock_id not in three.index.levels[0] or three.loc[(stock_id,date)].isna().any()):
                            three.loc[(stock_id,date),'投信買賣超(張)'] = float(data[i+2].getText().replace(',',''))
                            three.loc[(stock_id,date),'投信買賣超%'] = round(float(data[i+2].getText().replace(',',''))/total_release*100,2)
                            three.loc[(stock_id,date),'投信持股比例'] = round(float(data[i+6].getText().replace(',',''))/total_release*100,2)

                            three.loc[(stock_id,date),'外資買賣超(張)'] = float(data[i+1].getText().replace(',',''))
                            three.loc[(stock_id,date),'外資買賣超%'] = round(float(data[i+1].getText().replace(',',''))/total_release*100,2)
                            three.loc[(stock_id,date),'外資持股比例'] = round(float(data[i+5].getText().replace(',',''))/total_release*100,2)

                            three.loc[(stock_id,date),'自營商買賣超(張)'] = float(data[i+3].getText().replace(',',''))
                            three.loc[(stock_id,date),'自營商買賣超%'] = round(float(data[i+3].getText().replace(',',''))/total_release*100,2)
                            three.loc[(stock_id,date),'自營商持股比例'] = round(float(data[i+7].getText().replace(',',''))/total_release*100,2)
                            print('三大 update: ',stock_id,data[i].getText(),data[i+1].getText(),data[i+2].getText(),data[i+3].getText(),data[i+5].getText(),data[i+6].getText(),data[i+7].getText())
                except:
                    print('no new data 三大2',stock_id,i)
                    pass
        except:
            print('error: ', stock_id)
            continue
#     else:
#         print('no update')
three = three.sort_index()
three.to_pickle("/home/pineapple/Documents/stock/crawler/three/三大法人買賣超.pkl")