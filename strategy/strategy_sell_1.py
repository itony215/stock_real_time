import pandas as pd
from datetime import date
today = date.today()
all_stock = pd.read_csv("/home/pineapple/Documents/stock/crawler/strategy/stock_data/data/所有股票資訊_sell.csv")
result= all_stock[all_stock['A轉跌幅']<=-2]
result= result[result['昨日漲跌幅']>=2]
result= result[result['三大買賣超']<0]
result= result[result['成交量']>1000]
result.insert(0, "date", today)
result.to_csv("/home/pineapple/Documents/stock/crawler/strategy/stock_data/data/空方標的.csv",encoding='utf_8_sig', index = False)