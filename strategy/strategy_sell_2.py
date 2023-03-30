import pandas as pd
from datetime import date
today = date.today()
#today = '2023-02-20'
all_stock = pd.read_csv("/home/pineapple/Documents/stock/crawler/strategy/stock_data/data/所有股票資訊_sell.csv")
result= all_stock[all_stock['融券差額(張)']>0]
result= result[(result['融券差額(張)']-result['昨日融券'])>100]
#result= result[result['昨日融券']>0]
result= result[result['漲跌幅']>=2]
result= result[result['融券5N']>=2]
result= result[result['收盤價']>=15]
#result= result[result['三大買賣超']<0]
result= result[result['成交量']>500]
result.insert(0, "date", today)
result = result.sort_values(by=['融券差額(張)'], ascending=False)
result.to_csv("/home/pineapple/Documents/stock/crawler/strategy/stock_data/data/空方標的2.csv",encoding='utf_8_sig', index = False)