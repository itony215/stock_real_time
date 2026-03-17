import pandas as pd
from datetime import date
import os

# ===== LINE 設定 =====
from linebot import LineBotApi
from linebot.models import TextSendMessage
from linebot.exceptions import LineBotApiError

CHANNEL_ACCESS_TOKEN = '你的token'
YOUR_USER_ID = '你的user_id'

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)

def send_line_message(user_id, text_msg):
    try:
        line_bot_api.push_message(user_id, TextSendMessage(text=text_msg))
        print("訊息發送成功！")
    except LineBotApiError as e:
        print(f"發送失敗: {e}")

# ===== 檢查設定 =====
BASE_PATH = "/home/keywin/workspace/crawler/history"

FILES = {
    "開盤價": "開盤價.pkl",
    "最高價": "最高價.pkl",
    "最低價": "最低價.pkl",
    "收盤價": "收盤價.pkl",
    "成交股數": "成交股數.pkl",
    "成交筆數": "成交筆數.pkl"
}

today = pd.Timestamp(date.today())

def check_file(name, filename):
    path = os.path.join(BASE_PATH, filename)

    if not os.path.exists(path):
        return f"[❌] {name} 檔案不存在"

    df = pd.read_pickle(path)

    if today not in df.index:
        return f"[❌] {name} 沒有今日資料"

    today_data = df.loc[today]

    stock_count = today_data.count()
    if stock_count < 1000:
        return f"[❌] {name} 股票數量異常: {stock_count}"

    nan_ratio = today_data.isna().mean()
    if nan_ratio > 0.2:
        return f"[❌] {name} NaN 過多: {nan_ratio:.2%}"

    if (today_data.fillna(0) == 0).all():
        return f"[❌] {name} 全部為0"

    return f"[✅] {name} 正常"

def main():
    print(f"===== 檢查 {today.date()} =====")
    results = []

    for name, file in FILES.items():
        result = check_file(name, file)
        print(result)
        results.append(result)

    # ===== 整理訊息 =====
    msg = f"📊 台股資料檢查 ({today.date()})\n\n"
    msg += "\n".join(results)

    # ===== 判斷是否異常 =====
    if any("❌" in r for r in results):
        msg = "🚨【資料異常】🚨\n\n" + msg
        send_line_message(YOUR_USER_ID, msg)
    else:
        msg = "✅【資料正常】\n\n" + msg
        send_line_message(YOUR_USER_ID, msg)

if __name__ == "__main__":
    main()