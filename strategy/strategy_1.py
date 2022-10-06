import pandas as pd
from datetime import date
today = date.today()
all_stock = pd.read_csv("/home/pineapple/Documents/stock/crawler/strategy/stock_data/data/所有股票資訊.csv")
result= all_stock[(all_stock['投信買賣超(張)']>=1) &(all_stock['投信10買N天']==1)]
result.insert(0, "date", today)
result.to_csv("/home/pineapple/Documents/stock/crawler/strategy/stock_data/data/投信10日以上無買入_今日買入.csv",encoding='utf_8_sig', index = False)