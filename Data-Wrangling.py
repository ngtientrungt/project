#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
prices = pd.read_csv('E:\DAC k9\Python\Data Wrangling Practise/prices.csv')
sales = pd.read_csv('E:\DAC k9\Python\Data Wrangling Practise/sales.csv')

print(sales)
print(prices)


# In[2]:


import datetime
import time
sales["ordered_at"] = pd.to_datetime(sales["ordered_at"])
prices["updated_at"] = pd.to_datetime(prices["updated_at"])
sales1 = sales.sort_values(by = "ordered_at")
prices1 = prices.sort_values("updated_at")
print(sales1)
print(prices1)


# In[7]:


combine = pd.merge_asof(sales1, prices1,left_on='ordered_at',right_on='updated_at',by = "product_id",direction='nearest')
combine


# In[28]:


combine['listed_price'] = np.where(combine['ordered_at'] >= combine['updated_at'],combine['new_price'], combine['old_price'])
combine


# In[10]:


combine['revenue'] = combine['quantity_ordered'] * combine['listed_price']
total_revenue_by_product_and_price = combine.groupby(['product_id', 'listed_price'], as_index=False)['revenue'].sum()
total_revenue_by_product_and_price


# In[27]:


total_revenue = combine.pivot_table(values='revenue',index = ['product_id','listed_price'],aggfunc=np.sum)
total_revenue


# In[ ]:




