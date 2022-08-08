#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
# %matplotlib inline


# In[2]:


df = pd.read_excel('C:/Users/ABDO/Downloads/sample_-_superstore.xls')
df.tail()


# # Renaming columns

# In[3]:


cols = df.columns
cols


# In[4]:


new_cols = [x.lower().replace(' ','_').replace('-','_') for x in cols]
new_cols


# In[5]:


mapper = {} # the mapper to replace the old col_names with new col_names
for x,y in zip(cols,new_cols):
    mapper[x] = y
df.rename(columns=mapper, inplace=True)


# In[6]:


df.head(1)


# ### Data exploring

# In[7]:


df.describe()


# #### Searching for duplicates

# In[8]:


df.duplicated().sum()


# #### Searching for nulls

# In[9]:


df.isnull().sum().sum()


# ### Categories' comparison

# In[10]:


categories = df.groupby('category').sum()
x_axes = categories.index


# In[11]:


fig, (ax, ax1, ax2) = plt.subplots(nrows=1,ncols=3)
# plt.figure(figsize=(1000,4000))
ax.bar(x_axes, categories['sales'])
# ax.set_ylabel('Sales')
ax.set_title('Sales By Category')

ax1.bar(x_axes, categories['profit'])
ax1.set_title('Profit by category')

ax2.bar(x_axes, categories['quantity'])
ax2.set_title('Units Sold by Category')
plt.subplots_adjust(left=.1,right=3)
plt.show()


# In[12]:


fig, (ax, ax1) = plt.subplots(nrows=2,ncols=1)
# plt.figure(figsize=(50,90))
ax.bar(x_axes,categories['sales'], label='Sales')
ax.plot(categories['sales'],color='r')
ax.set_title('Total Sales by Category')
ax1.plot(categories['profit'], label='profit')
ax1.plot(categories['quantity'], label='units_sold')
ax1.set_title('profit Vs. units sold by Category')
plt.legend()
plt.subplots_adjust(top=2,bottom=.5)
plt.show()


# ### By region comaprison

# In[13]:


regions = df.groupby('region').sum()
region_names = regions.index
region_names


# In[14]:


fig, (ax, ax1) = plt.subplots(nrows=2, ncols=1)
ax.bar(region_names, regions['sales'], label='Total Sales')
ax.set_title('Total sales by region')
ax1.bar(region_names,regions['profit'], label='Profit')
ax1.plot(regions['quantity'],marker='x',c='r',label='Units Sold')
ax1.set_title('Profit Vs. units sold by region')
ax.legend()
ax1.legend(loc='upper left')
plt.subplots_adjust(top=2,bottom=.5)
plt.show()


# In[15]:


shipment_categories = df.groupby('category').sum()


# In[16]:


shipment_categories


# ## Digging deeper in products

# In[17]:


products = df.groupby('sub_category')


# In[18]:


products['sales', 'quantity', 'profit'].sum()


# In[19]:


products['sales'].sum().plot(kind='bar').set_title('Toatal Sales by subcategory')
plt.figure.figsize=(50,200)
plt.show()


# In[20]:


products['quantity'].sum().plot(kind='bar').set_title('Sold units by subcategory')
plt.figure.figsize=(50,200)
plt.show()


# In[21]:


products['profit'].sum().plot(kind='bar').set_title('Profit by subcategory')
plt.figure.figsize=(50,200)
plt.show()


# ### It is obvious that we have loss in 3 subcategories

# In[22]:


# Categories that cause loss
mask = products['profit'].sum() < 0
mask[mask]


# In[23]:


# How uch loss?
losses = products['profit'].sum().sort_values().head(3)
losses


# In[24]:


# Showing in graphs
ax = plt.pie(abs(losses.values))
plt.legend(labels=losses.index)
plt.show()


# ## Bookcases, Supplies and Tables cost the company a loss
# ### Why?
# ### Should we stop production?
# ### What are our alternatives?

# ## Searching for outliers

