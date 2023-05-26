import streamlit as st
import pandas as pd
from newspaper import Article
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from openbb_terminal.sdk import openbb

@st.cache_data

# Function to fetch and summarize news articles
def fetch_and_summarize_news(ticker):
    # Fetch news articles using OpenBB
    news = openbb.news(term=ticker, sort="published")
    df = pd.DataFrame({'Term': ticker, 'Title': news['title'], 'Date': news['published'], 'Link': news['link']})
    df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%Y-%m-%d')

    return df

# Streamlit app code
def main():
    st.title("News Summarizer")

    # Get user input for ticker symbol
    ticker = st.sidebar.text_input("Enter a Ticker Symbol")

    if ticker:
        st.write(f"Fetching and summarizing news articles for {ticker}...  This may take a minute.")

        st.write(f"While you wait, here is an inspirational quote:")
        st.write(f"You're only given a little spark of madness. You mustn't lose it. -Robin Williams")

        # Fetch and summarize news articles
        news_df = fetch_and_summarize_news(ticker)

        if not news_df.empty:
            st.write(f"Found {len(news_df)} news articles for {ticker}:")
            st.dataframe(news_df['Title'])
        else:
            st.write("No news articles found for the given ticker.")

if __name__ == '__main__':
    main()
