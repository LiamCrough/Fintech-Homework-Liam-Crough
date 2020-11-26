#!/usr/bin/env python
# coding: utf-8

#  #  A Whale off the Port(folio)
#  ---
# 
#  In this assignment, you'll get to use what you've learned this week to evaluate the performance among various algorithmic, hedge, and mutual fund portfolios and compare them against the S&P TSX 60 Index.

# In[1]:


# Initial imports
import pandas as pd
import numpy as np
import datetime as dt
from pathlib import Path
import seaborn as sn

get_ipython().run_line_magic('matplotlib', 'inline')


# # Data Cleaning
# 
# In this section, you will need to read the CSV files into DataFrames and perform any necessary data cleaning steps. After cleaning, combine all DataFrames into a single DataFrame.
# 
# Files:
# 
# * `whale_returns.csv`: Contains returns of some famous "whale" investors' portfolios.
# 
# * `algo_returns.csv`: Contains returns from the in-house trading algorithms from Harold's company.
# 
# * `sp_tsx_history.csv`: Contains historical closing prices of the S&P TSX 60 Index.

# ## Whale Returns
# 
# Read the Whale Portfolio daily returns and clean the data

# In[2]:


# Reading whale returns
whale_returns_data = Path("Resources/whale_returns.csv")

whale_returns_dataframe = pd.read_csv(whale_returns_data, index_col = "Date", parse_dates=True, infer_datetime_format=True )

whale_returns_dataframe.head(15)


# In[3]:


# Count nulls

whale_returns_dataframe.isnull().sum()


# In[4]:


# Drop nulls
whale_returns_dataframe.dropna(inplace=True)
whale_returns_dataframe.isnull().sum()


# # Algorithmic Daily Returns
# 
# 

# In[5]:


# Reading algorithmic returns
algo_returns_data = Path("Resources/algo_returns.csv")

algo_returns_dataframe = pd.read_csv(algo_returns_data, index_col = "Date", parse_dates=True, infer_datetime_format=True)

algo_returns_dataframe.sort_index(ascending = True, inplace = True)

algo_returns_dataframe.head(100)


# In[6]:


# Count nulls
algo_returns_dataframe.isnull().sum()


# In[7]:


# Drop nulls
algo_returns_dataframe.dropna(inplace = True)

algo_returns_dataframe.head()


# ## S&P TSX 60 Returns
# 
# Read the S&P TSX 60 historic closing prices and create a new daily returns DataFrame from the data. 

# In[8]:


# Reading S&P TSX 60 Closing Prices
sp_tsx_history = Path("Resources/sp_tsx_history.csv")

sp_tsx_dataframe = pd.read_csv(sp_tsx_history, index_col="Date", parse_dates=True, infer_datetime_format=True)

sp_tsx_dataframe.head(15)


# In[9]:


# Check Data Types
sp_tsx_dataframe.dtypes


# In[10]:


# Fix Data Types
sp_tsx_dataframe["Close"] = sp_tsx_dataframe["Close"].str.replace("$", "")
sp_tsx_dataframe["Close"] = sp_tsx_dataframe["Close"].str.replace(",", "")


sp_tsx_dataframe["Close"].dtype


# In[11]:


sp_tsx_dataframe["Close"] = sp_tsx_dataframe["Close"].astype('float')
sp_tsx_dataframe["Close"].dtype


# In[12]:


# Calculate Daily Returns
sp_tsx_daily_returns = sp_tsx_dataframe.pct_change() 
sp_tsx_daily_returns


# In[13]:


# Drop nulls
sp_tsx_daily_returns.dropna(inplace = True)
sp_tsx_daily_returns.head()


# In[14]:


sp_tsx_daily_returns.isnull().sum()


# In[15]:


# Rename `Close` Column to be specific to this portfolio.
sp_tsx_daily_returns.columns = ['SP_TSX']
sp_tsx_daily_returns


# ## Combine Whale, Algorithmic, and S&P TSX 60 Returns

# In[16]:


# Join Whale Returns, Algorithmic Returns, and the S&P TSX 60 Returns into a single DataFrame with columns for each portfolio's returns.
Combined_Returns_Dataframe = pd.concat([whale_returns_dataframe, algo_returns_dataframe, sp_tsx_daily_returns], axis = 'columns', join = 'inner')
Combined_Returns_Dataframe


# ---

# # Conduct Quantitative Analysis
# 
# In this section, you will calculate and visualize performance and risk metrics for the portfolios.

# ## Performance Anlysis
# 
# #### Calculate and Plot the daily returns.

# In[17]:


