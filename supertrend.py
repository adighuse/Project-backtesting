#import libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import copy
import data_download

plt.style.use('fivethirtyeight')
plt.rcParams['figure.figsize'] = (20,10)

def get_supertrend(high, low, close, lookback, multiplier):
    # ATR

    tr1 = pd.DataFrame(high - low)
    tr2 = pd.DataFrame(abs(high - close.shift(1)))
    tr3 = pd.DataFrame(abs(low - close.shift(1)))
    frames = [tr1, tr2, tr3]
    tr = pd.concat(frames, axis=1, join='inner').max(axis=1)
    atr = tr.ewm(lookback).mean()

    # H/L AVG AND BASIC UPPER & LOWER BAND

    hl_avg = (high + low) / 2
    upper_band = (hl_avg + multiplier * atr).dropna()
    lower_band = (hl_avg - multiplier * atr).dropna()

    # FINAL UPPER BAND
    final_bands = pd.DataFrame(columns=['upper', 'lower'])
    final_bands.iloc[:, 0] = [x for x in upper_band - upper_band]
    final_bands.iloc[:, 1] = final_bands.iloc[:, 0]
    for i in range(len(final_bands)):
        if i == 0:
            final_bands.iloc[i, 0] = 0
        else:
            if (upper_band[i] < final_bands.iloc[i - 1, 0]) | (close[i - 1] > final_bands.iloc[i - 1, 0]):
                final_bands.iloc[i, 0] = upper_band[i]
            else:
                final_bands.iloc[i, 0] = final_bands.iloc[i - 1, 0]

    # FINAL LOWER BAND

    for i in range(len(final_bands)):
        if i == 0:
            final_bands.iloc[i, 1] = 0
        else:
            if (lower_band[i] > final_bands.iloc[i - 1, 1]) | (close[i - 1] < final_bands.iloc[i - 1, 1]):
                final_bands.iloc[i, 1] = lower_band[i]
            else:
                final_bands.iloc[i, 1] = final_bands.iloc[i - 1, 1]

    # SUPERTREND

    supertrend = pd.DataFrame(columns=[f'supertrend_{lookback}'])
    supertrend.iloc[:, 0] = [x for x in final_bands['upper'] - final_bands['upper']]

    for i in range(len(supertrend)):
        if i == 0:
            supertrend.iloc[i, 0] = 0
        elif supertrend.iloc[i - 1, 0] == final_bands.iloc[i - 1, 0] and close[i] < final_bands.iloc[i, 0]:
            supertrend.iloc[i, 0] = final_bands.iloc[i, 0]
        elif supertrend.iloc[i - 1, 0] == final_bands.iloc[i - 1, 0] and close[i] > final_bands.iloc[i, 0]:
            supertrend.iloc[i, 0] = final_bands.iloc[i, 1]
        elif supertrend.iloc[i - 1, 0] == final_bands.iloc[i - 1, 1] and close[i] > final_bands.iloc[i, 1]:
            supertrend.iloc[i, 0] = final_bands.iloc[i, 1]
        elif supertrend.iloc[i - 1, 0] == final_bands.iloc[i - 1, 1] and close[i] < final_bands.iloc[i, 1]:
            supertrend.iloc[i, 0] = final_bands.iloc[i, 0]

    supertrend = supertrend.set_index(upper_band.index)
    supertrend = supertrend.dropna()[1:]

    # ST UPTREND/DOWNTREND

    upt = []
    dt = []
    close = close.iloc[len(close) - len(supertrend):]

    for i in range(len(supertrend)):
        if close[i] > supertrend.iloc[i, 0]:
            upt.append(supertrend.iloc[i, 0])
            dt.append(np.nan)
        elif close[i] < supertrend.iloc[i, 0]:
            upt.append(np.nan)
            dt.append(supertrend.iloc[i, 0])
        else:
            upt.append(np.nan)
            dt.append(np.nan)

    st, upt, dt = pd.Series(supertrend.iloc[:, 0]), pd.Series(upt), pd.Series(dt)
    upt.index, dt.index = supertrend.index, supertrend.index

    return st, upt, dt


