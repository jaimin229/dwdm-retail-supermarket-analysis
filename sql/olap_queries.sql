-- =============================================================================
-- Silver Oak College of Computer Application | BCA Semester 5
-- Course: Data Warehouse and Data Mining (4040233302)
-- Deliverable 5: Comprehensive OLAP Operations & Multi-Dimensional SQL Queries
-- =============================================================================

-- =============================================================================
-- 1. OLAP OPERATION: ROLL-UP
-- Aggregates daily transaction line items up to Monthly & Category summary levels
-- =============================================================================
SELECT 
    d.Month_Name,
    p.Product_Category,
    SUM(f.Quantity_Sold) AS Total_Units_Sold,
    ROUND(SUM(f.Discount_Amount_INR), 2) AS Total_Discounts_Given,
    ROUND(SUM(f.Line_Total_INR), 2) AS Total_Revenue_INR,
    ROUND(SUM(f.Net_Profit_INR), 2) AS Total_Net_Profit_INR
FROM Fact_Sales f
JOIN Dim_Date d ON f.Date_Key = d.Date_Key
JOIN Dim_Product p ON f.Product_Key = p.Product_Key
GROUP BY d.Month_Name, p.Product_Category
ORDER BY Total_Revenue_INR DESC;

-- =============================================================================
-- 2. OLAP OPERATION: DRILL-DOWN
-- Explodes high-level category totals down to granular SKU performance
-- =============================================================================
SELECT 
    p.Product_Category,
    p.Product_Name,
    p.Brand,
    COUNT(DISTINCT f.Transaction_ID) AS Basket_Appearances,
    SUM(f.Quantity_Sold) AS Units_Sold,
    ROUND(SUM(f.Line_Total_INR), 2) AS SKU_Revenue_INR
FROM Fact_Sales f
JOIN Dim_Product p ON f.Product_Key = p.Product_Key
WHERE p.Product_Category = 'Snacks & Beverages'
GROUP BY p.Product_Category, p.Product_Name, p.Brand
ORDER BY SKU_Revenue_INR DESC;

-- =============================================================================
-- 3. OLAP OPERATION: SLICE
-- Extracts a two-dimensional sub-plane by fixing Category = 'Dairy & Bakery'
-- =============================================================================
SELECT 
    d.Full_Date,
    d.Day_Name,
    p.Product_Name,
    SUM(f.Quantity_Sold) AS Units_Sold,
    ROUND(SUM(f.Line_Total_INR), 2) AS Daily_Category_Revenue_INR
FROM Fact_Sales f
JOIN Dim_Date d ON f.Date_Key = d.Date_Key
JOIN Dim_Product p ON f.Product_Key = p.Product_Key
WHERE p.Product_Category = 'Dairy & Bakery'
GROUP BY d.Full_Date, d.Day_Name, p.Product_Name
ORDER BY d.Full_Date ASC, Daily_Category_Revenue_INR DESC
LIMIT 10;

-- =============================================================================
-- 4. OLAP OPERATION: DICE
-- Constructs a focused multi-dimensional sub-cube via multi-criteria constraints
-- (Category IN ('Snacks & Beverages', 'Grocery & Staples') AND Age = 'Young Adult' AND Payment = 'UPI')
-- =============================================================================
SELECT 
    d.Day_Name,
    p.Product_Category,
    c.Customer_Age_Group,
    py.Payment_Mode,
    COUNT(f.Sales_Fact_Key) AS Scanned_Items_Count,
    ROUND(SUM(f.Line_Total_INR), 2) AS Diced_Revenue_INR
FROM Fact_Sales f
JOIN Dim_Date d ON f.Date_Key = d.Date_Key
JOIN Dim_Product p ON f.Product_Key = p.Product_Key
JOIN Dim_Customer c ON f.Customer_Key = c.Customer_Key
JOIN Dim_Payment py ON f.Payment_Key = py.Payment_Key
WHERE p.Product_Category IN ('Snacks & Beverages', 'Grocery & Staples')
  AND c.Customer_Age_Group = 'Young Adult (26-35)'
  AND py.Payment_Mode = 'UPI'
GROUP BY d.Day_Name, p.Product_Category, c.Customer_Age_Group, py.Payment_Mode
ORDER BY Diced_Revenue_INR DESC;

-- =============================================================================
-- 5. OLAP OPERATION: PIVOT (Cross-Tabulation)
-- Rotates axes to analyze Category Revenue broken down across all Payment Channels
-- =============================================================================
SELECT 
    p.Product_Category,
    ROUND(SUM(CASE WHEN py.Payment_Mode = 'UPI' THEN f.Line_Total_INR ELSE 0 END), 2) AS Revenue_UPI,
    ROUND(SUM(CASE WHEN py.Payment_Mode = 'Cash' THEN f.Line_Total_INR ELSE 0 END), 2) AS Revenue_Cash,
    ROUND(SUM(CASE WHEN py.Payment_Mode = 'Credit Card' THEN f.Line_Total_INR ELSE 0 END), 2) AS Revenue_CreditCard,
    ROUND(SUM(CASE WHEN py.Payment_Mode = 'Debit Card' THEN f.Line_Total_INR ELSE 0 END), 2) AS Revenue_DebitCard,
    ROUND(SUM(f.Line_Total_INR), 2) AS Total_Category_Revenue_INR
FROM Fact_Sales f
JOIN Dim_Product p ON f.Product_Key = p.Product_Key
JOIN Dim_Payment py ON f.Payment_Key = py.Payment_Key
GROUP BY p.Product_Category
ORDER BY Total_Category_Revenue_INR DESC;
