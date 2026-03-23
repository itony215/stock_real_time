import pandas as pd
import os
from datetime import date
from linebot import LineBotApi
from linebot.models import TextSendMessage
from linebot.exceptions import LineBotApiError
stock_have_futures = [
"1101",
"1102",
"1210",
"1216",
"1301",
"1303",
"1312",
"1314",
"1319",
"1326",
"1402",
"1440",
"1476",
"1477",
"1503",
"1504",
"1513",
"1536",
"1560",
"1565",
"1590",
"1605",
"1608",
"1609",
"1717",
"1718",
"1722",
"1795",
"1802",
"1904",
"1905",
"1907",
"1909",
"2002",
"2006",
"2014",
"2027",
"2049",
"2059",
"2105",
"2201",
"2231",
"2301",
"2303",
"2308",
"2312",
"2313",
"2317",
"2323",
"2324",
"2327",
"2328",
"2329",
"2330",
"2331",
"2332",
"2337",
"2338",
"2340",
"2344",
"2345",
"2347",
"2352",
"2353",
"2354",
"2355",
"2356",
"2357",
"2360",
"2367",
"2368",
"2371",
"2376",
"2377",
"2379",
"2382",
"2383",
"2385",
"2388",
"2392",
"2393",
"2401",
"2404",
"2408",
"2409",
"2412",
"2421",
"2439",
"2441",
"2449",
"2454",
"2455",
"2457",
"2458",
"2474",
"2481",
"2485",
"2486",
"2489",
"2492",
"2498",
"2515",
"2520",
"2542",
"2548",
"2603",
"2605",
"2606",
"2609",
"2610",
"2615",
"2618",
"2633",
"2634",
"2801",
"2834",
"2880",
"2881",
"2882",
"2883",
"2884",
"2885",
"2886",
"2887",
"2890",
"2891",
"2892",
"2913",
"2915",
"3005",
"3006",
"3008",
"3017",
"3019",
"3034",
"3035",
"3036",
"3037",
"3042",
"3044",
"3045",
"3078",
"3081",
"3105",
"3152",
"3189",
"3211",
"3227",
"3231",
"3260",
"3264",
"3293",
"3324",
"3374",
"3376",
"3380",
"3406",
"3443",
"3481",
"3529",
"3532",
"3533",
"3552",
"3653",
"3661",
"3665",
"3673",
"3680",
"3691",
"3702",
"3706",
"3711",
"3714",
"4123",
"4128",
"4162",
"4736",
"4743",
"4904",
"4919",
"4938",
"4958",
"5009",
"5269",
"5274",
"5347",
"5371",
"5388",
"5425",
"5457",
"5483",
"5534",
"5871",
"5876",
"5880",
"5904",
"6005",
"6116",
"6121",
"6139",
"6147",
"6153",
"6173",
"6176",
"6182",
"6188",
"6213",
"6223",
"6239",
"6245",
"6257",
"6269",
"6271",
"6274",
"6278",
"6279",
"6282",
"6285",
"6290",
"6414",
"6443",
"6472",
"6488",
"6505",
"6510",
"6526",
"6547",
"6669",
"6757",
"6770",
"8039",
"8044",
"8046",
"8069",
"8086",
"8112",
"8150",
"8163",
"8299",
"8358",
"8436",
"9904",
"9914",
"9938",
"9939",
"9945",
"9958"]
# ==========================================
# 1. 設定 LINE Messaging API 資訊
# ==========================================
# 請填入上一篇教學中取得的資料
CHANNEL_ACCESS_TOKEN = 'jgrDhhWI+3Qcepbj/RM0vNdzTx8hqTw4xYP7pxn5YIR9UkhvalIwIpEbGYw0y/RKawEEOQbgIPYBZAVOQPnUSyJjNfxUfpnNVQohlHls0JYpzonOBchiAaPEFeEn9T12hiDu1WIBs0Gp4QbDeYK0JAdB04t89/1O/w1cDnyilFU='
YOUR_USER_ID = 'U9cc157ff55a08d57beabd64bc29a3020'

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
notice = '兩長紅2趴籌碼異常:\n'
today = date.today()
#today = '2026-03-03'#
# 讀取資料
# 注意：請確認您的檔案路徑是否正確
try:
    all_stock = pd.read_csv("/home/keywin/workspace/crawler/strategy/stock_data/data/所有股票資訊_sell.csv")
except FileNotFoundError:
    print("找不到檔案，請檢查路徑")
    exit()

# 篩選條件
result = all_stock[all_stock['當日漲跌幅'] > 2]
result = result[result['昨日漲跌幅'] > 2]
result = result[result['三大買賣超'] < result['昨日三大']]
result = result[result['主力買賣超(張)'] < result['昨日主力']]
result = result[result['收盤價'] >= 15]
result = result[result['成交量'] > 500]

result.insert(0, "date", today)
result = result.sort_values(by=['融券差額(張)'], ascending=False)

# 存檔
result.to_csv("/home/keywin/workspace/crawler/strategy/stock_data/data/空方標的88(兩長紅2趴籌碼異常).csv", encoding='utf_8_sig', index=False)

# ==========================================
# 3. 整理數據並發送 LINE (修改處)
# ==========================================

# 為了讓手機好閱讀，我們只選取重要欄位，並排版
if not result.empty:
    # 取出要顯示的欄位
    df_display = result[['id', 'name', '收盤價', '當日漲跌幅', '三等份位階']]
    
    # 將 DataFrame 轉為字串，這裡做一點格式美化
    # 標題
    msg_content = f"{notice} {today}\n----------------\n"
    
    # 逐行加入股票資訊 (手機看表格容易跑版，建議用條列式)
    for index, row in df_display.iterrows():
        stock_id = str(row['id'])
        future_tag = "(期貨)" if stock_id in stock_have_futures else ""
    
        stock_info = f"[{stock_id} {row['name']}{future_tag}]\n價:{row['收盤價']} / 漲跌幅:{row['當日漲跌幅']}/ 三等份位階:{row['三等份位階']}\n"
        msg_content += stock_info + "\n"
        
        # Messaging API 單次文字上限為 5000 字，若股票太多可能要分段
        if len(msg_content) > 1500: 
            msg_content += "\n(僅顯示部分結果...)"
            break
            
    # 發送訊息
    send_line_message(YOUR_USER_ID, msg_content)

else:
    send_line_message(YOUR_USER_ID, f"{notice} {today}\n今日無符合條件標的。")