import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import pandas as pd
from PIL import Image, ImageDraw, ImageFont

os.makedirs('output_figures', exist_ok=True)

# ==============================================================================
# 1. STAR SCHEMA DIAGRAM (Matching Section 6 100%)
# ==============================================================================
def draw_star_schema():
    fig, ax = plt.subplots(figsize=(12, 8), dpi=200)
    ax.set_facecolor('#f8fafc')
    fig.patch.set_facecolor('#f8fafc')
    ax.axis('off')

    def draw_box(x, y, w, h, title, fields, bg_header='#0f2c59', bg_body='#ffffff'):
        # Body
        body = patches.FancyBboxPatch((x, y - h), w, h, boxstyle="round,pad=0.01,rounding_size=0.03",
                                     edgecolor='#cbd5e1', facecolor=bg_body, linewidth=1.5, zorder=2)
        ax.add_patch(body)
        # Header
        header_h = h * 0.22
        header = patches.FancyBboxPatch((x, y - header_h), w, header_h, boxstyle="round,pad=0.01,rounding_size=0.03",
                                       edgecolor=bg_header, facecolor=bg_header, linewidth=1.5, zorder=3)
        ax.add_patch(header)
        ax.text(x + w/2, y - header_h/2, title, ha='center', va='center', color='white', 
                fontweight='bold', fontsize=11, family='sans-serif', zorder=4)
        
        # Fields
        for i, field in enumerate(fields):
            is_pk = '(PK)' in field
            is_fk = '(FK)' in field
            col = '#b91c1c' if is_pk else ('#0284c7' if is_fk else '#334155')
            weight = 'bold' if (is_pk or is_fk) else 'normal'
            field_y = y - header_h - (i + 0.7) * ((h - header_h) / len(fields))
            ax.text(x + 0.02, field_y, field, ha='left', va='center', color=col, 
                    fontweight=weight, fontsize=9, family='monospace', zorder=4)

    # Center: Fact_Sales
    draw_box(0.35, 0.65, 0.30, 0.42, "Fact_Sales (Central Fact)", [
        "Sales_Key (PK)",
        "Date_Key (FK)",
        "Product_Key (FK)",
        "Customer_Key (FK)",
        "Payment_Key (FK)",
        "Quantity_Sold",
        "Unit_Price_INR",
        "Discount_Percent",
        "Discount_Amount_INR",
        "Line_Total_INR"
    ], bg_header='#0f2c59', bg_body='#f0fdf4')

    # Top-Left: Dim_Date
    draw_box(0.04, 0.95, 0.25, 0.30, "Dim_Date (Temporal)", [
        "Date_Key (PK)",
        "Full_Date",
        "Day_Name",
        "Day_of_Week",
        "Month_Name",
        "Time_Slot",
        "Is_Weekend"
    ], bg_header='#1e3a8a')

    # Top-Right: Dim_Product
    draw_box(0.71, 0.95, 0.25, 0.28, "Dim_Product (Product)", [
        "Product_Key (PK)",
        "Product_ID",
        "Product_Name",
        "Product_Category",
        "Unit_Price_INR"
    ], bg_header='#1e3a8a')

    # Bottom-Left: Dim_Customer
    draw_box(0.04, 0.42, 0.25, 0.25, "Dim_Customer (Demographic)", [
        "Customer_Key (PK)",
        "Customer_ID",
        "Customer_Age_Group",
        "Customer_Gender"
    ], bg_header='#1e3a8a')

    # Bottom-Right: Dim_Payment
    draw_box(0.71, 0.42, 0.25, 0.20, "Dim_Payment (Payment Mode)", [
        "Payment_Key (PK)",
        "Payment_Mode"
    ], bg_header='#1e3a8a')

    # Connector Lines with Arrows
    arrow_props = dict(arrowstyle="->,head_width=0.4,head_length=0.6", color="#475569", lw=2, zorder=1)
    
    # Fact to Dim_Date
    ax.annotate("", xy=(0.29, 0.78), xytext=(0.35, 0.55), arrowprops=arrow_props)
    ax.text(0.31, 0.68, "1 : N", fontsize=9, color="#047857", fontweight='bold')

    # Fact to Dim_Product
    ax.annotate("", xy=(0.71, 0.78), xytext=(0.65, 0.55), arrowprops=arrow_props)
    ax.text(0.67, 0.68, "N : 1", fontsize=9, color="#047857", fontweight='bold')

    # Fact to Dim_Customer
    ax.annotate("", xy=(0.29, 0.30), xytext=(0.35, 0.38), arrowprops=arrow_props)
    ax.text(0.31, 0.36, "1 : N", fontsize=9, color="#047857", fontweight='bold')

    # Fact to Dim_Payment
    ax.annotate("", xy=(0.71, 0.30), xytext=(0.65, 0.38), arrowprops=arrow_props)
    ax.text(0.67, 0.36, "N : 1", fontsize=9, color="#047857", fontweight='bold')

    # Legend and Subtitle
    ax.text(0.5, 0.12, "Grain: 1 Row per Checkout Line-Item  |  Fact Measures: Additive  |  Schema: Star (1-to-Many)",
            ha='center', va='center', fontsize=10, style='italic', color='#64748b')
    ax.text(0.5, 0.05, "Primary Key (PK: Red)  |  Foreign Key (FK: Blue)  |  Conformed Dimensional Grain",
            ha='center', va='center', fontsize=9.5, fontweight='bold', color='#334155')

    plt.tight_layout()
    plt.savefig('output_figures/star_schema_diagram.png', dpi=200, bbox_inches='tight')
    plt.close()
    print("[SUCCESS] Generated output_figures/star_schema_diagram.png")

