"""
Step 1: Extract Text from PDF
This script extracts text from a PDF file and saves it with page metadata.
"""

import os
import json
from pathlib import Path
import pdfplumber
from PyPDF2 import PdfReader


def extract_text_with_pdfplumber(pdf_path: str) -> list[dict]:
    """
    Extract text from PDF using pdfplumber (better for complex layouts).
    
    Args:
        pdf_path: Path to the PDF file
        
    Returns:
        List of dictionaries with page number and text content
    """
    pages_data = []
    
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            text = page.extract_text() or ""
            pages_data.append({
                "page_number": page_num,
                "text": text.strip(),
                "char_count": len(text),
                "source": os.path.basename(pdf_path)
            })
            print(f"Extracted page {page_num}/{len(pdf.pages)} - {len(text)} characters")
    
    return pages_data


def extract_text_with_pypdf2(pdf_path: str) -> list[dict]:
    """
    Extract text from PDF using PyPDF2 (faster, simpler layouts).
    
    Args:
        pdf_path: Path to the PDF file
        
    Returns:
        List of dictionaries with page number and text content
    """
    pages_data = []
    
    reader = PdfReader(pdf_path)
    total_pages = len(reader.pages)
    
    for page_num, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        pages_data.append({
            "page_number": page_num,
            "text": text.strip(),
            "char_count": len(text),
            "source": os.path.basename(pdf_path)
        })
        print(f"Extracted page {page_num}/{total_pages} - {len(text)} characters")
    
    return pages_data


def save_extracted_text(pages_data: list[dict], output_path: str):
    """Save extracted text to JSON file."""
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(pages_data, f, indent=2, ensure_ascii=False)
    print(f"\nSaved extracted text to: {output_path}")


def main():
    # Configuration
    pdf_path = os.path.join(os.path.dirname(__file__), "..", "CvUYJmmeNQwM9W6XY24h3g95.pdf")
    output_dir = os.path.join(os.path.dirname(__file__), "output")
    
    # Create output directory
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Verify PDF exists
    if not os.path.exists(pdf_path):
        print(f"Error: PDF not found at {pdf_path}")
        return
    
    print(f"Extracting text from: {pdf_path}\n")
    
    # Extract text using pdfplumber (better for complex layouts)
    # You can switch to extract_text_with_pypdf2 if needed
    pages_data = extract_text_with_pdfplumber(pdf_path)
    
    # Save extracted text
    output_path = os.path.join(output_dir, "extracted_text.json")
    save_extracted_text(pages_data, output_path)
    
    # Print summary
    total_chars = sum(p["char_count"] for p in pages_data)
    print(f"\n=== Extraction Summary ===")
    print(f"Total pages: {len(pages_data)}")
    print(f"Total characters: {total_chars:,}")
    print(f"Average chars/page: {total_chars // len(pages_data):,}")


if __name__ == "__main__":
    main()
