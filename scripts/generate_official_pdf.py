import os
import sys
import base64
import subprocess

def img_to_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode("utf-8")
            ext = path.split(".")[-1].lower()
            mime = "image/jpeg" if ext in ["jpg", "jpeg"] else "image/png"
            return f"data:{mime};base64,{b64}"
    return ""

def build_official_report():
    print("[INFO] Building official Silver Oak University DWDM report...")

    logo_b64 = img_to_base64("reports/silver_oak_logo.png")
    star_schema_b64 = img_to_base64("output_figures/star_schema_diagram.png")
    dtree_b64 = img_to_base64("output_figures/decision_tree_structure.png")
    conf_mat_b64 = img_to_base64("output_figures/confusion_matrix.png")
    clusters_b64 = img_to_base64("output_figures/customer_clusters.png")
    elbow_b64 = img_to_base64("output_figures/elbow_method_clustering.png")
    apriori_b64 = img_to_base64("output_figures/apriori_rules.png")

    with open("scripts/report_template.html", "r", encoding="utf-8") as f:
        template = f.read()

    html = (template
            .replace("{{LOGO_B64}}", logo_b64)
            .replace("{{STAR_SCHEMA_B64}}", star_schema_b64)
            .replace("{{DTREE_B64}}", dtree_b64)
            .replace("{{CONF_MAT_B64}}", conf_mat_b64)
            .replace("{{CLUSTERS_B64}}", clusters_b64)
            .replace("{{ELBOW_B64}}", elbow_b64)
            .replace("{{APRIORI_B64}}", apriori_b64))

    with open("academic_report_official.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("[SUCCESS] Created academic_report_official.html")

    # Render PDF using Microsoft Edge headless
    edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    if not os.path.exists(edge_path):
        edge_path = r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"

    abs_html = os.path.abspath("academic_report_official.html")
    abs_pdf = os.path.abspath("DWDM_Innovative_Assignment_4040233302.pdf")

    cmd = [
        edge_path,
        "--headless",
        "--disable-gpu",
        "--run-all-compositor-stages-before-draw",
        "--print-to-pdf-no-header",
        f"--print-to-pdf={abs_pdf}",
        f"file:///{abs_html}"
    ]

    print("[INFO] Printing PDF via Microsoft Edge...")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if os.path.exists(abs_pdf) and os.path.getsize(abs_pdf) > 0:
        print(f"[SUCCESS] Final PDF generated! Size: {os.path.getsize(abs_pdf):,} bytes")
        print(f"Path: {abs_pdf}")
    else:
        print(f"[ERROR] PDF generation failed: {res.stderr}")

if __name__ == '__main__':
    build_official_report()
