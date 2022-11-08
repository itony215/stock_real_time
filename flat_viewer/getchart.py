import requests
import pandas as pd
from datetime import datetime
import json
import time as t2

start = pd.read_pickle("/home/pineapple/Documents/stock/crawler/history/開盤價.pkl")

for stock_id in start.columns:
    try:
        #print(stock_id)    
        r = requests.get('https://tw.stock.yahoo.com/_td-stock/api/resource/FinanceChartService.ApacLibraCharts;symbols=%5B%22'+stock_id+'.TW%22%5D;')
        
        if(len(r.text)<30):
            print('no data: ', stock_id,r.text)
            t2.sleep(5)
            continue
        data = json.loads(r.text)
        
        previousClose = data[0]['chart']['meta']['previousClose']
        #print(previousClose)
        limitUpPrice = data[0]['chart']['meta']['limitUpPrice']
        #print(limitUpPrice)
        limitDownPrice = data[0]['chart']['meta']['limitDownPrice']
        #print(limitDownPrice)
        timestamp = data[0]['chart']['timestamp']
        time_str = timestamp[0]
        date_time = datetime.fromtimestamp(time_str)
        Y = date_time.strftime("%Y")
        m = date_time.strftime("%m")
        d = date_time.strftime("%d")
        #print("Output 2:", Y,m,d)
        open_price=	data[0]['chart']['indicators']['quote'][0]['open']
        volume=	data[0]['chart']['indicators']['quote'][0]['volume']

        # print(timestamp)
        # print(open_price)
        # print(volume)
        result =[]
        for idx, time  in enumerate(timestamp):
            result.append([float(time)*1000,float(open_price[idx]),float(volume[idx])])
        # open_price = data[0]['chart']['timestamp']
        result.append([previousClose,limitUpPrice,limitDownPrice,Y,m,d])
        #json_data = json.dumps(result)
        #print(type(result))
        with open('/home/pineapple/Documents/stock/crawler/flat_viewer/stream_data/flat_viewer_data/chart1k/chart_'+str(stock_id)+'.json', 'w') as json_file:
            json_file.write(json.dumps(result))
    except:
        print('error: ',stock_id)
    t2.sleep(3)