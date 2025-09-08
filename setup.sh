#!/bin/bash

# OCR Exercise Setup Script
# This script helps you set up the OCR project environment

echo "🚀 Setting up OCR Exercise Project..."
echo "====================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip first."
    exit 1
fi

echo "✅ pip3 found"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv .venv

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install Python dependencies
echo "📚 Installing Python dependencies..."
pip install -r requirements.txt

# Check if Tesseract is installed
if ! command -v tesseract &> /dev/null; then
    echo "⚠️  Tesseract OCR is not installed."
    echo "Please install Tesseract:"
    echo "  macOS: brew install tesseract"
    echo "  Ubuntu: sudo apt-get install tesseract-ocr"
    echo "  Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki"
else
    echo "✅ Tesseract OCR found: $(tesseract --version | head -1)"
fi

# Check if Poppler is installed
if ! command -v pdftoppm &> /dev/null; then
    echo "⚠️  Poppler (for pdf2image) is not installed."
    echo "Please install Poppler:"
    echo "  macOS: brew install poppler"
    echo "  Ubuntu: sudo apt-get install poppler-utils"
else
    echo "✅ Poppler found"
fi

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p uploads processed

# Copy environment file
if [ ! -f .env ]; then
    cp .env.example .env
    echo "📋 Created .env file from .env.example"
fi

echo ""
echo "🎉 Setup completed successfully!"
echo "================================="
echo "📋 Next steps:"
echo "  1. Activate virtual environment: source .venv/bin/activate"
echo "  2. Run Jupyter notebook: jupyter notebook ocr_exercise.ipynb"
echo "  3. Or run web app: python ocr_modul.py"
echo "  4. Access web interface at: http://127.0.0.1:5001/"
echo ""
echo "📖 For detailed instructions, see README.md"
echo ""
echo "Happy OCR processing! 🚀"
