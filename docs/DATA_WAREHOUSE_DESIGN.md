# Comprehensive Data Warehouse Architecture & Design

**Course**: Data Warehouse and Data Mining (Course Code: 4040233302)  
**Institution**: Silver Oak College of Computer Application  
**Department**: Department of Computer Application, BCA Semester 5th (A.Y. 2026-27)  
**Target Enterprise**: FreshMart Supermarket (Gota / SG Highway, Ahmedabad)  
**Deliverable**: Deliverable 3 (Data Warehouse Design - 5 Marks Rubric)

---

## 1. Enterprise Data Warehouse Overview

Retail supermarkets manage thousands of transactions daily across multiple billing counters. While operational Point-of-Sale (POS) systems (OLTP) excel at rapid ACID-compliant record insertion, they are inherently unsuited for complex analytical querying, historical trend discovery, and customer intelligence. 

The **FreshMart Enterprise Data Warehouse (EDW)** bridges this divide by consolidating, standardizing, and organizing transactional data into an optimized dimensional model capable of sub-second multi-dimensional analytical processing (OLAP) and predictive data mining.

---

## 2. Three-Tier Data Warehouse Architecture

The FreshMart Data Warehouse implements the industry-standard **Three-Tier Architecture**:

```
       ┌────────────────────────────────────────────────────────┐
       │   TOP TIER: FRONT-END ANALYTICAL & PRESENTATION TIER   │
       │  • OLAP Slice/Dice/Pivot Engines  • BI Dashboards     │
       │  • Data Mining Models (Apriori, Decision Trees, K-Means)│
       └──────────────────────────▲─────────────────────────────┘
                                  │ MDX / ANSI SQL
       ┌──────────────────────────┴─────────────────────────────┐
       │             MIDDLE TIER: OLAP SERVER TIER              │
       │  • Relational OLAP (ROLAP) Engine                      │
       │  • Multi-Dimensional OLAP (MOLAP) Pre-Aggregated Cubes │
       │  • Aggregation Cache & Dynamic Slicing Query Planner   │
       └──────────────────────────▲─────────────────────────────┘
                                  │ Star Schema Joins
       ┌──────────────────────────┴─────────────────────────────┐
       │     BOTTOM TIER: DATA REPOSITORY & STAGING LAYER       │
       │  • Staging Area (Cleaned CSV / Temporary ETL tables)   │
       │  • Enterprise Data Warehouse (Fact_Sales, Dim Tables)  │
       │  • Metadata Repository & Operational Audit Logs        │
       └──────────────────────────▲─────────────────────────────┘
                                  │ ETL Pipeline
       ┌──────────────────────────┴─────────────────────────────┐
       │            OPERATIONAL DATA SOURCES (OLTP)             │
       │  • POS Billing Terminals (Counters 1-4)                │
       │  • Barcode Scanners & Inventory ERP Logs               │
       └────────────────────────────────────────────────────────┘
```

### 2.1 Tier 1: Bottom Tier (Data Warehouse Storage & Staging)
- **Data Sources**: Operational POS billing machines capturing real-time barcode scans, inventory ERP databases, and customer loyalty mobile apps.
- **ETL Staging Area**: An intermediate isolated relational area where raw POS files undergo deduplication, missing value imputation, type casting, and outlier filtering before loading into the production warehouse.
- **Enterprise Data Warehouse Storage**: Houses the conformed dimension tables and the central `Fact_Sales` table designed under a Star Schema relational structure.

### 2.2 Tier 2: Middle Tier (OLAP Server)
- Implements an extended **ROLAP (Relational OLAP)** and **MOLAP (Multidimensional OLAP)** hybrid architecture.
- Maps multi-dimensional cubes (Time × Product × Customer × Store × Payment) directly over the underlying Star Schema relational tables.
- Employs indexed pre-aggregations (monthly roll-ups, category-wise revenue totals) to deliver instantaneous response times for executive queries.

### 2.3 Tier 3: Top Tier (Front-End Analytical Applications)
- **Executive Reporting**: SQL-driven query interfaces for store managers to assess daily sales targets.
- **OLAP Exploratory Tools**: Multi-dimensional slicers, drill-down tools, and cross-tabulation pivot views.
- **Data Mining Engine**: Python-based machine learning pipeline executing Market Basket Analysis (Apriori), Customer Retention Classification, and Behavioral Segmentation (K-Means).

---

## 3. Ralph Kimball's 4-Step Dimensional Design Process

The dimensional architecture strictly adheres to Ralph Kimball's acclaimed four-step dimensional modeling methodology:

```
┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│  Step 1: Choose  │ ──> │   Step 2: Declare │ ──> │ Step 3: Identify │ ──> │ Step 4: Identify │
│ Business Process │     │    the Grain     │     │  the Dimensions  │     │   the Measures   │
└──────────────────┘     └──────────────────┘     └──────────────────┘     └──────────────────┘
```

