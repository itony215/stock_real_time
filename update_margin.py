import pickle
import requests
from datetime import date
import pandas as pd
from bs4 import BeautifulSoup
from tqdm import tqdm
import os
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}
def transform_ym(date_str):   # 民國轉西元
    y, m, d = date_str.split('/')
    return str(int(y) + 1911) + '-' + m + '-' + d

def safe_float(s, default=None, log_info=None):
    """安全轉 float，若為空字串則回傳 default，並可記錄缺值資訊"""
    if s is None:
        if log_info:
            print(f"[缺值] {log_info} => None")
        return default
    s = s.strip().replace(',', '').replace('%', '')
    if s == '' or s == '-':
        if log_info:
            print(f"[缺值] {log_info} => '{s}'")
        return default
    try:
        return float(s)
    except ValueError:
        if log_info:
            print(f"[轉換錯誤] {log_info} => '{s}'")
        return default

# 檔案路徑
stock_list_path = "/home/keywin/workspace/crawler/history/stock_list.pkl"
margin_path = "/home/keywin/workspace/crawler/margin/融資融券.pkl"

# 讀取資料
stock_list = pd.read_pickle(stock_list_path)
margin = pd.read_pickle(margin_path)

today = date.today()

save_counter = 0  # 計數器

for idx, stock_id in enumerate(tqdm(stock_list.index), 1):
    if stock_id in margin.index.levels[0]:
        datestr = margin.loc[stock_id].iloc[-1].name.strftime("%Y-%m-%d")
    else:
        datestr = '2023-03-28'

    if datestr < str(today):
        try:       #https://jdata.yuanta.com.tw/z/zc/zcn/zcn_1101.djhtm,  jdata.yuanta.com.tw
            url = f'https://concords.moneydj.com/z/zc/zcn/zcn.djhtm?a={stock_id}&c={datestr}&d={str(today)}'
            r = requests.get(url, headers=headers)
            soup = BeautifulSoup(r.text, 'html.parser')
            data = soup.find_all("td", class_=["t3n0", "t3n1"])

            for i in range(1, int(len(data) - 4), 15):
                if transform_ym(data[i].getText()) != datestr:
                    print('update:', data[i].getText(), stock_id, data[i+4].getText(), data[i+11].getText())
                    date_key = transform_ym(data[i].getText())

                    margin.loc[(stock_id, date_key), '融資(張)'] = safe_float(data[i+4].getText(), 0, f"{stock_id}-{date_key}-融資(張)")
                    margin.loc[(stock_id, date_key), '融資差額(張)'] = safe_float(data[i+5].getText(), 0, f"{stock_id}-{date_key}-融資差額(張)")
                    margin.loc[(stock_id, date_key), '融資使用率'] = safe_float(data[i+7].getText(), 0, f"{stock_id}-{date_key}-融資使用率")

                    margin.loc[(stock_id, date_key), '融券(張)'] = safe_float(data[i+11].getText(), 0, f"{stock_id}-{date_key}-融券(張)")
                    margin.loc[(stock_id, date_key), '融券差額(張)'] = safe_float(data[i+12].getText(), 0, f"{stock_id}-{date_key}-融券差額(張)")
                    margin.loc[(stock_id, date_key), '券資比'] = safe_float(data[i+13].getText(), 0, f"{stock_id}-{date_key}-券資比")

                    save_counter += 1

                    # 每累積 100 筆儲存一次
                    if save_counter >= 100:
                        margin = margin.sort_index()
                        margin.to_pickle(margin_path)
                        print(f"已儲存 {save_counter} 筆更新")
                        save_counter = 0

        except Exception as e:
            print('error:', stock_id, e)
            continue

# 迴圈結束後，如果還有沒存的資料，一併儲存
if save_counter > 0:
    margin = margin.sort_index()
    margin.to_pickle(margin_path)
    print(f"最後儲存 {save_counter} 筆更新")