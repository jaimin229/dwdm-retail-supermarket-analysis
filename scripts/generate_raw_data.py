"""
Field Data Generation Script - FreshMart Supermarket POS Logs
Course: Data Warehouse and Data Mining (4040233302)
Institution: Silver Oak College of Computer Application, BCA Sem-5

This script simulates realistic point-of-sale (POS) raw field collection data 
from FreshMart Supermarket (Near Silver Oak University, Gota, Ahmedabad) across 
a 7-day monitoring period (18-Aug-2026 to 24-Aug-2026).

It intentionally injects realistic real-world data flaws:
- Inconsistent date formats (DD-MM-YYYY, YYYY/MM/DD, DD/MM/YYYY)
- Missing values (blank Customer Age Group, NaN Discount)
- Casing & spelling inconsistencies in Product Name and Category
- Duplicate scans (duplicate rows simulating barcode double-clicks)
- Outlier basket values
"""

import os
import random
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Set seeds for reproducibility
random.seed(42)
np.random.seed(42)

os.makedirs("data", exist_ok=True)
os.makedirs("scripts", exist_ok=True)
os.makedirs("docs", exist_ok=True)
os.makedirs("sql", exist_ok=True)
os.makedirs("output_figures", exist_ok=True)
os.makedirs("presentation", exist_ok=True)

# Product catalog by category
catalog = {
    "Dairy & Bakery": [
        ("Amul Taaza Milk 500ml", 27.0),
        ("Amul Gold Milk 500ml", 33.0),
        ("Amul Butter 100g", 58.0),
        ("Britannia Brown Bread 400g", 45.0),
        ("Amul Malai Paneer 200g", 92.0),
        ("Mother Dairy Curd 400g", 35.0),
        ("Amul Cheese Slices 200g", 140.0),
    ],
    "Grocery & Staples": [
        ("Aashirvaad Shudh Chakki Atta 5kg", 245.0),
        ("Fortune Sunlite Sunflower Oil 1L", 135.0),
        ("Tata Salt 1kg", 28.0),
        ("Tata Sampann Toor Dal 1kg", 165.0),
        ("India Gate Basmati Rice 1kg", 140.0),
        ("Madhur Pure & Hygienic Sugar 1kg", 48.0),
        ("Catch Red Chilli Powder 200g", 75.0),
    ],
    "Snacks & Beverages": [
        ("Lay's India's Magic Masala 50g", 20.0),
        ("Kurkure Masala Munch 85g", 20.0),
        ("Britannia Good Day Butter Cookies 120g", 30.0),
        ("Parle-G Gold Biscuits 250g", 30.0),
        ("Coca-Cola 750ml", 40.0),
        ("Thums Up 750ml", 40.0),
        ("Tata Tea Gold 250g", 150.0),
        ("Nescafe Classic Instant Coffee 50g", 195.0),
        ("Cadbury Dairy Milk Silk 60g", 85.0),
    ],
    "Personal Care": [
        ("Dove Deep Moisture Body Wash 190ml", 135.0),
        ("Dettol Original Bathing Soap 75g (Buy 3 Get 1)", 115.0),
        ("Colgate Strong Teeth Toothpaste 300g", 145.0),
        ("Head & Shoulders Cool Menthol Shampoo 180ml", 180.0),
        ("Nivea Men Dark Spot Reduction Creme 75ml", 160.0),
        ("Lifebuoy Total Handwash 750ml Refill", 119.0),
    ],
    "Household Essentials": [
        ("Surf Excel Easy Wash Detergent Powder 1kg", 140.0),
        ("Vim Dishwash Gel 500ml", 115.0),
        ("Harpic Disinfectant Bathroom Cleaner 500ml", 105.0),
        ("Lizol Surface Cleaner Citrus 500ml", 110.0),
        ("Good Knight Gold Flash Liquid Vaporizer Refill", 88.0),
        ("Origami Toilet Tissue Roll 4 in 1", 120.0),
    ]
}

age_groups = ["Youth (18-25)", "Young Adult (26-35)", "Middle-Aged (36-50)", "Senior (51+)"]
genders = ["Male", "Female"]
payment_modes = ["UPI", "Cash", "Credit Card", "Debit Card"]
counters = ["Counter 1 - Express", "Counter 2 - Regular", "Counter 3 - General", "Counter 4 - Self-Service"]

base_date = datetime(2026, 8, 18, 9, 30)
records = []
trans_counter = 1001

# Generate 70 distinct transactions with 1-5 items each -> approx 190-210 rows
num_transactions = 75

