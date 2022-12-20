import json
import os

with os.scandir('/home/pineapple/Documents/stock/crawler/flat_viewer/json/') as it:
    for entry in it:
        if entry.name.endswith(".json") and entry.is_file():
            with open(entry.path) as f:
                data = json.load(f)
                if(data['stock_data'][-1][2]==0):
                    #print(data['stock_data'][-1])
                    f.close()
                    os.remove(entry.path)