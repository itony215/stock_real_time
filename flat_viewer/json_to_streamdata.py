import json
from tqdm import tqdm
import os

with os.scandir('/home/pineapple/Documents/stock/crawler/flat_viewer/json/') as it:
    for entry in tqdm(it):
        if entry.name.endswith(".json") and entry.is_file():
            with open(entry.path) as f:
                data = json.load(f)
                #print(data['stock_data'])
                with open('/home/pineapple/Documents/stock/crawler/flat_viewer/stream_data/'+entry.name, 'w') as json_file:
                    json_file.write(str(data['stock_data']))