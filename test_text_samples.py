#!/usr/bin/env python3
"""
Test script for text-based FNOL samples
Tests the agent with filled sample documents (not blank templates)
"""

import os
import json
from llm_extractor import fallback_extraction
from claims_router import process_claim


def main():
    """Test with text samples."""
    print("="*80)
    print("TESTING WITH FILLED FNOL SAMPLES (Text Format)")
    print("="*80)
    print()
    
    sample_dir = "sample_documents"
    
    if not os.path.exists(sample_dir):
        print(f"❌ Sample directory not found: {sample_dir}")
        return
    
    # Get all text files
    files = [f for f in os.listdir(sample_dir) if f.endswith('.txt')]
    files.sort()
    
    if not files:
        print(f"❌ No .txt files found in {sample_dir}")
        return
    
    print(f"Found {len(files)} sample document(s)\n")
    
    for filename in files:
        filepath = os.path.join(sample_dir, filename)
        
        print("="*80)
        print(f"Processing: {filename}")
        print("="*80)
        print()
        
        # Read file
        with open(filepath, 'r') as f:
            text = f.read()
        
        print(f"📄 File size: {len(text):,} characters")
        print()
        
        # Extract fields using fallback (regex) method
        print("🔍 Extracting fields...")
        fields = fallback_extraction(text)
        
        # Route claim
        print("📦 Routing claim...")
        result = process_claim(fields)
        
        print()
        print("="*80)
        print("RESULT:")
        print("="*80)
        print()
        print(json.dumps(result, indent=2))
        print()
        print()


if __name__ == "__main__":
    main()
