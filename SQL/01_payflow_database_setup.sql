-- ===============================================
-- PAYMENT DATA ANALYTICS PROJECT
-- DATABASE SETUP
-- ===============================================

-- Database: payflow
-- Customers: 25,000
-- Transactions: 152,870

-- This file documents the database setup.
-- Database and tables have already been created.

-- ===============================================
-- 1. CREATE DATABASE
-- ===============================================

CREATE DATABASE IF NOT EXISTS payflow;

USE payflow;

-- ===============================================
-- 2. CREATE CUSTOMERS TABLE
-- ===============================================

CREATE TABLE IF NOT EXISTS customers (
customer_id VARCHAR(10) PRIMARY KEY,
signup_date DATE,
gender VARCHAR(10),
age INT,
city VARCHAR(100),
state VARCHAR(50),
customer_type VARCHAR(20),
acquisition_channel_id VARCHAR(10),
plan VARCHAR(20),
first_transaction_date DATE,
status VARCHAR(20)
);

-- ===============================================
-- 3. CREATE TRANSACTIONS TABLE
-- ===============================================

CREATE TABLE IF NOT EXISTS transactions (
transaction_id VARCHAR(20) PRIMARY KEY,
customer_id VARCHAR(10),
transaction_date DATE,
amount DECIMAL(12,2),
transaction_type VARCHAR(30),
payment_method VARCHAR(30),
transaction_status VARCHAR(20),

FOREIGN KEY (customer_id)
REFERENCES customers(customer_id)
);

-- ===============================================
-- 4. DATA VERIFICATION
-- ===============================================

-- Check total number of customers
SELECT COUNT(*) AS total_customers
FROM customers;

-- Check total number of transactions
SELECT COUNT(*) AS total_transactions
FROM transactions;

-- Check customers with missing transaction dates
SELECT
COUNT(*) AS total_customers,
COUNT(first_transaction_date) AS customers_with_transaction_dates,
SUM(first_transaction_date IS NULL) AS customers_without_transaction_dates
FROM customers;
