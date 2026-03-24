#!/bin/bash
# Setup script for the conference agent

set -e

echo "🤖 Grosse Conf 2026 - Setup Script"
echo "=========================================="
echo ""

# Check Python version
echo "Checking Python version..."
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python $PYTHON_VERSION found"

# Create virtual environment
echo ""
echo "Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "Virtual environment created"
else
    echo "Virtual environment already exists"
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate
echo "Virtual environment activated"

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip > /dev/null 2>&1
echo "pip upgraded"

# Install requirements
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt
echo "Dependencies installed"

# Create .env file if it doesn't exist
echo ""
echo "Setting up configuration..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "Created .env file from template"
    echo "⚠️  Please edit .env with your configuration"
else
    echo ".env file already exists"
fi

# Create data directory if needed
echo ""
echo "Checking data directory..."
DATA_DIR="mcp_servers/filesystem/data"
if [ -d "$DATA_DIR" ]; then
    echo "Data directory exists"
else
    mkdir -p "$DATA_DIR"
    echo "Data directory created"
fi

echo ""
echo "=========================================="
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "  1. Edit .env file with your configuration"
echo "  2. Activate venv: source venv/bin/activate"
echo "  3. Run agent: python scripts/run_agent.py"
echo ""
echo "For testing: pytest tests/"
echo ""
