import streamlit as st
import os
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('dark_background')

# Various Datetime Conveniences
from datetime import date, timedelta, datetime
from dateutil.relativedelta import relativedelta

# OpenBB Import Cluster
from openbb_terminal.stocks.stocks_helper import load
from openbb_terminal.common.feedparser_model import get_news

# Begin Code #
# Set default streamlit layout to wide
st.set_page_config(
        page_title="OpenBB [P3]",
        page_icon="coin",
        layout="wide",
)

def user_input():
    # User input to select the Ticker for the view
    ticker = st.sidebar.text_input(f"Enter a Ticker Symbol", value="AAPL")
    # Choose how many articles you want, default 25
    limit = st.sidebar.slider('How many articles?', 0, 100, 25)
    # Time logic
    default_start = (date.today() - relativedelta(months=6)).strftime('%Y-%m-%d')
    default_end = (date.today() + timedelta(days=1)).strftime('%Y-%m-%d')
    start = st.sidebar.date_input("Start Date", datetime.strptime(default_start, '%Y-%m-%d').date())
    end = st.sidebar.date_input("End Date", datetime.strptime(default_end, '%Y-%m-%d').date())
    return ticker, limit, start, end

ticker, limit, start, end = user_input()

start = pd.to_datetime(start).strftime('%Y-%m-%d')
end = pd.to_datetime(end).strftime('%Y-%m-%d')

# SIDEBAR #
with st.sidebar:
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
        st.markdown(f"Currently: <span style='color:{color}; font-weight:bold;'>${current_price:.2f} ({price_change:.2f})</span>", unsafe_allow_html=True)
    else:
        st.write("No close price to report")
    # Simple line chart for the "Close" in our Load
    st.line_chart(close_df["Close"])

# MAIN BODY #
# New Segment
st.subheader("News Articles")
# NEWS LOGIC
news_df = get_news(term=ticker, limit=limit)
# Ensures date is formatted convenientlystream
news_df['Date'] = pd.to_datetime(news_df['Date']).dt.strftime('%Y-%m-%d')
news_df = news_df.set_index('Date')
# This will print out the captured OpenBB data
if len(news_df) > 0:
    st.write(f"Found {len(news_df)} news articles for {ticker}:")
    st.write(news_df)
else:
    st.write("No news articles found for the given ticker.")