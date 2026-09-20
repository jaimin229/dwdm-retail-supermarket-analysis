# Master Viva-Voce Examination Guide: Data Warehouse & Data Mining

**Course**: Data Warehouse and Data Mining (Course Code: 4040233302)  
**Institution**: Silver Oak College of Computer Application, Department of Computer Application  
**Program**: Bachelor of Computer Application (BCA), Semester 5th (A.Y. 2026-27)  
**Project**: Retail Store / Supermarket Data Warehouse & Mining (FreshMart Case Study)

---

## Guide Overview

During the formal assessment (26/09/2026 to 30/09/2026), external and internal examiners evaluate both theoretical mastery and practical execution. This guide equips all team members with 25+ high-probability questions across five technical domains, complete with crisp, authoritative answers and project-specific defense points.

---

## Domain 1: Data Collection & Data Preprocessing (Fieldwork Defense)

### Q1. Why did you choose a retail supermarket domain for your innovative assignment?
**Answer**:
> *"Supermarkets represent the gold-standard operational domain for Data Warehouse and Data Mining. They generate high-velocity, multi-item transactional baskets that allow genuine demonstration of Ralph Kimball's dimensional modeling (Star Schema) and all three core data mining pillars: Market Basket Analysis (Apriori), Customer Classification (Decision Trees), and Customer Behavioral Segmentation (K-Means). Furthermore, real retail receipts exhibit authentic real-world data flaws like barcode double-scans and missing customer demographics, allowing us to showcase rigorous data cleaning."*

### Q2. What specific data flaws did you encounter in the raw data, and how did your pipeline resolve them?
**Answer**:
> *"In our raw dataset of 234 collected records from FreshMart Supermarket, we addressed four critical data quality issues:
> 1. **Duplicate Scans**: 6 redundant rows caused by cashier double-scanning were eliminated using composite key validation (`Transaction_ID`, `Product_Name`, `Time`).
> 2. **Missing Demographic Values**: Walk-in shoppers frequently bypassed loyalty registration. We imputed missing `Customer_Age_Group` using historical `Customer_ID` matching and statistical mode (`Young Adult (26-35)`). Missing discounts were zero-filled (`0.0%`).
> 3. **Format Heterogeneity**: Mixed date strings (`DD-MM-YYYY`, `YYYY/MM/DD`, `YYYY-MM-DD`) were normalized to strict ISO-8601 (`YYYY-MM-DD`), and product categories with erratic casing and abbreviations (e.g. 'snacks & bev.') were harmonized into 5 standardized departments.
> 4. **Statistical Outlier**: We detected an anomalous purchase quantity of 50 units on a perishable retail item using the $3 \times \text{IQR}$ threshold. With data steward sign-off, it was capped to the retail limit of 5 units to prevent centroid distortion in clustering."*

### Q3. Why use Interquartile Range (IQR) for outlier detection instead of standard Z-Score?
**Answer**:
> *"Z-Score relies on the mean and standard deviation, both of which are heavily sensitive to extreme outliers themselves. In skewed retail purchase distributions, extreme purchases artificially inflate the standard deviation, causing true outliers to be masked (masking effect). IQR relies on the median and percentiles ($Q_1$ and $Q_3$), which are non-parametric and robust against extreme values."*

---

## Domain 2: Data Warehouse Architecture & Dimensional Modeling

### Q4. Explain the Three-Tier Architecture of your Data Warehouse.
**Answer**:
> *"Our architecture consists of:
> 1. **Bottom Tier (Warehouse Storage)**: Contains the operational staging area and relational database hosting our conformed dimension tables and central `Fact_Sales` table.
> 2. **Middle Tier (OLAP Server)**: Employs a Relational OLAP (ROLAP) engine that models multi-dimensional cubes dynamically over our relational Star Schema, maintaining pre-aggregated summary tables for rapid querying.
> 3. **Top Tier (Front-End Presentation)**: Provides SQL querying, OLAP multi-dimensional slicing/dicing, and Python data mining algorithms (Apriori, Decision Trees, K-Means) for business decision-makers."*

