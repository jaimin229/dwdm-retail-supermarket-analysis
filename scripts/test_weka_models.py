import pandas as pd
import subprocess

df = pd.read_csv('data/cleaned_supermarket_data.csv')

# Option 1: Predict Payment_Mode from Demographics & Cart
header_pm = """@relation supermarket_payment_prediction

@attribute Customer_Age_Group {'Middle-Aged (36-50)','Senior (51+)','Young Adult (26-35)','Youth (18-25)'}
@attribute Customer_Gender {'Female','Male'}
@attribute Product_Category {'Dairy & Bakery','Grocery & Staples','Household Essentials','Personal Care','Snacks & Beverages'}
@attribute Quantity numeric
@attribute Unit_Price numeric
@attribute Discount_Percent numeric
@attribute Payment_Mode {'Cash','Credit Card','Debit Card','UPI'}

@data
"""
rows_pm = []
for _, r in df.iterrows():
    rows_pm.append(f"'{r['Customer_Age_Group']}','{r['Customer_Gender']}','{r['Product_Category']}',{r['Quantity']},{r['Unit_Price_INR']:.2f},{r['Discount_Percent']:.2f},'{r['Payment_Mode']}'")

with open('weka_data/test_payment_prediction.arff', 'w', encoding='utf-8') as f:
    f.write(header_pm + "\n".join(rows_pm) + "\n")

cmd1 = ['java', '--add-opens', 'java.base/java.lang=ALL-UNNAMED', '-cp', r'C:\Program Files\Weka-3-8-7\weka.jar', 'weka.classifiers.trees.J48', '-t', 'weka_data/test_payment_prediction.arff', '-c', 'last']
res1 = subprocess.run(cmd1, capture_output=True, text=True)
print("=== OPTION 1: PAYMENT MODE PREDICTION ===")
print(res1.stdout)

# Option 2: Predict Purchase_Level (Low, Medium, High) using Demographics and Category ONLY (No Total_Amount, No Unit_Price, No Quantity)
def get_purchase_level(amt):
    if amt < 75:
        return 'Low'
    elif amt <= 150:
        return 'Medium'
    else:
        return 'High'

df['Purchase_Level'] = df['Line_Total_INR'].apply(get_purchase_level)

header_pl = """@relation supermarket_basket_tier

@attribute Customer_Age_Group {'Middle-Aged (36-50)','Senior (51+)','Young Adult (26-35)','Youth (18-25)'}
@attribute Customer_Gender {'Female','Male'}
@attribute Payment_Mode {'Cash','Credit Card','Debit Card','UPI'}
@attribute Product_Category {'Dairy & Bakery','Grocery & Staples','Household Essentials','Personal Care','Snacks & Beverages'}
@attribute Purchase_Level {'Low','Medium','High'}

@data
"""
rows_pl = []
for _, r in df.iterrows():
    rows_pl.append(f"'{r['Customer_Age_Group']}','{r['Customer_Gender']}','{r['Payment_Mode']}','{r['Product_Category']}','{r['Purchase_Level']}'")

with open('weka_data/test_purchase_tier.arff', 'w', encoding='utf-8') as f:
    f.write(header_pl + "\n".join(rows_pl) + "\n")

cmd2 = ['java', '--add-opens', 'java.base/java.lang=ALL-UNNAMED', '-cp', r'C:\Program Files\Weka-3-8-7\weka.jar', 'weka.classifiers.trees.J48', '-t', 'weka_data/test_purchase_tier.arff', '-c', 'last']
res2 = subprocess.run(cmd2, capture_output=True, text=True)
print("=== OPTION 2: PURCHASE TIER PREDICTION (DEMOGRAPHICS & CATEGORY ONLY) ===")
print(res2.stdout)
