import streamlit as st
#Set default streamlit layout to wide
st.set_page_config(layout="wide")

import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('dark_background')
from datetime import date, timedelta, datetime
from dateutil.relativedelta import relativedelta
from openbb_terminal.stocks.stocks_helper import load
from openbb_terminal.common.behavioural_analysis.stocktwits_model import get_bullbear
from openbb_terminal.common.feedparser_model import get_news

default_start = (date.today() - relativedelta(months=6)).strftime('%Y-%m-%d')
default_end = (date.today() + timedelta(days=1)).strftime('%Y-%m-%d')

def user_input():
    # User input to select the Ticker for the view
    ticker = st.sidebar.text_input(f"Enter a Ticker Symbol", value="AAPL")
    # Choose how many articles you want, default 25
    limit = st.sidebar.slider('How many articles?', 0, 100, 25)
    # Time logic
    start = st.sidebar.date_input("Start Date", datetime.strptime(default_start, '%Y-%m-%d').date())
    end = st.sidebar.date_input("End Date", datetime.strptime(default_end, '%Y-%m-%d').date())
    return ticker, limit, start, end

ticker, limit, start, end = user_input()

start = pd.to_datetime(start).strftime('%Y-%m-%d')
end = pd.to_datetime(end).strftime('%Y-%m-%d')

# SIDEBAR #
# Grab closing price data
close = load(symbol=ticker, start_date=start, end_date=end)
close_df = pd.DataFrame({'Date': close.index, 'Open': close['Open'], 'Close': close['Close']})
close_df['Date'] = pd.to_datetime(close_df['Date']).dt.strftime('%Y-%m-%d')

# Color coded Close Price Changer
if not close_df.empty:
    current_price = close_df['Close'].iloc[-1]
    previous_price = close_df['Close'].iloc[-2]
    price_change = current_price - previous_price
    if price_change > 0:
        color = "green"
    elif price_change < 0:
        color = "red"
    else:
        color = "black"
    st.sidebar.markdown(f"Currently: <span style='color:{color}; font-weight:bold;'>${current_price:.2f} ({price_change:.2f})</span>", unsafe_allow_html=True)
else:
    st.sidebar.write("No close price to report")

st.sidebar.line_chart(close_df["Close"])

# MAIN BODY #
st.title("Snapshot")

# Column Structure
col1, col2, col3 = st.columns([2, 1, 3])

with col1:
    st.subheader("Sentiment")
    watchlist_count, n_cases, n_bull, n_bear = get_bullbear(symbol=ticker)
    if n_cases > 0:
        st.markdown(f"\nLast {n_cases} sentiment messages:")
        st.write(f"Bullish: :green[{round(100*n_bull/n_cases, 2)}]%")
        st.write(f"Bearish: :red[{round(100*n_bear/n_cases, 2)}]%")
    else:
        st.write("No messages found")

with col3:
    st.subheader("News Articles")
    # NEWS LOGIC
    news_df = get_news(term=ticker, limit=limit)
    # Ensures date is formatted convenientlystream
    news_df['Date'] = pd.to_datetime(news_df['Date']).dt.strftime('%Y-%m-%d')
    # This will print out the captured OpenBB data
    if len(news_df) > 0:
        st.write(f"Found {len(news_df)} news articles for {ticker}:")
        st.write(news_df)
    else:
        st.write("No news articles found for the given ticker.")
