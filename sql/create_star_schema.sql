-- =============================================================================
-- Silver Oak College of Computer Application
-- Department of Computer Application | BCA Semester 5 (A.Y. 2026-27)
-- Course: Data Warehouse and Data Mining (4040233302)
-- Innovative Assignment: Retail Store / Supermarket Data Warehouse Design
-- Deliverable 4: Star Schema Physical Relational DDL (ANSI SQL / PostgreSQL / MySQL)
-- =============================================================================

-- Drop tables if existing (for fresh clean deployment)
DROP TABLE IF EXISTS Fact_Sales CASCADE;
DROP TABLE IF EXISTS Dim_Product CASCADE;
DROP TABLE IF EXISTS Dim_Customer CASCADE;
DROP TABLE IF EXISTS Dim_Date CASCADE;
DROP TABLE IF EXISTS Dim_Store CASCADE;
DROP TABLE IF EXISTS Dim_Payment CASCADE;

-- =============================================================================
-- 1. DIMENSION TABLE: Dim_Date
-- Captures temporal hierarchy: Day -> Month -> Quarter -> Year
-- =============================================================================
CREATE TABLE Dim_Date (
    Date_Key INT PRIMARY KEY,               -- Surrogate Key: YYYYMMDD (e.g., 20260818)
    Full_Date DATE NOT NULL,                -- Calendar Date (e.g., '2026-08-18')
    Day_of_Week INT NOT NULL,               -- 1 (Monday) to 7 (Sunday)
    Day_Name VARCHAR(15) NOT NULL,          -- 'Monday', 'Tuesday', ...
    Day_of_Month INT NOT NULL,              -- 1 to 31
    Month_Number INT NOT NULL,              -- 1 to 12
    Month_Name VARCHAR(15) NOT NULL,        -- 'August', 'September', ...
    Quarter VARCHAR(5) NOT NULL,            -- 'Q1', 'Q2', 'Q3', 'Q4'
    Year INT NOT NULL,                      -- 2026
    Is_Weekend BOOLEAN NOT NULL             -- TRUE for Sat/Sun, FALSE otherwise
);

-- =============================================================================
-- 2. DIMENSION TABLE: Dim_Product
-- Captures product hierarchy: SKU / Product -> Category -> Department
-- Employs Slowly Changing Dimension (SCD) Type 2 tracking
-- =============================================================================
CREATE TABLE Dim_Product (
    Product_Key INT AUTO_INCREMENT PRIMARY KEY, -- Surrogate Key
    Product_ID VARCHAR(20) NOT NULL,            -- Operational Natural Key (e.g., 'SKU-101')
    Product_Name VARCHAR(100) NOT NULL,         -- Descriptive item name
    Product_Category VARCHAR(50) NOT NULL,      -- Department (e.g., 'Dairy & Bakery')
    Brand VARCHAR(50) NOT NULL,                 -- Brand (e.g., 'Amul', 'Tata', 'Britannia')
    Package_Size VARCHAR(30),                   -- e.g., '500ml', '1kg', '100g'
    Base_MRP_INR DECIMAL(10, 2) NOT NULL,       -- Base retail price
    Row_Effective_Date DATE NOT NULL,           -- SCD Type 2 tracking start
    Row_Expiration_Date DATE DEFAULT '9999-12-31', -- SCD Type 2 tracking end
    Is_Current BOOLEAN DEFAULT TRUE             -- Active flag
);

-- =============================================================================
-- 3. DIMENSION TABLE: Dim_Customer
-- Captures customer demographic and behavioral cohort dimensions
-- =============================================================================
CREATE TABLE Dim_Customer (
    Customer_Key INT AUTO_INCREMENT PRIMARY KEY, -- Surrogate Key
    Customer_ID VARCHAR(20) NOT NULL,            -- Operational Loyalty / POS ID
    Age_Group VARCHAR(30) NOT NULL,              -- 'Youth (18-25)', 'Young Adult (26-35)', ...
    Gender VARCHAR(10) NOT NULL,                 -- 'Male', 'Female'
    Customer_Segment VARCHAR(40) NOT NULL,       -- K-Means Derived: 'Budget Quick Shopper', etc.
    Loyalty_Tier VARCHAR(20) DEFAULT 'Standard', -- 'Standard', 'Silver', 'Gold'
    Registration_Date DATE                       -- Member enrollment date
);

