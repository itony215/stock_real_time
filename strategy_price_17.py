import pandas as pd
import os
import requests
from datetime import date
def lineNotify(token, msg):
    url = "https://notify-api.line.me/api/notify"
    headers = {
        "Authorization": "Bearer " + token
    }
   
    payload = {'message': msg}
    #files = {'imageFile': open(picURI, 'rb')}
    r = requests.post(url, headers = headers, params = payload)
    return r.status_code
notice = '頂背離:\n'

stock_list_df = pd.read_pickle("/home/pitaya/Documents/stock_hub/crawler/history/stock_list.pkl")
volumn = pd.read_pickle("/home/pitaya/Documents/stock_hub/crawler/history/成交股數.pkl")
high = pd.read_pickle("/home/pitaya/Documents/stock_hub/crawler/history/最高價.pkl")
low = pd.read_pickle("/home/pitaya/Documents/stock_hub/crawler/history/最低價.pkl")
start = pd.read_pickle("/home/pitaya/Documents/stock_hub/crawler/history/開盤價.pkl")
end = pd.read_pickle("/home/pitaya/Documents/stock_hub/crawler/history/收盤價.pkl")

delta = end.diff()

# 將價格變動分為上漲和下跌
gain = (delta.where(delta > 0, 0)).fillna(0)
loss = (-delta.where(delta < 0, 0)).fillna(0)

# 計算平均上漲和平均下跌
window_length = 6
avg_gain = gain.rolling(window=window_length, min_periods=1).mean()
avg_loss = loss.rolling(window=window_length, min_periods=1).mean()

# 計算相對強弱（RS）
rs = avg_gain / avg_loss

# 計算 RSI
rsi = 100 - (100 / (1 + rs))
# 取得最後一天的 RSI
last_day_rsi = rsi.iloc[-1]

# 過濾出最後一天 RSI 大於 80 的股票
rsi_above_80 = last_day_rsi[last_day_rsi > 80]

# 過濾出前 30 天最大的 RSI 不是出現在最後一天的股票
filtered_stocks = []
for stock in rsi_above_80.index:
    last_30_days_rsi = rsi[stock].iloc[-31:-1]  # 前 30 天的 RSI
    if last_30_days_rsi.max() != last_day_rsi[stock]:
        filtered_stocks.append(stock)

final_filtered_stocks = []
for stock in filtered_stocks:
    if end[stock].iloc[-1] > 20 and volumn[stock].iloc[-1] > 1000000:
        # 檢查最後一天收盤價是否大於開盤價
        if end[stock].iloc[-1] > start[stock].iloc[-1]:
            # 檢查過去 10 天內收盤價大於開盤價的天數是否小於 6 天
            last_10_days = end[stock].iloc[-10:] > start[stock].iloc[-10:]
            if last_10_days.sum() < 6:
                final_filtered_stocks.append(stock)

#print("最後一天 RSI 大於 80 且前 30 天最大的 RSI 不是出現在最後一天，股價大於 20 且成交量大於 1000000，最後一天收盤價大於開盤價，且過去 10 天內收盤價大於開盤價的天數小於 6 的股票：")
for stock in final_filtered_stocks:
    stock_name = stock_list_df[stock_list_df.index==stock]['name'].values[0]
    stock_price = end[stock].iloc[-1]
    notice += f"{stock}, {stock_name}, {stock_price}" + '\n'



lineNotify('X57Kb4EhV6073WKCE9UU2eT3IBvxmY44LPtmdUwwS8O', notice)