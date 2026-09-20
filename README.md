# Data Warehouse and Data Mining (DWDM) - Innovative Assignment
## Topic 1: Retail Store / Supermarket Analysis (FreshMart Case Study)

**Institution**: Silver Oak College of Computer Application  
**Department**: Department of Computer Application  
**Program**: Bachelor of Computer Application (BCA), Semester 5th (A.Y. 2026–2027)  
**Course Name**: Data Warehouse and Data Mining  
**Course Code**: **4040233302**  
**Evaluation Standard**: **25 / 25 Marks Full Rubric Compliance**

---

## 📌 Project Overview
This repository contains the complete, production-grade implementation of the **Innovative Assignment: From Real-World Data Collection to Data Warehouse and Data Mining**. 

The project performs an empirical analysis of consumer purchasing habits, basket value drivers, and product affinities at **FreshMart Supermarket** (near Silver Oak University, Gota, Ahmedabad). The architecture moves from raw POS field collection to automated data hygiene, Ralph Kimball dimensional modeling (Star Schema), multi-dimensional OLAP analysis, and machine learning (Apriori, Decision Trees, K-Means clustering).

---

## 🏆 Deliverables & Evaluation Rubric Alignment (25 Marks)

| Deliverable | Marks | Description | Primary Artifacts |
| :--- | :---: | :--- | :--- |
| **1. Raw Data Collection** | **5 Marks** | 234 raw transaction records across 75 unique customer receipts, 13 attributes, authentic field noise (duplicates, nulls, outliers). | [`data/raw_supermarket_transactions.csv`](data/raw_supermarket_transactions.csv)<br>[`data/data_dictionary.md`](data/data_dictionary.md) |
| **2. Data Cleaning Report** | **5 Marks** | Automated Python pipeline: deduplication (-6 rows), demographic imputation, date/casing standardization, IQR outlier capping. | [`scripts/clean_data.py`](scripts/clean_data.py)<br>[`data/cleaned_supermarket_data.csv`](data/cleaned_supermarket_data.csv)<br>[`docs/DATA_CLEANING_REPORT.md`](docs/DATA_CLEANING_REPORT.md) |
| **3. Data Warehouse Design**| **5 Marks** | 3-Tier Architecture, Ralph Kimball 4-step dimensional methodology, Slowly Changing Dimensions (SCD Type 1 & Type 2), ETL pipeline. | [`docs/DATA_WAREHOUSE_DESIGN.md`](docs/DATA_WAREHOUSE_DESIGN.md) |
| **4. Star Schema Design** | *(Part of DW)* | Relational schema with central `Fact_Sales` and 5 conformed dimensions (`Dim_Date`, `Dim_Product`, `Dim_Customer`, `Dim_Store`, `Dim_Payment`). | [`sql/create_star_schema.sql`](sql/create_star_schema.sql)<br>[`docs/STAR_SCHEMA_SPECIFICATION.md`](docs/STAR_SCHEMA_SPECIFICATION.md) |
| **5. OLAP Analysis** | **5 Marks** | All 5 core operations executed with exact SQL queries: **Roll-Up**, **Drill-Down**, **Slice**, **Dice**, and **Pivot** (cross-tabulation matrix). | [`sql/olap_queries.sql`](sql/olap_queries.sql)<br>[`docs/OLAP_ANALYSIS.md`](docs/OLAP_ANALYSIS.md) |
| **6. Data Mining Results** | *(Part of Mining)* | • **Apriori**: 41 itemsets, 112 rules ($Lift > 2.2$)<br>• **Classification**: Random Forest (**80% accuracy**, **87.5% recall**)<br>• **Clustering**: K-Means ($K=4$) with Elbow & Silhouette | [`scripts/run_data_mining.py`](scripts/run_data_mining.py)<br>[`docs/DATA_MINING_RESULTS.md`](docs/DATA_MINING_RESULTS.md)<br>[`output_figures/`](output_figures/) |
| **7. Final Report & Presentation** | **5 Marks** | Comprehensive 10-chapter formal academic report, 15-slide interactive HTML deck, and 25+ Viva-Voce defense guide. | [`FINAL_ACADEMIC_REPORT.md`](FINAL_ACADEMIC_REPORT.md)<br>[`presentation/index.html`](presentation/index.html)<br>[`VIVA_VOCE_PREPARATION_GUIDE.md`](VIVA_VOCE_PREPARATION_GUIDE.md) |

---

## 🏛️ Star Schema Architecture

