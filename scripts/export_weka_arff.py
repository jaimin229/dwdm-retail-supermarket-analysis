import os
import pandas as pd

def generate_perfect_weka_arff():
    os.makedirs('weka_data', exist_ok=True)
    df = pd.read_csv('data/cleaned_supermarket_data.csv')
    
    # Standardize names without special chars
    def clean_str(s):
        return "'" + str(s).strip() + "'"

    # Compute Purchase_Level
    def get_purchase_level(amt):
        if amt < 200:
            return 'Low'
        elif amt <= 600:
            return 'Medium'
        else:
            return 'High'

    df['Purchase_Level'] = df['Line_Total_INR'].apply(get_purchase_level)

    # 1. Classification ARFF
    age_groups = [f"'{x}'" for x in sorted(df['Customer_Age_Group'].unique())]
    genders = [f"'{x}'" for x in sorted(df['Customer_Gender'].unique())]
    payments = [f"'{x}'" for x in sorted(df['Payment_Mode'].unique())]
    categories = [f"'{x}'" for x in sorted(df['Product_Category'].unique())]
    purchase_levels = ['Low', 'Medium', 'High']

    header_class = f"""@relation supermarket_classification

@attribute Customer_Age_Group {{{','.join(age_groups)}}}
@attribute Customer_Gender {{{','.join(genders)}}}
@attribute Payment_Mode {{{','.join(payments)}}}
@attribute Product_Category {{{','.join(categories)}}}
@attribute Quantity numeric
@attribute Unit_Price numeric
@attribute Discount_Percent numeric
@attribute Total_Amount numeric
@attribute Purchase_Level {{{','.join(purchase_levels)}}}

@data
"""
    rows_class = []
    for _, r in df.iterrows():
        age = clean_str(r['Customer_Age_Group'])
        gen = clean_str(r['Customer_Gender'])
        pay = clean_str(r['Payment_Mode'])
        cat = clean_str(r['Product_Category'])
        rows_class.append(f"{age},{gen},{pay},{cat},{r['Quantity']},{r['Unit_Price_INR']:.2f},{r['Discount_Percent']:.2f},{r['Line_Total_INR']:.2f},{r['Purchase_Level']}")

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
    for _, r in df.iterrows():
        rows_clust.append(f"{r['Quantity']},{r['Unit_Price_INR']:.2f},{r['Discount_Percent']:.2f},{r['Line_Total_INR']:.2f}")

    with open('weka_data/supermarket_clustering.arff', 'w', encoding='utf-8') as f:
        f.write(header_clust + "\n".join(rows_clust) + "\n")

    # 3. Association ARFF
    # Basket by Transaction_ID
    baskets = df.groupby('Transaction_ID')['Product_Category'].apply(lambda s: list(set(s))).reset_index()
    unique_cats = sorted(df['Product_Category'].unique())
    clean_cat_names = [c.replace(' & ', '_').replace(' ', '_') for c in unique_cats]

    header_assoc = "@relation supermarket_association\n\n"
    for c in clean_cat_names:
        header_assoc += f"@attribute {c} {{t, ?}}\n"
    header_assoc += "\n@data\n"

    rows_assoc = []
    for _, r in baskets.iterrows():
        b_cats = r['Product_Category']
        row_str = ",".join(['t' if cat in b_cats else '?' for cat in unique_cats])
        rows_assoc.append(row_str)

    with open('weka_data/supermarket_association.arff', 'w', encoding='utf-8') as f:
        f.write(header_assoc + "\n".join(rows_assoc) + "\n")

    print("[SUCCESS] All 3 ARFF files generated cleanly!")

if __name__ == '__main__':
    generate_perfect_weka_arff()
