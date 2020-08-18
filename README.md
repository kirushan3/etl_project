# ETL Project


# Real Estate Listings and Walk Score in Calgary

![42930188 S](images/42930188_s.jpg)

## Objective

• Extracting Real Estate listings in Calgary, Alberta
and Walk Scores for corresponding house addresses.
• Walk Score analyzes the walking routes of these
addresses to nearby amenities. Points are awarded
based on the distance to amenities in each
category.
• Transforming retrieved data into easy-to-read tables
• Loading transformed data into relational and nonrelational
databases for optimal functionality


## Data Sources

• Remax Canada: https://www.remax.ca/ab/calgary-real-estate

• Walk Score: https://www.walkscore.com/CA-AB/Calgary



# Extract

## Scraping Calgary Real Estate Data

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
