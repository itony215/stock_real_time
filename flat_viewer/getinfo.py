import requests
import pandas as pd
import time

start = pd.read_pickle("/home/pineapple/Documents/stock/crawler/history/開盤價.pkl")

for stock_id in start.columns:
    try:
        r = requests.get('https://tw.stock.yahoo.com/_td-stock/api/resource/StockServices.stockList;fields=avgPrice%2Corderbook;symbols='+stock_id)
        if(len(r.text)<30):
            print('no data: ', stock_id,r.text)
            time.sleep(5)
            continue
        #data = json.loads(r.text)
        with open('/home/pineapple/Documents/stock/crawler/flat_viewer/stream_data/flat_viewer_data/info/info_'+str(stock_id)+'.json', 'w',encoding='utf8') as json_file:
            json_file.write(r.text)
    except:
        print('error: ', stock_id)
    time.sleep(3)