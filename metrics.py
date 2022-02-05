
def percent_profitable(dataframe):
    total_trades=dataframe.shape[0]
    wining_trades=0
    for i in dataframe.index:
#     print(i)
#     wining_trades=0
        if dataframe['P/L'][i]>0:
#         print(output['P/L'][i])
            wining_trades=wining_trades+1
    Percent_profitable=wining_trades/total_trades
    print("Percent Profitable",Percent_profitable)
    return Percent_profitable*100


def Average_trade_profit(indicator,dataframe):
    invested_amount=10000
    if indicator=='SUPERTREND(10,3)':
        total_profit=20971
    if indicator=='EMA(9,26)':
        total_profit=19908
    total_net_profit= total_profit-invested_amount
    print(dataframe['equity'][1])
    total_trades=dataframe.shape[0]
    Average_trade_net_profit=total_net_profit/total_trades
    return Average_trade_net_profit

def succefull_trades(dataframe):
    wining_trades = 0
    for i in dataframe.index:
        if dataframe['P/L'][i] > 0:
           wining_trades = wining_trades + 1
    return wining_trades

def failed_trades(dataframe):
    failed_trades=0
    for i in dataframe.index:
        if dataframe['P/L'][i] < 0:
            failed_trades = failed_trades + 1
    return failed_trades

def profit_percentage(dataframe):
    investment_value=10000
    total_investment_return = dataframe['P/L'].cumsum().tail(1)
    profit_perc=(total_investment_return/investment_value)*100
    return profit_perc

def max_drawdown(dataframe):
    drawdown=dataframe['Drawdown'].min()
    return drawdown

def CAGR(dataframe):
    periods=4
    invested_value=10000
    current_investment_value = dataframe['equity'].tail(1)
    cagr=(current_investment_value/invested_value) ** (1 / periods) - 1
    return cagr