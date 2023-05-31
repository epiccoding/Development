import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date
from datetime import datetime
from openbb_terminal.sdk import openbb

@st.cache_data

# This will use OpenBB to fetch 100 news articles in GoogleNews using the ticker entered
def get_news(ticker):
    # OpenBB calling code for news
    news = openbb.news(term=ticker, sort="published")
    # Creates a Pandas dataframe for the elements captured by OpenBB
    news_df = pd.DataFrame({'Term': ticker, 'Title': news['title'], 'Date': news['published'], 'Link': news['link']})
    # Ensures date is formatted conveniently
    news_df['Date'] = pd.to_datetime(news_df['Date']).dt.strftime('%Y-%m-%d')
    return news_df

def get_close(ticker):
    # Grab closing price data
    end_date = pd.Timestamp(date.today()) + pd.DateOffset(days=1)
    start_date = pd.Timestamp(date.today()) - pd.DateOffset(months=6) # Get a little bit extra in case of weekend
    close = openbb.stocks.load(symbol=ticker, start_date=start_date, end_date=end_date)
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
            fig, ax = plt.subplots()
            chart_df.plot(x='Date', y='Close', ax=ax)
            ax.set_title(f"{ticker} 6 Month Close Price")
            ax.set_xlabel("Date")
            ax.set_ylabel("Close")
            st.sidebar.pyplot(fig)
            current_price = chart_df['Close'].iloc[-1]
            previous_price = chart_df['Close'].iloc[-2]
            price_change = current_price - previous_price

            if price_change > 0:
                color = "green"
            elif price_change < 0:
                color = "red"
            else:
                color = "black"

            st.sidebar.markdown(f"The current Close Price is: <span style='color:{color}; font-weight:bold;'>${current_price:.2f}</span>", unsafe_allow_html=True)
        else:
            st.sidebar.write("No close price to report")

        st.markdown(f"Fetching news for {ticker}...  While you wait, here is an inspirational quote:")
        st.markdown(f"""
            >You're only given a little spark of madness. You mustn't lose it. -**:blue[Robin Williams]**"""
        )

        # This will print out the captured OpenBB data
        news_df = get_news(ticker)
        if len(news_df) > 0:
            st.write(f"Found {len(news_df)} news articles for {ticker}:")
            st.write(news_df[['Date', 'Title', 'Link']])
        else:
            st.write("No news articles found for the given ticker.")

if __name__ == '__main__':
    main()