### Step 1: Choose the Business Process
- **Selected Process**: **Retail Supermarket Point-of-Sale (POS) Checkout Operations**.
- **Rationale**: The POS checkout event is the core revenue-generating activity of the business, directly capturing product affinities, pricing adjustments, customer demographic cohorts, and payment tender behavior.

### Step 2: Declare the Grain
- **Defined Grain**: **One individual row per scanned line-item on a customer's retail sales receipt**.
- **Impact**: Declaring atomic line-item grain provides maximum analytical flexibility. It allows executive analysts to roll up to store-wide monthly revenue while concurrently empowering data mining algorithms to analyze individual item combinations in a market basket.

### Step 3: Identify the Dimensions
Dimensions provide the contextual "who, what, where, when, and how" surrounding each transaction:
1. **`Dim_Date` (When)**: Day, day of week, month, quarter, year, weekend indicator.
2. **`Dim_Product` (What)**: Item name, category, brand, package size, base MRP.
3. **`Dim_Customer` (Who)**: Customer ID, age group, gender, behavioral segment, loyalty tier.
4. **`Dim_Store` (Where)**: Billing counter ID, counter name, checkout lane type (Express vs Regular).
5. **`Dim_Payment` (How)**: Tender mode (UPI, Cash, Credit Card, Debit Card), gateway channel.

### Step 4: Identify the Numeric Facts (Measures)
Facts represent quantitative, additive measurements captured during the checkout event:
- `Quantity_Sold`: Count of units purchased (Fully Additive)
- `Unit_Price_INR`: Base retail price per item (Non-Additive / Semi-Additive)
- `Discount_Percent`: Percentage promotional price markdown
- `Discount_Amount_INR`: Monetary discount conceded (Fully Additive)
- `Line_Total_INR`: Final net amount collected from customer (Fully Additive)
- `Estimated_Cost_INR`: Wholesale procurement cost (Fully Additive)
- `Net_Profit_INR`: Net operating margin generated = `Line_Total_INR - Estimated_Cost_INR` (Fully Additive)

---

## 4. Slowly Changing Dimension (SCD) Management

Retail entities continually evolve. To balance storage efficiency against historical reporting integrity, the FreshMart Data Warehouse deploys a hybrid SCD strategy:

### 4.1 SCD Type 1 (Overwrite)
- **Application**: Corrections to typographical errors in customer names, gender corrections, or billing counter nomenclature.
- **Mechanism**: Overwrites the existing attribute value without creating new records. Historical values are not preserved.

### 4.2 SCD Type 2 (Add New Row with History Preservation)
- **Application**: **Product Price Alterations & Re-Categorization**.
- **Mechanism**: When a manufacturer revises an MRP (e.g. Amul Butter rises from ₹58 to ₹62), a new record is inserted into `Dim_Product` with a new surrogate `Product_Key`.
- **Audit Columns Employed**:
  - `Row_Effective_Date`: Timestamp when the price became active.
  - `Row_Expiration_Date`: Timestamp when the price expired (defaults to `'9999-12-31'` for active rows).
  - `Is_Current`: Boolean flag (`TRUE` for current catalog pricing, `FALSE` for obsolete pricing).
- **Benefit**: Ensures that historical sales from prior months are evaluated against their true contemporaneous prices without altering past financial reports.

---

## 5. ETL (Extract, Transform, Load) Pipeline Architecture

```
[POS Billing Logs]  ──> [Staging DB] ──> [Data Cleansing & Validation] ──> [Surrogate Key Generator] ──> [Fact & Dim Loading]
```

1. **Extraction (E)**: Automated cron batch jobs extract raw POS comma-separated log files from billing counters at the close of every business day (22:30 IST).
2. **Transformation (T)**:
   - Duplicate elimination (handling scanner double-clicks).
   - Demographic imputation using customer profile lookup tables and statistical mode.
   - ISO date harmonization (`YYYY-MM-DD`).
   - Outlier quantity capping via statistical IQR thresholds.
   - Surrogate key generation via sequence lookups in dimension tables.
3. **Loading (L)**:
   - Conformed dimensions are updated first to ensure referential integrity.
   - `Fact_Sales` records are loaded using bulk-insert pipelines with indexed foreign keys.

---

## 6. Metadata Repository Architecture

The Data Warehouse metadata repository is structured into three essential tiers:
1. **Technical Metadata**: Table schemas, data types, primary and foreign key constraints, indexing structures, ETL execution runtimes, and partition definitions.
2. **Business Metadata**: Business definitions of metrics (e.g., precise accounting definition of *Net Profit* vs *Gross Revenue*), category taxonomies, and data ownership policies.
3. **Operational Metadata**: Daily row count ingestion logs, missing value frequency alerts, error logs, and data steward validation timestamps.
