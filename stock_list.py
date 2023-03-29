import pandas as pd
import requests
from io import StringIO
import json
from datetime import date
def transform_date2(date):
        y, m, d = date.split('/')
        return str(int(y)-1911) + '/' + m  + '/' + d
stock_list_old = pd.read_pickle("/home/pineapple/Documents/stock/crawler/history/stock_list.pkl")
res = requests.get("http://isin.twse.com.tw/isin/C_public.jsp?strMode=2")
df11 = pd.read_html(res.text)[0]
res2 = requests.get("http://isin.twse.com.tw/isin/C_public.jsp?strMode=4")
df12 = pd.read_html(res2.text)[0]

df11.columns = df11.iloc[0]
df11 = df11.iloc[1:]

df12.columns = df12.iloc[0]
df12 = df12.iloc[1:]
stock_list_new = df11.append(df12)

stock_list_new = stock_list_new[stock_list_new['產業別'].notna()]
stock_list_new = stock_list_new.set_index('有價證券代號及名稱')

today = date.today()
day = today.strftime("%Y/%m/%d")
datestr = today.strftime("%Y%m%d")
# datestr = '20230324'
# day = '2023/03/24'
datestr2 = transform_date2(day)
df_time=pd.Timestamp(day)
# 上市
r = requests.post('https://www.twse.com.tw/exchangeReport/MI_INDEX?response=csv&date=' + datestr + '&type=ALL')
df = pd.read_csv(StringIO(r.text.replace("=", "")), header=["證券代號" in l for l in r.text.split("\n")].index(True)-1, index_col=['證券代號'])
df=df[df.index.str.len() <5]
df1 = df.iloc[:, 0:1]
#上櫃
r = requests.post('https://www.tpex.org.tw/web/stock/aftertrading/daily_close_quotes/stk_quote_result.php?l=zh-tw&d=' + datestr2)
json_data = json.loads(r.text)
stock_json = json_data["aaData"]
df2 = pd.DataFrame(stock_json)
df2 = df2.set_index([0])
df2=df2[df2.index.str.len() <5]
df3 = df2.iloc[:, 0:1]
df3.columns = ['證券名稱']
stock_list_df = df1.append(df3)


for i in stock_list_df.index:
    try:
        
        if(i in stock_list_old.index):
            #print(stock_list_old.loc[i])
            pass
        else:

            name = stock_list_df.loc[i][0]
            cate = stock_list_new[(stock_list_new.index.str.contains(i))]['產業別'][0]
            row = pd.Series({'name':name,'category':cate},name=str(i))
            stock_list_old = stock_list_old.append(row)
            print('add ', i, name)
    except:
        print('error', i)
        

#stock_list_old.columns = ["name","category"]
#stock_list_old.set_index(keys ="stock_id",inplace=True)
stock_list_old.to_pickle("/home/pineapple/Documents/stock/crawler/history/stock_list.pkl")
