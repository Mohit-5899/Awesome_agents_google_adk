#!/bin/bash

# AI News Podcast Agent - Setup Script
# This script automates the installation and configuration process

set -e  # Exit on error

echo "╔══════════════════════════════════════════════════════════╗"
echo "║   AI News Podcast Agent - Automated Setup               ║"
echo "║   Powered by Google ADK & Gemini                        ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# Check Python version
echo "🔍 Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Found Python $python_version"

# Check if Python 3.10+
required_version="3.10"
if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Error: Python 3.10 or higher is required"
    echo "   Current version: $python_version"
    exit 1
fi

# Create virtual environment
echo ""
echo "📦 Creating virtual environment..."
if [ -d "venv" ]; then
    echo "⚠️  Virtual environment already exists. Removing..."
    rm -rf venv
fi
python3 -m venv venv
echo "✓ Virtual environment created"

# Activate virtual environment
echo ""
echo "🔌 Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"

# Upgrade pip
echo ""
echo "⬆️  Upgrading pip..."
pip install --upgrade pip > /dev/null 2>&1
echo "✓ Pip upgraded"

# Install dependencies
echo ""
echo "📚 Installing dependencies..."
pip install -r requirements.txt
echo "✓ Dependencies installed"

# Setup .env file
echo ""
echo "🔐 Setting up environment variables..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "✓ Created .env file from template"
    echo ""
    echo "⚠️  IMPORTANT: Please edit .env and add your GEMINI_API_KEY"
    echo "   You can get one from: https://ai.google.dev/"
    echo ""
else
    echo "✓ .env file already exists"
fi

# Create outputs directory
echo ""
echo "📁 Creating outputs directory..."
mkdir -p outputs
echo "✓ Outputs directory created"

# Test installation
echo ""
echo "🧪 Testing installation..."
python3 -c "import google.adk; print('✓ Google ADK imported successfully')"
python3 -c "import yfinance; print('✓ yfinance imported successfully')"
python3 -c "from agent import root_agent; print('✓ Agent loaded successfully')"

echo ""
echo "╔══════════════════════════════════════════════════════════╗"
echo "║   ✅ Setup Complete!                                    ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""
echo "📋 Next Steps:"
echo ""
echo "1. Configure your API key:"
echo "   • Edit .env file and add: GEMINI_API_KEY=your_key_here"
echo "   • Or export it: export GEMINI_API_KEY='your_key_here'"
echo ""
echo "2. Start the agent with ADK Web UI:"
echo "   • Run: adk web --host 0.0.0.0 --port 8000"
echo "   • Open: http://localhost:8000"
echo ""
echo "3. Or use the command line:"
echo "   • Run: adk run"
echo ""
echo "📖 For more information, read README.md"
echo ""
echo "🎉 Happy building!"
echo ""