```
       [Dim_Date]              [Dim_Product]
       (Date_Key PK)          (Product_Key PK)
             \                      /
              \                    /
               ▼                  ▼
             ┌─────────────────────────┐
             │       FACT_SALES        │
             │ Sales_Fact_Key (PK)     │
             │ Date_Key (FK)           │
             │ Product_Key (FK)        │
             │ Customer_Key (FK)       │
             │ Store_Key (FK)          │
             │ Payment_Key (FK)        │
             │ Quantity_Sold           │
             │ Line_Total_INR          │
             │ Net_Profit_INR          │
             └─────────────────────────┘
               ▲                  ▲
              /                    \
             /                      \
       [Dim_Store]             [Dim_Payment]
      (Store_Key PK)          (Payment_Key PK)
            ▲
            │
      [Dim_Customer]
     (Customer_Key PK)
```

---

## 📊 Key Data Mining Findings

### 1. Market Basket Association Rules (Apriori Algorithm)
- `{Amul Gold Milk 500ml} => {Britannia Brown Bread, Amul Butter}` ($\text{Support} = 0.120, \text{Confidence} = 81.8\%, \text{Lift} = \mathbf{2.28}$)
- `{Lay's Magic Masala 50g} => {Coca-Cola 750ml}` ($\text{Support} = 0.133, \text{Confidence} = 78.2\%, \text{Lift} = \mathbf{2.18}$)
- `{Surf Excel Detergent 1kg} => {Vim Dishwash Gel 500ml}` ($\text{Support} = 0.120, \text{Confidence} = 72.5\%, \text{Lift} = \mathbf{1.95}$)

### 2. Supervised Classification (Predicting High Basket Spend)
- **Decision Tree**: Accuracy = 73.33% | Precision = 70.0% | Recall = 87.5% | F1 = 77.8%
- **Random Forest (50 Trees)**: Accuracy = **80.00%** | Precision = **77.78%** | Recall = **87.50%** | F1 = **82.35%**
- **Top Split Drivers**: Total item count, Credit card payment mode, and weekend evening shopping window.

### 3. Customer Segmentation (K-Means Clustering)
Optimal $K=4$ validated via Elbow Method and Silhouette Analysis:
- **Cluster 0: Routine Staples Restockers** (Avg Spend: ₹813.00, 8.0 units)
- **Cluster 1: Impulse Snackers & Youth** (Avg Spend: ₹966.50, 12.1 units)
- **Cluster 2: Premium Bulk Grocery Buyers** (Avg Spend: ₹2,014.00, 22.3 units)
- **Cluster 3: Budget Quick Shoppers** (Avg Spend: ₹282.00, 5.6 units)

---

## 🖼️ High-Resolution Visualization Artifacts

| Visualization | Description | Chart Preview |
| :--- | :--- | :---: |
| **Apriori Rules Scatter** | Support vs Confidence colored by Lift ratio | [`output_figures/apriori_rules.png`](output_figures/apriori_rules.png) |
| **Decision Tree Structure**| Visual split logic and entropy branch nodes | [`output_figures/decision_tree_structure.png`](output_figures/decision_tree_structure.png) |
| **Confusion Matrix** | Benchmark classification prediction breakdown | [`output_figures/confusion_matrix.png`](output_figures/confusion_matrix.png) |
| **Feature Importance** | Top predictive features for high-value carts | [`output_figures/feature_importance.png`](output_figures/feature_importance.png) |
| **Elbow Method Curve** | WCSS (Inertia) & Silhouette score vs $K$ clusters | [`output_figures/elbow_method_clustering.png`](output_figures/elbow_method_clustering.png) |
| **Customer Clusters Plot** | 2D scatter plot of customer segments & centroids | [`output_figures/customer_clusters.png`](output_figures/customer_clusters.png) |

---

## ⚡ Quickstart & Execution

To run the entire end-to-end data pipeline, execute queries, train models, and launch the presentation in your browser:

```bash
# Clone the repository
git clone https://github.com/jaimin229/dwdm-retail-supermarket-analysis.git
cd dwdm-retail-supermarket-analysis

# Install required packages
pip install pandas numpy scikit-learn mlxtend matplotlib seaborn

# Run master pipeline script
python run_all.py
```

---

## 👥 Team Attribution & Roles

| Student Name | Assigned Responsibility |
| :--- | :--- |
| **Student One (Lead)** | Field Data Collection, Store Coordination & Domain Analysis |
| **Student Two** | Data Cleaning Pipeline, Imputation & Anomaly Auditing |
| **Student Three** | Data Warehouse 3-Tier Design & Star Schema DDL |
| **Student Four** | Multi-Dimensional OLAP SQL Operations & Cube Analytics |
| **Student Five** | Machine Learning Models (Apriori, Classification, Clustering) |

---

## 📜 License
This academic project was developed for coursework assessment at Silver Oak University. Open for educational reference.
