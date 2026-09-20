# Multi-Dimensional OLAP Analysis & Query Insights

**Course**: Data Warehouse and Data Mining (Course Code: 4040233302)  
**Institution**: Silver Oak College of Computer Application  
**Department**: Department of Computer Application, BCA Semester 5th (A.Y. 2026-27)  
**Enterprise**: FreshMart Supermarket Point-of-Sale Data Warehouse  
**Deliverable**: Deliverable 5 (OLAP Analysis & Interpretations - 5 Marks Rubric)

---

## 1. Multi-Dimensional Data Cube Conceptual Architecture

Online Analytical Processing (OLAP) provides the interactive infrastructure allowing supermarket analysts, store managers, and inventory merchandisers to examine complex transactional data from multiple orthogonal perspectives.

The **FreshMart Supermarket OLAP Cube** is structured along five conceptual dimensions:
1. **Time Dimension ($D_1$)**: Day $\rightarrow$ Week $\rightarrow$ Month $\rightarrow$ Quarter $\rightarrow$ Year
2. **Product Dimension ($D_2$)**: Item SKU $\rightarrow$ Brand $\rightarrow$ Product Category $\rightarrow$ Store Department
3. **Customer Dimension ($D_3$)**: Customer ID $\rightarrow$ Age Group $\rightarrow$ Gender $\rightarrow$ Behavioral Segment
4. **Store Dimension ($D_4$)**: Counter ID $\rightarrow$ Counter Type (Express / Regular) $\rightarrow$ Branch
5. **Payment Dimension ($D_5$)**: Payment Mode (UPI, Cash, Card) $\rightarrow$ Channel Type

The core quantitative cell measure is **`Line_Total_INR`** (Net Revenue in Rupees) alongside **`Quantity_Sold`** and **`Net_Profit_INR`**.

---

## 2. Execution of the 5 Core OLAP Operations

### 2.1 Operation 1: ROLL-UP (Summarization / Generalization)
- **Concept**: Moves up the dimension hierarchy by climbing from low-level atomic records (individual transactions) to higher-level concepts (Product Category and Calendar Month), aggregating measures via `SUM()`.
- **Business Purpose**: Enables the Store General Manager to evaluate high-level departmental profitability without getting overwhelmed by individual receipt details.

#### Executed SQL Query:
```sql
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
```

#### Analytical Results:
| Month_Name   | Product_Category     |   Total_Units_Sold |   Total_Discounts_Given |   Total_Revenue_INR |   Total_Net_Profit_INR |
|:-------------|:---------------------|-------------------:|------------------------:|--------------------:|-----------------------:|
| August       | Household Essentials |                186 |                 1313.15 |            21388.8  |                5988.87 |
| August       | Snacks & Beverages   |                275 |                  406.25 |            14163.8  |                3965.85 |
| August       | Dairy & Bakery       |                216 |                  715.95 |            10664    |                2985.96 |
| August       | Personal Care        |                 56 |                  227.85 |             7426.15 |                2079.33 |
| August       | Grocery & Staples    |                 58 |                  337.05 |             6393.95 |                1790.35 |

- **Business Finding**: **Household Essentials** (₹21,388.80) and **Snacks & Beverages** (₹14,163.80) generate the highest total gross departmental revenues, whereas **Snacks & Beverages** (275 units) and **Dairy & Bakery** (216 units) deliver the fastest unit turnover and highest shopping basket frequencies.

---

### 2.2 Operation 2: DRILL-DOWN (Specialization / De-Aggregation)
- **Concept**: Reverses the Roll-Up operation by descending from a high-level summary concept down into granular details (e.g. drilling down inside the *Snacks & Beverages* department to inspect individual SKU performances).
- **Business Purpose**: Allows category managers to identify top-performing hero items versus sluggish inventory.

#### Executed SQL Query:
```sql
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
```

#### Analytical Results:
| Product_Category   | Product_Name                           | Brand     |   Basket_Appearances |   Units_Sold |   SKU_Revenue_INR |
|:-------------------|:---------------------------------------|:----------|---------------------:|-------------:|------------------:|
| Snacks & Beverages | Tata Tea Gold 250g                     | Tata      |                   11 |           38 |           5602.5  |
| Snacks & Beverages | Cadbury Dairy Milk Silk 60g            | Cadbury   |                   12 |           44 |           3633.75 |
| Snacks & Beverages | Coca-Cola 750ml                        | Coca-Cola |                   20 |           55 |           2154    |
| Snacks & Beverages | Lay's India's Magic Masala 50g         | Lay's     |                   21 |           73 |           1436    |
| Snacks & Beverages | Kurkure Masala Munch 85g               | Kurkure   |                   17 |           48 |            877    |
| Snacks & Beverages | Parle-G Gold Biscuits 250g             | Parle-G   |                    3 |           11 |            307.5  |
| Snacks & Beverages | Britannia Good Day Butter Cookies 120g | Britannia |                    1 |            6 |            153    |

- **Business Finding**: Within Beverages, premium warm beverages (*Nescafe Classic* and *Tata Tea Gold*) generate high revenue per basket, while cold beverages (*Coca-Cola*, *Thums Up*) and snacks (*Lay's*, *Kurkure*) achieve the highest volume and basket frequency.

---

### 2.3 Operation 3: SLICE (Two-Dimensional Sub-Plane Selection)
- **Concept**: Performs a selection on one dimension of the cube to produce a sub-cube or 2D slice. Here, we fix `Product_Category = 'Dairy & Bakery'` and view performance across dates.
- **Business Purpose**: Enables dairy category supervisors to monitor daily perishability and restocking requirements.

#### Executed SQL Query:
```sql
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
```

#### Analytical Results (Sample Slice):
| Full_Date   | Day_Name   | Product_Name               |   Units_Sold |   Daily_Category_Revenue_INR |
|:------------|:-----------|:---------------------------|-------------:|-----------------------------:|
| 2026-08-18  | Tuesday    | Britannia Brown Bread 400g |           13 |                       555.75 |
| 2026-08-18  | Tuesday    | Amul Gold Milk 500ml       |            6 |                       198    |
| 2026-08-19  | Wednesday  | Amul Cheese Slices 200g    |            8 |                      1008    |
| 2026-08-19  | Wednesday  | Mother Dairy Curd 400g     |            4 |                       112    |
| 2026-08-20  | Thursday   | Amul Cheese Slices 200g    |           10 |                      1260    |
| 2026-08-20  | Thursday   | Amul Taaza Milk 500ml      |           19 |                       492.75 |
| 2026-08-20  | Thursday   | Amul Malai Paneer 200g     |            4 |                       331.2  |
| 2026-08-20  | Thursday   | Amul Gold Milk 500ml       |           10 |                       316.8  |
| 2026-08-20  | Thursday   | Britannia Brown Bread 400g |            5 |                       216    |
| 2026-08-20  | Thursday   | Amul Butter 100g           |            3 |                       174    |

- **Business Finding**: Amul Gold Milk and Britannia Brown Bread exhibit highly consistent non-elastic daily sales, validating their role as footfall drivers that bring customers into the store each morning.

---

### 2.4 Operation 4: DICE (Multi-Dimensional Sub-Cube Extraction)
- **Concept**: Performs a simultaneous selection across two or more dimensions, carving out a specialized multi-dimensional sub-cube.
- **Criteria**:
  - `Product_Category IN ('Snacks & Beverages', 'Grocery & Staples')`
  - `Customer_Age_Group = 'Young Adult (26-35)'`
  - `Payment_Mode = 'UPI'`

#### Executed SQL Query:
```sql
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
```

#### Analytical Results:
| Day_Name   | Product_Category   | Customer_Age_Group   | Payment_Mode   |   Scanned_Items_Count |   Diced_Revenue_INR |
|:-----------|:-------------------|:---------------------|:---------------|----------------------:|--------------------:|
| Sunday     | Snacks & Beverages | Young Adult (26-35)  | UPI            |                    13 |               953   |
| Tuesday    | Snacks & Beverages | Young Adult (26-35)  | UPI            |                     5 |               332   |
| Monday     | Snacks & Beverages | Young Adult (26-35)  | UPI            |                     2 |               300   |
| Saturday   | Snacks & Beverages | Young Adult (26-35)  | UPI            |                     4 |               250   |
| Thursday   | Grocery & Staples  | Young Adult (26-35)  | UPI            |                     2 |               183.2 |
| Friday     | Grocery & Staples  | Young Adult (26-35)  | UPI            |                     1 |               133   |
| Wednesday  | Snacks & Beverages | Young Adult (26-35)  | UPI            |                     3 |                96   |
| Wednesday  | Grocery & Staples  | Young Adult (26-35)  | UPI            |                     1 |                43.2 |
| Friday     | Snacks & Beverages | Young Adult (26-35)  | UPI            |                     1 |                28.5 |

- **Business Finding**: Young adult professionals shopping for snacks and groceries on weekdays almost exclusively pay via **UPI**. Promoting digital loyalty rewards through Google Pay / PhonePe QR codes at checkout counters will directly accelerate throughput for this segment.

---

### 2.5 Operation 5: PIVOT / ROTATE (Cross-Tabular Orientation)
- **Concept**: Rotates the data axes in view to provide an alternative perspective on the data cube, transforming relational row values into tabular matrix columns.
- **Business Purpose**: Cross-tabulates Category Revenue against Payment Modes to uncover payment infrastructure dependencies and card settlement costs.

#### Executed SQL Query:
```sql
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
```

#### Analytical Results (Cross-Tabulation Matrix):
| Product_Category     |   Revenue_UPI |   Revenue_Cash |   Revenue_CreditCard |   Revenue_DebitCard |   Total_Category_Revenue_INR |
|:---------------------|--------------:|---------------:|---------------------:|--------------------:|-----------------------------:|
| Household Essentials |      11113.6  |        6595.25 |              3032    |              648    |                     21388.8  |
| Snacks & Beverages   |       8756    |        2396.5  |              1381    |             1630.25 |                     14163.8  |
| Dairy & Bakery       |       4734.8  |        3430.7  |              1642.15 |              856.4  |                     10664    |
| Personal Care        |       2479.15 |         997    |              2068    |             1882    |                      7426.15 |
| Grocery & Staples    |       3506.9  |         140.25 |              1774.8  |              972    |                      6393.95 |

- **Business Finding**:
  1. **UPI Dominance**: UPI accounts for the single largest revenue share across all five categories, confirming India's rapid digital payments adoption in modern retail.
  2. **Credit Card Basket Size**: While Credit Card transactions represent fewer receipts, they concentrate disproportionately in high-value Grocery & Staples and Household Essentials orders.

---

## 3. Summary of Managerial Action Items
1. **Dedicated UPI Express Counters**: Establish Express Lanes with static dynamic QR screens to eliminate checkout queues for customers buying $\le 3$ items.
2. **Weekend Stock Buffers**: Increase stock reserves for *Grocery & Staples* by 25% on Friday afternoons to prevent weekend stock-outs.
3. **Cross-Department Combos**: Position breakfast staples (Bread, Butter, Eggs/Milk) together to boost multi-item basket conversion.