# Plot daily returns of all portfolios
Combined_Returns_Dataframe.plot(figsize = (20,10))


# #### Calculate and Plot cumulative returns.

# In[108]:


# Calculate cumulative returns of all portfolios
Cumulative_Returns = (1+ Combined_Returns_Dataframe).cumprod()
# Plot cumulative returns
Cumulative_Returns.plot(figsize = (20,10))


# In[ ]:





# ---

# ## Risk Analysis
# 
# Determine the _risk_ of each portfolio:
# 
# 1. Create a box plot for each portfolio. 
# 2. Calculate the standard deviation for all portfolios
# 4. Determine which portfolios are riskier than the S&P TSX 60
# 5. Calculate the Annualized Standard Deviation

# ### Create a box plot for each portfolio
# 

# In[19]:


# Box plot to visually show risk
Combined_Returns_Dataframe.plot(kind = 'box', legend = True, figsize = (20,10))


# ### Calculate Standard Deviations

# In[20]:


# Calculate the daily standard deviations of all portfolios
df_daily_std = pd.DataFrame(Combined_Returns_Dataframe.std()).rename(columns = {0: "Standard_Deviation"})
df_daily_std.index.name = "Fund_Name"
df_daily_std


# ### Determine which portfolios are riskier than the S&P TSX 60

# In[101]:


# Calculate the daily standard deviation of S&P TSX 60

# Determine which portfolios are riskier than the S&P TSX 60
df_daily_std["Standard_Deviation"] = df_daily_std["Standard_Deviation"].astype('float')

df_daily_std["Standard_Deviation"].dtype

Risk_Analysis = df_daily_std[df_daily_std["Standard_Deviation"] > df_daily_std.loc["SP_TSX", "Standard_Deviation"]]

print(Risk_Analysis)
print("--------------------------------")             
print("All Funds within this dataframe have more risk than the S&P TSX 60 due to a higher standard deviation. See description above")



# ### Calculate the Annualized Standard Deviation

# In[22]:


# Calculate the annualized standard deviation (252 trading days)
Annualized_Standard_Deviation = df_daily_std*np.sqrt(252)

Annualized_Standard_Deviation = pd.DataFrame(Annualized_Standard_Deviation['Standard_Deviation'])


Annualized_Standard_Deviation


# ---

# ## Rolling Statistics
# 
# Risk changes over time. Analyze the rolling statistics for Risk and Beta. 
# 
# 1. Calculate and plot the rolling standard deviation for the S&P TSX 60 using a 21-day window
# 2. Calculate the correlation between each stock to determine which portfolios may mimick the S&P TSX 60
# 3. Calculate and plot a 60-day Beta for Berkshire Hathaway Inc compared to the S&P 60 TSX

# ### Calculate and plot rolling `std` for all portfolios with 21-day window

# In[23]:


# Calculate the rolling standard deviation for all portfolios using a 21-day window
Rolling_Standard_Deviation = Combined_Returns_Dataframe.rolling(window = 21).std()

Rolling_Standard_Deviation_Dataframe = pd.DataFrame(Rolling_Standard_Deviation)

Rolling_Standard_Deviation_Dataframe


# In[24]:


# Plot the rolling standard deviation
Rolling_Standard_Deviation.plot(figsize = (25,10))


# ### Calculate and plot the correlation

# In[104]:


# Calculate the correlation
Correlation = pd.DataFrame(Combined_Returns_Dataframe.corr())
#Display the Correlation Matrix
Correlation


# In[ ]:





# ### Calculate and Plot Beta for a chosen portfolio and the S&P 60 TSX

# In[105]:


# Calculate covariance of a single portfolio
Covariance_BerkshireHathaway = Combined_Returns_Dataframe['BERKSHIRE HATHAWAY INC'].cov(Combined_Returns_Dataframe['SP_TSX'])

print(f"The Covariance of Berkshire Hathaway compared to the S&P is {Covariance_BerkshireHathaway}")

# Calculate variance of S&P TSX
Variance_TSX = Combined_Returns_Dataframe['SP_TSX'].var()
print(f"The Variance of the S&P is {Variance_TSX}")


# In[84]:


# Computing beta
Rolling_Covariance = Combined_Returns_Dataframe['BERKSHIRE HATHAWAY INC'].rolling(window = 60).cov(Combined_Returns_Dataframe['SP_TSX'])
Rolling_Variance = Combined_Returns_Dataframe['SP_TSX'].rolling(window = 60).var()


# In[86]:


Rolling_Beta = Rolling_Covariance / Rolling_Variance

Rolling_Beta.plot(figsize = (20,10), title = "60 Day Rolling Beta")
# Plot beta trend


