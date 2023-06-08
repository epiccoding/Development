import streamlit as st
import os
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('dark_background')

# Various Datetime Conveniences
from datetime import date, timedelta, datetime
from dateutil.relativedelta import relativedelta

# OpenBB Import Cluster
from openbb_terminal.keys_model import set_finnhub_key
from openbb_terminal.stocks.stocks_helper import load
from openbb_terminal.stocks.options.options_sdk_helper import get_full_option_chain
from openbb_terminal.stocks.comparison_analysis.sdk_helpers import get_similar
from openbb_terminal.stocks.fundamental_analysis.finnhub_model import get_rating_over_time
from openbb_terminal.common.behavioural_analysis.stocktwits_model import get_bullbear
from openbb_terminal.common.feedparser_model import get_news

os.environ["API_FINNHUB_KEY"] = st.secrets["API_FINNHUB_KEY"]
API_FINNHUB_KEY = st.secrets["API_FINNHUB_KEY"]

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
# Header
col1, col2 = st.columns([4, 1])
with col1:
    st.title("Snapshot")

with col2:
    st.markdown("[![github](https://img.icons8.com/?size=128&id=52539&format=png)](https://github.com/epiccoding/Bootcamp)")
st.markdown("---")

# Main Content
col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    # Sentiment, what would I be without it?
    st.subheader("Sentiment")
    watchlist_count, n_cases, n_bull, n_bear = get_bullbear(symbol=ticker)
    if n_cases > 0:
        st.markdown(f"\nLast {n_cases} sentiment messages:")
        st.write(f"Bullish: :green[{round(100*n_bull/n_cases, 2)}]%")
        st.write(f"Bearish: :red[{round(100*n_bear/n_cases, 2)}]%")
    else:
        st.write("No messages found")

    # Found the ratings feature to be an interesting way to incorporate additional sentiment around the stock
    set_finnhub_key(key=API_FINNHUB_KEY, persist = True)
    rating_df = get_rating_over_time(symbol=ticker).set_index('period')
    most_recent_month = rating_df.index.max()
    form_date = datetime.fromisoformat(most_recent_month)
    formatted_date = form_date.strftime('%B %Y')
    st.subheader(f"As of {formatted_date}")
    recent_rating_df = rating_df.loc[most_recent_month].reset_index()
    valid_columns = recent_rating_df.select_dtypes(include='number').columns
    recent_rating_df['count'] = recent_rating_df[valid_columns].sum(axis=1)
    recent_rating_df['date'] = most_recent_month
    recent_rating_df = recent_rating_df.rename(columns={'index':'rating'})
    print_ratings_df = pd.DataFrame(recent_rating_df[['rating','count']].set_index('rating'))
    print_ratings_df
    
with col2:
    # OpenBB has a list of the option contracts and the openInterest around it
    st.subheader("Options")
    options = get_full_option_chain(symbol=ticker)
    options.sort_values("volume", inplace=True, ascending=False)
    options

with col3:
    # This function specifically utilizes the Finnhub API to provide similar companies to the highlighted
    # In full transparency I am skeptical of the listed companies to the companies I investigated
    st.subheader("Similar Companies")
    similar = get_similar(symbol=ticker, source="Finnhub")
    similar

st.markdown('''---''')

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