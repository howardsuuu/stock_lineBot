# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import yfinance as yf
import numpy as np
import pandas as pd
import datetime
# import matplotlib.pyplot as plt
# pd.set_option("display.max_rows", None)

# from stock_pandas import StockDataFrame
# import plotly.graph_objs as go


# %%
### Stock list
stocks = ['pltr', 'aal', 'mac']


# %%
## Get instant Data
# .download() is for rapid use of getting data

def get_insta_price():
    
    global inst_dic
    inst_dic = {}

    for inst_stock in stocks:
        raw_today = yf.download(tickers=inst_stock, period='1', interval = '1m')
        inst_dic[inst_stock] = raw_today
        # print(type(inst_stock), type(raw_today))
    return inst_dic
get_insta_price()


# %%
### Get History Data

def get_ma(): # Return Dict

    global ma_dic
    ma_dic = {}

    for hist_stock in stocks:
        raw_df = yf.Ticker(hist_stock).history(period='max')
        simple_df = raw_df[['Close', 'Volume']].copy() # extract col
        #.drop(['High', 'Low', 'Dividends', 'Stock Splits'], axis = 1, inplace = False)
        # simple_hist.columns = ['open', 'close', 'volume'] # rename col
        simple_df['ma_5'] = simple_df.iloc[:-1, 0].rolling(window = 5, min_periods = 1).mean()
        simple_df['ma_10'] = simple_df.iloc[:-1, 0].rolling(window = 10, min_periods = 1).mean()
        simple_df['ma_20'] = simple_df.iloc[:-1, 0].rolling(window = 20, min_periods = 1).mean()
        simple_df['ma_60'] = simple_df.iloc[:-1, 0].rolling(window = 60, min_periods = 1).mean()
        # simple_df['ma_120'] = simple_df['Close'].iloc[:-1, 0].rolling(window = 120, min_periods = 1).mean()
        # simple_df['ma_240'] = simple_df['Close'].iloc[:-1, 0].rolling(window = 240, min_periods = 1).mean()

        ## For plotting
        # simple_df['Signal'] = 0.0
        # simple_df['Signal'] = np.where(simple_df['ma_20'] > simple_df['ma_60'], 1., 0.)
        # simple_df['Position'] = simple_df['Signal'].diff()


        ## temporarily unavailable
        # st_hist = StockDataFrame(simple_hist) # Turn into st_pandas form
        # ['ma:X'] creates a Series, [[ma, ma, ma]] creates DataFrame
        # st_hist[['ma:5', 'ma:10', 'ma:20', 'ma:60', 'ma:120', 'ma:200']]

        # return st_hist
        ma_dic[hist_stock] = simple_df
        
    return ma_dic
get_ma()
# -----------------Selecting Data-------------------
# # # Get each Col name
# ma_dic['pltr'].columns

# # # Get multi-Series (Cols)
# ma_dic['pltr'][['open', 'ma:5']]

# # Get a Serie (a Col)
# ma_dic['pltr']['ma:5']

# ----
# a = ma_dic['pltr'].iloc[-1]['ma_5']
# ma_dic['voo'].iloc[-1]
# ma_dic['voo'].at['2021-05-28', 'Close']
# ma_dic['voo']['ma_60'][-2] == ma_dic['voo'].iloc[-2]['ma_60'] -> TRUE
# ----------------
# 判斷高點
# ma_dic['voo']['ma_5'].idxmax()
# 判斷 200 MA 斜率
# iroc = original[app].diff() / ma_dic['voo']['ma'].diff()

# 股價跌破 200 MA


# %%
### 判斷 MA
short_term, mid_term, = {},{}
Sbuy_or_sell, Mbuy_or_sell, = {},{}

