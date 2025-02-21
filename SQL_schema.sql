DROP TABLE IF EXISTS CUSTOMERS;
DROP TABLE IF EXISTS ORDERS;
DROP TABLE IF EXISTS SEATS;
CREATE TABLE CUSTOMERS (
    order_num INT,
    first_nam VARCHAR(255),
    last_nam VARCHAR(255),
    hashed_id VARCHAR(255),
    city VARCHAR(255),
    state VARCHAR(255),
    staate_name VARCHAR(255),
    zip VARCHAR(255),
    country VARCHAR(255)
);
CREATE TABLE ORDERS (
    order_num INT,
    ord_time TIMESTAMP,
    ord_oper VARCHAR(255),
    ord_location VARCHAR(255),
    tix_tran_num INT,
    e_event_cod VARCHAR(255),
    p_perf_date TIMESTAMP,
    evt_kind_nam VARCHAR(255),
    tix_tran_time TIMESTAMP,
    mkt_price_type VARCHAR(255)
);
CREATE TABLE SEATS (
    order_num INT,
    tix_tran_num INT,
    area VARCHAR(255),
    section VARCHAR(255),
    row VARCHAR(255),
    seat_num INT,
    price_code VARCHAR(255),
    ppn_name VARCHAR(255),
    price_per_seat FLOAT,
    zone int,
    zone_name_1 VARCHAR(255),
    zone_name_2 VARCHAR(255),
    fee_amount FLOAT,
    fee_type VARCHAR(255),
    action_time TIMESTAMP,
    action VARCHAR(255),
    action_id FLOAT,
    seat_retuned INT
);
DROP VIEW IF EXISTS sales_view;
CREATE VIEW sales_view AS
SELECT 
    c.order_num,
    c.city,
    c.state,
    c.zip,
    c.country,
    o.ord_time,
    o.ord_location,
    o.mkt_price_type,
    o.evt_kind_nam as 'event_kind',
    o.e_event_cod as 'event_code',
    COUNT(s.price_per_seat) as ticket_count,
    ROUND(SUM(s.price_per_seat), 2) as revenue
FROM customer c
INNER JOIN orders_table o ON c.order_num = o.order_num
INNER JOIN seat s ON c.order_num = s.order_num
GROUP BY
    c.order_num,
    c.city,
    c.state,
    c.zip,
    c.country,
    o.ord_time,
    o.mkt_price_type,
    o.evt_kind_nam;
DROP INDEX IF EXISTS idx_customers_order_num ON CUSTOMERS;
DROP INDEX IF EXISTS idx_orders_order_num ON ORDERS;
DROP INDEX IF EXISTS idx_seats_order_num ON SEATS;
CREATE INDEX idx_customer_order_num ON CUSTOMERS(order_num);
CREATE INDEX idx_orders_table_order_num ON ORDERS(order_num);
CREATE INDEX idx_seat_order_num ON SEATS(order_num);