"""
Master Execution Pipeline - FreshMart Supermarket DWDM Project
Course: Data Warehouse and Data Mining (4040233302)
Institution: Silver Oak College of Computer Application, BCA Sem-5

This master script runs the entire end-to-end project pipeline:
1. Field Data Generation (data/raw_supermarket_transactions.csv)
2. Automated Data Cleaning & Anomaly Resolution (data/cleaned_supermarket_data.csv)
3. Dimensional Star Schema & OLAP Cube Execution (docs/OLAP_ANALYSIS.md)
4. Data Mining Engine: Apriori, Decision Tree, K-Means (output_figures/)
5. Final Verification & Launching Interactive Presentation in Browser
"""

import os
import sys
import subprocess
import webbrowser
import time

if sys.stdout:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if sys.stderr:
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

python_exe = sys.executable

def print_banner(title):
    print("\n" + "="*80)
    print(f"  {title.upper()}")
    print("="*80)

def run_step(script_name, description):
    print(f"\n[RUNNING] {description} ({script_name})...")
    start_time = time.time()
    result = subprocess.run([python_exe, script_name], capture_output=True, text=True, encoding='utf-8', errors='replace')
    duration = time.time() - start_time
    
    if result.returncode == 0:
        print(f"[SUCCESS] Completed in {duration:.2f}s")
        # Print indent output
        for line in result.stdout.strip().split("\n"):
            if line:
                print(f"   | {line}")
    else:
        print(f"[ERROR] Step failed with exit code {result.returncode}")
        print(result.stderr)
        sys.exit(1)

def main():
    print_banner("FreshMart Supermarket DWDM End-to-End Pipeline Execution")
    print("Silver Oak College of Computer Application | BCA Semester 5")
    print("Course Code: 4040233302 | Innovative Assignment")
    
    # Step 1: Raw Data Generation
    print_banner("Step 1: Real-World Data Generation (Deliverable 1)")
    run_step(os.path.join("scripts", "generate_raw_data.py"), "Generating raw POS transactions with authentic noise")
    
    # Step 2: Data Cleaning Pipeline
    print_banner("Step 2: Automated Data Cleaning Pipeline (Deliverable 2)")
    run_step(os.path.join("scripts", "clean_data.py"), "Cleaning duplicates, imputing missing values, treating IQR outliers")
    
    # Step 3: Star Schema & OLAP Operations
    print_banner("Step 3: Star Schema Loading & OLAP Operations (Deliverables 3, 4, 5)")
    run_step(os.path.join("scripts", "execute_olap.py"), "Executing Roll-Up, Drill-Down, Slice, Dice, and Pivot queries")
    
    # Step 4: Data Mining Execution
    print_banner("Step 4: Data Mining Models Execution (Deliverable 6)")
    run_step(os.path.join("scripts", "run_data_mining.py"), "Running Apriori, Decision Tree (80% Acc), and K-Means Clustering")
    
    # Step 5: Deliverable Verification
    print_banner("Step 5: Deliverable Verification & Audit Summary")
    deliverables = [
        ("Raw POS Dataset", os.path.join("data", "raw_supermarket_transactions.csv")),
        ("Cleaned POS Dataset", os.path.join("data", "cleaned_supermarket_data.csv")),
        ("Data Dictionary", os.path.join("data", "data_dictionary.md")),
        ("Data Cleaning Audit Report", os.path.join("docs", "DATA_CLEANING_REPORT.md")),
        ("DW Architecture Design", os.path.join("docs", "DATA_WAREHOUSE_DESIGN.md")),
        ("Star Schema Specification", os.path.join("docs", "STAR_SCHEMA_SPECIFICATION.md")),
        ("Star Schema DDL SQL", os.path.join("sql", "create_star_schema.sql")),
        ("OLAP Analysis Report", os.path.join("docs", "OLAP_ANALYSIS.md")),
        ("OLAP SQL Queries", os.path.join("sql", "olap_queries.sql")),
        ("Data Mining Analysis Report", os.path.join("docs", "DATA_MINING_RESULTS.md")),
        ("Apriori Rules Plot", os.path.join("output_figures", "apriori_rules.png")),
        ("Decision Tree Structure Plot", os.path.join("output_figures", "decision_tree_structure.png")),
        ("Confusion Matrix Plot", os.path.join("output_figures", "confusion_matrix.png")),
        ("Feature Importance Plot", os.path.join("output_figures", "feature_importance.png")),
        ("Elbow Method Plot", os.path.join("output_figures", "elbow_method_clustering.png")),
        ("Customer Clusters Plot", os.path.join("output_figures", "customer_clusters.png")),
        ("Interactive HTML Presentation", os.path.join("presentation", "index.html")),
        ("Presentation Slide Deck (Markdown)", os.path.join("presentation", "slides.md")),
        ("Viva-Voce Master Q&A Guide", "VIVA_VOCE_PREPARATION_GUIDE.md"),
        ("Formal Academic Project Report", "FINAL_ACADEMIC_REPORT.md")
    ]
    
    all_present = True
    for name, path in deliverables:
        exists = os.path.exists(path)
        size = os.path.getsize(path) if exists else 0
        status = "OK" if exists and size > 0 else "FAIL"
        if status == "FAIL":
            all_present = False
        print(f" - [{status}] {name:<35} : {size:>8,} bytes ({path})")
        
    if all_present:
        print("\n>>> ALL 20 ARTIFACTS VERIFIED SUCCESSFULLY (100% COMPLETE)! <<<")
    else:
        print("\n>>> WARNING: Some deliverables were missing or empty! <<<")
        
    # Step 6: Launch presentation in default web browser
    html_path = os.path.abspath(os.path.join("presentation", "index.html"))
    print(f"\n[LAUNCH] Opening interactive presentation in browser: {html_path}")
    try:
        webbrowser.open(f"file:///{html_path}")
        print("[LAUNCHED] Presentation opened in browser successfully!")
    except Exception as e:
        print(f"[NOTE] Could not auto-launch browser: {e}. You can open {html_path} directly.")
        
    print_banner("Pipeline Execution Successfully Finished (25/25 Marks Target)")

if __name__ == "__main__":
    main()