def notify_params():

    for i in stocks[:]:
        # ------------------------------------------------------------------
        # 短行情
        if inst_dic[i]['Close'][-1] > ma_dic[i]['ma_5'][-2] > ma_dic[i]['ma_10'][-2]:
            short_term[i] = '短多'
        elif ma_dic[i]['ma_10'][-2] > ma_dic[i]['ma_5'][-2] > inst_dic[i]['Close'][-1]:
            short_term[i] = '短空'
        elif ma_dic[i]['ma_10'][-2] > inst_dic[i]['Close'][-1] > ma_dic[i]['ma_5'][-2]:
            short_term[i] = '短盤整'
        else:
            short_term[i] = "行情不定(短)"

        # 短 Buy or Sell
        if ma_dic[i]['ma_5'][-2] > ma_dic[i]['ma_10'][-2]:
            Sbuy_or_sell[i] = '5突破10'
        elif ma_dic[i]['ma_5'][-2] > inst_dic[i]['Close'][-1]:
            Sbuy_or_sell[i] = '減碼(短)'
        elif ma_dic[i]['ma_10'][-2] > inst_dic[i]['Close'][-1]:
            Sbuy_or_sell[i] = '清倉(短)'
        else:
            Sbuy_or_sell[i] = 'short hold'
        # ------------------------------------------------------------------
        # 中行情
        if inst_dic[i]['Close'][-1] > ma_dic[i]['ma_20'][-2] > ma_dic[i]['ma_60'][-2]:
            mid_term[i] = '中期多'
        elif ma_dic[i]['ma_60'][-2] > ma_dic[i]['ma_20'][-2] > inst_dic[i]['Close'][-1]:
            mid_term[i] = '中期空'
        elif ma_dic[i]['ma_60'][-2] > inst_dic[i]['Close'][-1] > ma_dic[i]['ma_20'][-2]:
            mid_term[i] = '中期盤整'
        else:
            mid_term[i] = "mid hold"
        # 中 Buy or Sell
        if ma_dic[i]['ma_60'][-2] > ma_dic[i]['ma_20'][-2]:
            Mbuy_or_sell[i] = '20跌破60'
        elif ma_dic[i]['ma_20'][-2] > inst_dic[i]['Close'][-1]:
            Mbuy_or_sell[i] = '減碼(中)'
        elif ma_dic[i]['ma_60'][-2] > inst_dic[i]['Close'][-1]:
            Mbuy_or_sell[i] = '清倉(中)'
        else:
            Mbuy_or_sell[i] = 'Mid觀察'
        # ------------------------------------------------------------------
        # # 長行情
        # if inst_dic[i]['Close'][-1] > ma_dic[i]['ma_120'][-2] > ma_dic[i]['ma_240'][-2]:
        #     long_term[i] = '長多'
        # elif ma_dic[i]['ma_240'][-2] > ma_dic[i]['ma_120'][-2] > inst_dic[i]['Close'][-1]:
        #     long_term[i] = '長短'
        # elif ma_dic[i]['ma_240'][-2] > inst_dic[i]['Close'][-1] > ma_dic[i]['ma_120'][-2]:
        #     long_term[i] = '長期盤整'
        # else:
        #     long_term[i] = "行情不定(長)"

        # # 長 Buy or Sell
        # if ma_dic[i]['ma_240'][-2] > ma_dic[i]['ma_120'][-2]:
        #     Lbuy_or_sell[i] = '120 跌破 240'
        # elif ma_dic[i]['ma_20'][-2] > inst_dic[i]['Close'][-1]:
        #     Lbuy_or_sell[i] = '減碼(長)'
        # elif ma_dic[i]['ma_60'][-2] > inst_dic[i]['Close'][-1]:
        #     Lbuy_or_sell[i] = '賣光(長)'
        # else:
        #     Lbuy_or_sell[i] = 'Long觀察'
    return short_term, mid_term, Sbuy_or_sell, Mbuy_or_sell


# %%
import requests

def line_notify(msg):
  param = {'message': msg}
  headers = {
        "Authorization": "Bearer " + 'GU4ig4X7MLzvjzVYGV7KYwWF1BvYgkQ5s42Kl2upSNY', 
        "Content-Type" : "application/x-www-form-urlencoded"
    }
  r = requests.post("https://notify-api.line.me/api/notify", headers = headers, params = param)
  
  return r.status_code

if __name__ == "__main__":
  token = 'GU4ig4X7MLzvjzVYGV7KYwWF1BvYgkQ5s42Kl2upSNY'


# %%
from collections import defaultdict

def organized_data_push():
    

    notify_params()
    dd = defaultdict(list)
    for d in (short_term, mid_term, Sbuy_or_sell, Mbuy_or_sell): # you can list as many input dicts as you want here
        for key, value in d.items():
            dd[key].append(value)

    for i in dd:
        param = '/ '.join(dd[i])
        line_notify(i.upper() + ' ' + param)

organized_data_push()


# %%
# data = yf.download(tickers='PLTR', period='1d', interval='1m')

# fig = go.Figure()
# fig.add_trace(go.Candlestick(x=data.index,
#                             open=data['Open'],
#                             high=data['High'],
#                             low=data['Low'],
#                             close=data['Close'], name = 'market data'))


# fig.update_layout(
#     title='VOO live share price evoliution',
#     yaxis_title='Stock Price'
# )

# fig.update_xaxes(
#     rangeslider_visible = True,
#     rangeselector = dict(
#         buttons = list([
#             dict(count=15, label='15m', step='minute', stepmode='backward'),
#             dict(count=45, label='45m', step='minute', stepmode='backward'),
#             dict(count=1, label='HTD', step='hour', stepmode='todate'),
#             dict(count=3, label='3h', step='hour', stepmode='backward'),
#             dict(step='all')
#         ])
#     )
# )
# fig.show()

# %% [markdown]
# 