def symbols_backtesting(df_st_demo):
    all_trades = []
    #     df = pd.read_csv('st_data.csv')

    trade = {"Symbol": "Reliance", "Buy/Sell": None, "Entry": None, "Entry Date": None, "Exit": None,
             "Exit Date": None}
    # print(df)
    position = None
    for i in range(1, len(df_st_demo)):
        if (df_st_demo['Close'][i - 1] <= df_st_demo['st'][i - 1] and df_st_demo['Close'][i] > df_st_demo['st'][
            i] and position != "Buy"):
            if trade["Symbol"] is not None:
                trade["Exit"] = df_st_demo["Close"][i]
                trade["Exit Date"] = df_st_demo.index[i]
                all_trades.append(copy.deepcopy(trade))
            if position is not None:
                trade["Symbol"] = "Reliance"
                trade["Buy/Sell"] = "Buy"
                trade["Entry"] = df_st_demo["Close"][i]
                trade["Entry Date"] = df_st_demo.index[i]
            position = "Buy"
        if (df_st_demo['Close'][i - 1] >= df_st_demo['st'][i - 1] and df_st_demo['Close'][i] < df_st_demo['st'][
            i] and position != "Sell"):
            if trade["Symbol"] is not None:
                trade["Exit"] = df_st_demo["Close"][i]
                trade["Exit Date"] = df_st_demo.index[i]
                all_trades.append(copy.deepcopy(trade))
            if position is not None:
                trade["Symbol"] = "Reliance"
                trade["Buy/Sell"] = "Sell"
                trade["Entry"] = df_st_demo["Close"][i]
                trade["Entry Date"] = df_st_demo.index[i]
            position = "Sell"

    dt_st = pd.DataFrame(all_trades)
    return dt_st


def statistics(dt_st):
    symbol_list = ["Reliance"]
    #     data = symbols_backtesting(df_st_demo)
    # risk_percent = 5 / 100
    #        dt_st = pd.DataFrame(data)
    dt_st["P/L"] = np.where(dt_st["Buy/Sell"] == "Buy",
                            (100 * (dt_st["Exit"] - dt_st["Entry"]) / dt_st["Entry"]),
                            (100 * (dt_st["Entry"] - dt_st["Exit"]) / dt_st["Entry"]))
    dt_st = dt_st[dt_st["Buy/Sell"] == "Buy"].reset_index(drop=True)

    dt_st["Probability"] = 100 * (np.where(dt_st["P/L"] > 0, 1, 0).cumsum()) / (
        np.where(dt_st["P/L"] != np.NaN, 1, 0).cumsum())
    dt_st["Return"] = dt_st["P/L"].cumsum()
    dt_st["Drawdown"] = dt_st["Return"] - (dt_st["Return"].cummax().apply(lambda x: x if x > 0 else 0))
    dt_st.to_csv('final_st.csv', )

    return dt_st

def cumulative_profit(dt_st):
    # calculating equity column
    dt_st['equity']=10000
    for i in range(len(dt_st)):
        temp=(dt_st['equity'][i]*dt_st['Return'][i])/100
        dt_st['equity'][i]=dt_st['equity'][i]+temp

    # # changing date type
    for col in dt_st.columns:
        if dt_st[col].dtype == '<M8[ns]':
            dt_st[col] = dt_st[col].dt.date
    # dt_st1 = dt_st.set_index('Entry Date')

    return dt_st

def display_result():
    # df_st_demo=pd.read_pickle('reliance.pkl')
    # data_download.get_data("Re")
    df_st_demo = data_download.get_data("RELIANCE.NS")
    df_st_demo['st'],df_st_demo['upt'],df_st_demo['dt']=get_supertrend(high=df_st_demo['High'], low=df_st_demo['Low'], close=df_st_demo['Close'],lookback=10, multiplier=3)
    df_st_demo=symbols_backtesting(df_st_demo)
    basic_stats_df = statistics(df_st_demo)
    detail_stats= cumulative_profit(basic_stats_df)
    return detail_stats