### Q5. What is the difference between Ralph Kimball and Bill Inmon approaches to Data Warehousing? Which did you follow?
**Answer**:
> *"**Bill Inmon** champions a Top-Down approach: building an enterprise-wide, fully normalized (3NF) Corporate Information Factory first, from which departmental data marts are extracted.  
> **Ralph Kimball** champions a Bottom-Up dimensional approach: starting with business processes (like POS transactions) modeled directly into dimensional Star Schemas linked by conformed dimensions, creating an Enterprise Data Warehouse iteratively.  
> *We followed the **Kimball Approach** because it is business-process centric, query-optimized for OLAP, and far faster to deliver for modern retail operations."*

### Q6. Walk through the 4 steps of Kimball's Dimensional Design for your project.
**Answer**:
> *"1. **Choose the Business Process**: Retail Point-of-Sale (POS) checkout line-item scanning.  
> 2. **Declare the Grain**: Exactly one row per scanned line item on a customer sales receipt.  
> 3. **Identify the Dimensions**: `Dim_Date` (when), `Dim_Product` (what), `Dim_Customer` (who), `Dim_Store` (where), and `Dim_Payment` (how).  
> 4. **Identify the Facts/Measures**: `Quantity_Sold`, `Unit_Price_INR`, `Discount_Amount_INR`, `Line_Total_INR`, `Estimated_Cost_INR`, and `Net_Profit_INR`."*

### Q7. Why did you select a Star Schema over a Snowflake Schema?
**Answer**:
> *"The Star Schema keeps dimension tables completely denormalized. In our retail environment:
> - **Query Performance**: Slicing revenue by Product, Store, and Date requires only single-hop joins (`Fact_Sales` joined directly to each dimension). In a Snowflake schema, normalizing products into Categories, Subcategories, and Brands forces expensive multi-table joins that degrade OLAP responsiveness.
> - **Simplicity**: Business users and reporting tools can easily understand and query a Star Schema without complex SQL joins.
> - **Storage**: While Snowflake saves minor disk space by eliminating duplicate text strings, modern storage costs are negligible compared to query execution latency."*

### Q8. What is a Surrogate Key, and why not use operational Natural Keys (like Product Barcode or Invoice Number)?
**Answer**:
> *"A Surrogate Key is an artificially generated integer (e.g., `Product_Key INT AUTO_INCREMENT`) with no intrinsic business meaning. We decouple from operational natural keys because:
> 1. Natural keys can change or be reused by source operational systems.
> 2. Integer surrogate keys yield significantly faster join indexes and occupy less disk storage than variable-length alphanumeric strings.
> 3. Surrogate keys are mandatory to support **Slowly Changing Dimensions (SCD Type 2)**, allowing multiple historical rows for the same natural product code."*

### Q9. How does your Data Warehouse handle Slowly Changing Dimensions (SCD)?
**Answer**:
> *"We implement a hybrid strategy:
> - **SCD Type 1 (Overwrite)**: Applied to customer phone numbers or typographical corrections where historical values carry no analytical value.
> - **SCD Type 2 (Add New Row with History Tracking)**: Applied to `Dim_Product` for retail price and packaging changes. We maintain audit columns: `Row_Effective_Date`, `Row_Expiration_Date`, and an active flag `Is_Current`. This guarantees past sales figures are evaluated against contemporaneous historical prices without rewriting history."*

---

## Domain 3: Multi-Dimensional OLAP Operations

