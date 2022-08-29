import pandas as pd

high = pd.read_pickle("/home/pineapple/Documents/stock/crawler/history/最高價.pkl")
low = pd.read_pickle("/home/pineapple/Documents/stock/crawler/history/最低價.pkl")
start = pd.read_pickle("/home/pineapple/Documents/stock/crawler/history/開盤價.pkl")
end = pd.read_pickle("/home/pineapple/Documents/stock/crawler/history/收盤價.pkl")
volumn = pd.read_pickle("/home/pineapple/Documents/stock/crawler/history/成交股數.pkl")

for s in (high.columns):
    try:
        id = str(s)
        result = pd.concat([start[id],high[id],low[id],end[id],round(volumn[id]/1000,2)], axis=1, keys=["開盤價", "最高價", "最低價", "收盤價","量"])
        result['漲跌幅'] = round(result['收盤價'].pct_change()*100,2)
        result['Mean_5']= result['收盤價'].rolling(5).mean()
        result['Std_5']= result['收盤價'].rolling(5).std()
        result['BBand_top']= result['Mean_5']+result['Std_5']*0.895
        result['BBand_down']= result['Mean_5']-result['Std_5']*0.895
        result['over_top']= result.apply(lambda x : 1 if x['收盤價'] >= x['BBand_top'] else 0, axis=1)
        #result['over_top'] = result['over_top'].astype(int)
        result['count'] = result['over_top'].cumsum()-result['over_top'].cumsum().where(result['over_top']==0).ffill().fillna(0).astype(int)
        #result['count'] = result['over_top'].shift(1) + result['over_top'] if result['over_top'] > 0 else 0
        #result['count'] = result['count']+(result['count'].shift(1)>=1).astype(int)
        #result.loc[result['over_top']<1, 'count'] = 0
        #result['Fruit Total']= result.iloc[:, -3:-1].sum(axis=1)
        #result['count2'] = result['count'] + result['over_top']
        #result['count'] = result.apply(lambda x : x['over_top'].shift(1)+1 if x['over_top'] >= 1 else 0, axis=1)#result['over_top'].shift(1)
        #print(result['over_top'])
        #reversed_df = result.iloc[::-1]
        #reversed_df.to_csv("./個股資料/"+id+".csv",encoding='utf_8_sig')
        result.to_csv("/home/pineapple/Documents/stock/crawler/stock_over_bband/"+id+".csv",encoding='utf_8_sig')
    except:
        pass