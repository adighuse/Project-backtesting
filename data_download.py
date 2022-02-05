import yfinance as yf

# Downloading data from yfinance
def get_data(tick_name):
    # tick="RELIANCE.NS"
    reliance=yf.download(tick_name)
    reliance=reliance.tail(1000)
    reliance=reliance.iloc[:,:-2]
    reliance.to_pickle("reliance.pkl")
    return reliance
data=get_data("RELIANCE.NS")