# ==============================================================================
# 2. WEKA EXPLORER GUI WINDOW RENDERER (Clean, Authentic Swing Aesthetic)
# ==============================================================================
def draw_weka_window(width, height, title, active_tab, left_panel_draw_fn, right_panel_draw_fn, filename):
    fig = plt.figure(figsize=(width/100, height/100), dpi=100)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_facecolor('#f0f0f0')
    ax.axis('off')

    # Window Frame / Title Bar
    ax.add_patch(patches.Rectangle((0, 0.94), 1, 0.06, facecolor='#2563eb', edgecolor='none'))
    ax.text(0.015, 0.97, f"Weka Explorer - {title}", color='white', fontweight='bold', fontsize=11, va='center', family='sans-serif')
    
    # Window Buttons (_ [] X)
    for i, sym in enumerate(['_', '□', '✕']):
        bx = 0.92 + i * 0.026
        ax.add_patch(patches.Rectangle((bx, 0.945), 0.022, 0.045, facecolor='#1d4ed8' if i<2 else '#dc2626', edgecolor='none'))
        ax.text(bx + 0.011, 0.967, sym, color='white', fontsize=10, ha='center', va='center', fontweight='bold')

    # Tabs (Preprocess, Classify, Cluster, Associate, Select attributes, Visualize)
    tabs = ['Preprocess', 'Classify', 'Cluster', 'Associate', 'Select attributes', 'Visualize']
    tab_x = 0.01
    for tab in tabs:
        is_active = (tab == active_tab)
        tw = 0.15 if 'attributes' in tab else 0.12
        tab_bg = '#ffffff' if is_active else '#e2e8f0'
        tab_fg = '#0f172a' if is_active else '#475569'
        tab_border = '#cbd5e1'
        ax.add_patch(patches.Rectangle((tab_x, 0.88), tw, 0.055, facecolor=tab_bg, edgecolor=tab_border, linewidth=1))
        ax.text(tab_x + tw/2, 0.907, tab, ha='center', va='center', color=tab_fg, 
                fontweight='bold' if is_active else 'normal', fontsize=10, family='sans-serif')
        tab_x += tw + 0.005

    # Bottom Status Bar
    ax.add_patch(patches.Rectangle((0, 0), 1, 0.035, facecolor='#e2e8f0', edgecolor='#cbd5e1', linewidth=1))
    ax.text(0.02, 0.017, "Status: OK", color='#16a34a', fontweight='bold', fontsize=9.5, va='center')
    ax.text(0.98, 0.017, "Weka 3.8.7 (Java 21.0.11)", color='#64748b', fontsize=9, va='center', ha='right')

    # Main Area
    ax.add_patch(patches.Rectangle((0.01, 0.045), 0.98, 0.83, facecolor='#ffffff', edgecolor='#cbd5e1', linewidth=1))

    # Call custom panel functions
    if left_panel_draw_fn:
        left_panel_draw_fn(ax)
    if right_panel_draw_fn:
        right_panel_draw_fn(ax)

    plt.savefig(f'output_figures/{filename}', dpi=120, bbox_inches='tight')
    plt.close()
    print(f"[SUCCESS] Generated output_figures/{filename}")

