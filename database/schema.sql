-- =====================================================================
-- SnapKart - Retail Billing and Inventory Management System
-- Database Schema Definition (MySQL 8.0+)
-- =====================================================================

CREATE DATABASE IF NOT EXISTS smart_store_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE smart_store_db;

-- 1. Store Business Operating Hours
CREATE TABLE IF NOT EXISTS store_hours (
    day_name VARCHAR(10) PRIMARY KEY,
    open_time TIME NOT NULL,
    close_time TIME NOT NULL,
    is_closed_today BOOLEAN DEFAULT FALSE
);

-- Seed default operating hours (09:00 AM to 09:00 PM; Sunday 10:00 AM to 06:00 PM)
INSERT INTO store_hours (day_name, open_time, close_time, is_closed_today)
VALUES
    ('Monday', '09:00:00', '21:00:00', FALSE),
    ('Tuesday', '09:00:00', '21:00:00', FALSE),
    ('Wednesday', '09:00:00', '21:00:00', FALSE),
    ('Thursday', '09:00:00', '21:00:00', FALSE),
    ('Friday', '09:00:00', '21:00:00', FALSE),
    ('Saturday', '09:00:00', '21:00:00', FALSE),
    ('Sunday', '10:00:00', '18:00:00', FALSE)
ON DUPLICATE KEY UPDATE day_name=day_name;

-- 2. Registered Customers
CREATE TABLE IF NOT EXISTS customers (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(120) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    phone VARCHAR(20) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 3. Product Catalog & Inventory
CREATE TABLE IF NOT EXISTS inventory (
    item_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    category VARCHAR(80) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    stock_quantity INT NOT NULL,
    INDEX idx_category (category),
    INDEX idx_name (name),
    INDEX idx_catalog_category_stock (category, stock_quantity, item_id),
    INDEX idx_catalog_stock_item (stock_quantity, item_id)
);

-- 4. Completed Sales / Orders
CREATE TABLE IF NOT EXISTS sales (
    sale_id INT AUTO_INCREMENT PRIMARY KEY,
    sale_datetime DATETIME NOT NULL,
    total_amount DECIMAL(10, 2) NOT NULL,
    payment_method VARCHAR(50) DEFAULT 'UPI',
    customer_id INT NULL,
    CONSTRAINT fk_sales_customer FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE SET NULL,
    INDEX idx_sale_datetime (sale_datetime)
);

-- 5. Individual Line Items for Each Sale
CREATE TABLE IF NOT EXISTS sale_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sale_id INT NOT NULL,
    item_id INT NOT NULL,
    quantity INT NOT NULL,
    unit_price DECIMAL(10, 2) NOT NULL,
    subtotal DECIMAL(10, 2) NOT NULL,
    CONSTRAINT fk_items_sale FOREIGN KEY (sale_id) REFERENCES sales(sale_id) ON DELETE CASCADE,
    CONSTRAINT fk_items_inventory FOREIGN KEY (item_id) REFERENCES inventory(item_id) ON DELETE CASCADE,
    INDEX idx_sale_id (sale_id),
    INDEX idx_item_id (item_id)
);
