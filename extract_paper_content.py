import zipfile
import re
import xml.etree.ElementTree as ET
import os

docx_path = '../paper/S-DBPA.docx'
extracted_text = ""

if os.path.exists(docx_path):
    try:
        with zipfile.ZipFile(docx_path) as z:
            with z.open('word/document.xml') as f:
                tree = ET.parse(f)
                root = tree.getroot()
                
                # Namespace map
                ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
                
                # Extract text from prompts (paragraphs)
                for p in root.findall('.//w:p', ns):
                    text = ''.join([node.text for node in p.findall('.//w:t', ns) if node.text])
                    if text:
                        extracted_text += text + "\n"
        
        print(extracted_text)
    except Exception as e:
        print(f"Error reading docx: {e}")
else:
    print(f"File not found: {docx_path}")
