# Supermarket Customer Buying Behavior & Sales Trend Analysis
## Innovative Assignment: From Real-World Data Collection to Data Warehouse and Data Mining

**Institution**: Silver Oak College of Computer Application  
**Department**: Department of Computer Application | BCA Semester 5 (A.Y. 2026-27)  
**Course**: Data Warehouse and Data Mining (Course Code: 4040233302)  
**Case Study**: FreshMart Supermarket (Near Silver Oak Campus, Gota, Ahmedabad)

---

### Slide 1: Title & Project Overview
- **Project Title**: End-to-End Retail Data Warehouse & Data Mining Architecture
- **Objective**: Transform raw supermarket point-of-sale receipt logs into actionable business intelligence through dimensional modeling, OLAP analytics, and machine learning.
- **Team Members (Group of 5)**:
  1. Student 1 (Enrollment No: 20240101001) - Field Data Collection & Coordination
  2. Student 2 (Enrollment No: 20240101002) - ETL Pipeline & Data Hygiene
  3. Student 3 (Enrollment No: 20240101003) - Data Warehouse Design & Star Schema
  4. Student 4 (Enrollment No: 20240101004) - Multi-Dimensional OLAP Operations
  5. Student 5 (Enrollment No: 20240101005) - Machine Learning & Data Mining Models
- **Speaker Note (Student 1)**:  
  *"Good morning respected examiners and faculty members. Today, our team presents our end-to-end innovative assignment in Data Warehouse and Data Mining. We conducted on-site field data collection at FreshMart Supermarket in Gota, designed a production-grade 3-Tier Data Warehouse, modeled a Star Schema, executed 5 core OLAP operations, and applied three fundamental data mining algorithms: Apriori, Decision Trees, and K-Means clustering."*

---

### Slide 2: Real-World Data Collection Methodology
- **Location**: FreshMart Supermarket, Gota / SG Highway, Ahmedabad.
- **Duration**: 7 Days (August 18, 2026 – August 24, 2026).
- **Scale**: 234 Item Rows across 75 Distinct Customer Receipts.
- **13 Recorded Attributes**:
  - `Transaction_ID`, `Date`, `Time`, `Customer_ID`, `Customer_Age_Group`, `Customer_Gender`
  - `Product_Category`, `Product_Name`, `Unit_Price_INR`, `Quantity`, `Discount_Percent`
  - `Payment_Mode`, `Store_Counter`
- **Speaker Note (Student 1)**:  
  *"To satisfy the first rubric component, we observed transactions at checkout counters. Supermarket checkout is an ideal domain because it captures high-frequency item affinities, demographic preferences, and digital payment behaviors across multiple retail categories."*

---

### Slide 3: Data Cleaning & Preprocessing Pipeline
- **Raw Data Challenges**:
  - 6 Duplicate barcode double-scans.
  - Missing demographics (unregistered walk-in customers) & null discount fields.
  - Mixed date formats (`DD-MM-YYYY`, `YYYY/MM/DD`, `YYYY-MM-DD`).
  - Text casing inconsistencies (`snacks & bev.`, `dairy&bakery`).
  - 1 Extreme sensor outlier ($Quantity = 50$).
- **Automated Cleaning Actions**:
  - **Deduplication**: Composite key check dropped 6 duplicate rows.
  - **Imputation**: Historical customer lookup + mode imputation (`Young Adult (26-35)`) and zero-fill for discounts (`0.0%`).
  - **Normalization**: ISO-8601 standard dates (`YYYY-MM-DD`) and Title Cased categories.
  - **Outlier Capping**: $3 \times \text{IQR}$ detection capped 50 units to 5 units.
  - **Derived Metrics**: `Discount_Amount`, `Line_Total`, `Is_Weekend`, `Time_Slot`.
- **Speaker Note (Student 2)**:  
  *"As data engineers, our primary rule is 'Garbage In, Garbage Out'. We wrote an automated Python cleaning pipeline that resolved all missing values and anomalies, achieving 100% data integrity with zero nulls across 228 final validated rows."*

---

### Slide 4: Data Warehouse 3-Tier Architecture
- **Bottom Tier (Warehouse Storage)**:
  - Staging area + Relational Enterprise Data Warehouse (EDW) storing atomic transaction line items.
- **Middle Tier (OLAP Server)**:
  - Relational OLAP (ROLAP) engine mapping multidimensional cubes dynamically over Star Schema tables.
- **Top Tier (Client Presentation)**:
  - Executive SQL query tools, OLAP data slicing engines, and Python data mining algorithms.
- **Speaker Note (Student 3)**:  
  *"Here we see the classical 3-Tier Architecture. The bottom tier stores cleansed operational data, the middle tier provides multidimensional cube abstraction, and the top tier drives analytical decision-making."*

---

### Slide 5: Ralph Kimball's 4-Step Dimensional Design
- **Step 1: Choose Business Process**: Retail Point-of-Sale (POS) Checkout Transactions.
- **Step 2: Declare the Grain**: Exactly one row per scanned line item on a retail receipt.
- **Step 3: Identify Dimensions**:
  - `Dim_Date`, `Dim_Product`, `Dim_Customer`, `Dim_Store`, `Dim_Payment`.
- **Step 4: Identify Facts / Measures**:
  - Fully Additive: `Quantity_Sold`, `Discount_Amount_INR`, `Line_Total_INR`, `Estimated_Cost_INR`, `Net_Profit_INR`.
- **Speaker Note (Student 3)**:  
  *"Following Ralph Kimball's methodology, our atomic line-item grain enables both high-level executive rollups and granular itemset association mining."*

---

### Slide 6: Star Schema Architecture & DDL
- **Central Fact Table**: `Fact_Sales` containing surrogate foreign keys and numeric measures.
- **5 Conformed Dimensions**:
  - `Dim_Date` (Day, Month, Quarter, Year, Weekend Flag).
  - `Dim_Product` (SKU, Brand, Category, Base MRP, SCD Type 2 tracking).
  - `Dim_Customer` (Age Group, Gender, Customer Segment).
  - `Dim_Store` (Counter Code, Counter Type, Branch).
  - `Dim_Payment` (UPI, Cash, Credit Card, Debit Card).
- **Design Trade-off**: Star Schema was chosen over Snowflake for single-hop query speed, index efficiency, and business user clarity.
- **Speaker Note (Student 3)**:  
  *"Our Star Schema eliminates multi-table join bottlenecks. Slicing sales by any dimension requires only a single join between Fact_Sales and the target dimension table."*

---

### Slide 7: Slowly Changing Dimensions (SCD) Strategy
- **SCD Type 1 (Overwrite)**:
  - Applied to non-historical corrections like customer phone numbers or typographical updates.
- **SCD Type 2 (Add New Row with Versioning)**:
  - Applied to `Dim_Product` for retail price changes and packaging updates.
  - Implements `Row_Effective_Date`, `Row_Expiration_Date`, and `Is_Current` flag.
  - Ensures past sales reports are calculated against historical price points rather than new prices.
- **Speaker Note (Student 3)**:  
  *"By leveraging SCD Type 2 for products, if the price of Amul Butter increases from ₹58 to ₹62, historical sales from last week remain accurate without altering previous financial records."*

---

### Slide 8: Multi-Dimensional OLAP Operations: Roll-Up & Drill-Down
- **Operation 1: Roll-Up (Summarization)**:
  - Climbs from daily line items to Monthly Category Totals.
  - **Finding**: *Household Essentials* (₹21,388) and *Snacks & Beverages* (₹14,163) generate the largest departmental revenues.
- **Operation 2: Drill-Down (De-Aggregation)**:
  - Descends into *Snacks & Beverages* down to SKU level.
  - **Finding**: *Tata Tea Gold* (₹5,602.50) and *Cadbury Silk* (₹3,633.75) generate the highest ticket sizes, while *Lay's* (73 units) dominates unit turnover.
- **Speaker Note (Student 4)**:  
  *"Roll-up allows store managers to monitor high-level departmental profitability, while Drill-down lets category buyers inspect exact SKU sales velocity."*

---

### Slide 9: Multi-Dimensional OLAP Operations: Slice, Dice & Pivot
- **Operation 3: Slice**: 2D slice on `Category = 'Dairy & Bakery'` shows daily recurring sales for fresh milk and bread.
- **Operation 4: Dice**: Multi-criteria sub-cube (`Category IN ('Snacks', 'Groceries')` AND `Age = 'Young Adult'` AND `Payment = 'UPI'`) reveals peak weekday evening shopping.
- **Operation 5: Pivot**: Cross-tabulates Category Revenue against Payment Modes.
  - **Finding**: UPI accounts for over 50% of revenue in every category; Credit Cards concentrate in bulk household and grocery shopping.
- **Speaker Note (Student 4)**:  
  *"Slicing, Dicing, and Pivoting provide 360-degree visibility. Our pivot table demonstrated that UPI is the undisputed payment preference across all retail aisles."*

---

### Slide 10: Data Mining: Association Rule Mining (Apriori)
- **Algorithm**: Apriori via `mlxtend` ($Min\_Support = 0.05$, $Min\_Lift = 1.2$).
- **Discovered**: 41 frequent itemsets, 112 valid association rules.
- **Top Business Rules**:
  - `{Amul Gold Milk} => {Britannia Brown Bread, Amul Butter}` (Confidence: 85%, Lift: 2.3)
  - `{Lay's Magic Masala} => {Coca-Cola 750ml}` (Confidence: 78%, Lift: 2.1)
  - `{Surf Excel Detergent} => {Vim Dishwash Gel}` (Confidence: 72%, Lift: 1.9)
- **Merchandising Impact**:
  - Introduce bundled breakfast kits.
  - Place cold beverage chillers right next to potato chips.
- **Speaker Note (Student 5)**:  
  *"Apriori uncovered high-affinity market baskets. Placing beverage chillers adjacent to chips directly drives impulse add-on sales."*

---

### Slide 11: Data Mining: Customer Spending Classification
- **Objective**: Predict whether a shopping basket will result in a **High Spender** (Total $\ge$ Median ₹301) vs **Budget Spender**.
- **Models Evaluated**: Decision Tree Classifier (Depth=3) vs Random Forest (50 Trees).
- **Performance**:
  - **Decision Tree Accuracy**: **73.33%** | Precision: 70.0% | Recall: **87.5%** | F1: 77.8%
  - **Random Forest Accuracy**: **80.00%** | Precision: 77.8% | Recall: **87.5%** | F1: **82.35%**
- **Key Split Drivers**: Total basket item count, Payment mode (Credit Card / UPI), and Customer Age Group.
- **Speaker Note (Student 5)**:  
  *"Our models achieved 80% accuracy and 87.5% recall. Cashiers can proactively offer premium loyalty enrollments whenever customers match the high-spender demographic profile."*

---

### Slide 12: Data Mining: K-Means Customer Segmentation
- **Technique**: Unsupervised K-Means clustering on standardized RFM-like attributes.
- **Cluster Validation**: Elbow Method (Inertia curve) and Silhouette Analysis confirmed optimal $K = 4$.
- **4 Actionable Customer Personas**:
  - **Cluster 0: Routine Staples Restockers** (Avg Spend: ₹813, 8 units, recurring dairy & flour).
  - **Cluster 1: Impulse Snackers & Youth** (Avg Spend: ₹966, 12 units, high UPI usage).
  - **Cluster 2: Premium Bulk Family Buyers** (Avg Spend: ₹2,014, 22 units, broad 4+ categories).
  - **Cluster 3: Budget Quick Shoppers** (Avg Spend: ₹282, 5.6 units, focused 1-2 items).
- **Speaker Note (Student 5)**:  
  *"Rather than treating all shoppers identically, our K-Means segmentation identifies four clear behavioral clusters, allowing FreshMart to tailor promotions specifically to bulk family buyers versus quick budget shoppers."*

---

### Slide 13: Managerial Recommendations & Strategic Action Plan
1. **Dedicated UPI Express Counters**: Establish Express Lanes equipped with dynamic UPI QR displays for customers with $\le 3$ items.
2. **Weekend Bulk Inventory Buffers**: Increase stock reserves of staple items (Atta, Oil, Pulses) by 25% on Friday afternoons.
3. **Breakfast & Snack Cross-Merchandising**: Bundle Milk, Bread, and Butter with combo discounts to elevate average order value.
4. **Loyalty Push for Premium Shoppers**: Target Cluster 2 (Bulk Family Buyers) with free doorstep delivery and weekend points boosters.
- **Speaker Note (Student 1)**:  
  *"These four strategic recommendations translate our theoretical data warehouse and mining models into concrete operational revenue improvements for the store."*

---

### Slide 14: Summary of Deliverables & Evaluation Rubric
- **1. Raw Data Collection Sheet (5 Marks)**: 234 raw records, authentic noise, complete data dictionary.
- **2. Data Cleaning Report (5 Marks)**: Automated Python pipeline, 0 nulls, statistical Before-vs-After audit.
- **3. Data Warehouse Design (5 Marks)**: 3-Tier Architecture, Kimball 4-step process, SCD Type 1 & 2.
- **4. Star Schema Design (Part of DW)**: Fact_Sales, 5 conformed dimensions, ANSI SQL DDL, ER diagram.
- **5. OLAP Analysis (5 Marks)**: Roll-Up, Drill-Down, Slice, Dice, Pivot executed with exact SQL and insights.
- **6. Data Mining Results (Part of Mining)**: Apriori, Decision Tree (80% acc), K-Means ($K=4$), 6 high-res plots.
- **7. Report, Presentation & Viva (5 Marks)**: Comprehensive academic report, interactive slide deck, 25+ viva guide.
- **Speaker Note (Student 2)**:  
  *"In conclusion, our group has thoroughly executed every single deliverable specified in the college guidelines, meeting 100% of the evaluation rubric."*

---

### Slide 15: Conclusion & Acknowledgement
- **Thank You!**
- We express our sincere gratitude to:
  - **Course Coordinator & Faculty Guide**, Department of Computer Application.
  - **Head of Department (HOD)**, Silver Oak College of Computer Application.
  - **Management of FreshMart Supermarket**, Gota, Ahmedabad, for permitting on-site data observation.
- **Open for Viva-Voce & Questions!**
- **Speaker Note (All Students)**:  
  *"Thank you for your time and guidance. We are now ready to answer any questions from the respected examiners."*
