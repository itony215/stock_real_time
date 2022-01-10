# stock_real_time
抓取即時股價及量
## Usage
每五秒更新買價跟即時買量的5分K
```
python 5k.py
```
每五分鐘(299秒)判斷是否達條件並通知
```
python alert.py
```

## 資料來源

[台灣證券交易所 - 基本市況報導網站](https://mis.twse.com.tw/stock/index.jsp)

## 證交所 API

整理twse的 API 清單如下：

- getChartOhlcStatis
- getDailyRangeOnlyKD
- getDailyRangeWithMA
- getOhlc
- getShowChart
- getStock
- getStockInfo
- getStockNames
- resetSession

### getStockInfo Usage

其中 `getStockInfo` 可以用來抓取當前的交易資訊，用法如下：

```
http://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch=STOCK_NUMBER&_=CURRENT_TIME
```

參數設置：

- STOCK_NUMBER 是該隻股票的種類和號碼，ex. `tse_1101.tw`，
- 也可以用 `|` 一次 query 很多筆股票資料。ex. `tse_1101.tw|otc_8299.tw|tse_2330.tw`
- CURRENT_TIME 是當下的 epoch time，單位是毫秒，不設也沒差

### getStockInfo Response

分析 response 的 JSON 可以得到：

- msgArray
- queryTime
- rtcode
- referer
- rtmessage
- userDelay

其主要資訊都在 `msgArray` 中，分為以下幾類：

#### 股票資訊

- c：股票代號，ex. `1101`
- ch：Channel，ex. `1101.tw`
- ex：上市或上櫃，ex. `tse`,`otc`
- n：股票名稱，ex. `台泥`
- nf：似乎為全名，ex. `台灣水泥股份有限公司`

#### 即時交易資訊

- z：最近成交價，ex. `42.85`
- tv：Temporal Volume，當盤成交量，ex. `1600`
- v：Volume，當日累計成交量，ex. `11608`
- a：最佳五檔賣出價格，ex. `42.85_42.90_42.95_43.00_43.05_`
- f：最價五檔賣出數量，ex. `83_158_277_571_233_`
- b：最佳五檔買入價格，ex. `42.80_42.75_42.70_42.65_42.60_`
- g：最佳五檔買入數量，ex. `10_28_10_2_184_`
- tlong：資料時間，ex. `1424755800000`
- t：資料時間，ex. `13:30:00`
- ip：好像是一個 flag，3 是暫緩收盤股票, 2 是趨漲, 1 是趨跌， ex. `0`

#### 日資訊

- d：今日日期，ex. `20220110`
- h：今日最高，ex. `42.90`
- l：今日最低，ex. `42.35`
- o：開盤價，ex. `42.40`
- u：漲停點，ex. `45.10`
- w：跌停點，ex. `39.20`
- y：昨收，ex. `42.15`

#### 不明
- i： ex. `01`
- it： ex. `12`
- p： ex. `0`
