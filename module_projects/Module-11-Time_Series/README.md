# Background
You’re a growth analyst at MercadoLibreLinks to an external site.. With over 200 million users, MercadoLibre is the most popular e-commerce site in Latin America. You've been tasked with analyzing the company's financial and user data in clever ways to help the company grow. So, you want to find out if the ability to predict search traffic can translate into the ability to successfully trade the stock.

# View My Google Colab
https://colab.research.google.com/drive/1D_G1glE533b1JbRSR9yuTG8_Yxz2hxrS?usp=sharing

---
# Step 1: Find Unusual Patterns in Hourly Google Search Traffic

The data science manager asks if the Google search traffic for the company links to any financial events at the company. Or, does the search traffic data just present random noise? To answer this question, pick out any unusual patterns in the Google search data for the company, and connect them to the corporate financial events.

To do so, complete the following steps:

1. Read the search data into a DataFrame, and then slice the data to just the month of May 2020. (During this month, MercadoLibre released its quarterly financial results.) Use hvPlot to visualize the results. Do any unusual patterns exist?

    > ![1.1](Images/1.1.PNG)

2. Calculate the total search traffic for the month, and then compare the value to the monthly median across all months. Did the Google search traffic increase during the month that MercadoLibre released its financial results?

    > The search traffic was greater in May than the median

---
# Step 2: Mine the Search Traffic Data for Seasonality

Marketing realizes that they can use the hourly search data, too. If they can track and predict interest in the company and its platform for any time of day, they can focus their marketing efforts around the times that have the most traffic. This will get a greater return on investment (ROI) from their marketing budget.

To that end, you want to mine the search traffic data for predictable seasonal patterns of interest in the company. To do so, complete the following steps:

1. Group the hourly search data to plot the average traffic by the day of the week (for example, Monday vs. Friday).

    > ![2.1](Images/2.1.PNG)

2. Using hvPlot, visualize this traffic as a heatmap, referencing the `index.hour` as the x-axis and the `index.dayofweek` as the y-axis. 

    > ![2.2](Images/2.2.PNG)

    Does any day-of-week effect that you observe concentrate in just a few hours of that day?

    >  It looks like mostly in the morning and evening hours of the beginning of the week and very end of the week.

3. Group the search data by the week of the year. 

    > ![2.3](Images/2.3.PNG)

    Does the search traffic tend to increase during the winter holiday period (weeks 40 through 52)?

    > Yes, you can see quite an increase near the end of the year and very beginning of the year generally correlating to winter months.

---
# Step 3: Relate the Search Traffic to Stock Price Patterns

You mention your work on the search traffic data during a meeting with people in the finance group at the company. They want to know if any relationship between the search data and the company stock price exists, and they ask if you can investigate.

To do so, complete the following steps:

1. Read in and plot the stock price data. Concatenate the stock price data to the search data in a single DataFrame.

2. Market events emerged during the year of 2020 that many companies found difficult. But, after the initial shock to global financial markets, new customers and revenue increased for e-commerce platforms. Slice the data to just the first half of 2020 (`2020-01` to `2020-06` in the DataFrame), and then use hvPlot to plot the data. 

    > ![3.2](Images/3.2.PNG)

    Do both time series indicate a common trend that’s consistent with this narrative?

    > There is some similarities to be observed here.  That said there are also some significant divergence from that trend.  All together it shows at the very least a trend of activity correlated with significant rises and falls.

3. Create a new column in the DataFrame named “Lagged Search Trends” that offsets, or shifts, the search traffic by one hour. Create two additional columns:

    * “Stock Volatility”, which holds an exponentially weighted four-hour rolling average of the company’s stock volatility

    * “Hourly Stock Return”, which holds the percent change of the company's stock price on an hourly basis

4. Review the time series correlation, and then answer the following question: Does a predictable relationship exist between the lagged search traffic and the stock volatility or between the lagged search traffic and the stock price returns?

    > Yes, you can see the negative -14% correlation between volatility and searches. Additionally, it appears there's a slight positive correlation between the lagged search and hourly return +1.8%.

---

# Step 4: Create a Time Series Model with Prophet

Now, you need to produce a time series model that analyzes and forecasts patterns in the hourly search data. To do so, complete the following steps:

1. Set up the Google search data for a Prophet forecasting model.

2. After estimating the model, plot the forecast. How's the near-term forecast for the popularity of MercadoLibre?

    > ![4.2](Images/4.2.PNG)

    > Forecast indications aren't great.  There appears to be a significant decline in popularity on the horizon.

3. Plot the individual time series components of the model to answer the following questions:

    > ![4.3](Images/4.3.PNG)

    * What time of day exhibits the greatest popularity?

    > Right around midnight we see the peak in popularity, followed by a quick decline.

    * Which day of the week gets the most search traffic?

    > Tuesday appears to wield the highest search traffic.

    * What's the lowest point for search traffic in the calendar year?

    > Right around Halloween or end of October.

## Step 5 (Optional): Forecast Revenue by Using Time Series Models

A few weeks after your initial analysis, the finance group follows up to find out if you can help them solve a different problem. Your fame as a growth analyst in the company continues to grow!

Specifically, the finance group wants a forecast of the total sales for the next quarter. This will dramatically increase their ability to plan budgets and to help guide expectations for the company investors.

To do so, complete the following steps:

1. Read in the daily historical sales (that is, revenue) figures, and then apply a Prophet model to the data. The daily sales figures are quoted in millions of USD dollars.

2. Interpret the model output to identify any seasonal patterns in the company's revenue. For example, what are the peak revenue days? (Mondays? Fridays? Something else?)

3. Produce a sales forecast for the finance group. Give them a number for the expected total sales in the next quarter. Include the best- and worst-case scenarios to help them make better plans.