-- =============================================================================
-- 4. DIMENSION TABLE: Dim_Store
-- Captures physical supermarket terminal and store geography
-- =============================================================================
CREATE TABLE Dim_Store (
    Store_Key INT AUTO_INCREMENT PRIMARY KEY,    -- Surrogate Key
    Counter_Code VARCHAR(20) NOT NULL,           -- 'C1', 'C2', 'C3', 'C4'
    Counter_Name VARCHAR(50) NOT NULL,           -- 'Counter 1 - Express', etc.
    Counter_Type VARCHAR(30) NOT NULL,           -- 'Express', 'Regular', 'Self-Service'
    Store_Branch VARCHAR(50) DEFAULT 'FreshMart - Gota Branch',
    City VARCHAR(30) DEFAULT 'Ahmedabad',
    State VARCHAR(30) DEFAULT 'Gujarat'
);

-- =============================================================================
-- 5. DIMENSION TABLE: Dim_Payment
-- Captures payment channel and financial settlement details
-- =============================================================================
CREATE TABLE Dim_Payment (
    Payment_Key INT AUTO_INCREMENT PRIMARY KEY,  -- Surrogate Key
    Payment_Mode VARCHAR(30) NOT NULL,           -- 'UPI', 'Cash', 'Credit Card', 'Debit Card'
    Payment_Channel VARCHAR(30) NOT NULL,        -- 'Digital Realtime', 'Physical Currency', 'Card POS'
    Gateway_Provider VARCHAR(40) NOT NULL        -- 'NPCI / UPI', 'Reserve Bank / Cash', 'Visa/Mastercard'
);

-- =============================================================================
-- 6. CENTRAL FACT TABLE: Fact_Sales
-- Grain: One row per scanned line-item on a customer receipt
-- Contains Foreign Keys pointing to dimensions + Fully Additive Numeric Measures
-- =============================================================================
CREATE TABLE Fact_Sales (
    Sales_Fact_Key BIGINT AUTO_INCREMENT PRIMARY KEY, -- Fact surrogate key
    
    -- Foreign Keys to Conformed Dimensions
    Date_Key INT NOT NULL,
    Product_Key INT NOT NULL,
    Customer_Key INT NOT NULL,
    Store_Key INT NOT NULL,
    Payment_Key INT NOT NULL,
    
    -- Degenerate Dimension (Receipt Invoice Number)
    Transaction_ID VARCHAR(30) NOT NULL,
    
    -- Fully Additive Measures
    Quantity_Sold INT NOT NULL CHECK (Quantity_Sold > 0),
    Unit_Price_INR DECIMAL(10, 2) NOT NULL,
    Discount_Percent DECIMAL(5, 2) DEFAULT 0.0,
    Discount_Amount_INR DECIMAL(10, 2) DEFAULT 0.0,
    Line_Total_INR DECIMAL(10, 2) NOT NULL,
    Estimated_Cost_INR DECIMAL(10, 2) NOT NULL,
    Net_Profit_INR DECIMAL(10, 2) NOT NULL,
    
    -- Foreign Key Referential Integrity Constraints
    CONSTRAINT fk_sales_date FOREIGN KEY (Date_Key) REFERENCES Dim_Date(Date_Key),
    CONSTRAINT fk_sales_product FOREIGN KEY (Product_Key) REFERENCES Dim_Product(Product_Key),
    CONSTRAINT fk_sales_customer FOREIGN KEY (Customer_Key) REFERENCES Dim_Customer(Customer_Key),
    CONSTRAINT fk_sales_store FOREIGN KEY (Store_Key) REFERENCES Dim_Store(Store_Key),
    CONSTRAINT fk_sales_payment FOREIGN KEY (Payment_Key) REFERENCES Dim_Payment(Payment_Key)
);

-- =============================================================================
-- Performance Optimization: B-Tree Indexes on Foreign Keys for Fast OLAP Joins
-- =============================================================================
CREATE INDEX idx_fact_date ON Fact_Sales(Date_Key);
CREATE INDEX idx_fact_product ON Fact_Sales(Product_Key);
CREATE INDEX idx_fact_customer ON Fact_Sales(Customer_Key);
CREATE INDEX idx_fact_store ON Fact_Sales(Store_Key);
CREATE INDEX idx_fact_payment ON Fact_Sales(Payment_Key);
CREATE INDEX idx_fact_trans ON Fact_Sales(Transaction_ID);
