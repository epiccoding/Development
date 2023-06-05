import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('dark_background')
from datetime import date
from openbb_terminal.stocks.stocks_helper import load
from openbb_terminal.common.feedparser_model import get_news

@st.cache_data
def news(ticker):
    # OpenBB calling code for news
    news_df = get_news(term=ticker, limit=50)
    # Ensures date is formatted conveniently
    news_df['Date'] = pd.to_datetime(news_df['Date']).dt.strftime('%Y-%m-%d')
    return news_df

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

            st.sidebar.markdown(f"**6 Month Close Price**")
            fig, ax = plt.subplots()
            chart_df.plot(x='Date', y='Close', ax=ax)
            ax.set_xlabel("")
            ax.set_ylabel("")
            plt.xticks([])
            st.sidebar.pyplot(fig)

        else:
            st.sidebar.write("No close price to report")

        st.markdown(f"Fetching news for {ticker}...  While you wait, here is an inspirational quote:")
        st.markdown(f"""
            >You're only given a little spark of madness. You mustn't lose it. -**:blue[Robin Williams]**"""
        )

        # This will print out the captured OpenBB data
        news_df = news(ticker)
        if len(news_df) > 0:
            st.write(f"Found {len(news_df)} news articles for {ticker}:")
            st.write(news_df)
        else:
            st.write("No news articles found for the given ticker.")

if __name__ == '__main__':
    main()