for t in range(num_transactions):
    trans_id = f"TXN-{trans_counter}"
    trans_counter += 1
    
    # Time spread across 7 days
    day_offset = random.randint(0, 6)
    hour_offset = random.randint(9, 21) # 9 AM to 9 PM
    min_offset = random.randint(0, 59)
    current_dt = base_date + timedelta(days=day_offset, hours=hour_offset - 9, minutes=min_offset)
    
    # Inconsistent date formats
    format_choice = random.random()
    if format_choice < 0.60:
        date_str = current_dt.strftime("%Y-%m-%d")
    elif format_choice < 0.85:
        date_str = current_dt.strftime("%d-%m-%Y")
    else:
        date_str = current_dt.strftime("%Y/%m/%d")
        
    time_str = current_dt.strftime("%H:%M:%S")
    
    # Customer profile
    cust_id = f"CUST-{random.randint(501, 560):03d}"
    age = random.choice(age_groups)
    gender = random.choice(genders)
    pay_mode = random.choices(payment_modes, weights=[0.55, 0.20, 0.15, 0.10])[0]
    counter = random.choice(counters)
    
    # Pick 1 to 5 items for this transaction basket
    # Frequent itemset correlations injected for realistic Apriori mining:
    # Rule 1: Milk -> Bread or Butter
    # Rule 2: Chips / Kurkure -> Cold Drink (Coca-Cola / Thums Up)
    # Rule 3: Detergent -> Dishwash Gel / Bathroom cleaner
    basket_items = []
    r_basket = random.random()
    if r_basket < 0.25:
        # Breakfast cluster
        basket_items.append(("Dairy & Bakery", "Amul Gold Milk 500ml", 33.0))
        basket_items.append(("Dairy & Bakery", "Britannia Brown Bread 400g", 45.0))
        if random.random() > 0.4:
            basket_items.append(("Dairy & Bakery", "Amul Butter 100g", 58.0))
        if random.random() > 0.6:
            basket_items.append(("Snacks & Beverages", "Tata Tea Gold 250g", 150.0))
    elif r_basket < 0.50:
        # Snack & party cluster
        basket_items.append(("Snacks & Beverages", "Lay's India's Magic Masala 50g", 20.0))
        basket_items.append(("Snacks & Beverages", "Coca-Cola 750ml", 40.0))
        if random.random() > 0.3:
            basket_items.append(("Snacks & Beverages", "Kurkure Masala Munch 85g", 20.0))
        if random.random() > 0.5:
            basket_items.append(("Snacks & Beverages", "Cadbury Dairy Milk Silk 60g", 85.0))
    elif r_basket < 0.70:
        # Household sanitation cluster
        basket_items.append(("Household Essentials", "Surf Excel Easy Wash Detergent Powder 1kg", 140.0))
        basket_items.append(("Household Essentials", "Vim Dishwash Gel 500ml", 115.0))
        if random.random() > 0.4:
            basket_items.append(("Household Essentials", "Harpic Disinfectant Bathroom Cleaner 500ml", 105.0))
    else:
        # Random multi-category grocery shopping
        num_items = random.randint(1, 4)
        for _ in range(num_items):
            cat = random.choice(list(catalog.keys()))
            prod, price = random.choice(catalog[cat])
            if (cat, prod, price) not in basket_items:
                basket_items.append((cat, prod, price))
                
    for cat, prod, price in basket_items:
        qty = random.choices([1, 2, 3, 4, 5], weights=[0.55, 0.25, 0.10, 0.07, 0.03])[0]
        disc = random.choices([0.0, 5.0, 10.0, 15.0, 20.0], weights=[0.45, 0.25, 0.15, 0.10, 0.05])[0]
        
        # Inconsistent Category and Product casing/typos in raw data
        raw_cat = cat
        raw_prod = prod
        raw_age = age
        raw_disc = disc
        
        noise_chance = random.random()
        if noise_chance < 0.04:
            raw_age = "" # Missing age
        if noise_chance < 0.05:
            raw_cat = cat.lower() # lowercase category
        elif noise_chance < 0.08:
            if "Snacks" in cat:
                raw_cat = "Snacks & Bev."
            elif "Dairy" in cat:
                raw_cat = "Dairy&Bakery"
                
        if noise_chance < 0.04:
            raw_disc = np.nan # Missing discount
            
        records.append({
            "Transaction_ID": trans_id,
            "Date": date_str,
            "Time": time_str,
            "Customer_ID": cust_id,
            "Customer_Age_Group": raw_age,
            "Customer_Gender": gender,
            "Product_Category": raw_cat,
            "Product_Name": raw_prod,
            "Unit_Price_INR": price,
            "Quantity": qty,
            "Discount_Percent": raw_disc,
            "Payment_Mode": pay_mode,
            "Store_Counter": counter
        })

df_raw = pd.DataFrame(records)

# Inject intentional duplicate rows (e.g. double scanning an item)
dup_rows = df_raw.sample(n=6, random_state=101)
df_raw = pd.concat([df_raw, dup_rows], ignore_index=True)

# Inject an intentional extreme outlier quantity to demonstrate anomaly detection
outlier_idx = random.randint(10, len(df_raw) - 10)
df_raw.loc[outlier_idx, "Quantity"] = 50 # massive bulk error on standard retail item

# Shuffle rows slightly to simulate real continuous log
df_raw = df_raw.sample(frac=1.0, random_state=42).reset_index(drop=True)

raw_path = os.path.join("data", "raw_supermarket_transactions.csv")
df_raw.to_csv(raw_path, index=False)

print(f"[SUCCESS] Generated raw supermarket transaction dataset: {raw_path}")
print(f"Total Rows: {len(df_raw)}")
print(f"Unique Transactions: {df_raw['Transaction_ID'].nunique()}")
print(f"Null Values per Column:\n{df_raw.isnull().sum()}")
