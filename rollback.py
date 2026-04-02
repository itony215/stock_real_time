import pandas as pd
import os

# 設定檔案路徑清單
file_paths = {
    "最高價": "/home/keywin/workspace/crawler/history/最高價.pkl",
    "最低價": "/home/keywin/workspace/crawler/history/最低價.pkl",
    "開盤價": "/home/keywin/workspace/crawler/history/開盤價.pkl",
    "收盤價": "/home/keywin/workspace/crawler/history/收盤價.pkl",
    "成交股數": "/home/keywin/workspace/crawler/history/成交股數.pkl",
    "成交筆數": "/home/keywin/workspace/crawler/history/成交筆數.pkl"
}

def rollback_last_date():
    # 1. 先確認所有檔案是否存在
    for name, path in file_paths.items():
        if not os.path.exists(path):
            print(f"錯誤：找不到檔案 {path}")
            return

    # 2. 以「開盤價」作為基準，找出最後一個日期
    base_df = pd.read_pickle(file_paths["開盤價"])
    if base_df.empty:
        print("資料夾中沒有資料可刪除。")
        return
        
    last_date = base_df.index[-1]
    print(f"預計刪除的最後一筆日期為: {last_date}")

    # 確認是否執行
    confirm = input(f"確定要刪除所有檔案中 {last_date} 的資料嗎？(y/n): ")
    if confirm.lower() != 'y':
        print("操作已取消。")
        return

    # 3. 逐一處理每個檔案
    for name, path in file_paths.items():
        df = pd.read_pickle(path)
        
        # 檢查最後一筆日期是否一致
        if df.index[-1] == last_date:
            # 移除最後一筆日期（drop 掉最後一個 index）
            df_new = df.drop(index=last_date)
            
            # 存回原位
            df_new.to_pickle(path)
            print(f"--- {name} 刪除成功，剩餘筆數: {len(df_new)}")
        else:
            print(f"⚠️ 警告：{name} 的最後日期 ({df.index[-1]}) 與基準不符，略過。")

    print("\n所有檔案已完成回退。現在你可以重新執行爬蟲程式補抓資料。")

if __name__ == "__main__":
    rollback_last_date()