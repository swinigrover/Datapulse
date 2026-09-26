-- DataPulse Database Schema
-- Business Intelligence & Sales Analytics Platform

-- Drop tables if they exist (for clean setup)
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS products;

-- Create Customers Table
CREATE TABLE customers (
    customer_id VARCHAR(50) PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL,
    segment VARCHAR(50) NOT NULL,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100) NOT NULL,
    region VARCHAR(50) NOT NULL
);

-- Create Products Table
CREATE TABLE products (
    product_id VARCHAR(50) PRIMARY KEY,
    product_name VARCHAR(200) NOT NULL,
    category VARCHAR(100) NOT NULL,
    sub_category VARCHAR(100) NOT NULL,
    unit_price DECIMAL(10, 2) NOT NULL
);

-- Create Orders Table
CREATE TABLE orders (
    order_id VARCHAR(50) PRIMARY KEY,
    order_date DATE NOT NULL,
    customer_id VARCHAR(50) NOT NULL,
    product_id VARCHAR(50) NOT NULL,
    region VARCHAR(50) NOT NULL,
    category VARCHAR(100) NOT NULL,
    sub_category VARCHAR(100) NOT NULL,
    quantity INTEGER NOT NULL,
    sales DECIMAL(15, 2) NOT NULL,
    profit DECIMAL(15, 2) NOT NULL,
    discount DECIMAL(5, 4) NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

-- Create Indexes for Performance
CREATE INDEX idx_orders_order_date ON orders(order_date);
CREATE INDEX idx_orders_customer_id ON orders(customer_id);
CREATE INDEX idx_orders_product_id ON orders(product_id);
CREATE INDEX idx_orders_region ON orders(region);
CREATE INDEX idx_orders_category ON orders(category);
CREATE INDEX idx_customers_region ON customers(region);
CREATE INDEX idx_customers_segment ON customers(segment);
CREATE INDEX idx_products_category ON products(category);
