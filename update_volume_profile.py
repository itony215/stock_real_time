import pandas as pd
import numpy as np
import requests
import datetime
from io import StringIO
from bs4 import BeautifulSoup
from IPython.display import display, clear_output
from urllib.request import urlopen
import sched
import time
import os.path as path
import json
from tqdm import tqdm

stock_list = pd.read_pickle("/home/pineapple/Documents/stock/crawler/stock_list.pkl")

for i in tqdm(stock_list.index):
    try:
        #print(i)
        r = requests.get("https://concords.moneydj.com/Z/ZC/ZCW/ZCWG/ZCWG_"+str(i)+"_30.djhtm")
        data = r.text.split("GetBcdData('", 1)[-1].split("')")[0]
        data = data.split(' ')
        lst = eval(data[0])
        lst2 = eval(data[1])
        df = pd.DataFrame(lst2,lst, columns = ['ma30'])
        df.to_csv("/home/pineapple/Documents/stock/crawler/price_volumn/"+str(i)+".csv")
    except:
        print("error", i)