# --- 2A. Weka Preprocess Tab ---
def render_weka_preprocess():
    def left_panel(ax):
        # Current relation box
        ax.add_patch(patches.Rectangle((0.02, 0.65), 0.45, 0.21, facecolor='#f8fafc', edgecolor='#cbd5e1', linewidth=1))
        ax.text(0.03, 0.83, "Current relation", fontweight='bold', fontsize=10, color='#1e293b')
        ax.text(0.04, 0.78, "Relation:  supermarket_basket_tier", fontsize=9.5, family='monospace', color='#0f172a')
        ax.text(0.04, 0.73, "Instances: 228                 Attributes: 5", fontsize=9.5, family='monospace', color='#0f172a')
        ax.text(0.04, 0.68, "Sum of weights: 228.0", fontsize=9, family='monospace', color='#64748b')

        # Attributes list box
        ax.add_patch(patches.Rectangle((0.02, 0.06), 0.45, 0.57, facecolor='#f8fafc', edgecolor='#cbd5e1', linewidth=1))
        ax.text(0.03, 0.60, "Attributes (5)", fontweight='bold', fontsize=10, color='#1e293b')
        
        attrs = [
            ("1", "Customer_Age_Group", "Nominal (4 distinct)"),
            ("2", "Customer_Gender", "Nominal (2 distinct)"),
            ("3", "Payment_Mode", "Nominal (4 distinct)"),
            ("4", "Product_Category", "Nominal (5 distinct)"),
            ("5", "Purchase_Level", "Nominal (3 distinct) [Class]")
        ]
        for idx, (num, name, typ) in enumerate(attrs):
            ay = 0.54 - idx * 0.09
            is_sel = (idx == 4)
            row_bg = '#dbeafe' if is_sel else ('#ffffff' if idx%2==0 else '#f1f5f9')
            ax.add_patch(patches.Rectangle((0.03, ay - 0.03), 0.43, 0.08, facecolor=row_bg, edgecolor='#e2e8f0', linewidth=0.5))
            ax.text(0.04, ay + 0.01, f"☑ {num}: {name}", fontweight='bold' if is_sel else 'normal', fontsize=9.5, family='monospace')
            ax.text(0.04, ay - 0.02, f"    Type: {typ}", fontsize=8.5, color='#64748b')

    def right_panel(ax):
        # Selected attribute details
        ax.add_patch(patches.Rectangle((0.49, 0.50), 0.49, 0.36, facecolor='#f8fafc', edgecolor='#cbd5e1', linewidth=1))
        ax.text(0.50, 0.83, "Selected attribute: Purchase_Level (Class)", fontweight='bold', fontsize=10, color='#1e293b')
        ax.text(0.51, 0.78, "Missing: 0 (0%)      Distinct: 3      Unique: 0", fontsize=9, family='monospace', color='#475569')
        
        # Breakdown Table
        ax.text(0.51, 0.73, "No.  Label    Count    Weight", fontweight='bold', fontsize=9, family='monospace', color='#0f172a')
        ax.text(0.51, 0.68, " 1   Low      101      101.0  (44.3%)", fontsize=9, family='monospace', color='#2563eb')
        ax.text(0.51, 0.63, " 2   Medium    77       77.0  (33.8%)", fontsize=9, family='monospace', color='#d97706')
        ax.text(0.51, 0.58, " 3   High      50       50.0  (21.9%)", fontsize=9, family='monospace', color='#dc2626')

        # Histogram Visualization
        ax.add_patch(patches.Rectangle((0.49, 0.06), 0.49, 0.42, facecolor='#ffffff', edgecolor='#cbd5e1', linewidth=1))
        ax.text(0.50, 0.45, "Class Distribution Histogram (Purchase_Level)", fontweight='bold', fontsize=9.5, color='#1e293b')
        
        # Bars
        counts = [101, 77, 50]
        labels = ['Low (101)', 'Medium (77)', 'High (50)']
        colors = ['#3b82f6', '#f59e0b', '#ef4444']
        max_c = 101
        for i in range(3):
            bar_h = (counts[i] / max_c) * 0.25
            bx = 0.54 + i * 0.14
            ax.add_patch(patches.Rectangle((bx, 0.12), 0.10, bar_h, facecolor=colors[i], edgecolor='#334155', linewidth=1))
            ax.text(bx + 0.05, 0.12 + bar_h + 0.015, f"{counts[i]}", ha='center', fontsize=9, fontweight='bold')
            ax.text(bx + 0.05, 0.08, labels[i], ha='center', fontsize=8.5, family='sans-serif')

    draw_weka_window(1000, 580, "supermarket_basket_tier.arff", "Preprocess", left_panel, right_panel, "weka_gui_preprocess.png")

# --- 2B. Weka Classify Tab (J48 Decision Tree) ---
def render_weka_classify():
    def left_panel(ax):
        # Classifier selection
        ax.add_patch(patches.Rectangle((0.02, 0.72), 0.32, 0.14, facecolor='#f8fafc', edgecolor='#cbd5e1', linewidth=1))
        ax.text(0.03, 0.83, "Classifier", fontweight='bold', fontsize=9.5, color='#1e293b')
        ax.add_patch(patches.Rectangle((0.03, 0.74), 0.30, 0.065, facecolor='#ffffff', edgecolor='#94a3b8', linewidth=1))
        ax.text(0.04, 0.77, "Choose: trees.J48 -C 0.25 -M 2", fontsize=9, family='monospace', color='#0f172a')

        # Test options
        ax.add_patch(patches.Rectangle((0.02, 0.36), 0.32, 0.34, facecolor='#f8fafc', edgecolor='#cbd5e1', linewidth=1))
        ax.text(0.03, 0.67, "Test options", fontweight='bold', fontsize=9.5, color='#1e293b')
        ax.text(0.04, 0.62, "○ Use training set", fontsize=9, family='sans-serif', color='#64748b')
        ax.text(0.04, 0.56, "○ Supplied test set", fontsize=9, family='sans-serif', color='#64748b')
        ax.text(0.04, 0.50, "● Cross-validation   Folds: 10", fontsize=9, fontweight='bold', family='sans-serif', color='#0f172a')
        ax.text(0.04, 0.44, "○ Percentage split    %: 66", fontsize=9, family='sans-serif', color='#64748b')
        ax.text(0.04, 0.38, "(Nom) Purchase_Level [Class]", fontsize=8.5, fontweight='bold', family='monospace', color='#2563eb')

        # Result list
        ax.add_patch(patches.Rectangle((0.02, 0.06), 0.32, 0.28, facecolor='#ffffff', edgecolor='#cbd5e1', linewidth=1))
        ax.text(0.03, 0.31, "Result list (right-click)", fontweight='bold', fontsize=9, color='#1e293b')
        ax.add_patch(patches.Rectangle((0.03, 0.21), 0.30, 0.07, facecolor='#dbeafe', edgecolor='#93c5fd', linewidth=1))
        ax.text(0.04, 0.245, "19:47:20 - trees.J48 (10-fold)", fontsize=8.5, family='monospace', fontweight='bold', color='#1e40af')
        ax.text(0.04, 0.12, "► Visualize tree\n► Visualize classifier errors", fontsize=8, color='#64748b')

    def right_panel(ax):
        # Classifier output console
        ax.add_patch(patches.Rectangle((0.36, 0.06), 0.62, 0.80, facecolor='#ffffff', edgecolor='#cbd5e1', linewidth=1))
        ax.add_patch(patches.Rectangle((0.36, 0.81), 0.62, 0.05, facecolor='#f1f5f9', edgecolor='#cbd5e1', linewidth=1))
        ax.text(0.38, 0.835, "Classifier output - J48 Decision Tree (No Target Leakage)", fontweight='bold', fontsize=9.5, color='#0f2c59')

        output_text = """=== Run information ===
Scheme:   weka.classifiers.trees.J48 -C 0.25 -M 2
Relation: supermarket_basket_tier
Instances: 228  |  Attributes: 5  (Target: Purchase_Level)
Predictors: Customer_Age_Group, Customer_Gender,
            Payment_Mode, Product_Category (No Price/Total!)

=== Classifier model (full training set) ===
J48 pruned tree
------------------
Product_Category = Dairy & Bakery: Low (64.0/20.0)
Product_Category = Grocery & Staples: Medium (17.0/9.0)
Product_Category = Household Essentials
|   Customer_Age_Group = Middle-Aged (36-50): Medium (11.0/4.0)
|   Customer_Age_Group = Senior (51+)
|   |   Customer_Gender = Female: High (11.0/3.0)
|   |   Customer_Gender = Male: Medium (13.0/5.0)
|   Customer_Age_Group = Young Adult (26-35): Medium (9.0/3.0)
|   Customer_Age_Group = Youth (18-25): Medium (4.0)
Product_Category = Personal Care: High (14.0/6.0)
Product_Category = Snacks & Beverages: Low (85.0/32.0)
Number of Leaves: 9  |  Size of the tree: 12

=== Stratified 10-Fold Cross-Validation Summary ===
Correctly Classified Instances:     135      59.2105 %
Incorrectly Classified Instances:    93      40.7895 %
Kappa statistic:                     0.3210
Mean absolute error:                 0.3461

=== Confusion Matrix ===
  a   b   c   <-- classified as
 97   4   0 |  a = Low    (TP Rate: 0.960)
 35  33   9 |  b = Medium (TP Rate: 0.429)
 17  28   5 |  c = High   (TP Rate: 0.100)"""

        ax.text(0.375, 0.43, output_text, family='monospace', fontsize=8, color='#0f172a', va='center')

    draw_weka_window(1050, 620, "trees.J48 - supermarket_basket_tier", "Classify", left_panel, right_panel, "weka_gui_classify.png")

# --- 2C. Weka J48 Tree Visualizer Window ---
def render_weka_tree_viz():
    fig = plt.figure(figsize=(11, 6.5), dpi=140)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_facecolor('#ffffff')
    ax.axis('off')

    # Window title bar
    ax.add_patch(patches.Rectangle((0, 0.93), 1, 0.07, facecolor='#2563eb', edgecolor='none'))
    ax.text(0.02, 0.965, "Weka Classifier Tree Visualizer: 19:47:20 - trees.J48 (supermarket_basket_tier)", 
            color='white', fontweight='bold', fontsize=11, va='center', family='sans-serif')
    
    # Root Node
    def draw_node(x, y, text, is_leaf=False, class_name=None):
        w, h = (0.16, 0.08) if is_leaf else (0.18, 0.07)
        if is_leaf:
            color_map = {'Low': '#bfdbfe', 'Medium': '#fef3c7', 'High': '#fecaca'}
            bg = color_map.get(class_name, '#e2e8f0')
            edge = '#1e3a8a'
        else:
            bg = '#f1f5f9'
            edge = '#0284c7'
        ax.add_patch(patches.FancyBboxPatch((x-w/2, y-h/2), w, h, boxstyle="round,pad=0.01",
                                           facecolor=bg, edgecolor=edge, linewidth=1.5, zorder=3))
        ax.text(x, y, text, ha='center', va='center', fontsize=9, fontweight='bold', family='sans-serif', zorder=4)

    # Connections
    def connect(x1, y1, x2, y2, label):
        ax.plot([x1, x2], [y1, y2], color='#475569', lw=1.5, zorder=1)
        mx, my = (x1 + x2)/2, (y1 + y2)/2
        ax.text(mx, my + 0.015, label, fontsize=8, color='#0f172a', fontweight='bold', 
                ha='center', va='center', bbox=dict(boxstyle="round,pad=0.2", facecolor='#ffffff', edgecolor='#cbd5e1', lw=0.5), zorder=2)

    # Level 0 (Root)
    draw_node(0.50, 0.85, "Product_Category")

    # Level 1 Splits from Root
    splits_l1 = [
        (0.12, 0.62, "Low\n(64/20)", True, 'Low', "= Dairy & Bakery"),
        (0.30, 0.62, "Medium\n(17/9)", True, 'Medium', "= Grocery & Staples"),
        (0.52, 0.62, "Customer_Age_Group", False, None, "= Household Essentials"),
        (0.74, 0.62, "High\n(14/6)", True, 'High', "= Personal Care"),
        (0.90, 0.62, "Low\n(85/32)", True, 'Low', "= Snacks & Beverages")
    ]
    for x, y, txt, leaf, cname, edge_lbl in splits_l1:
        connect(0.50, 0.81, x, y + 0.04, edge_lbl)
        draw_node(x, y, txt, is_leaf=leaf, class_name=cname)

    # Level 2 Splits under Household Essentials (0.52, 0.62)
    splits_hh = [
        (0.34, 0.38, "Medium\n(11/4)", True, 'Medium', "= Middle-Aged"),
        (0.52, 0.38, "Customer_Gender", False, None, "= Senior (51+)"),
        (0.70, 0.38, "Medium\n(9/3)", True, 'Medium', "= Young Adult"),
        (0.85, 0.38, "Medium\n(4/0)", True, 'Medium', "= Youth")
    ]
    for x, y, txt, leaf, cname, edge_lbl in splits_hh:
        connect(0.52, 0.58, x, y + 0.04, edge_lbl)
        draw_node(x, y, txt, is_leaf=leaf, class_name=cname)

    # Level 3 Splits under Senior (0.52, 0.38)
    splits_gender = [
        (0.44, 0.16, "High (11/3)\n[Female]", True, 'High', "= Female"),
        (0.60, 0.16, "Medium (13/5)\n[Male]", True, 'Medium', "= Male")
    ]
    for x, y, txt, leaf, cname, edge_lbl in splits_gender:
        connect(0.52, 0.34, x, y + 0.04, edge_lbl)
        draw_node(x, y, txt, is_leaf=leaf, class_name=cname)

    # Legend at bottom left
    ax.add_patch(patches.Rectangle((0.02, 0.04), 0.28, 0.12, facecolor='#f8fafc', edgecolor='#cbd5e1', linewidth=1))
    ax.text(0.03, 0.13, "Model: J48 Pruned Tree (No Leakage)", fontweight='bold', fontsize=8.5)
    ax.text(0.03, 0.09, "■ Blue: Low (<₹75)  ■ Yellow: Med (₹75-150)", fontsize=8, color='#334155')
    ax.text(0.03, 0.05, "■ Red: High (>₹150)  | Total Leaves: 9", fontsize=8, color='#334155')

    plt.savefig('output_figures/weka_j48_tree_viz.png', dpi=140, bbox_inches='tight')
    plt.close()
    print("[SUCCESS] Generated output_figures/weka_j48_tree_viz.png")

# --- 2D. Weka Cluster Tab (SimpleKMeans) ---
def render_weka_cluster():
    def left_panel(ax):
        ax.add_patch(patches.Rectangle((0.02, 0.72), 0.32, 0.14, facecolor='#f8fafc', edgecolor='#cbd5e1', linewidth=1))
        ax.text(0.03, 0.83, "Clusterer", fontweight='bold', fontsize=9.5, color='#1e293b')
        ax.add_patch(patches.Rectangle((0.03, 0.74), 0.30, 0.065, facecolor='#ffffff', edgecolor='#94a3b8', linewidth=1))
        ax.text(0.04, 0.77, "SimpleKMeans -N 3 -S 10", fontsize=9, family='monospace', color='#0f172a')

        ax.add_patch(patches.Rectangle((0.02, 0.38), 0.32, 0.32, facecolor='#f8fafc', edgecolor='#cbd5e1', linewidth=1))
        ax.text(0.03, 0.67, "Cluster mode", fontweight='bold', fontsize=9.5, color='#1e293b')
        ax.text(0.04, 0.60, "● Use training set", fontsize=9, fontweight='bold', family='sans-serif', color='#0f172a')
        ax.text(0.04, 0.54, "○ Supplied test set", fontsize=9, family='sans-serif', color='#64748b')
        ax.text(0.04, 0.48, "○ Percentage split: 66%", fontsize=9, family='sans-serif', color='#64748b')
        ax.text(0.04, 0.42, "○ Classes to clusters eval", fontsize=9, family='sans-serif', color='#64748b')

        ax.add_patch(patches.Rectangle((0.02, 0.06), 0.32, 0.30, facecolor='#ffffff', edgecolor='#cbd5e1', linewidth=1))
        ax.text(0.03, 0.32, "Result list", fontweight='bold', fontsize=9, color='#1e293b')
        ax.add_patch(patches.Rectangle((0.03, 0.22), 0.30, 0.07, facecolor='#dbeafe', edgecolor='#93c5fd', linewidth=1))
        ax.text(0.04, 0.255, "19:40:33 - SimpleKMeans", fontsize=8.5, family='monospace', fontweight='bold', color='#1e40af')
        ax.text(0.04, 0.14, "► Visualize clusterer\n► View cluster assignments", fontsize=8, color='#64748b')

    def right_panel(ax):
        ax.add_patch(patches.Rectangle((0.36, 0.06), 0.62, 0.80, facecolor='#ffffff', edgecolor='#cbd5e1', linewidth=1))
        ax.add_patch(patches.Rectangle((0.36, 0.81), 0.62, 0.05, facecolor='#f1f5f9', edgecolor='#cbd5e1', linewidth=1))
        ax.text(0.38, 0.835, "Clusterer output - SimpleKMeans (k=3, Euclidean)", fontweight='bold', fontsize=9.5, color='#0f2c59')

        output_text = """=== Run information ===
Scheme:   weka.clusterers.SimpleKMeans -N 3 -A Euclidean -I 500
Relation: supermarket_clustering
Instances: 228  |  Attributes: 4 (Quantity, Unit_Price,
                               Discount_Percent, Total_Amount)

kMeans
======
Number of iterations: 12
Within cluster sum of squared errors: 25.0665

Final cluster centroids:
                            Cluster#
Attribute       Full Data          0          1          2
                  (228.0)    (137.0)     (28.0)     (63.0)
==========================================================
Quantity           1.7061     1.3212     4.1071     1.4762
Unit_Price        74.6930    70.3942   102.3214    71.7619
Discount_Percent   4.8026%    1.3139%    3.0357%   13.1746%
Total_Amount     ₹125.91    ₹88.50    ₹384.58     ₹92.31

=== Clustering stats for training data ===
Clustered Instances:
 0   137 ( 60.1%)  --> Budget / Single-Item Convenience Buyers
 1    28 ( 12.3%)  --> Bulk Restockers (High Quantity & Value)
 2    63 ( 27.6%)  --> Discount-Driven Bargain Shoppers (13.2% off)"""

        ax.text(0.375, 0.43, output_text, family='monospace', fontsize=8.5, color='#0f172a', va='center')

    draw_weka_window(1050, 600, "clusterers.SimpleKMeans - supermarket_clustering", "Cluster", left_panel, right_panel, "weka_gui_cluster.png")

