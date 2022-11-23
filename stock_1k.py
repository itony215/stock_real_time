from datetime import datetime, timedelta, date
import requests as r
import time
import numpy as np
import json
import pandas as pd
import os.path


today = date.today()
datestr = today.strftime("%Y%m%d")
stock_list = pd.read_pickle("/home/pitaya/Documents/stock/stock_list.pkl")
for stock_no in stock_list.index:
    try:
        filepath = "/home/pitaya/Documents/stock/stock_1k/"+datestr+"_"+stock_no+".json"
        if(os.path.exists(filepath)):
            #print('pass', stock_no)
            continue
        url = "https://tw.stock.yahoo.com/_td-stock/api/resource/StockServices.stockList;fields=avgPrice%2Corderbook;symbols="+stock_no
        url2 = "https://tw.stock.yahoo.com/_td-stock/api/resource/FinanceChartService.ApacLibraCharts;symbols=%5B%22"+stock_no+".TW%22%5D;"
        res2 = r.get(url2)
        data2 = res2.json()
        res = r.get(url)
        data = res.json()
        timestamp = data2[0]['chart']['timestamp']
        openPrice = data2[0]['chart']['indicators']['quote'][0]['open']
        closePrice = data2[0]['chart']['indicators']['quote'][0]['close']
        highPrice = data2[0]['chart']['indicators']['quote'][0]['high']
        lowPrice = data2[0]['chart']['indicators']['quote'][0]['low']
        volumn = data2[0]['chart']['indicators']['quote'][0]['volume']
        res = r.get(url)
        data = res.json()
        inMarket = [data[0]['inMarket']]*7

        outMarket = [data[0]['outMarket']]*7
        avgPrice = []
        for i in range(0,len(openPrice)):
            #print(o[:i+1])
            avgPrice.append(round(np.average(openPrice[:i+1],weights = volumn[:i+1]),2))
        jsonObject = {"symbolName": data[0]['symbolName'],"sectorName": data[0]['sectorName'],
                              "stockId": stock_no, "date": datestr,
                              "timestamp": timestamp, "avgPrice": avgPrice,"inMarket": inMarket,
                              "outMarket": outMarket, "openPrice":openPrice,"closePrice":closePrice,
                              "highPrice":highPrice, "lowPrice":lowPrice, "volumn":volumn}
                #print(jsonObject)
        file = open(filepath, "w")
        json.dump(jsonObject, file)
        file.close()
        #print('done: ', stock_no)
    except:
        print('error ', stock_no)
    time.sleep(7)