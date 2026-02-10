import pandas as pd
import os
from datetime import date
from linebot import LineBotApi
from linebot.models import TextSendMessage
from linebot.exceptions import LineBotApiError

# ==========================================
# 1. 設定 LINE Messaging API 資訊
# ==========================================
# 請填入上一篇教學中取得的資料
CHANNEL_ACCESS_TOKEN = ''
YOUR_USER_ID = ''

# 初始化機器人
line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)

def send_line_message(user_id, text_msg):
    try:
        line_bot_api.push_message(user_id, TextSendMessage(text=text_msg))
        print("訊息發送成功！")
    except LineBotApiError as e:
        print(f"發送失敗: {e}")

# ==========================================
# 2. 您的選股邏輯 (保持不變)
# ==========================================
notice = '融券認輸等一根長紅:\n'
today = date.today()

# 讀取資料
# 注意：請確認您的檔案路徑是否正確
try:
    all_stock = pd.read_csv("/home/keywin/workspace/crawler/strategy/stock_data/data/所有股票資訊_sell.csv")
except FileNotFoundError:
    print("找不到檔案，請檢查路徑")
    exit()

# 篩選條件
result = all_stock[all_stock['融券5增張'] > 0]
result= result[result['融券5MAX']==result['前日融券']]
result= result[result['前日融券']>(result['融券5增張']/2)]
result= result[result['融資差額(張)']>0]
result= result[result['當日漲跌幅']>=3]
result= result[result['融券差額(張)']>0]

result= result[result['收盤價']>=15]
result = result[result['成交量'] > 500]

result.insert(0, "date", today)
result = result.sort_values(by=['融券5增張'], ascending=False)

# 存檔
result.to_csv("/home/keywin/workspace/crawler/strategy/stock_data/data/空方標的11(融券認輸等一根長紅).csv", encoding='utf_8_sig', index=False)

# ==========================================
# 3. 整理數據並發送 LINE (修改處)
# ==========================================

# 為了讓手機好閱讀，我們只選取重要欄位，並排版
if not result.empty:
    # 取出要顯示的欄位
    df_display = result[['id', 'name', '收盤價', '融券差額(張)']]
    
    # 將 DataFrame 轉為字串，這裡做一點格式美化
    # 標題
    msg_content = f"{notice} {today}\n----------------\n"
    
    # 逐行加入股票資訊 (手機看表格容易跑版，建議用條列式)
    for index, row in df_display.iterrows():
        stock_info = f"[{row['id']} {row['name']}]\n價:{row['收盤價']} / 券差:{row['融券差額(張)']}\n"
        msg_content += stock_info + "\n"
        
        # Messaging API 單次文字上限為 5000 字，若股票太多可能要分段
        if len(msg_content) > 1500: 
            msg_content += "\n(僅顯示部分結果...)"
            break
            
    # 發送訊息
    send_line_message(YOUR_USER_ID, msg_content)

else:
    send_line_message(YOUR_USER_ID, f"{notice} {today}\n今日無符合條件標的。")
