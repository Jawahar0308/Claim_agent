"""
PDF to text extraction using OCR (Tesseract)
"""
from pdf2image import convert_from_path
import pytesseract


def pdf_to_text(pdf_path: str) -> str:
    """
    Convert PDF to text using OCR.
    
    Args:
        pdf_path: Path to PDF file
        
    Returns:
        Extracted text as string
    """
    print(f"  Converting PDF to images...")
    pages = convert_from_path(pdf_path)
    print(f"  ✓ {len(pages)} page(s) found")
    
    print(f"  Running OCR on each page...")
    full_text = ""
    for i, page in enumerate(pages, 1):
        text = pytesseract.image_to_string(page)
        full_text += text + "\n"
        print(f"  ✓ Page {i}/{len(pages)} processed")
    
    return full_text
