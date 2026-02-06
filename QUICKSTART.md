# Quick Start Guide

## One-Command Setup

```bash
./setup.sh
```

This installs everything needed (takes 5-10 minutes).

## Run Your First Claim

```bash
python3 main.py ACORD-Automobile-Loss-Notice.pdf
```

## What You'll See

```
================================================================================
INSURANCE CLAIMS AGENT - Local LLM Version
100% FREE - No API keys needed!
================================================================================

📄 Processing: ACORD-Automobile-Loss-Notice.pdf

🔍 STEP 1: Extracting text from PDF with OCR...
  Converting PDF to images...
  ✓ 4 page(s) found
  Running OCR on each page...
  ✓ Page 1/4 processed
  ✓ Page 2/4 processed
  ✓ Page 3/4 processed
  ✓ Page 4/4 processed
  ✓ Extracted 14,412 characters

🤖 STEP 2: Extracting fields with local LLM (Ollama)...
  Calling local LLM (this may take 10-30 seconds)...
  ✓ LLM response received
  ✓ Extracted 7 fields

📦 STEP 3: Applying routing rules...
  ✓ Route: Fast-track

================================================================================
✅ FINAL OUTPUT (JSON)
================================================================================

{
  "extractedFields": {
    "policyNumber": "AUTO-2024-12345",
    ...
  },
  "missingFields": [],
  "recommendedRoute": "Fast-track",
  "reasoning": "Estimated damage ($5,000) is below $25,000 threshold"
}
```

## Manual Setup Steps

If `./setup.sh` doesn't work:

### 1. Install system packages:
```bash
sudo apt-get install tesseract-ocr poppler-utils
```

### 2. Install Python packages:
```bash
pip3 install -r requirements.txt
```

### 3. Install Ollama + Llama2:
```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama2
```

### 4. Test:
```bash
python3 main.py ACORD-Automobile-Loss-Notice.pdf
```

## Key Benefits

✅ **$0 Cost** - Free forever  
✅ **No API Keys** - Nothing to configure  
✅ **Works Offline** - After initial setup  
✅ **Private** - Data stays on your machine  
✅ **Unlimited** - Process as many documents as you want  

## Need Help?

- **Ollama not working?** → Run: `ollama pull llama2`
- **Slow processing?** → Normal for local LLMs (10-30 sec is expected)
- **Tesseract error?** → Run: `sudo apt-get install tesseract-ocr`

---

**Time to first result:** ~15 minutes (including setup)  
**Cost:** $0.00  
**Ongoing maintenance:** None