# In[25]:


# further more
products['profit'].max() # max profit


# In[26]:


# min profit
products['profit'].min()


# In[27]:


# profit range
profit_range = products['profit'].max() - products['profit'].min()
profit_range


# In[28]:


profit_range.sort_values()


# # Highlight operations with negative profit or losing ones

# In[29]:


causing_loss_opertions = df.query('profit <= 0')
causing_loss_opertions.head()


# In[30]:


# Number of non profitable operations
causing_loss_opertions.shape[0]


# # let's get backwards again
# ### what is the profit per unit sold?
# ### what if the calculations were wrong? Should I ignore negative numbers?
# 

# In[31]:


# finding profit per unit, unit cost and unit price
# unit_price = total_sales / quantity
df['unit_price'] = df['sales'] / df['quantity']
# unit_profit = profit / quantity
df['unit_profit'] = df['profit'] / df['quantity']
#  unit_cost = unit_price - unit_profit
df['unit_cost'] = df['unit_price'] - df['unit_profit']


# In[32]:


# lets see
df.head(2)


# In[33]:


causing_loss_opertions = df.query('profit <= 0')
causing_loss_opertions.head()


# # Pick a unit to test suppose (FUR-BO-10001798):
#  ### - Compare once with profit and with loss.
#  ### - Get a clue.

# In[53]:


prod_fur_bo_10001798 = df.query('product_id == "FUR-BO-10001798"')
prod_fur_bo_10001798


# # Findings for FUR-BO-10001798 :
# ### - Unit cost is constant = 110.0232.
# ### - Unit price without discount = 130.980
# ### - So the margin profit is 130.980 - 110.0232 = 20.9568
# ### - Margin profit percentage of sales price is 20.9568 / 130.980 = .16

# # Another piece of tables

# In[35]:


tables_df = df.query('sub_category == "Tables"')
tables_df.head()


# ### Testing : FUR-TA-10004534

# In[36]:


pro_FUR_TA_10004534 = df.query('product_id == "FUR-TA-10004534"')
pro_FUR_TA_10004534


# # Findings for FUR-TA-10004534:
# ### - Unit cost is constant = 170.897
# ### - Unit price without discount = 205.90
# ### - So the margin profit is 205.9 - 170.897 = 35.003
# ### - Margin profit percentage of sales price is 35.003 / 205.9 = .16999999

# # One last piece of supplies

# In[50]:


supplies_df = df.query('sub_category == "Supplies"')
supplies_df['product_id']


# # Testing OFF-SU-10003936

# In[54]:


prod_OFF_SU_10003936 = df.query('product_id == "OFF-SU-10003936"')
prod_OFF_SU_10003936


# # Findings for product OFF-SU-10003936 :
# ### - Unit cost is constant = 3.1482
# ### - Unit price without discount = 3.180
# ### - So the margin profit is 3.180 - 3.1482 = .0318
# ### - Margin profit percentage of sales price is .0318 / 3.180 = .01

# # Conclusion:
# ## Based on data from products FUR-BO-10001798, FUR-TA-10004534, and OFF-SU-10003936:
# ### * margin percentage is crucial and missing with discount percentage will cause that obviously noticed loss.
# # Recommendation:
# ### ** Put a strict discount policy that will maximize profit as much as possible

# In[ ]:





# # Customers analysis

# In[55]:


# Customer types
customer_types = df.groupby('segment')


# In[56]:


customer_types['sales','quantity', 'profit'].sum()


# In[57]:


ax = plt.pie(customer_types['profit'].sum(),labels=customer_types.indices)
# plt.legend()
plt.title('Profit by customer type')
plt.show()


# In[58]:


customers_groups = df.groupby('customer_name')


# In[59]:


customers = customers_groups['sales','quantity', 'profit'].sum()
customers


# In[60]:


customers.sort_values(by='profit')


# In[62]:


top_10_customers = customers.sort_values(by='profit').tail(10)
top_10_customers


# In[ ]:




