# ETL Project


# Real Estate Listings and Walk Score in Calgary

![42930188 S](images/42930188_s.jpg)

## Overview

Just recently, you landed a new job in another province and are trying to decide if you want to buy a new home or apartment.
You have contacted a real estate company to provide you with a detailed copy of the current listings in the province.
Unfortunately, the copies provided only contains the current prices of the houes and apartments but gives no indication of the walking,
transit, and biking routes to nearby amenities. You would like the information provided to include ratings based on the distances to amenities 
in each category.
This might pose a slight problem because you want to have all route options available to you and at anytime you need. You decide to get down 
to some digging by performing an ETL challenge on two websites; ReMax and Walk Score.


## Objective

• Extract Real Estate listings in Calgary, Alberta
and Walk Scores for corresponding house addresses.

• Transforming retrieved data into easy-to-read tables.

• Loading transformed data into relational and nonrelational
databases for optimal functionality.



## Data Sources

• Remax Canada: https://www.remax.ca/ab/calgaryreal-estate

• Walk Score: https://www.walkscore.com/CAAB/
Calgary


# Extraction

## Scraping Calgary Real Estate Data



### Libraries imported


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




### Using BeautifulSoup to scrape property details (house address, house details).


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


# Data Transformation Process


	address_df = pd.DataFrame(house_address)
	
	new_df = address_df[0].str.split(' ', 2, expand=True)
	new_df["price"] = new_df[1].str.replace("$", "")
	new_df["price"] = new_df["price"].str.replace(",", "")
	new_df["price"] = pd.to_numeric(new_df["price"])
	
	del new_df[0]
	del new_df[1]
	new_df.head()


	
	final_df = new_df[2].str.split(', Calgary, AB, ', expand=True)
	final_df.head()
	


	
	df_add = pd.concat([new_df, final_df], axis=1)
	del df_add[2]
	df_add.columns = ["price", "address", "postal_code"]
	df_add.head()
	


	
	details = pd.DataFrame(house_details)
	details_df_temp = details[0].str.split('|', expand=True)
	details_df_temp.head()
	


	
	details_df_bed = details_df_temp[0].str.replace(' bed', '')
	details_df_bath = details_df_temp[1].str.replace(' bath', '')
	details_df_area = details_df_temp[2].str.replace(' sqft', '')
	


	
	details_df_bath_all = details_df_bath.str.split('+', expand=True)
	details_df_bath_full = details_df_bath_all[0]
	details_df_bath_half = details_df_bath_all[1]
	


	
	details_df_bed = details_df_bed.replace('N/A', np.nan)
	details_df_bed = pd.to_numeric(details_df_bed)
	details_df_area = details_df_area.replace('N/A', np.nan)
	details_df_area = pd.to_numeric(details_df_area)
	details_df_bath_full = details_df_bath_full.replace('N/A', np.nan)
	details_df_bath_full = pd.to_numeric(details_df_bath_full)
	details_df_bath_half = details_df_bath_half.replace('N/A', np.nan)
	details_df_bath_half = pd.to_numeric(details_df_bath_half)
	


	
	data = {'bed':details_df_bed, 'full_bath':details_df_bath_full, 'half_bath':details_df_bath_half,
       'property_area':details_df_area, 'property_type':details_df_temp[3]}
	   


	
	details_df = pd.DataFrame(data)
	details_df.head()
	

## Creating Calgary Listings DataFrame

	
	calgary_df_dup = pd.concat([df_add, details_df], axis=1)
	calgary_df = calgary_df_dup.drop_duplicates()
	calgary_df.head()
	

## Store Calgary Listings as CSV

	
	calgary_df.to_csv('calgary_df.csv', index=False)
	



## Reading data from saved Calgary Listings



	
	calgary_df = pd.read_csv('calgary_df.csv')
	calgary_df.head()
	


## Scraping Walk Score Data

	
	post_code_list = []
	
	for i in calgary_df["postal_code"]:
    post_code_list.append(i)
	


	
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


## Creating the Walk Score DataFrame

	
	score_df_trans = {'postal_code':post_code_list, 
                  'walk_score':scores_walk, 
                  'bike_score':scores_bike, 
                  'transit_score':scores_transit}
	score_df_dup = pd.DataFrame(score_df_trans)
	score_df = score_df_dup.drop_duplicates()
	score_df.head()
	


## Saving Walk Score data to CSV

	
	score_df.to_csv('score_df.csv', index=False)
	



# # MongoDB
	
	import pymongo
	from pymongo import MongoClient
	
	conn = 'mongodb://localhost:27017'
	
	client = MongoClient(conn)
	
	
	db = client.realestate_db
	
	collection = db.calgary
	calgary_dict = calgary_df.to_dict("records")
	collection.insert_many(calgary_dict)
	
	collection = db.score
	score_dict = score_df.to_dict("records")
	collection.insert_many(score_dict)





# # PostgreSQL

	
	calgary_df = pd.read_csv('calgary_df.csv')
	score_df = pd.read_csv('score_df.csv')
	
	rds_connection_string = "postgres:123@localhost:5432/realestate_db"
	engine = create_engine(f'postgresql://{rds_connection_string}')
	
	calgary_df.to_sql(name= "calgary", con=engine, if_exists="replace", index=False)
	score_df.to_sql(name= "score", con=engine, if_exists="append", index=False)
	



# # MySQL

	
	engine = create_engine(f'mysql+pymysql://root:Myp@sswordis123@localhost/realestate_db', pool_recycle=3600)
	calgary_df.to_sql(name="calgary", con=engine, if_exists="replace", index=False)
	score_df.to_sql(name="score", con=engine, if_exists="append", index=False)
	


# # SQL Server

	import urllib
	import pyodbc
	
	quoted = urllib.parse.quote_plus("DRIVER={SQL Server};SERVER=DAYOTHOMPSON;DATABASE=realestate_db")
	engine = create_engine('mssql+pyodbc:///?odbc_connect={}'.format(quoted))
	cal_df.to_sql('calgary', schema='dbo', con = engine, chunksize=200, method='multi', index=False, if_exists='replace')
	score_df.to_sql('score', schema='dbo', con = engine, chunksize=200, method='multi', index=False, if_exists='append')
	










Using BeautifulSoup to scrape property details (house address, house details).
![Picture1](images/Picture1.png)







![Picture2png](images/Picture2png.png)


## Scraping Walk Score Data

Using the corresponding addresses from the Calgary real estate data

![Picture3](images/Picture3.png)


# Transform

## Cleaning the Calgary Real Estate Data

#### First data frame: Address and Price details

![Picture4](images/Picture4.png)


• Values separated into columns: price, address, postal code,
• Price column type changed to integer

![Picture5](images/Picture5.png)

#### Second data frame: House details
• Values separated into columns: bedrooms, bath, property type

![Picture6](images/Picture6.png)

#### Joining the Calgary Real Estate Data frames
• Concatenating House Address/Price details and
House details data frames.

![Picture7](images/Picture7.png)


## Cleaning the Walk Score Data
• Data converted into data frame and columns
named.

![Picture8](images/Picture8.png)

![Picture9](images/Picture9.png)

# Load

## Loading to Relational Database

### PostgreSQL

Creating connection and loading data to realestate_db

![Picture10](images/Picture10.png)

#### Loaded Data

![Picture11a](images/Picture11a.png)

![Picture12](images/Picture12.png)

## Loading to Non-relational Database

### MongoDB

Creating connection and loading data to realestate_db

![Picture13](images/Picture13.png)

#### Loaded Data
![Screen Shot 2020 08 16 At 8.19.32 PM](images/Screen%20Shot%202020-08-16%20at%208.19.32%20PM.png)

![Screen Shot 2020 08 16 At 8.18.31 PM](images/Screen%20Shot%202020-08-16%20at%208.18.31%20PM.png)

## Converting to a Web-based Application

![Screen Shot 2020 08 16 At 8.31.57 PM](images/Screen%20Shot%202020-08-16%20at%208.31.57%20PM.png)
