import os
import pandas as pd

def export_weka_arff():
    os.makedirs('weka_data', exist_ok=True)
    df_clean = pd.read_csv('data/cleaned_supermarket_data.csv')
    print(f"Loaded {len(df_clean)} cleaned records.")

    # Compute Purchase_Level
    def get_purchase_level(amt):
        if amt < 200:
            return 'Low'
        elif amt <= 600:
            return 'Medium'
        else:
            return 'High'

    df_clean['Purchase_Level'] = df_clean['Line_Total_INR'].apply(get_purchase_level)

    # 1. Classification ARFF
    header_class = """@relation supermarket_classification

@attribute Customer_Age_Group {Youth,Young_Adult,Middle_Aged,Senior}
@attribute Customer_Gender {Male,Female,Other}
@attribute Payment_Mode {Cash,UPI,Credit_Card,Debit_Card}
@attribute Product_Category {Grocery,Dairy,Bakery,Beverages,Personal_Care,Household}
@attribute Quantity numeric
@attribute Unit_Price numeric
@attribute Discount_Percent numeric
@attribute Total_Amount numeric
@attribute Purchase_Level {Low,Medium,High}

@data
"""
    rows_class = []
    for _, r in df_clean.iterrows():
        cat = str(r['Product_Category']).replace(' ', '_')
        pay = str(r['Payment_Mode']).replace(' ', '_')
        age = str(r['Customer_Age_Group']).replace(' ', '_')
        rows_class.append(f"{age},{r['Customer_Gender']},{pay},{cat},{r['Quantity']},{r['Unit_Price_INR']:.2f},{r['Discount_Percent']:.2f},{r['Line_Total_INR']:.2f},{r['Purchase_Level']}")

    with open('weka_data/supermarket_classification.arff', 'w', encoding='utf-8') as f:
        f.write(header_class + "\n".join(rows_class) + "\n")

    # 2. Clustering ARFF
    header_clust = """@relation supermarket_clustering

@attribute Quantity numeric
@attribute Unit_Price numeric
@attribute Discount_Percent numeric
@attribute Total_Amount numeric

@data
"""
    rows_clust = []
    for _, r in df_clean.iterrows():
        rows_clust.append(f"{r['Quantity']},{r['Unit_Price_INR']:.2f},{r['Discount_Percent']:.2f},{r['Line_Total_INR']:.2f}")

    with open('weka_data/supermarket_clustering.arff', 'w', encoding='utf-8') as f:
        f.write(header_clust + "\n".join(rows_clust) + "\n")

    # 3. Association ARFF (Group items by Transaction_ID or Customer_ID)
    baskets = df_clean.groupby('Transaction_ID')['Product_Category'].apply(lambda x: list(set(x))).reset_index()
    all_categories = sorted(list(set(df_clean['Product_Category'])))

    header_assoc = "@relation supermarket_association\n\n"
    for cat in all_categories:
        header_assoc += f"@attribute {cat} {{t, ?}}\n"
    header_assoc += "\n@data\n"

    rows_assoc = []
    for _, r in baskets.iterrows():
        b_cats = r['Product_Category']
        row_str = ",".join(['t' if cat in b_cats else '?' for cat in all_categories])
        rows_assoc.append(row_str)

    with open('weka_data/supermarket_association.arff', 'w', encoding='utf-8') as f:
        f.write(header_assoc + "\n".join(rows_assoc) + "\n")

    print("Successfully generated all 3 ARFF files in weka_data/:")
    print(" - weka_data/supermarket_classification.arff")
    print(" - weka_data/supermarket_clustering.arff")
    print(" - weka_data/supermarket_association.arff")

if __name__ == '__main__':
    export_weka_arff()
