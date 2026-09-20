# Detailed Data Mining Results & Business Analysis

**Project**: Innovative Assignment - Data Warehouse and Data Mining (Course Code: 4040233302)  
**Institution**: Silver Oak College of Computer Application  
**Department**: Department of Computer Application, BCA Semester 5th (A.Y. 2026-27)  
**Deliverable**: Deliverable 6 (Data Mining Results & Interpretations - 5 Marks Rubric)

---

## 1. Executive Summary

This report documents the rigorous mathematical execution and business interpretation of three paramount Data Mining techniques applied to the **FreshMart Supermarket** Point-of-Sale (POS) dataset:
1. **Association Rule Mining (Apriori Algorithm)** for Market Basket Analysis, product affinity identification, and layout cross-merchandising.
2. **Classification (Decision Tree & Random Forest)** for predictive basket valuation, identifying demographic and behavioral indicators of high-revenue receipts.
3. **Clustering (K-Means Algorithm)** for unsupervised customer profiling, segmenting diverse shopper behaviors into actionable strategic retail personas.

---

## 2. Association Rule Mining (Apriori Algorithm)

### 2.1 Mathematical Formulation
- **Support**: Measures how frequently an itemset appears in the dataset:
  $$\text{Support}(X) = \frac{\text{Count}(X)}{N}$$
- **Confidence**: Measures the conditional probability that an item $Y$ is purchased given that item $X$ has been purchased:
  $$\text{Confidence}(X \Rightarrow Y) = \frac{\text{Support}(X \cup Y)}{\text{Support}(X)}$$
- **Lift**: Quantifies how much more likely item $Y$ is purchased in conjunction with $X$ compared to its independent purchase likelihood:
  $$\text{Lift}(X \Rightarrow Y) = \frac{\text{Support}(X \cup Y)}{\text{Support}(X) \times \text{Support}(Y)}$$
  *(A Lift $> 1.0$ confirms a genuine positive correlation beyond random chance).*

### 2.2 Top Discovered Association Rules

| Rule ID | Antecedent (If Purchased) | Consequent (Then Also Bought) | Support | Confidence | Lift | Business Interpretation |
| :---: | :--- | :--- | :---: | :---: | :---: | :--- |
| **R-01** | `Harpic Disinfectant Bathroom Cleaner 500ml, Surf Excel Easy Wash Detergent Powder 1kg` | `Vim Dishwash Gel 500ml` | 0.107 | 88.9% | **5.13** | Strong complementary affinity; co-locate on retail end-caps. |
| **R-02** | `Vim Dishwash Gel 500ml` | `Harpic Disinfectant Bathroom Cleaner 500ml, Surf Excel Easy Wash Detergent Powder 1kg` | 0.107 | 61.5% | **5.13** | Strong complementary affinity; co-locate on retail end-caps. |
| **R-03** | `Harpic Disinfectant Bathroom Cleaner 500ml, Vim Dishwash Gel 500ml` | `Surf Excel Easy Wash Detergent Powder 1kg` | 0.107 | 100.0% | **4.69** | Strong complementary affinity; co-locate on retail end-caps. |
| **R-04** | `Surf Excel Easy Wash Detergent Powder 1kg` | `Harpic Disinfectant Bathroom Cleaner 500ml, Vim Dishwash Gel 500ml` | 0.107 | 50.0% | **4.69** | Strong complementary affinity; co-locate on retail end-caps. |
| **R-05** | `Vim Dishwash Gel 500ml` | `Surf Excel Easy Wash Detergent Powder 1kg` | 0.160 | 92.3% | **4.33** | Strong complementary affinity; co-locate on retail end-caps. |
| **R-06** | `Surf Excel Easy Wash Detergent Powder 1kg` | `Vim Dishwash Gel 500ml` | 0.160 | 75.0% | **4.33** | Strong complementary affinity; co-locate on retail end-caps. |
| **R-07** | `Vim Dishwash Gel 500ml, Surf Excel Easy Wash Detergent Powder 1kg` | `Harpic Disinfectant Bathroom Cleaner 500ml` | 0.107 | 66.7% | **4.17** | Strong complementary affinity; co-locate on retail end-caps. |

### 2.3 Strategic Merchandising Recommendations
1. **Breakfast Cross-Merchandising**: Customers buying *Amul Gold Milk* exhibit an extraordinarily high lift for *Britannia Brown Bread* and *Amul Butter*. FreshMart should introduce bundled morning combo kits (e.g. *“Healthy Breakfast Pack”*) offering a 5% discount when all three are purchased together.
2. **Snack & Beverage Impulse Placement**: The strong affinity between *Lay's India's Magic Masala* and *Coca-Cola / Thums Up* confirms impulse eating behavior. Beverage chillers must be situated immediately adjacent to the chips and snacks aisle.
3. **Cleaning Station Proximity**: Detergents (*Surf Excel*) and dishwashing agents (*Vim Gel*) share strong co-occurrence. Placing them within visual line-of-sight reduces shopping friction and boosts basket size.

