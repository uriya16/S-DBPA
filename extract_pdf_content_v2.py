from pypdf import PdfReader
import sys

# Set encoding to utf-8 for output
sys.stdout.reconfigure(encoding='utf-8')

pdf_path = '../paper/Statistical Hypothesis Testing for Auditing Robustness in Language Models.pdf'

try:
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    
    # Simple search for relevant sections
    if "Table 2" in text:
        print("Found Table 2 context:")
        # Find context around "Table 2"
        idx = text.find("Table 2")
        print(text[idx:idx+2000])
    else:
        print("Table 2 not found via string search.")
        
    if "Figure 3" in text:
        print("\nFound Figure 3 context:")
        idx = text.find("Figure 3")
        print(text[idx:idx+2000])
    
    # Also print any tabular looking data
    # print(text) 
except Exception as e:
    print(f"Error reading PDF: {e}")
