import requests
import pandas as pd
import os
import sys
from tqdm import tqdm

# --- 設定路徑 ---

STOCK_LIST_PATH = "/home/keywin/workspace/crawler/history/stock_list.pkl"
MAIN_PLAYERS_PKL = "/home/keywin/workspace/crawler/history/主力買賣超張.pkl"
HOUSE_DIFF_PKL = "/home/keywin/workspace/crawler/history/買賣家數差.pkl"

# 1. 載入資料
stock_list = pd.read_pickle(STOCK_LIST_PATH)

def load_or_create(path):
    if os.path.exists(path):
        return pd.read_pickle(path)
    return pd.DataFrame()

df_main = load_or_create(MAIN_PLAYERS_PKL)
df_house = load_or_create(HOUSE_DIFF_PKL)

# 取得目前資料庫最後日期 (YYYY-MM-DD)
last_date_db = df_main.index[-1] if not df_main.empty else "2024-09-04"
headers = {"User-Agent": "Mozilla/5.0", "Referer": "https://www.yuanta.com.tw/"}

# --- [關鍵] 檢查第一支股票決定是否更新 ---
first_stock = str(stock_list.index[0])
print(f"🔍 正在檢查指標股 {first_stock} 是否有新資料...")

try:
    check_url = f"https://ytdf.yuanta.com.tw/prod/yesidmz/api/chipanalysis/maininoutcharts?symbol={first_stock}"
    r = requests.get(check_url, headers=headers, timeout=10)
    if r.status_code == 200:
        api_data = r.json().get('data', {}).get('mainInOutChartDayInfos', [])
        if api_data:
            # 格式化 API 最新日期
            api_raw = api_data[0]['date']
            api_latest = f"{api_raw[:4]}-{api_raw[4:6]}-{api_raw[6:]}"
            
            if api_latest <= last_date_db:
                print(f"☕ API 最新日期 {api_latest} <= 資料庫日期 {last_date_db}。")
                print(">>> 全市場資料尚未更新，直接跳過本次作業。")
                sys.exit() # 這裡直接中斷整個程式
            else:
                print(f"🚀 偵測到新日期 {api_latest}，準備同步全市場資料...")
except Exception as e:
    print(f"預檢失敗: {e}，保險起見嘗試更新。")

# --- 2. 開始全市場抓取 ---
new_data_main = {}
new_data_house = {}

for stock_id in tqdm(stock_list.index, desc="同步台股籌碼"):
    s_id = str(stock_id)
    url = f"https://ytdf.yuanta.com.tw/prod/yesidmz/api/chipanalysis/maininoutcharts?symbol={s_id}"
    
    try:
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code != 200: continue
        
        raw_json = r.json()
        chart_infos = raw_json.get('data', {}).get('mainInOutChartDayInfos', [])
        if not chart_infos: continue
        
        # 增量收集：只拿比資料庫新的日期
        for item in chart_infos:
            d_raw = item['date']
            d_str = f"{d_raw[:4]}-{d_raw[4:6]}-{d_raw[6:]}"
            
            if d_str > last_date_db:
                new_data_main[(d_str, s_id)] = float(item['overBoughtOverSold'])
                new_data_house[(d_str, s_id)] = float(item['securitiesCompCount'])
            else:
                break # 碰到舊日期就換下一檔股票
                
    except Exception as e:
        print(f"\n{s_id} 錯誤: {e}")
        continue

# --- 3. 填入數據與存檔 ---
if new_data_main:
    # 建立臨時二維表
    update_main = pd.Series(new_data_main).unstack()
    update_house = pd.Series(new_data_house).unstack()

    # 合併與優化
    df_main = update_main.combine_first(df_main).astype('float32').sort_index()
    df_house = update_house.combine_first(df_house).astype('float32').sort_index()

    # 存檔
    df_main.to_pickle(MAIN_PLAYERS_PKL)
    df_house.to_pickle(HOUSE_DIFF_PKL)
    print(f"✅ 更新成功！目前資料範圍至：{df_main.index[-1]}")
else:
    print("無新資料需要合併。")