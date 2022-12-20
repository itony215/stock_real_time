import pickle
import requests
from datetime import date
from io import StringIO
import pandas as pd
import json
def transform_date(date):   
        y, m, d = date.split('/')
        return str(int(y)+1911) + '/' + m  + '/' + d

high = pd.read_pickle("/home/pineapple/Documents/stock/crawler/history/最高價.pkl")
low = pd.read_pickle("/home/pineapple/Documents/stock/crawler/history/最低價.pkl")
start = pd.read_pickle("/home/pineapple/Documents/stock/crawler/history/開盤價.pkl")
end = pd.read_pickle("/home/pineapple/Documents/stock/crawler/history/收盤價.pkl")
volumn = pd.read_pickle("/home/pineapple/Documents/stock/crawler/history/成交股數.pkl")
count = pd.read_pickle("/home/pineapple/Documents/stock/crawler/history/成交筆數.pkl")

today = date.today()
df_time=pd.Timestamp(today)
day = today.strftime("%Y/%m/%d")
datestr = today.strftime("%Y%m%d")
#if start.index[-1] < df_time:
startPrice={}
highPrice={}
lowPrice={}
endPrice={}
volumnPart={}
countPart={}
#datestr = '20220722'
#上市
r = requests.post('https://www.twse.com.tw/exchangeReport/MI_INDEX?response=csv&date=' + datestr + '&type=ALL')
if datestr in r.headers["Content-disposition"] and len(r.text)>0:
    print('it is today data')
    df = pd.read_csv(StringIO(r.text.replace("=", "")), header=["證券代號" in l for l in r.text.split("\n")].index(True)-1, index_col=['證券代號'])
    df=df[df.index.str.len() <5]
    #display(df)     
    for i in df.index:
        try:
            startPrice[i] = float(df['開盤價'][i].replace(',',''))
            highPrice[i] = float(df['最高價'][i].replace(',',''))
            lowPrice[i] = float(df['最低價'][i].replace(',',''))
            endPrice[i] = float(df['收盤價'][i].replace(',',''))
            volumnPart[i] = float(df['成交股數'][i].replace(',',''))
            countPart[i] = float(df['成交筆數'][i].replace(',',''))
        except:
            print('error 1:', i)
            continue
#上櫃
r2 = requests.post('https://www.tpex.org.tw/web/stock/aftertrading/daily_close_quotes/stk_quote_result.php')
json_data = json.loads(r2.text)
stock_json = json_data["aaData"]
#print(stock_json)
if transform_date(json_data['reportDate']) == day and len(r.text)>0:
    print('it is today data 2')
    df2 = pd.DataFrame(stock_json)
    df2 = df2.set_index([0])
    df2=df2[df2.index.str.len() <5]
    for j in df2.index:
        try:
            startPrice[j] = float(df2.loc[j][4].replace(',',''))
            highPrice[j] = float(df2.loc[j][5].replace(',',''))
            lowPrice[j] = float(df2.loc[j][6].replace(',',''))
            endPrice[j] = float(df2.loc[j][2].replace(',',''))
            volumnPart[j] = float(df2.loc[j][8].replace(',',''))
            countPart[j] = float(df2.loc[j][10].replace(',',''))
        except:
            print('error 2:', j)
            continue
        
start_new = pd.DataFrame([startPrice], index = [df_time])
start_merge = pd.concat([start,start_new])
start_merge.index.name = 'date'
start_merge.columns.name= 'stock_id'
start_merge = start_merge[~start_merge.index.duplicated(keep='last')]
start_merge.to_pickle("/home/pineapple/Documents/stock/crawler/history/開盤價.pkl")

high_new = pd.DataFrame([highPrice], index = [df_time])
high_merge = pd.concat([high,high_new])
high_merge.index.name = 'date'
high_merge.columns.name= 'stock_id'
high_merge = high_merge[~high_merge.index.duplicated(keep='last')]
high_merge.to_pickle("/home/pineapple/Documents/stock/crawler/history/最高價.pkl")

low_new = pd.DataFrame([lowPrice], index = [df_time])
low_merge = pd.concat([low,low_new])
low_merge.index.name = 'date'
low_merge.columns.name= 'stock_id'
low_merge = low_merge[~low_merge.index.duplicated(keep='last')]
low_merge.to_pickle("/home/pineapple/Documents/stock/crawler/history/最低價.pkl")

end_new = pd.DataFrame([endPrice], index = [df_time])
end_merge = pd.concat([end,end_new])
end_merge.index.name = 'date'
end_merge.columns.name= 'stock_id'
end_merge = end_merge[~end_merge.index.duplicated(keep='last')]
end_merge.to_pickle("/home/pineapple/Documents/stock/crawler/history/收盤價.pkl")

volumn_new = pd.DataFrame([volumnPart], index = [df_time])
volumn_merge = pd.concat([volumn,volumn_new])
volumn_merge.index.name = 'date'
volumn_merge.columns.name= 'stock_id'
volumn_merge = volumn_merge[~volumn_merge.index.duplicated(keep='last')]
volumn_merge.to_pickle("/home/pineapple/Documents/stock/crawler/history/成交股數.pkl")

count_new = pd.DataFrame([countPart], index = [df_time])
count_merge = pd.concat([count,count_new])
count_merge.index.name = 'date'
count_merge.columns.name= 'stock_id'
count_merge = count_merge[~count_merge.index.duplicated(keep='last')]
count_merge.to_pickle("/home/pineapple/Documents/stock/crawler/history/成交筆數.pkl")