#!/usr/bin/env python3
"""
Insurance Claims Agent - Local LLM Version
Processes FNOL PDFs using OCR + Local Ollama LLM (100% FREE)

Usage:
    python3 main.py <path-to-pdf>
"""

import sys
import json
import os
from ocr_extractor import pdf_to_text
from llm_extractor import extract_with_llm
from claims_router import process_claim


def main():
    """Main entry point."""
    print("="*80)
    print("INSURANCE CLAIMS AGENT - Local LLM Version")
    print("100% FREE - No API keys needed!")
    print("="*80)
    print()
    
    # Check arguments
    if len(sys.argv) < 2:
        print("❌ Usage: python3 main.py <path-to-pdf>")
        print()
        print("Example:")
        print("  python3 main.py sample.pdf")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    
    # Check file exists
    if not os.path.exists(pdf_path):
        print(f"❌ ERROR: File not found: {pdf_path}")
        sys.exit(1)
    
    print(f"📄 Processing: {pdf_path}")
    print()
    
    # Step 1: OCR extraction
    print("🔍 STEP 1: Extracting text from PDF with OCR...")
    try:
        text = pdf_to_text(pdf_path)
        print(f"  ✓ Extracted {len(text):,} characters")
    except Exception as e:
        print(f"  ❌ OCR failed: {e}")
        print()
        print("💡 Make sure tesseract-ocr and poppler-utils are installed:")
        print("   sudo apt-get install tesseract-ocr poppler-utils")
        sys.exit(1)
    
    print()
    
    # Step 2: LLM field extraction
    print("🤖 STEP 2: Extracting fields with local LLM (Ollama)...")
    try:
        fields = extract_with_llm(text)
    except Exception as e:
        print(f"  ❌ Extraction failed: {e}")
        sys.exit(1)
    
    print()
    
    # Step 3: Routing decision
    print("📦 STEP 3: Applying routing rules...")
    result = process_claim(fields)
    print(f"  ✓ Route: {result['recommendedRoute']}")
    
    print()
    print("="*80)
    print("✅ FINAL OUTPUT (JSON)")
    print("="*80)
    print()
    print(json.dumps(result, indent=2))
    print()
    print("="*80)


if __name__ == "__main__":
    main()
