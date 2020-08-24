#!/usr/bin/env python
# coding: utf-8

# # Real Estate Listings on ReMax and Walk Score

# In[6]:


import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import time
from splinter import Browser
from sqlalchemy import create_engine
import warnings
warnings.filterwarnings('ignore')
print('Libraries imported!')


# # Calgary

# In[8]:


house_address = []
house_details = []

base_url = 'https://www.remax.ca/ab/calgary-real-estate?page='
urls = [base_url + str(x) for x in range(1,301)]

for url in urls:
    # Parse HTML with Beautiful Soup
    time.sleep(5)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    try:
        addresses = soup.find_all('div', class_='left-content flex-one')
        for address in addresses:
            house_address.append(address.text)
    except:
        house_address.append(np.nan)
        
    try:
        details = soup.find_all('div', class_='property-details')
        for detail in details:
            house_details.append(detail.text)
    except:
        house_details.append(np.nan)


# In[9]:


address_df = pd.DataFrame(house_address)

new_df = address_df[0].str.split(' ', 2, expand=True)
new_df["price"] = new_df[1].str.replace("$", "")
new_df["price"] = new_df["price"].str.replace(",", "")
new_df["price"] = pd.to_numeric(new_df["price"])

del new_df[0]
del new_df[1]
new_df.head()


# In[10]:


final_df = new_df[2].str.split(', Calgary, AB, ', expand=True)
final_df.head()


# In[11]:


df_add = pd.concat([new_df, final_df], axis=1)
del df_add[2]
df_add.columns = ["price", "address", "postal_code"]
df_add.head()


# In[12]:


details = pd.DataFrame(house_details)

details_df_temp = details[0].str.split('|', expand=True)

details_df_temp.head()


# In[14]:


details_df_bed = details_df_temp[0].str.replace(' bed', '')
details_df_bath = details_df_temp[1].str.replace(' bath', '')
details_df_area = details_df_temp[2].str.replace(' sqft', '')


# In[15]:


details_df_bath_all = details_df_bath.str.split('+', expand=True)
details_df_bath_full = details_df_bath_all[0]
details_df_bath_half = details_df_bath_all[1]


# In[16]:


details_df_bed = details_df_bed.replace('N/A', np.nan)
details_df_bed = pd.to_numeric(details_df_bed)
details_df_area = details_df_area.replace('N/A', np.nan)
details_df_area = pd.to_numeric(details_df_area)
details_df_bath_full = details_df_bath_full.replace('N/A', np.nan)
details_df_bath_full = pd.to_numeric(details_df_bath_full)
details_df_bath_half = details_df_bath_half.replace('N/A', np.nan)
details_df_bath_half = pd.to_numeric(details_df_bath_half)


# In[17]:


data = {'bed':details_df_bed, 'full_bath':details_df_bath_full, 'half_bath':details_df_bath_half,
       'property_area':details_df_area, 'property_type':details_df_temp[3]}


# In[18]:


details_df = pd.DataFrame(data)
details_df.head()


# In[19]:


calgary_df_dup = pd.concat([df_add, details_df], axis=1)
calgary_df = calgary_df_dup.drop_duplicates()
calgary_df.head()


# In[20]:


calgary_df.to_csv('calgary_df.csv', index=False)


# ----------------

# ### Walk Score

# In[21]:


calgary_df = pd.read_csv('calgary_df.csv')
calgary_df.head()


# In[22]:


post_code_list = []

for i in calgary_df["postal_code"]:
    post_code_list.append(i)


# In[23]:


scores_walk = []
scores_bike = []
scores_transit = []

for i in post_code_list:

    try:
        postal_code = i.replace(" ", "%20")
        url_score = "https://www.walkscore.com/score/" + str(postal_code)
        time.sleep(5)

        # Parse HTML with Beautiful Soup
        response = requests.get(url_score)
        code_soup = BeautifulSoup(response.text, 'html.parser')

        if 'pp.walk.sc/badge/walk/score' in str(code_soup):
            ws = str(code_soup).split('pp.walk.sc/badge/walk/score/')[1][:2].replace('.','')
            scores_walk.append(ws)
        else:
            ws = 'N/A'
            scores_walk.append(ws)
        if 'pp.walk.sc/badge/bike/score' in str(code_soup):
            bs = str(code_soup).split('pp.walk.sc/badge/bike/score/')[1][:2].replace('.','')
            scores_bike.append(bs)
        else:
            bs = 'N/A'
            scores_bike.append(bs)
        if 'pp.walk.sc/badge/transit/score' in str(code_soup):
            ts = str(code_soup).split('pp.walk.sc/badge/transit/score/')[1][:2].replace('.','')
            scores_transit.append(ts)
        else:
            ts = 'N/A'
            scores_transit.append(ts)
    except:
        ws = 'N/A'
        scores_walk.append(ws)
        bs = 'N/A'
        scores_bike.append(bs)
        ts = 'N/A'
        scores_transit.append(ts)


# In[24]:


score_df_trans = {'postal_code':post_code_list, 
                  'walk_score':scores_walk, 
                  'bike_score':scores_bike, 
                  'transit_score':scores_transit}
score_df_dup = pd.DataFrame(score_df_trans)
score_df = score_df_dup.drop_duplicates()
score_df.head()


# In[25]:


score_df.to_csv('score_df.csv', index=False)


# -------------------

# # PostgreSQL

# In[26]:


calgary_df = pd.read_csv('calgary_df.csv')
score_df = pd.read_csv('score_df.csv')


# In[28]:


rds_connection_string = "postgres:123@localhost:5432/realestate_db"
engine = create_engine(f'postgresql://{rds_connection_string}')

calgary_df.to_sql(name= "calgary", con=engine, if_exists="replace", index=False)
score_df.to_sql(name= "score", con=engine, if_exists="append", index=False)


# # MongoDB

# In[29]:


import pymongo
from pymongo import MongoClient

conn = 'mongodb://localhost:27017'
# Making a Connection with MongoClient
client = MongoClient(conn)
# database
db = client.realestate_db

collection = db.calgary
calgary_dict = calgary_df.to_dict("records")
collection.insert_many(calgary_dict)

collection = db.score
score_dict = score_df.to_dict("records")
collection.insert_many(score_dict)


# # MySQL

# In[30]:



engine = create_engine(f'mysql+pymysql://root:Myp@sswordis123@localhost/realestate_db', pool_recycle=3600)
calgary_df.to_sql(name="calgary", con=engine, if_exists="replace", index=False)
score_df.to_sql(name="score", con=engine, if_exists="append", index=False)


# # SQL Server

# In[ ]:


import urllib
import pyodbc


quoted = urllib.parse.quote_plus("DRIVER={SQL Server};SERVER=DAYOTHOMPSON;DATABASE=realestate_db")
engine = create_engine('mssql+pyodbc:///?odbc_connect={}'.format(quoted))
cal_df.to_sql('calgary', schema='dbo', con = engine, chunksize=200, method='multi', index=False, if_exists='replace')
score_df.to_sql('score', schema='dbo', con = engine, chunksize=200, method='multi', index=False, if_exists='append')

