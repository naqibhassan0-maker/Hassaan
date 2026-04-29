#!/bin/bash
set -e

echo "🚀 Smart Money Concepts Dashboard - Startup"
echo "==========================================="

cd /workspaces/Hassaan

echo ""
echo "📦 Installing dependencies..."
pip install -r requirements.txt --quiet

echo "✅ Dependencies installed!"
echo ""
echo "🎯 Starting Streamlit dashboard..."
echo "📊 Access at: http://localhost:8501"
echo ""

streamlit run streamlit_app.py --client.showErrorDetails=true
