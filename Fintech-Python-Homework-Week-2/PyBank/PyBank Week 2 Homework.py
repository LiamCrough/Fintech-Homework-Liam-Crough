#!/usr/bin/env python
# coding: utf-8

# In[16]:


#import csv file
from pathlib import Path


# In[17]:


csvpath = ("/Users/Liam/Desktop/Homework_Week 2_PyBank_Resources_budget_data.csv")


# In[18]:


#import pandas
import pandas as pd


# In[19]:


data = pd.read_csv(csvpath)


# In[20]:


data


# In[21]:


#establish dataframe
df = pd.DataFrame(data)


# In[22]:


index = df.index
number_of_rows = len(index)


# In[23]:


# show output

print("FINANCIAL ANALYSIS IS BELOW")
print("----------------------------")
print("TOTAL MONTHS ARE EQUAL TO:")
print(number_of_rows)
print("----------------------------")
print("TOTAL OF PROFIT AND LOSS IS EQUAL TO: ")
print(df["Profit/Losses"].sum())
print("----------------------------")
print("AVERAGE CHANGE WAS EQUAL TO: ")
print(df["Profit/Losses"].mean())
print("----------------------------")
print("GREATEST INCREASE WAS: ")
print(df[df['Profit/Losses'] == df['Profit/Losses'].max()])
print("----------------------------")
print("GREATEST DECREASE WAS ")
print(df[df['Profit/Losses'] == df['Profit/Losses'].min()])


# In[33]:


# create text file output

import sys

stdoutOrigin = sys.stdout
sys.stdout = open("Financial Analysis Output.txt", "w")

print("FINANCIAL ANALYSIS IS BELOW")
print("----------------------------")
print("TOTAL MONTHS ARE EQUAL TO:")
print(number_of_rows)
print("----------------------------")
print("TOTAL OF PROFIT AND LOSS IS EQUAL TO: ")
print(df["Profit/Losses"].sum())
print("----------------------------")
print("AVERAGE CHANGE WAS EQUAL TO: ")
print(df["Profit/Losses"].mean())
print("----------------------------")
print("GREATEST INCREASE WAS: ")
print(df[df['Profit/Losses'] == df['Profit/Losses'].max()])
print("----------------------------")
print("GREATEST DECREASE WAS ")
print(df[df['Profit/Losses'] == df['Profit/Losses'].min()])

sys.stdout.close()
sys.stdout=stdoutOrigin


# In[ ]:





# In[ ]:





# In[ ]:




