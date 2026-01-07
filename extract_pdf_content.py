from pypdf import PdfReader
import re

pdf_path = '../paper/Statistical Hypothesis Testing for Auditing Robustness in Language Models.pdf'

try:
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    
    print(text)
except Exception as e:
    print(f"Error reading PDF: {e}")