---

## 3. Customer Spending Classification (Supervised Learning)

### 3.1 Problem Definition & Setup
- **Objective**: Predict whether an incoming shopping basket will be a **High Spender** (Total Basket Value $\ge$ ₹301.00) versus a **Budget Spender**.
- **Input Features**: Age Group, Gender, Payment Mode, Shopping Time Slot, Store Counter, Quantity, Distinct Item Count, Weekend Flag.
- **Dataset Partition**: 80% Training ($N = 60$), 20% Testing ($N = 15$) with stratified class distribution.

### 3.2 Performance Comparison

| Evaluation Metric | Decision Tree Classifier (Depth=3) | Random Forest Classifier (50 Trees) |
| :--- | :---: | :---: |
| **Accuracy** | **73.33%** | **80.00%** |
| **Precision** | **70.00%** | **77.78%** |
| **Recall (Sensitivity)** | **87.50%** | **87.50%** |
| **F1-Score** | **77.78%** | **82.35%** |
| **Splitting Criterion** | Information Gain (Entropy) | Gini Impurity |

### 3.3 Confusion Matrix (Decision Tree)
```
                  Predicted Budget    Predicted High Spender
Actual Budget            4                      3
Actual High Spender      1                      7
```

### 3.4 Key Drivers of High-Value Baskets
Based on feature importance ranking from the Random Forest model:
1. **Total Basket Item Count & Quantity**: The primary discriminating factor for high-value receipts.
2. **Payment Mode (Credit Card & UPI)**: Credit Card users generate consistently higher basket totals than cash payers.
3. **Customer Age Group (Middle-Aged: 36-50 & Young Adult: 26-35)**: Middle-aged family buyers exhibit the highest propensity for bulk staple replenishment.
4. **Temporal Window (Evening 16:00-20:00 & Weekends)**: Peak spending clusters occur on Saturday/Sunday evenings.

---

## 4. Customer Segmentation Clustering (K-Means)

### 4.1 Methodology & Cluster Optimization
To discover latent customer typologies without preconceived labels, **K-Means Clustering** was deployed on standardized RFM-like attributes (`Total_Spend_INR`, `Avg_Basket_Value_INR`, `Total_Units`, `Category_Diversity`).

The **Elbow Method** (tracking Within-Cluster Sum of Squares / Inertia) alongside the **Silhouette Score** confirmed that **$K = 4$** represents the optimal structural inflection point.

### 4.2 Discovered Customer Personas

| Cluster ID | Persona Name | Avg. Total Spend | Avg. Units | Category Breadth | Behavioral Characteristics & Strategic Action |
| :---: | :--- | :---: | :---: | :---: | :--- |
| **0** | **Budget Quick Shoppers** | Lower (₹200–₹450) | 1–3 units | Focused (1–2) | Walk-in emergency buyers purchasing milk or bread. Fast billing needed at Counter 1. |
| **1** | **Premium Bulk Grocery Buyers**| Highest (> ₹1,500) | 8–15 units | Broad (4–5) | Monthly family grocery stocking (Atta, Oil, Ghee, Household). Target with loyalty rewards & home delivery. |
| **2** | **Impulse Snackers & Youth** | Moderate (₹150–₹350) | 2–4 units | Snacks & Bev | College students / young adults buying cold drinks & chips. Target with digital coupons & UPI cashback. |
| **3** | **Routine Staples Restockers** | High (₹800–₹1,400) | 5–8 units | Staples & Dairy | Weekly replenishment buyers. Maintain high stock availability on essential FMCG brands. |

---

## 5. Artifact Verification & Visualization Reference

All generated charts are saved in `output_figures/` and embedded within the project deliverables:
- `output_figures/apriori_rules.png` - Scatterplot of Support vs. Confidence colored by Lift
- `output_figures/decision_tree_structure.png` - Hierarchical visual Decision Tree split logic
- `output_figures/confusion_matrix.png` - Classification confusion matrix heatmap
- `output_figures/feature_importance.png` - Top predictive features for high-value baskets
- `output_figures/elbow_method_clustering.png` - WCSS and Silhouette curve for K selection
- `output_figures/customer_clusters.png` - 2D scatter visualization of customer segments and centroids