# ## Rolling Statistics Challenge: Exponentially Weighted Average 
# 
# An alternative way to calculate a rolling window is to take the exponentially weighted moving average. This is like a moving window average, but it assigns greater importance to more recent observations. Try calculating the [`ewm`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.ewm.html) with a 21-day half-life.

# In[28]:


# Use `ewm` to calculate the rolling window
Exponential_Weighted_Average = Combined_Returns_Dataframe.ewm(span = 21).mean()
(1+Exponential_Weighted_Average).cumprod().plot(figsize = (20,10))


# ---

# # Sharpe Ratios
# In reality, investment managers and thier institutional investors look at the ratio of return-to-risk, and not just returns alone. After all, if you could invest in one of two portfolios, and each offered the same 10% return, yet one offered lower risk, you'd take that one, right?
# 
# ### Using the daily returns, calculate and visualize the Sharpe ratios using a bar plot

# In[29]:


# Annualized Sharpe Ratios
Sharpe_Ratio = Combined_Returns_Dataframe.mean() / Combined_Returns_Dataframe.std()


# In[30]:


# Visualize the sharpe ratios as a bar plot
Sharpe_Ratio.plot(kind = 'bar')


# ### Determine whether the algorithmic strategies outperform both the market (S&P TSX 60) and the whales portfolios.
# 
# The first algorithmic strategy (algo 1) outperforms the market and all of the whales portfolios in terms of returns as well as risk aversion, as evident by the returns accompanied by the sharpe ratios as a technical indicator. 
# 
# Algorithm 2 (algo 2) has a slightly lower sharpe ratio and as per the most recent data, did not outperform Berkshire Hathaway in terms of returns. Whilst it was able to beat the market in terms of risk and returns, Berkshire Hathaway appeares to be a superior choice for investment due to their lower levels of risk and higher returns than algo 2.

# ---

# # Create Custom Portfolio
# 
# In this section, you will build your own portfolio of stocks, calculate the returns, and compare the results to the Whale Portfolios and the S&P TSX 60. 
# 
# 1. Choose 3-5 custom stocks with at last 1 year's worth of historic prices and create a DataFrame of the closing prices and dates for each stock.
# 2. Calculate the weighted returns for the portfolio assuming an equal number of shares for each stock
# 3. Join your portfolio returns to the DataFrame that contains all of the portfolio returns
# 4. Re-run the performance and risk analysis with your portfolio to see how it compares to the others
# 5. Include correlation analysis to determine which stocks (if any) are correlated

# ## Choose 3-5 custom stocks with at last 1 year's worth of historic prices and create a DataFrame of the closing prices and dates for each stock.
# 
# For this demo solution, we fetch data from three companies listes in the S&P TSX 60 index.
# 
# * `SHOP` - [Shopify Inc](https://en.wikipedia.org/wiki/Shopify)
# 
# * `OTEX` - [Open Text Corporation](https://en.wikipedia.org/wiki/OpenText)
# 
# * `L` - [Loblaw Companies Limited](https://en.wikipedia.org/wiki/Loblaw_Companies)

# In[31]:


# Reading data from 1st stock
Shopify = pd.read_csv(Path("Resources/shop_historical.csv"), parse_dates = True, index_col = "Date", infer_datetime_format = True)
Shopify.rename(columns = {"Close" : 'Shopify'}, inplace = True)

Shopify = Shopify.drop(['Symbol'], axis = 1)

Shopify


# In[32]:


# Reading data from 2nd stock
Open_Text_Corporation = pd.read_csv(Path("Resources/otex_historical.csv"), index_col = "Date", parse_dates = True, infer_datetime_format = True)
Open_Text_Corporation.rename(columns = {'Close' : 'Open_Text_Corporation'}, inplace = True)
Open_Text_Corporation = Open_Text_Corporation.drop(['Symbol'], axis = 1)

Open_Text_Corporation


# In[33]:


# Reading data from 3rd stock
Loblaw_Companies = pd.read_csv(Path("Resources/l_historical.csv"), parse_dates = True, index_col = "Date", infer_datetime_format = True)
Loblaw_Companies = Loblaw_Companies.rename(columns = {"Close" : "LobLaw Companies"})

Loblaw_Companies = Loblaw_Companies.drop(["Symbol"], axis = 1)
Loblaw_Companies


# In[34]:


# Combine all stocks in a single DataFrame
Stock_Portfolio = pd.DataFrame(pd.concat((Shopify, Open_Text_Corporation, Loblaw_Companies), axis = 1, join = "inner"))
Stock_Portfolio.sort_index(ascending = True, inplace = True)
Stock_Portfolio


