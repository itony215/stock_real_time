import pickle
import requests
import datetime
from io import StringIO
import pandas as pd
import dataframe_image as dfi
from bs4 import BeautifulSoup

def send_line_notify(token, message, image_path):
    url = "https://notify-api.line.me/api/notify"
    headers = {"Authorization": "Bearer " + token}
    payload = {"message": message}
    files = {"imageFile": open(image_path, "rb")}
    r = requests.post(url, headers=headers, params=payload, files=files)
    return r.status_code

# Save the DataFrame as an image


end = pd.read_pickle("./history/收盤價.pkl")


try:
    r = requests.get('https://jdata.yuanta.com.tw/z/ze/zew/zew.djhtm')
    soup = BeautifulSoup(r.text, 'html.parser')
    table = soup.find_all('table')
    table_str = str(table)
    table_io = StringIO(table_str)
    df = pd.read_html(table_io)[-1]
    new_df = df[1:]
    new_df.columns = new_df.iloc[0]
    new_df = new_df.drop(new_df.index[0])  
    new_df['股票名稱'] =  new_df['股票名稱'].str[21:-9]
    new_df = new_df.iloc[:, :-3]
    new_df[['ID', 'name']] = new_df['股票名稱'].str.split("','", expand=True)
    #new_df = new_df[['ID', 'name', '撮合方式', '處份起始日', '處份截止日']]
    moving_average = end.rolling(window=20).mean()

    # Filter new_df to include only rows where the closing price is above the moving average
    filtered_df = new_df[new_df['ID'].isin(end.columns)]
    filtered_df = filtered_df[filtered_df.apply(lambda row: end[row['ID']].iloc[-1] > moving_average[row['ID']].iloc[-1], axis=1)]
    filtered_df = filtered_df[['ID', 'name', '撮合方式', '處份 起始日', '處份 截止日']]
    print(filtered_df)
except:
    print('no data')
df_styled = filtered_df.style.background_gradient() 
dfi.export(df_styled,"filtered_df.png")
send_line_notify('X57Kb4EhV6073WKCE9UU2eT3IBvxmY44LPtmdUwwS8O', '多頭處置股', 'filtered_df.png')