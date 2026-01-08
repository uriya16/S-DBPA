try:
    from docx import Document
except ImportError:
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "python-docx"])
    from docx import Document

import os

path = "paper/S-DBPA.docx"
if os.path.exists(path):
    doc = Document(path)
    print("--- S-DBPA Content ---")
    for para in doc.paragraphs:
        if para.text.strip():
            print(para.text)
else:
    print(f"File not found: {path}")