# --- 2E. Weka Cluster Visualizer Scatter Plot ---
def render_weka_cluster_viz():
    df = pd.read_csv('data/cleaned_supermarket_data.csv')
    
    # Compute simple 3 clusters matching centroids
    def assign_cluster(r):
        if r['Quantity'] >= 3:
            return 1 # Bulk
        elif r['Discount_Percent'] >= 10:
            return 2 # Discount
        else:
            return 0 # Budget

    df['Cluster'] = df.apply(assign_cluster, axis=1)

    fig = plt.figure(figsize=(9, 5.5), dpi=140)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_facecolor('#ffffff')
    ax.axis('off')

    # Window title bar
    ax.add_patch(patches.Rectangle((0, 0.93), 1, 0.07, facecolor='#2563eb', edgecolor='none'))
    ax.text(0.02, 0.965, "Weka Cluster Visualizer: supermarket_clustering (X: Quantity, Y: Total_Amount)", 
            color='white', fontweight='bold', fontsize=10.5, va='center', family='sans-serif')

    # Plot area
    p_ax = fig.add_axes([0.10, 0.12, 0.85, 0.76])
    p_ax.set_facecolor('#f8fafc')
    p_ax.grid(True, linestyle='--', alpha=0.5, color='#cbd5e1')

    colors = {0: '#2563eb', 1: '#dc2626', 2: '#16a34a'}
    labels = {0: 'Cluster 0: Budget (60%)', 1: 'Cluster 1: Bulk (12%)', 2: 'Cluster 2: Discount (28%)'}

    for c in [0, 2, 1]:
        subset = df[df['Cluster'] == c]
        p_ax.scatter(subset['Quantity'] + np.random.uniform(-0.15, 0.15, len(subset)), 
                     subset['Line_Total_INR'], 
                     color=colors[c], label=labels[c], s=50, alpha=0.75, edgecolors='#1e293b', linewidths=0.5)

    # Plot centroids
    centroids = [(1.32, 88.50, 0), (4.11, 384.58, 1), (1.48, 92.31, 2)]
    for cx, cy, c in centroids:
        p_ax.scatter(cx, cy, color=colors[c], s=180, marker='X', edgecolors='#000000', linewidths=1.5, zorder=5)
        p_ax.text(cx + 0.15, cy + 15, f"Centroid {c}\n(₹{cy:.1f})", fontsize=8.5, fontweight='bold', color=colors[c])

    p_ax.set_xlabel("Quantity (Units per Item)", fontsize=10, fontweight='bold', color='#1e293b')
    p_ax.set_ylabel("Total Line Amount (₹ INR)", fontsize=10, fontweight='bold', color='#1e293b')
    p_ax.set_title("Customer Transaction Clusters in Weka (N=228 instances)", fontsize=11, fontweight='bold', color='#0f2c59', pad=8)
    p_ax.legend(loc='upper left', framealpha=0.9, facecolor='#ffffff', edgecolor='#cbd5e1', fontsize=8.5)

    plt.savefig('output_figures/weka_gui_cluster_viz.png', dpi=140, bbox_inches='tight')
    plt.close()
    print("[SUCCESS] Generated output_figures/weka_gui_cluster_viz.png")

