# importing neccessary libraries
import streamlit as st
import EMA
import metrics
import supertrend
# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    menu=["Strategy Backtest","Conclusion"]
    choice=st.sidebar.selectbox("Menu",menu)
    if choice=="Strategy Backtest":
        st.title('Strategy backtesting')
        option = st.selectbox("Which strategy you would like to backtest", ("EMA(9,26)", "SUPERTREND(10,3)"))
        if (option=="EMA(9,26)"):
            st.dataframe(EMA.display_result())
            st.subheader("Trading summary")
            metric_1, metric_2, metric_3, metric_4 = st.columns(4)
            metric_1.metric("Total Trades",EMA.display_result().shape[0])
            metric_2.metric("Successful Trades",metrics.succefull_trades(EMA.display_result()))
            metric_3.metric("Failed Trades",metrics.failed_trades(EMA.display_result()))
            metric_4.metric("% Profitable","%.2f" %metrics.percent_profitable(EMA.display_result()))
            metric_5, metric_6, metric_7,metric_8 = st.columns(4)
            metric_5.metric("Average Trade net profit","%.2f" %metrics.Average_trade_profit("EMA(9,26)", EMA.display_result()))
            metric_6.metric("Profit %","%.2f" %metrics.profit_percentage(EMA.display_result()))
            metric_7.metric("Maximum Drawdown","%.2f" % metrics.max_drawdown(EMA.display_result()))
            metric_8.metric("CAGR", "%.2f" % metrics.CAGR(EMA.display_result()))
            st.subheader("Equity curve")
            a=EMA.display_result().set_index('Entry Date')
            st.line_chart(a['equity'])
            st.subheader("Max Drawdown")
            st.line_chart(a['Drawdown'])
            st.text("")
            st.text("Profit gained from the EMA(9,26) strategy by investing 10k in RELIANCE : 9908")
            st.text("Profit percentage of the EMA(9,26) strategy : 99%")


        if(option=="SUPERTREND(10,3)"):
            st.dataframe(supertrend.display_result())
            st.subheader("Trading summary")
            metric_1,metric_2,metric_3,metric_4=st.columns(4)
            metric_1.metric("Total Trades", supertrend.display_result().shape[0])
            metric_2.metric("Successful Trades",metrics.succefull_trades(supertrend.display_result()))
            metric_3.metric("Failed Trades",metrics.failed_trades(supertrend.display_result()))
            metric_4.metric("% Profitable:","%.2f" %metrics.percent_profitable(supertrend.display_result()))
            metric_5, metric_6, metric_7,metric_8 = st.columns(4)
            metric_5.metric("Average Trade net profit:","%.2f" %metrics.Average_trade_profit('SUPERTREND(10,3)',supertrend.display_result()))
            metric_6.metric("profit %","%.2f" % metrics.profit_percentage(supertrend.display_result()))
            metric_7.metric("Maximum Drawdown","%.2f" %metrics.max_drawdown(supertrend.display_result()))
            metric_8.metric("CAGR","%.2f" %metrics.CAGR(supertrend.display_result()))

            st.subheader("Equity curve")
            a = supertrend.display_result().set_index('Entry Date')
            st.line_chart(a['equity'])
            st.subheader("Max Drawdown")
            st.line_chart(a['Drawdown'])
            st.text("")
            st.write("Profit gained from the Supertrend(10,3) strategy by investing 10k in RELIANCE : 10843")
            st.write("Profit percentage of the Supertrend(10,3) strategy : 108%")

    if choice=="Conclusion":
        st.header('Conclusion')
        st.text("With a Profit Percentage of 108% of SUPERTREND(10,3) over profit percentage")
        st.text(" of 99% of EMA(9,26)and also with higher CAGR of 20% over 19% of EMA(9,26)")
        st.text("We can preferred SUPERTREND(10,3) over EMA(9,26)")