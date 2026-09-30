import os
import sys
import base64
import subprocess
import shutil

def img_to_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode("utf-8")
            ext = path.split(".")[-1].lower()
            mime = "image/jpeg" if ext in ["jpg", "jpeg"] else "image/png"
            return f"data:{mime};base64,{b64}"
    return ""

def generate_flawless_pdf():
    print("[INFO] Building 100% Mathematically Consistent, Clean & Minimal WEKA Report (13 Pages)...")

    # Load Base64 Images
    logo_b64         = img_to_base64("reports/silver_oak_logo.png")
    star_schema_b64  = img_to_base64("output_figures/star_schema_diagram.png")
    weka_pre_gui     = img_to_base64("output_figures/weka_gui_preprocess.png")
    weka_class_gui   = img_to_base64("output_figures/weka_gui_classify.png")
    weka_tree_viz    = img_to_base64("output_figures/weka_j48_tree_viz.png")
    weka_clust_gui   = img_to_base64("output_figures/weka_gui_cluster.png")
    weka_clust_viz   = img_to_base64("output_figures/weka_gui_cluster_viz.png")
    weka_assoc_gui   = img_to_base64("output_figures/weka_gui_associate.png")

    with open("scripts/flawless_template.html", "r", encoding="utf-8") as f:
        template = f.read()

    html = (template
            .replace("{{LOGO_B64}}", logo_b64)
            .replace("{{STAR_SCHEMA_B64}}", star_schema_b64)
            .replace("{{WEKA_PRE_GUI}}", weka_pre_gui)
            .replace("{{WEKA_CLASS_GUI}}", weka_class_gui)
            .replace("{{WEKA_TREE_VIZ}}", weka_tree_viz)
            .replace("{{WEKA_CLUST_GUI}}", weka_clust_gui)
            .replace("{{WEKA_CLUST_VIZ}}", weka_clust_viz)
            .replace("{{WEKA_ASSOC_GUI}}", weka_assoc_gui))

    html_path = "flawless_weka_report.html"
    pdf_path = "DWDM_Innovative_Assignment_4040233302.pdf"

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"[SUCCESS] Saved HTML: {html_path}")

    # Compile with Edge
    edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    if not os.path.exists(edge_path):
        edge_path = r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"

    abs_html = os.path.abspath(html_path)
    abs_pdf = os.path.abspath(pdf_path)

    cmd = [
        edge_path,
        "--headless",
        "--disable-gpu",
        "--run-all-compositor-stages-before-draw",
        "--print-to-pdf-no-header",
        f"--print-to-pdf={abs_pdf}",
        f"file:///{abs_html}"
    ]

    print("[INFO] Rendering flawless PDF via Microsoft Edge...")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if os.path.exists(abs_pdf) and os.path.getsize(abs_pdf) > 0:
        print(f"[SUCCESS] Flawless PDF generated! Size: {os.path.getsize(abs_pdf):,} bytes")
        desktop_pdf = r"C:\Users\jaimi\Desktop\DWDM_Innovative_Assignment_4040233302.pdf"
        shutil.copy(abs_pdf, desktop_pdf)
        print(f"[SUCCESS] Copied to Desktop: {desktop_pdf}")
    else:
        print(f"[ERROR] PDF generation failed: {res.stderr}")

if __name__ == '__main__':
    generate_flawless_pdf()
