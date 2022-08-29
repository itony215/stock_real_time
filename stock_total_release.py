import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import time
from tqdm import tqdm


stock_list_df = pd.read_pickle("/home/pineapple/Documents/stock/crawler/stock_list.pkl")
stock_total_release = pd.read_pickle("/home/pineapple/Documents/stock/crawler/stock_total_release.pkl")
result = []
for s in tqdm(stock_list_df.index):
    r = requests.get('https://concords.moneydj.com/z/zc/zcm/zcm_'+str(s)+'.djhtm')
    soup = BeautifulSoup(r.text, 'html.parser')
    data = soup.find_all("td", class_ = ["t3n1"])
    #print(data[0].getText().replace(',','')) 
    # if '00' in s[:2]:
    #     ok = ''
    # else:
    #     ok = None
    # while ok is None:
    try:
        if('%' in data[2].getText().replace(',','')):
            ok = data[1].getText().replace(',','')
        else:
            ok = data[2].getText().replace(',','')
        if(s in stock_total_release.index):
            if(stock_total_release.loc[s,'total']!=ok):
                print('new value:',s,ok)
                stock_total_release.loc[s,'total']=ok
        else:
            name = stock_list_df[stock_list_df.index==s]['name'].values[0]
            total = data[2].getText().replace(',','')
            stock_total_release.loc[s]=[name, total]
            print('get new: ',s,name,total)
    except:
        print('Error ', s, stock_list_df[stock_list_df.index==s]['name'].values[0])
        time.sleep(1)
        pass
    time.sleep(1)
#new_df = pd.DataFrame(result)
#new_df.columns =['stock_id','name','total']
#new_df.set_index('stock_id', inplace=True)
#new_df.to_csv("/home/pineapple/Documents/stock/crawler/stock_total_release.csv",encoding='utf_8_sig', index = False)
#new_df.to_pickle("/home/pineapple/Documents/stock/crawler/stock_total_release.pkl")
stock_total_release.to_pickle("/home/pineapple/Documents/stock/crawler/stock_total_release.pkl")