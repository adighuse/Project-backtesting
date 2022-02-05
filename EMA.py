# importing libraries
import yfinance as yf
import pandas as pd
import copy
import ta
import numpy as np
import data_download

def symbols_backtesting(data):
    all_trades = []
    df = pd.read_pickle('reliance.pkl')
    df['ema_9'] = ta.trend.EMAIndicator(df['Close'], window=9, fillna=True).ema_indicator()
    df['ema_26'] = ta.trend.EMAIndicator(df['Close'], window=26, fillna=True).ema_indicator()
    trade = {"Symbol": "Reliance", "Buy/Sell": None, "Entry": None, "Entry Date": None, "Exit": None,
                 "Exit Date": None}
    position = None
    for i in df.index:
        if (df["ema_9"][i] > df["ema_26"][i] and position != "Buy"):
            if trade["Symbol"] is not None:
                trade["Exit"] = (df["Close"][i] - (df["Close"][i] * 5) / 100 or df["Close"][i])
                trade["Exit Date"] = i
                all_trades.append(copy.deepcopy(trade))
            if position is not None:
                trade["Symbol"] = "Reliance"
                trade["Buy/Sell"] = "Buy"
                trade["Entry"] = df["Close"][i]
                # trade['SL'] = df["Close"][i] - (df["Close"][i] * 5) / 100
                trade["Entry Date"] = i
            position = "Buy"
        if (df["ema_9"][i] < df["ema_26"][i] and position != "Sell"):
            if trade["Symbol"] is not None:
                trade["Exit"] = df["Close"][i]
                trade["Exit Date"] = i
                all_trades.append(copy.deepcopy(trade))
            if position is not None:
                trade["Symbol"] = "Reliance"
                trade["Buy/Sell"] = "Sell"
                # trade['SL'] = df["Close"][i] + (df["Close"][i] * 5) / 100
                trade["Entry"] = df["Close"][i]
                trade["Entry Date"] = i
            position = "Sell"
    return all_trades


def statistics(data):
    symbol_list = ["Reliance"]
    data = symbols_backtesting(symbol_list)
    if data:
       # risk_percent = 5 / 100
       df = pd.DataFrame(data)
       df["P/L"] = np.where(df["Buy/Sell"] == "Buy",
                         (100 * (df["Exit"] - df["Entry"]) / df["Entry"]),
                         (100 * (df["Entry"] - df["Exit"]) / df["Entry"]))
       df = df[df["Buy/Sell"] == "Buy"].reset_index(drop=True)

       df["Probability"] = 100 * (np.where(df["P/L"] > 0, 1, 0).cumsum()) / (
        np.where(df["P/L"] != np.NaN, 1, 0).cumsum())
       df["Return"] = df["P/L"].cumsum()
       df["Drawdown"] = df["Return"] - (df["Return"].cummax().apply(lambda x: x if x > 0 else 0))
       df.to_csv('final.csv', )

#     st.dataframe(df)
    else:
        print("No Trades")
    return df

def cumulative_profit(df):
    # calculating equity column
    df['equity']=10000
    for i in range(len(df)):
        temp=(df['equity'][i]*df['Return'][i])/100
        df['equity'][i]=df['equity'][i]+temp
        print(df['equity'][i])
    # changing data type from datetypeindex to date
    for col in df.columns:
        if df[col].dtype == '<M8[ns]':
            df[col] = df[col].dt.date
    # df.set_index('Entry Date',inplace=True)
    print("Finished")
    return df


def display_result():
    data=data_download.get_data("RELIANCE.NS")
    data=symbols_backtesting(data)
    basic_stats=statistics(data)
    detail_stats=cumulative_profit(basic_stats)
    return detail_stats