# In[ ]:





# In[ ]:


# Reorganize portfolio data by having a column per symbol


# In[35]:


# Calculate daily returns
Stock_Portfolio_Returns = Stock_Portfolio.pct_change()
# Drop NAs
Stock_Portfolio.dropna(inplace = True)

# Display sample data

Stock_Portfolio_Returns


# ## Calculate the weighted returns for the portfolio assuming an equal number of shares for each stock

# In[121]:


# Set weights
weights = [1/3, 1/3, 1/3]

# Calculate portfolio return
Weighted_Portfolio = Stock_Portfolio_Returns.dot(weights)
Weighted_Portfolio_Returns = Weighted_Portfolio.pct_change()
Weighted_Portfolio_Returns.dropna(inplace = True)


# Display sample data
Weighted_Portfolio_Returns = pd.DataFrame(Weighted_Portfolio_Returns)
Weighted_Portfolio_Returns = Weighted_Portfolio_Returns.rename(columns = {0:'Custom Portfolio'})
Weighted_Portfolio_Returns


# ## Join your portfolio returns to the DataFrame that contains all of the portfolio returns

# In[40]:


# Join your returns DataFrame to the original returns DataFrame
All_Portfolio_Returns = pd.concat((Weighted_Portfolio_Returns, Combined_Returns_Dataframe), axis = 1, join = 'inner')


All_Portfolio_Returns


# In[53]:


# Only compare dates where return data exists for all the stocks (drop NaNs)
All_Portfolio_Returns.dropna(inplace = True)


# ## Re-run the risk analysis with your portfolio to see how it compares to the others

# ### Calculate the Annualized Standard Deviation

# In[119]:


# Calculate the annualized `std`
All_Portfolio_Standard_Deviation = pd.DataFrame(All_Portfolio_Returns.std())

Annualized_Portfolio_Standard_Deviation = All_Portfolio_Standard_Deviation*np.sqrt(252)
Annualized_Portfolio_Standard_Deviation = Annualized_Portfolio_Standard_Deviation.rename(columns = {0:'Standard Deviation'})

Annualized_Portfolio_Standard_Deviation


# ### Calculate and plot rolling `std` with 21-day window

# In[126]:


# Calculate rolling standard deviation
All_Portfolio_Rolling_Standard_Deviation = All_Portfolio_Returns.rolling(window = 21).std()

# Plot rolling standard deviation
All_Portfolio_Rolling_Standard_Deviation.plot(figsize = (20,10), title = "Rolling Standard Deviations")


# ### Calculate and plot the correlation

# In[91]:


# Calculate and plot the correlation

Correlation_All = pd.DataFrame(All_Portfolio_Returns.corr())

Correlation_All


# In[ ]:





# ### Calculate and Plot Beta for Your Portfolio compared to the S&P 60 TSX

# In[94]:


# Calculate and plot Beta
Rolling_Covariance2 = All_Portfolio_Returns['Custom Portfolio'].rolling(window = 60).cov(All_Portfolio_Returns['SP_TSX'])
Rolling_Variance2 = All_Portfolio_Returns['SP_TSX'].rolling(window = 60).var()

Rolling_Beta_2 = Rolling_Covariance2 / Rolling_Variance2

print(Rolling_Beta_2)

Rolling_Beta_2.plot(figsize = (20,10), title = '60 Day Rolling Beta for Custom Portfolio')


# ### Using the daily returns, calculate and visualize the Sharpe ratios using a bar plot

# In[109]:


# Calculate Annualzied Sharpe Ratios
Annualized_Sharpe_Ratios = (All_Portfolio_Returns.mean()*252) / (All_Portfolio_Returns.std()*np.sqrt(252))

Annualized_Sharpe_Ratios = pd.DataFrame(Annualized_Sharpe_Ratios)

Annualized_Sharpe_Ratios = Annualized_Sharpe_Ratios.rename(columns = {0: 'Annualized Sharpe Ratios'})

Annualized_Sharpe_Ratios


# In[110]:


# Visualize the sharpe ratios as a bar plot
Annualized_Sharpe_Ratios.plot(kind = 'bar', figsize = (20,10), title = 'Sharpe Ratios Annualized')


# ### How does your portfolio do?
# 
# Write your answer here!

# In[122]:


print("With an extremely high standard deviation and a negative Sharpe Ratio the custom portfolio demonstrates a risky investment. However, its returns were higher than that of its competitors, implying that this is perhaps not the best portfolio for a risk averse investor"
     )


# In[ ]:





# In[128]:


get_ipython().system('pwd')


# In[ ]:




