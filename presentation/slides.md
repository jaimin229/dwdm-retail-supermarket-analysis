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
  - `Dim_Date` (When), `Dim_Product` (What), `Dim_Customer` (Who), `Dim_Store` (Where), `Dim_Payment` (How).
- **Step 4: Identify Facts / Measures**:
  - Fully Additive: `Quantity_Sold`, `Discount_Amount_INR`, `Line_Total_INR`, `Estimated_Cost_INR`, `Net_Profit_INR`.
- **Slowly Changing Dimensions (SCD) Policy**:
  - **SCD Type 1 (Overwrite)**: Applied to non-historical demographic corrections.
  - **SCD Type 2 (History Preservation)**: Applied to `Dim_Product` using `Row_Effective_Date`, `Row_Expiration_Date`, and `Is_Current` flags for retail price changes.
- **Speaker Note (Student 3)**:  
  *"Following Ralph Kimball's methodology, our atomic line-item grain enables both high-level executive rollups and granular itemset association mining. SCD Type 2 ensures historical price changes don't distort past reports."*

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

### Slide 7: OLAP Operations: Roll-Up & Drill-Down
- **Operation 1: Roll-Up (Summarization)**:
  - Climbs from daily line items to Monthly Category Totals.
  - **Finding**: *Household Essentials* (₹21,388.80) and *Snacks & Beverages* (₹14,163.80) generate the largest departmental revenues.
- **Operation 2: Drill-Down (De-Aggregation)**:
  - Descends into *Snacks & Beverages* down to SKU level.
  - **Finding**: *Tata Tea Gold* (₹5,602.50) and *Cadbury Silk* (₹3,633.75) generate the highest ticket sizes, while *Lay's* (73 units) dominates unit turnover.
- **Speaker Note (Student 4)**:  
  *"Roll-up allows store managers to monitor high-level departmental profitability, while Drill-down lets category buyers inspect exact SKU sales velocity."*

---

### Slide 8: OLAP Operations: Slice, Dice & Pivot
- **Operation 3: Slice**: 2D slice on `Category = 'Dairy & Bakery'` shows daily recurring sales for fresh milk and bread.
- **Operation 4: Dice**: Multi-criteria sub-cube (`Category IN ('Snacks', 'Groceries')` AND `Age = 'Young Adult'` AND `Payment = 'UPI'`) reveals peak weekday evening shopping.
- **Operation 5: Pivot**: Cross-tabulates Category Revenue against Payment Modes.
  - **Exact Finding**: UPI accounts for ₹30,590.45 (50.95% of total revenue) dominating all aisles; Cash represents ₹13,559.70 (22.59%); Credit Cards represent ₹9,897.95 (16.49%) concentrated in bulk household orders; Debit Cards represent ₹5,988.65 (9.97%).
- **Speaker Note (Student 4)**:  
  *"Slicing, Dicing, and Pivoting provide 360-degree visibility. Our pivot table proved that UPI is the undisputed payment preference across all retail aisles."*

---

### Slide 9: Data Mining: Market Basket Analysis (Apriori)
- **Algorithm**: Apriori via `mlxtend` ($Min\_Support = 0.05$, $Min\_Lift = 1.2$).
- **Discovered**: 41 frequent itemsets, 112 valid association rules.
- **Top Business Rules**:
  - `{Harpic Cleaner, Surf Excel} => {Vim Dishwash Gel}` (Confidence: 88.9%, Lift: **5.13**)
  - `{Surf Excel Detergent} => {Vim Dishwash Gel}` (Confidence: 75.0%, Lift: **4.33**)
  - `{Amul Gold Milk} => {Britannia Brown Bread, Amul Butter}` (Confidence: 85.0%, Lift: **2.35**)
  - `{Lay's Magic Masala} => {Coca-Cola 750ml}` (Confidence: 78.2%, Lift: **2.18**)
- **Merchandising Impact**:
  - Co-locate cleaning agents on dedicated household end-caps.
  - Introduce bundled breakfast kits at the store entrance.
  - Place cold beverage chillers right next to potato chips.
- **Speaker Note (Student 5)**:  
  *"Apriori uncovered high-affinity market baskets. Placing cleaning agents together and beverage chillers adjacent to chips directly drives impulse add-on sales."*

---

### Slide 10: Data Mining: Customer Spending Classification
- **Objective**: Predict whether a shopping basket will result in a **High Spender** (Total $\ge$ Median ₹301.00) vs **Budget Spender**.
- **Models Evaluated**: Decision Tree Classifier (Depth=3) vs Random Forest (50 Trees).
- **Performance Benchmark**:
  - **Decision Tree**: Accuracy = 73.33% | Precision = 70.00% | Recall = 87.50% | F1 = 77.78%
  - **Random Forest**: Accuracy = **80.00%** | Precision = **77.78%** | Recall = **87.50%** | F1 = **82.35%**
- **Key Split Drivers**: Total basket item count, Payment mode (Credit Card / UPI), and Customer Age Group.
- **Speaker Note (Student 5)**:  
  *"Our models achieved 80% accuracy and 87.5% recall. Cashiers can proactively offer premium loyalty enrollments whenever customers match the high-spender demographic profile."*

---

### Slide 11: Data Mining: Decision Tree Hierarchy & Split Rules
- **White-Box Tree Architecture**:
  - Root split on Total Item Count ($\ge 3$ items $\rightarrow$ High Spender probability 92%).
  - Secondary splits on Credit Card payment mode and weekend evening hours.
- **Feature Importance (Random Forest)**:
  - Total Basket Item Count (0.42 importance score).
  - Credit Card Payment Mode (0.21 importance score).
  - Customer Age Group - Middle-Aged (0.16 importance score).
- **Speaker Note (Student 5)**:  
  *"The Decision Tree's white-box interpretability gives supermarket staff transparent, explainable rules for customer checkout segmentation."*

---

### Slide 12: Data Mining: K-Means Customer Segmentation
- **Technique**: Unsupervised K-Means clustering on standardized RFM attributes.
- **Cluster Validation**: Elbow Method (Inertia curve inflection) and Silhouette Analysis confirmed optimal $K = 4$.
- **4 Data-Driven Customer Personas**:
  - **Cluster 3: Budget Quick Shoppers** (Avg Spend: ₹282.07, 5.6 units, 1.5 categories).
  - **Cluster 0: Routine Staples Restockers** (Avg Spend: ₹812.94, 8.0 units, 1.5 categories).
  - **Cluster 1: Impulse Snackers & Diverse Shoppers** (Avg Spend: ₹966.52, 12.1 units, 3.3 categories).
  - **Cluster 2: Premium Bulk Grocery Buyers** (Avg Spend: ₹2,013.79, 22.3 units, 4.3 categories).
- **Speaker Note (Student 5)**:  
  *"K-Means segmentation identified four clear behavioral clusters, allowing FreshMart to tailor promotions specifically to bulk family buyers versus quick budget shoppers."*

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
