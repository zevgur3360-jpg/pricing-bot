#!/bin/bash
# Quick start script for Shopping Assistant

echo "🛒 Starting Shopping Assistant..."
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed."
    echo "Please install Python 3.8 or later."
    exit 1
fi

# Check if openai package is installed
if ! python3 -c "import openai" &> /dev/null; then
    echo "⚠️  Installing required packages..."
    pip3 install -q openai
    echo "✅ Installation complete!"
    echo ""
fi

# Run the shopping assistant
python3 shopping_assistant.py


