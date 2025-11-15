#!/bin/bash

# Quantum Battleship Backend Runner
# This script sets up and runs the Flask server

echo "🎮 Quantum Battleship Backend 🎮"
echo "================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

# Check if .env exists, if not copy from example
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "🚀 Starting Flask server..."
echo "   Server will be available at: http://localhost:5000"
echo "   Press Ctrl+C to stop"
echo ""

# Run the Flask app
python app.py