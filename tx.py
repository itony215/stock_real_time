from datetime import datetime, timedelta, date
import requests as r
import sched
import time
st = sched.scheduler(time.time, time.sleep)
import json
today = date.today()
datestr = today.strftime("%Y%m%d")

def tx_crawler(): 
    filepath = "./day/"+datestr+"_tx.json"
    try:
        with open(filepath,'r+') as json_file:
            old_data = json.load(json_file)
            #print(old_data)
            timestamp = old_data['timestamp']
            price = old_data['price']
            volumn = old_data['volumn']
    except:
        print('new one')
        timestamp= []
        price=[]
        volumn = []

    res = r.get("https://tw.quote.finance.yahoo.net/quote/q?type=tick&perd=1m&mkt=10&sym=%23001")
    #print(res.text[5:-2])
    tick_index = res.text.rfind('tick')
    #print(res.text[index-1:-3])
    data_string = '{'+res.text[tick_index-1:-2]
    data = json.loads(data_string)
    
    #script_text = soup.find('tick').get_text()
    #print(soup.tick)
    if(len(timestamp)<len(data)):
        timestamp = [x['t'] for x in data]
        price = [x['p'] for x in data]
        volumn = [x['v'] for x in data]
        jsonObject = {"timestamp": timestamp, "price": price, "volumn":volumn}
        file = open(filepath, "w")
        json.dump(jsonObject, file)
        file.close()
    else:
        print('no update')
        

    time = datetime.now()  
    print("更新時間:" + str(time.hour)+":"+str(time.minute)+":"+str(time.second))
    
    #display(df)
    
    start_time = datetime.strptime(str(time.date())+'08:30', '%Y-%m-%d%H:%M')
    end_time =  datetime.strptime(str(time.date())+'13:35', '%Y-%m-%d%H:%M')
    
    if time >= start_time and time <= end_time:
        st.enter(60, 0, tx_crawler)

    
st.enter(1, 0, tx_crawler)
st.run()