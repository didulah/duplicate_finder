-- Test database and sample duplicate data for Duplicate Finder & Cleaner tool
-- Run this entire file in SQLTools (or MySQL Command Line Client) against your local_mysql connection

-- Create a dedicated test database
CREATE DATABASE IF NOT EXISTS duplicate_finder_test;
USE duplicate_finder_test;

-- Create a customers table (simulates a real-world table with duplicate rows)
DROP TABLE IF EXISTS customers;
CREATE TABLE customers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100),
    email VARCHAR(100),
    phone VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert unique records
INSERT INTO customers (full_name, email, phone) VALUES
('Nimal Perera', 'nimal.perera@example.com', '0771234567'),
('Kamala Silva', 'kamala.silva@example.com', '0777654321'),
('Ruwan Fernando', 'ruwan.fernando@example.com', '0712345678'),
('Ishara Jayasuriya', 'ishara.j@example.com', '0761112223');

-- Insert duplicate records (same email, different id - this is what the tool should detect)
INSERT INTO customers (full_name, email, phone) VALUES
('Nimal Perera', 'nimal.perera@example.com', '0771234567'),
('Nimal Perera', 'nimal.perera@example.com', '0771234567'),
('Kamala Silva', 'kamala.silva@example.com', '0777654321');

SELECT email, COUNT(*) AS duplicate_count
FROM duplicate_finder_test.customers
GROUP BY email
HAVING COUNT(*) > 1;
-- Verify: check row count and duplicate groups
SELECT COUNT(*) AS total_rows FROM customers;

SELECT email, COUNT(*) AS duplicate_count
FROM customers
GROUP BY email
HAVING COUNT(*) > 1;