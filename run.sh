#!/bin/bash
# Smart Money Concepts Dashboard - Startup Script
# This script ensures all dependencies are installed before running Streamlit

set -e

echo "🚀 Smart Money Concepts Dashboard - Startup"
echo "==========================================="

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed or not in PATH"
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "✅ Python version: $PYTHON_VERSION"

# Install/upgrade pip
echo "📦 Ensuring pip is up to date..."
python3 -m pip install --upgrade pip --quiet

# Install requirements
echo "📦 Installing dependencies from requirements.txt..."
python3 -m pip install -r requirements.txt --quiet

# Verify imports
echo "✅ Verifying all imports..."
python3 test_imports.py

if [ $? -eq 0 ]; then
    echo ""
    echo "🎯 All checks passed! Starting Streamlit dashboard..."
    echo "📊 Dashboard URL: http://localhost:8501"
    echo ""
    python3 -m streamlit run streamlit_app.py --logger.level=info
else
    echo "❌ Import verification failed. Please check the output above."
    exit 1
fi
