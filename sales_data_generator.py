import pandas as pd
from sqlalchemy import create_engine
import os
import numpy as np

# sql auth parameters
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_name = os.getenv('DB_NAME')
# Database connection string
db_connection_str = f'mysql+mysqlconnector://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
engine = create_engine(db_connection_str)

# Identifying number of additional rows to generate
orders_and_times_query = """
SELECT order_num, ord_time
FROM sales_view;
"""

sales_df = pd.read_sql_query(orders_and_times_query, engine)
sales_df['date'] = sales_df['ord_time']

# Calculate average orders per day
average_daily_orders = sales_df.groupby('date').size().mean()
std_daily_orders = sales_df.groupby('date').size().std()
np.random.seed(2)
num_orders = max(1, int(np.random.normal(loc=average_daily_orders, scale = std_daily_orders)))

# Now that we have a number of orders to generate, we can populate orders and customers data
order_num = pd.read_sql_query('SELECT MAX(order_num) FROM CUSTOMERS;', engine)
for i in range(num_orders):
    order_num = order_num + 1
    new_order = {
        'order_num': order_num
    }
    print(order_num)
print(num_orders)
print(average_daily_orders)
print(std_daily_orders)
