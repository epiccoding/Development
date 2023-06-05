import streamlit as st
import pandas as pd
import requests
import os
import sys
from openbb_terminal.stocks.stocks_helper import load

@st.cache_data
def get_close(ticker):
    # Grab closing price data
    end_date = pd.Timestamp(date.today()) + pd.DateOffset(days=1)
    start_date = pd.Timestamp(date.today()) - pd.DateOffset(months=6) # Get a little bit extra in case of weekend
    close = load(symbol=ticker, start_date=start_date, end_date=end_date)
    close_df = pd.DataFrame({'Date': close.index, 'Open': close['Open'], 'Close': close['Close']})
    close_df['Date'] = pd.to_datetime(close_df['Date']).dt.strftime('%Y-%m-%d')
    return close_df

# Streamlit app code
def main():
    st.title("News App")
    # User input Ticker symbol here
    ticker = st.sidebar.text_input(f"Enter a Ticker Symbol", value="AAPL")
    # If one selected then:
    if ticker:
        chart_df = get_close(ticker)
        if not chart_df.empty:
            current_price = chart_df['Close'].iloc[-1]
            previous_price = chart_df['Close'].iloc[-2]
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

        st.markdown(f"Fetching news for {ticker}...  While you wait, here is an inspirational quote:")
        st.markdown(f"""
            >You're only given a little spark of madness. You mustn't lose it. -**:blue[Robin Williams]**"""
        )

if __name__ == '__main__':
    main()
