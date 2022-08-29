import pandas as pd
all_stock = pd.read_csv("/home/pineapple/Documents/stock/crawler/strategy/所有股票資訊.csv")
result= all_stock[(all_stock['投信買賣超%']>=0.01) &(all_stock['投信10買N天']==1)]
result.to_csv("/home/pineapple/Documents/stock/crawler/strategy/投信10日以上無買入_今日買入.csv",encoding='utf_8_sig', index = False)