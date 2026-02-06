#!/bin/bash
set -e

echo "=========================================="
echo "Insurance Claims Agent - Setup Script"
echo "Local LLM Version (100% FREE)"
echo "=========================================="
echo ""

# Step 1: System dependencies
echo "📦 Step 1: Installing system dependencies..."
if ! command -v tesseract &> /dev/null; then
    echo "  Installing tesseract-ocr and poppler-utils..."
    sudo apt-get update -qq
    sudo apt-get install -y tesseract-ocr poppler-utils
    echo "  ✓ System dependencies installed"
else
    echo "  ✓ Tesseract already installed"
fi

echo ""

# Step 2: Python dependencies
echo "🐍 Step 2: Installing Python dependencies..."
pip3 install -r requirements.txt --quiet --user
echo "  ✓ Python packages installed"

echo ""

# Step 3: Ollama installation
echo "🤖 Step 3: Installing Ollama (local LLM)..."
if ! command -v ollama &> /dev/null; then
    echo "  Downloading and installing Ollama..."
    curl -fsSL https://ollama.com/install.sh | sh
    echo "  ✓ Ollama installed"
else
    echo "  ✓ Ollama already installed"
fi

echo ""

# Step 4: Download LLM model
echo "📥 Step 4: Downloading Llama2 model (3.8GB, one-time)..."
echo "  This may take a few minutes..."
ollama pull llama2
echo "  ✓ Model downloaded"

echo ""
echo "=========================================="
echo "✅ Setup Complete!"
echo "=========================================="
echo ""
echo "🎉 You're ready to process FNOL claims!"
echo ""
echo "Usage:"
echo "  python3 main.py your-fnol-document.pdf"
echo ""
echo "Features:"
echo "  ✅ 100% FREE (no API costs)"
echo "  ✅ Runs offline (no internet needed)"
echo "  ✅ Private (data stays on your machine)"
echo "  ✅ Fast OCR + Local AI processing"
echo ""
