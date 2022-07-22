import os
import json
import requests

def lineNotify(token, msg):
    url = "https://notify-api.line.me/api/notify"
    headers = {
        "Authorization": "Bearer " + token
    }
   
    payload = {'message': msg}
    r = requests.post(url, headers = headers, params = payload)
    return r.status_code
notice = '弱勢股:\n'
with os.scandir('/home/pineapple/Documents/stock/day/') as it:
    for entry in it:
        #print(entry)
        if entry.name.endswith(".json") and entry.is_file():
            #print('2222',entry.name, entry.path)
            with open(entry.path,'r+') as json_file:
                old_data = json.load(json_file)
                #print(old_data)
                openPrice = old_data['openPrice'][-1]
                #print('error', openPrice,entry.name)
                inMarket = old_data['inMarket'][-1]
                outMarket = old_data['outMarket'][-1]
                avgPrice = old_data['avgPrice'][-1]
    
                if(avgPrice>openPrice and inMarket>outMarket):
                    print(old_data["symbolName"],old_data["stockId"])
                    notice += old_data["symbolName"]+old_data["stockId"] + '\n'

lineNotify('X57Kb4EhV6073WKCE9UU2eT3IBvxmY44LPtmdUwwS8O', notice)