### Q10. What are the 5 core OLAP operations? Explain each in the context of your supermarket dataset.
**Answer**:
> *"1. **Roll-Up**: Aggregation climbing up a concept hierarchy (e.g., rolling up daily POS sales into Monthly Category Totals).
> 2. **Drill-Down**: The inverse of Roll-Up, stepping down from summary concepts into granular details (e.g., drilling down from the *Snacks & Beverages* category into specific SKUs like *Lay's* or *Coca-Cola*).
> 3. **Slice**: Selecting a 2D plane by filtering a single dimension (e.g., fixing `Product_Category = 'Dairy & Bakery'` across all dates).
> 4. **Dice**: Selecting a sub-cube by filtering across two or more dimensions simultaneously (e.g., `Category IN ('Snacks', 'Groceries')` AND `Age_Group = 'Young Adult'` AND `Payment_Mode = 'UPI'`).
> 5. **Pivot (Rotate)**: Rotating the multidimensional axes to provide a cross-tabulated view (e.g., displaying Product Categories along rows and Payment Modes along columns to compare channel revenue)."*

### Q11. What is the difference between ROLAP, MOLAP, and HOLAP?
**Answer**:
> *"1. **ROLAP (Relational OLAP)**: Stores data in relational tables (Star Schema) and uses extended SQL (`CUBE`, `ROLLUP`, `GROUP BY`) to query directly against the relational database. Highly scalable for massive volumes.
> 2. **MOLAP (Multidimensional OLAP)**: Stores data in proprietary multidimensional arrays (cubes). Yields blazing-fast query speeds due to pre-computation, but requires extensive pre-aggregation storage.
> 3. **HOLAP (Hybrid OLAP)**: Combines both approaches—storing high-level summary aggregations in MOLAP cubes for fast executive retrieval, while leaving detailed atomic records in ROLAP relational tables for drill-down."*

---

## Domain 4: Data Mining - Association Rule Mining (Apriori)

### Q12. How does the Apriori algorithm work? What is the Apriori Principle?
**Answer**:
> *"The Apriori algorithm performs Market Basket Analysis by iteratively finding frequent itemsets using candidate generation.
> - **The Apriori Principle (Downward Closure Property)** states: *'All non-empty subsets of a frequent itemset must also be frequent.'* Conversely, if an itemset is infrequent, all its supersets will inevitably be infrequent and can be immediately pruned, avoiding an exponential combinatorial explosion ($2^N$)."*

### Q13. Define Support, Confidence, and Lift. Write their mathematical formulas.
**Answer**:
> *"1. **Support**: Fraction of total transactions containing itemset $X$:
>    $$\\text{Support}(X) = \\frac{\\text{Frequency}(X)}{N}$$
> 2. **Confidence**: Conditional probability that basket contains consequent $Y$ given it contains antecedent $X$:
>    $$\\text{Confidence}(X \\Rightarrow Y) = \\frac{\\text{Support}(X \\cup Y)}{\\text{Support}(X)}$$
> 3. **Lift**: Ratio of observed joint occurrence to expected occurrence under statistical independence:
>    $$\\text{Lift}(X \\Rightarrow Y) = \\frac{\\text{Support}(X \\cup Y)}{\\text{Support}(X) \\times \\text{Support}(Y)}$$
>    - $\\text{Lift} = 1$: Independent (no correlation).
>    - $\\text{Lift} > 1$: Positive correlation (items complement each other).
>    - $\\text{Lift} < 1$: Negative correlation (items substitute each other)."*

### Q14. What was the most impactful association rule discovered in your supermarket data, and what business action did you recommend?
**Answer**:
> *"Our top rule was `{Amul Gold Milk} => {Britannia Brown Bread, Amul Butter}` with a high confidence and lift $> 2.0$.  
> **Business Action**: We recommended creating a bundled morning *'Healthy Breakfast Kit'* placed near the entrance, and positioning bread and butter in the same visual aisle as the milk chiller to capitalize on high impulse basket conversion."*

---

## Domain 5: Data Mining - Classification & Clustering

### Q15. What problem did your Classification model solve, and what features were most predictive?
**Answer**:
> *"We formulated a binary classification task to predict whether a customer transaction will result in a **High Spender** (Basket Total $\ge$ Median) versus a **Budget Spender**.
> - Models used: **Decision Tree Classifier** (interpretable white-box model) and **Random Forest** (ensemble of 50 trees).
> - Top Predictive Features: Total item count, Payment Mode (Credit Card/UPI vs Cash), Customer Age Group (Middle-Aged family buyers), and shopping time slot (Evening/Weekends)."*

### Q16. What evaluation metrics did you use for classification? Why is accuracy alone insufficient?
**Answer**:
> *"We evaluated:
> 1. **Accuracy** (Our Decision Tree achieved 73.3%, Random Forest achieved 80.0%).
> 2. **Precision**: Measures how many predicted high spenders were truly high spenders.
> 3. **Recall (Sensitivity)**: Measures what percentage of actual high spenders our model successfully caught (achieved 87.5%).
> 4. **F1-Score**: Harmonic mean of Precision and Recall (achieved 82.4%).
> 5. **Confusion Matrix**: Visual breakdown of True Positives, False Positives, True Negatives, False Negatives.  
> *Accuracy alone is misleading if class distributions are imbalanced, whereas Precision, Recall, and F1-score expose false alarm and missed opportunity rates."*

### Q17. How does the Decision Tree select its split at each node? Explain Information Gain and Gini Impurity.
**Answer**:
> *"At each candidate split, the tree evaluates feature thresholds to maximize the purity of descendant child nodes:
> - **Entropy**: Measures impurity/uncertainty in a set $S$:
>   $$\\text{Entropy}(S) = -\\sum p_i \\log_2(p_i)$$
> - **Information Gain**: The reduction in entropy achieved by partitioning on attribute $A$:
>   $$\\text{Gain}(S, A) = \\text{Entropy}(S) - \\sum \\frac{|S_v|}{|S|} \\text{Entropy}(S_v)$$
> - **Gini Impurity**: Probability of incorrectly labeling a randomly chosen element:
>   $$\\text{Gini}(S) = 1 - \\sum p_i^2$$
> In our script, we used Entropy for the Decision Tree and Gini for the Random Forest."*

### Q18. How does K-Means Clustering work? Why did you scale your features with StandardScaler?
**Answer**:
> *"K-Means is an unsupervised partition-based clustering algorithm:
> 1. Randomly initializes $K$ centroids (we used `k-means++` for optimal distant initialization).
> 2. Assigns each customer to their nearest centroid based on Euclidean distance.
> 3. Recomputes centroids as the arithmetic mean of assigned points.
> 4. Repeats until convergence (centroids stabilize).  
> *We applied `StandardScaler` because Euclidean distance is sensitive to attribute magnitude. Without scaling, `Total_Spend_INR` (varying in thousands) would completely overpower `Total_Units` (varying between 1 and 15), creating distorted clusters."*

### Q19. How did you determine the optimal number of clusters ($K$)?
**Answer**:
> *"We combined two complementary techniques:
> 1. **The Elbow Method**: Plotted Within-Cluster Sum of Squares (Inertia) across $K = 2$ to $7$. The curve displayed a prominent elbow inflection point at $K = 4$.
> 2. **Silhouette Analysis**: Evaluated cluster separation and cohesion, validating that $K = 4$ maximizes intra-cluster compactness and inter-cluster distance."*

### Q20. Describe the 4 Customer Personas discovered by your K-Means model.
**Answer**:
> *"1. **Budget Quick Shoppers (Cluster 3)**: Low spend (~₹282), few items (1–3), high cash/UPI usage for emergency items.
> 2. **Routine Staples Restockers (Cluster 0)**: Moderate-to-high spend (~₹813), recurring grocery items (Atta, Oil, Milk).
> 3. **Impulse Snackers & Youth (Cluster 1)**: Young adults purchasing cold drinks, chips, and confectionery primarily using UPI.
> 4. **Premium Bulk Grocery Buyers (Cluster 2)**: Highest spend (~₹2,014), large basket size (15–25 units), multi-category grocery stocking, frequent credit card payers."*

---

## Domain 6: Practical Implementation & Team Collaboration

### Q21. What technology stack did you utilize to build this project?
**Answer**:
> *- **Programming Language**: Python 3.11  
> - **Data Processing**: `pandas`, `numpy`  
> - **Data Mining & ML**: `mlxtend` (Apriori & Association Rules), `scikit-learn` (Decision Trees, Random Forest, K-Means, StandardScaler)  
> - **Data Visualization**: `matplotlib`, `seaborn`  
> - **Database / SQL**: ANSI SQL DDL and SQLite3 relational engine  
> - **Documentation & Presentation**: Markdown, Mermaid Diagrams, and Responsive HTML5/CSS3 presentation viewer.*

### Q22. How did your team divide responsibilities during the assignment?
**Answer**:
> *- **Student 1 (Lead & Field Data Collection)**: Supermarket visit coordination, questionnaire formulation, raw transaction logging.  
> - **Student 2 (Data Preprocessing & Cleaning)**: Python cleaning pipeline, deduplication, missing value imputation, IQR outlier detection.  
> - **Student 3 (Data Warehouse & Star Schema)**: Kimball dimensional modeling, Fact & Dimension design, SQL DDL generation.  
> - **Student 4 (OLAP Queries & Architecture)**: OLAP cube design, 5 core operations (Roll-up, Drill-down, Slice, Dice, Pivot) and SQL execution.  
> - **Student 5 (Data Mining & Reporting)**: Apriori rule mining, Decision Tree classification, K-Means clustering, and report consolidation.*
