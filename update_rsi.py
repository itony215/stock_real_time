import pandas as pd

# 讀取數據
rsi_new = pd.read_pickle("./history/最低價.pkl")
end = pd.read_pickle("./history/收盤價.pkl")
rsi = pd.read_pickle("./history/RSI.pkl")

def wilder_sma(data, window):
    """計算 Wilder 的移動平均"""
    wma = pd.Series(index=data.index)
    wma.iloc[window - 1] = data.iloc[:window].mean()  # 第一個平均值
    for i in range(window, len(data)):
        wma.iloc[i] = (wma.iloc[i - 1] * (window - 1) + data.iloc[i]) / window
    return wma

def calculate_rsi_wilder(data, window=5):
    delta = data.diff()
    
    gain = wilder_sma(delta.where(delta > 0, 0), window)
    loss = wilder_sma(-delta.where(delta < 0, 0), window)
    
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    
    return rsi
if(rsi_new.index[-1] > rsi.index[-1]):
    for stock_id in end.columns:
        rsi_new[stock_id] = calculate_rsi_wilder(end[stock_id][-200:])
    
    last_rsi_date = rsi.index[-1]    
    new_data = rsi_new.loc[last_rsi_date:][1:]
    
    rsi = pd.concat([rsi, new_data])
    rsi.to_pickle("./history/RSI.pkl")
    print('更新完畢')
else:
    print('已經是最新資料')