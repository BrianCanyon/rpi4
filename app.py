## Overview:
# This workbook is meant to capture the requirements listed in 'Part 1: Data Modeling' section
# of the take home project given to be by Two Circles. At a high level, this includes:
#       - ingestion of .csv files
#       - data cleaning/transformation
#       - authentication and publishing to sql

# importing libraries used throughout the workbook
import pandas as pd
from sqlalchemy import create_engine
import os

# The .csv file is delimited with a pipe, note the additional parameter within the read_csv function
customer_df = pd.read_csv('/home/brian.canyon/Documents/Case Study_Customer.csv', delimiter='|')
order_df = pd.read_csv('/home/brian.canyon/Documents/Case Study_Order.csv', delimiter='|')
seat_df = pd.read_csv('/home/brian.canyon/Documents/Case Study_Seat.csv', delimiter='|')

# The column 'order_num' is a primary key for all tables. In the customer and order table, it is meant
# to be unique. Below remove duplicated values but keeps the first. Ideally, reaching out to the upstream
# owner of this data set would be done to address duplications. 
customer_clean = customer_df.drop_duplicates(subset='order_num', keep='first')
order_clean = order_df.drop_duplicates(subset='order_num', keep='first')

# The column 'evt_kind_nam' from the orders table has a mix of capitalization from upper
# and lower. This code standardizes the text in that column.
order_clean['evt_kind_name'] = order_clean['evt_kind_nam'].str.title()
order_clean = order_clean.drop(columns=['evt_kind_nam'])
# DateTime columns are being read as strings, this block fixes dt data types
order_clean['ord_time'] = pd.to_datetime(order_clean['ord_time'], format = '%m/%d/%Y %H:%M', \
                                         errors = 'coerce')
order_clean['tix_tran_time'] = pd.to_datetime(order_clean['tix_tran_time'], format = '%m/%d/%Y %H:%M', \
                                              errors = 'coerce')
order_clean['p_perf_date'] = pd.to_datetime(order_clean['p_perf_date'], format = '%m/%d/%Y', \
                                            errors = 'coerce')
seat_df['actiontime'] = pd.to_datetime(seat_df['actiontime'], format = '%m/%d/%Y %H:%M', \
                                       errors = 'coerce')

# Adjusting column names to be consistantly in snake_case
seat_df['seat_num'] = seat_df['seannum']
seat_df['price_code'] = seat_df['price_cod']
seat_df['zone_name_1'] = seat_df['zonename1']
seat_df['zone_name_2'] = seat_df['zonename2']
seat_df['fee_amount'] = seat_df['feeamt']
seat_df['fee_type'] = seat_df['feetype']
seat_df['action_time'] = seat_df['actiontime']
seat_df['action_id'] = seat_df['actionid']
seat_df = seat_df.drop(columns=['seannum', 'price_cod', 'zonename1', 'zonename2',\
                                'feeamt', 'feetype', 'actiontime', 'actionid'])

# Database connection details
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_name = os.getenv('DB_NAME')

# Database connection string
db_connection_str = f'mysql+mysqlconnector://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
engine = create_engine(db_connection_str)

# Load data into the SQL database
customer_clean.to_sql('CUSTOMERS', engine, if_exists='replace', index=False)
order_clean.to_sql('ORDERS', engine, if_exists='replace', index=False)
seat_df.to_sql('SEATS', engine, if_exists='replace', index=False)