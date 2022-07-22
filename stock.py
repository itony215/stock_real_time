from datetime import datetime, timedelta, date
import requests as r
import sched
import time
st = sched.scheduler(time.time, time.sleep)
import json
today = date.today()
datestr = today.strftime("%Y%m%d")

def each_stock(stock_no, datestr, timestamp, openPrice, volumn, inMarket, outMarket, avgPrice,filepath):
    url = f"https://tw.stock.yahoo.com/_td-stock/api/resource/StockServices.stockList;fields=avgPrice%2Corderbook;symbols={stock_no}"
    url2 = f"https://tw.stock.yahoo.com/_td-stock/api/resource/FinanceChartService.ApacLibraCharts;symbols=%5B%22{stock_no}.TW%22%5D;"

    res2 = r.get(url2)
    data2 = res2.json()

    tmp = data2[0]['chart']['timestamp']
    o = data2[0]['chart']['indicators']['quote'][0]['open']
    v = data2[0]['chart']['indicators']['quote'][0]['volume']
    #print(len(tmp))

    if(len(timestamp)<len(tmp)):
        s = set(timestamp)
        new_data_t = [x for x in tmp if x not in s]
        num = len(new_data_t)

        res = r.get(url)
        data = res.json()
        openPrice_new = o[-num:]
        volumn_new = v[-num:]
        if len(timestamp) > 0:
            avgPrice_new = avgPrice[-1] if float(data[0]['avgPrice'])==0 else float(data[0]['avgPrice'])
            inMarket_new = inMarket[-1] if data[0]['inMarket']==0 else data[0]['inMarket']
            outMarket_new = outMarket[-1] if data[0]['outMarket']==0 else data[0]['outMarket']
        else:
            avgPrice_new = float(data[0]['avgPrice'])
            inMarket_new = data[0]['inMarket']
            outMarket_new = data[0]['outMarket']

        avgPrice_new = [avgPrice_new] * len(new_data_t)
        inMarket_new = [inMarket_new] * len(new_data_t)
        outMarket_new = [outMarket_new] * len(new_data_t)
#         print(avgPrice_new)
#         print(inMarket_new)
#         print(outMarket_new)
#         avgPrice_new[-1] = float(data[0]['avgPrice'])
#         inMarket_new[-1] = data[0]['inMarket']
#         outMarket_new[-1] = data[0]['outMarket']

        timestamp = tmp
        avgPrice = avgPrice + avgPrice_new
        inMarket = inMarket + inMarket_new
        outMarket = outMarket + outMarket_new
        openPrice = openPrice + openPrice_new
        volumn = volumn + volumn_new
        #print(data[0])
        jsonObject = {"symbolName": data[0]['symbolName'],"sectorName": data[0]['sectorName'],
                      "stockId": stock_no, "date": datestr,
                      "timestamp": timestamp, "avgPrice": avgPrice,"inMarket": inMarket,
                      "outMarket": outMarket, "openPrice":openPrice, "volumn":volumn}
        #print(jsonObject)
        file = open(filepath, "w")
        json.dump(jsonObject, file)
        file.close()

    else:
        print('no update: ', stock_no)


def stock_crawler(): 
    stock_list = ['1605','1795','2002','2303','2313','2317','2327','2330','2340','2344',
                '2368','2379','2409','2453','2481','2497','2498','2603','2606','2618',
                '3006','3008','3034','3035','3037','3141','3169','3189','3228','3406',
                '3443','3532','3558','3675','3680','4162','4755','4768','4919','5269',
                '5425','5483','6104','6138','6182','6187','6217','6231','6469','6488',
                '6515','6531','6719','8028','8046','8069','8299','8478','9945']


    for stock_no in stock_list:
        filepath = "/home/pineapple/Documents/stock/day/"+datestr+"_"+stock_no+".json"
        try:
            with open(filepath,'r+') as json_file:
                old_data = json.load(json_file)
                #print(old_data)
                timestamp = old_data['timestamp']
                openPrice = old_data['openPrice']
                volumn = old_data['volumn']
                inMarket = old_data['inMarket']
                outMarket = old_data['outMarket']
                avgPrice = old_data['avgPrice']

        except:
            print('new one')
            timestamp= []
            openPrice=[]
            volumn = []
            inMarket = []
            outMarket = []
            avgPrice = [] 

        try:
            each_stock(stock_no, datestr, timestamp, openPrice, volumn, inMarket, outMarket, avgPrice,filepath)
        except:   
            print('error: ', stock_no) 
            continue

    time = datetime.now()  
    print("更新時間:" + str(time.hour)+":"+str(time.minute)+":"+str(time.second))
    
    #display(df)
    
    start_time = datetime.strptime(str(time.date())+'08:55', '%Y-%m-%d%H:%M')
    end_time =  datetime.strptime(str(time.date())+'13:35', '%Y-%m-%d%H:%M')
    
    if time >= start_time and time <= end_time:
        st.enter(69, 0, stock_crawler)

    
st.enter(1, 0, stock_crawler)
st.run()