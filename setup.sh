#!/bin/bash

# Professional Setup Script for Smart Sort AI
echo "🧠 Initializing Smart Sort AI Environment..."

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ Virtual environment created."
fi

# Install/Update dependencies
echo "📦 Installing dependencies..."
./venv/bin/pip install --upgrade pip
./venv/bin/pip install -r requirements.txt

echo "------------------------------------------------"
echo "✨ Setup Complete!"
echo "🚀 Run the dry-run to see it in action:"
echo "   ./venv/bin/python3 main.py test_downloads/ --dry-run"
echo "------------------------------------------------"
