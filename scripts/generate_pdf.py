"""
Academic PDF Generator for DWDM Innovative Assignment
Converts FINAL_ACADEMIC_REPORT.md into a beautifully formatted, print-ready PDF using headless Microsoft Edge.
"""

import os
import sys
import subprocess
from markdown_it import MarkdownIt

if sys.stdout:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

md_path = "FINAL_ACADEMIC_REPORT.md"
html_path = "academic_report_printable.html"
pdf_path = "DWDM_Innovative_Assignment_4040233302.pdf"

print("[INFO] Reading FINAL_ACADEMIC_REPORT.md...")
with open(md_path, "r", encoding="utf-8") as f:
    md_content = f.read()

# Convert markdown to HTML
md = MarkdownIt("commonmark", {"breaks": True, "html": True})
html_body = md.render(md_content)

# Academic Print CSS styling
styled_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>DWDM Innovative Assignment - Silver Oak College of Computer Application</title>
  <style>
    @page {{
      size: A4;
      margin: 20mm 15mm 20mm 15mm;
      @bottom-right {{
        content: counter(page);
      }}
    }}
    
    body {{
      font-family: 'Times New Roman', Times, serif;
      font-size: 11pt;
      line-height: 1.5;
      color: #111;
      margin: 0;
      padding: 0;
    }}
    
    h1, h2, h3, h4 {{
      font-family: 'Calibri', 'Arial', sans-serif;
      color: #0f2c59;
      page-break-after: avoid;
    }}
    
    h1 {{
      font-size: 18pt;
      text-align: center;
      margin-top: 24pt;
      margin-bottom: 12pt;
      border-bottom: 2px solid #0f2c59;
      padding-bottom: 6pt;
    }}
    
    h2 {{
      font-size: 14pt;
      margin-top: 18pt;
      margin-bottom: 8pt;
      border-bottom: 1px solid #ccc;
      padding-bottom: 4pt;
    }}
    
    h3 {{
      font-size: 12pt;
      margin-top: 12pt;
      margin-bottom: 6pt;
    }}
    
    table {{
      width: 100%;
      border-collapse: collapse;
      margin: 12pt 0;
      font-size: 9.5pt;
      page-break-inside: avoid;
    }}
    
    th, td {{
      border: 1px solid #444;
      padding: 5pt 7pt;
      text-align: left;
    }}
    
    th {{
      background-color: #f0f4f8;
      color: #0f2c59;
      font-weight: bold;
    }}
    
    pre, code {{
      font-family: 'Courier New', Courier, monospace;
      font-size: 9pt;
      background-color: #f8f9fa;
    }}
    
    pre {{
      border: 1px solid #ddd;
      padding: 8pt;
      overflow-x: auto;
      page-break-inside: avoid;
      white-space: pre-wrap;
    }}
    
    blockquote {{
      border-left: 3px solid #0f2c59;
      margin: 8pt 0;
      padding-left: 10pt;
      font-style: italic;
      color: #333;
    }}
    
    .page-break {{
      page-break-after: always;
    }}
    
    /* Cover Page Styling */
    .cover-page {{
      text-align: center;
      padding-top: 40pt;
      page-break-after: always;
    }}
  </style>
</head>
<body>
{html_body}
</body>
</html>
"""

with open(html_path, "w", encoding="utf-8") as f:
    f.write(styled_html)

print(f"[SUCCESS] Saved printable HTML: {html_path}")

# Run Microsoft Edge headless to generate PDF
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

print("[INFO] Invoking Microsoft Edge to print PDF...")
res = subprocess.run(cmd, capture_output=True, text=True)
if os.path.exists(pdf_path) and os.path.getsize(pdf_path) > 0:
    print(f"[SUCCESS] PDF generated successfully! ({os.path.getsize(pdf_path):,} bytes)")
    print(f"File Location: {abs_pdf}")
else:
    print(f"[ERROR] Failed to generate PDF: {res.stderr}")