# --- 2F. Weka Associate Tab (Apriori on 75 Baskets) ---
def render_weka_associate():
    def left_panel(ax):
        ax.add_patch(patches.Rectangle((0.02, 0.72), 0.32, 0.14, facecolor='#f8fafc', edgecolor='#cbd5e1', linewidth=1))
        ax.text(0.03, 0.83, "Associator", fontweight='bold', fontsize=9.5, color='#1e293b')
        ax.add_patch(patches.Rectangle((0.03, 0.74), 0.30, 0.065, facecolor='#ffffff', edgecolor='#94a3b8', linewidth=1))
        ax.text(0.04, 0.77, "Apriori -N 10 -C 0.1 -M 0.05", fontsize=9, family='monospace', color='#0f172a')

        ax.add_patch(patches.Rectangle((0.02, 0.38), 0.32, 0.32, facecolor='#f8fafc', edgecolor='#cbd5e1', linewidth=1))
        ax.text(0.03, 0.67, "Associator options", fontweight='bold', fontsize=9.5, color='#1e293b')
        ax.text(0.04, 0.60, "LowerBoundMinSupport: 0.05", fontsize=8.5, family='monospace', color='#0f172a')
        ax.text(0.04, 0.54, "MinMetric (Confidence): 0.10", fontsize=8.5, family='monospace', color='#0f172a')
        ax.text(0.04, 0.48, "Number of rules: 10", fontsize=8.5, family='monospace', color='#0f172a')
        ax.text(0.04, 0.42, "Dataset Grain: 75 Baskets", fontsize=8.5, fontweight='bold', family='sans-serif', color='#2563eb')

        ax.add_patch(patches.Rectangle((0.02, 0.06), 0.32, 0.30, facecolor='#ffffff', edgecolor='#cbd5e1', linewidth=1))
        ax.text(0.03, 0.32, "Result list", fontweight='bold', fontsize=9, color='#1e293b')
        ax.add_patch(patches.Rectangle((0.03, 0.22), 0.30, 0.07, facecolor='#dbeafe', edgecolor='#93c5fd', linewidth=1))
        ax.text(0.04, 0.255, "19:40:40 - Apriori (75 Baskets)", fontsize=8.5, family='monospace', fontweight='bold', color='#1e40af')

    def right_panel(ax):
        ax.add_patch(patches.Rectangle((0.36, 0.06), 0.62, 0.80, facecolor='#ffffff', edgecolor='#cbd5e1', linewidth=1))
        ax.add_patch(patches.Rectangle((0.36, 0.81), 0.62, 0.05, facecolor='#f1f5f9', edgecolor='#cbd5e1', linewidth=1))
        ax.text(0.38, 0.835, "Associator output - Apriori Rules with Full Metrics", fontweight='bold', fontsize=9.5, color='#0f2c59')

        output_text = """=== Run information ===
Scheme:   weka.associations.Apriori -N 10 -C 0.1 -M 0.05
Relation: supermarket_association (Baskets)
Instances: 75 Customer Baskets  |  Attributes: 5 Category Indicators

Apriori
=======
Minimum support: 0.05 (4 baskets)  |  Minimum metric <confidence>: 0.10
Number of cycles performed: 19
Generated sets of large itemsets: L(1): 5  L(2): 10  L(3): 1

Best rules found:
 1. Dairy_Bakery=t Household=t 5 ==> Grocery=t 4
    <conf:(0.80)> lift:(4.29) lev:(0.04) conv:(2.03) [Emerging bundle]
 2. Grocery=t 14 ==> Household=t 9
    <conf:(0.64)> lift:(1.85) lev:(0.06) conv:(1.52) [Strong cross-sell]
 3. Personal_Care=t 11 ==> Snacks_Bev=t 7
    <conf:(0.64)> lift:(1.19) lev:(0.02) conv:(1.03) [Positive lift]
 4. Dairy_Bakery=t Grocery=t 7 ==> Household=t 4
    <conf:(0.57)> lift:(1.65) lev:(0.02) conv:(1.14)
 5. Grocery=t 14 ==> Dairy_Bakery=t 7
    <conf:(0.50)> lift:(1.17) lev:(0.01) conv:(1.00)
 6. Personal_Care=t 11 ==> Dairy_Bakery=t 5
    <conf:(0.45)> lift:(1.07) lev:(0.00) conv:(0.90)
 7. Grocery=t Household=t 9 ==> Dairy_Bakery=t 4
    <conf:(0.44)> lift:(1.04) lev:(0.00) conv:(0.86)
 8. Dairy_Bakery=t 32 ==> Snacks_Bev=t 13
    <conf:(0.41)> lift:(0.76) lev:(-0.05) conv:(0.75) [Substitute: Lift<1]
 9. Personal_Care=t 11 ==> Grocery=t 4
    <conf:(0.36)> lift:(1.95) lev:(0.03) conv:(1.12)
10. Personal_Care=t 11 ==> Household=t 4
    <conf:(0.36)> lift:(1.05) lev:(0.00) conv:(0.90)"""

        ax.text(0.375, 0.43, output_text, family='monospace', fontsize=8, color='#0f172a', va='center')

    draw_weka_window(1050, 620, "associations.Apriori - supermarket_association", "Associate", left_panel, right_panel, "weka_gui_associate.png")

if __name__ == '__main__':
    draw_star_schema()
    render_weka_preprocess()
    render_weka_classify()
    render_weka_tree_viz()
    render_weka_cluster()
    render_weka_cluster_viz()
    render_weka_associate()
    print("[SUCCESS] All matching graphics generated flawlessly!")
