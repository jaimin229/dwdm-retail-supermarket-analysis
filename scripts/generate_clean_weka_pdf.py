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

def build_clean_minimal_weka_pdf():
    print("[INFO] Building 100% Clean & Minimal WEKA Report (13 Pages)...")

    # Load authentic base64 images
    logo_b64 = img_to_base64("reports/silver_oak_logo.png")
    star_schema_b64 = img_to_base64("output_figures/star_schema_diagram.png")
    
    # Weka screenshots from reference
    weka_classify_gui = img_to_base64("ref_images/page_6_img_1.png")
    weka_classify_res = img_to_base64("ref_images/page_6_img_2.png")
    weka_tree_viz     = img_to_base64("ref_images/page_7_img_1.png")
    weka_conf_mat     = img_to_base64("ref_images/page_7_img_2.png")
    
    weka_cluster_gui  = img_to_base64("ref_images/page_8_img_2.png")
    weka_cluster_res  = img_to_base64("ref_images/page_9_img_1.png")
    weka_cluster_viz  = img_to_base64("ref_images/page_10_img_2.png")
    
    weka_assoc_gui    = img_to_base64("ref_images/page_11_img_2.png")
    weka_assoc_res    = img_to_base64("ref_images/page_12_img_2.png")

    with open("scripts/clean_minimal_template.html", "r", encoding="utf-8") as f:
        template = f.read()

    html = (template
            .replace("{{LOGO_B64}}", logo_b64)
            .replace("{{STAR_SCHEMA_B64}}", star_schema_b64)
            .replace("{{WEKA_CLASSIFY_GUI}}", weka_classify_gui)
            .replace("{{WEKA_CLASSIFY_RES}}", weka_classify_res)
            .replace("{{WEKA_TREE_VIZ}}", weka_tree_viz)
            .replace("{{WEKA_CONF_MAT}}", weka_conf_mat)
            .replace("{{WEKA_CLUSTER_GUI}}", weka_cluster_gui)
            .replace("{{WEKA_CLUSTER_RES}}", weka_cluster_res)
            .replace("{{WEKA_CLUSTER_VIZ}}", weka_cluster_viz)
            .replace("{{WEKA_ASSOC_GUI}}", weka_assoc_gui)
            .replace("{{WEKA_ASSOC_RES}}", weka_assoc_res))

    html_path = "clean_weka_report.html"
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

    print("[INFO] Rendering clean minimal PDF via Microsoft Edge...")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if os.path.exists(abs_pdf) and os.path.getsize(abs_pdf) > 0:
        print(f"[SUCCESS] Clean Minimal PDF generated! Size: {os.path.getsize(abs_pdf):,} bytes")
        # Copy to desktop
        desktop_pdf = r"C:\Users\jaimi\Desktop\DWDM_Innovative_Assignment_4040233302.pdf"
        import shutil
        shutil.copy(abs_pdf, desktop_pdf)
        print(f"[SUCCESS] Copied to Desktop: {desktop_pdf}")
    else:
        print(f"[ERROR] PDF generation failed: {res.stderr}")

if __name__ == '__main__':
    build_clean_minimal_weka_pdf()
