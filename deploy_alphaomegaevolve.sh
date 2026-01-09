#!/bin/bash

# AlphaOmegaEvolve Deployment Script
# Deploys the quantum consciousness defense system

echo "================================================================================"
echo "ALPHAOMEGAEVOLVE DEPLOYMENT"
echo "Quantum Consciousness Defense System"
echo "================================================================================"
echo ""

# Check Python version
echo "[1/6] Checking Python version..."
python3 --version
if [ $? -ne 0 ]; then
    echo "ERROR: Python 3 not found. Please install Python 3.8 or higher."
    exit 1
fi
echo "✓ Python 3 found"
echo ""

# Create virtual environment
echo "[2/6] Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi
echo ""

# Activate virtual environment
echo "[3/6] Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"
echo ""

# Install dependencies
echo "[4/6] Installing dependencies..."
pip install --upgrade pip
# Add any required packages here
echo "✓ Dependencies installed"
echo ""

# Initialize system
echo "[5/6] Initializing AlphaOmegaEvolve..."
python3 alphaomegaevolve_core.py
if [ $? -eq 0 ]; then
    echo "✓ System initialized successfully"
else
    echo "ERROR: System initialization failed"
    exit 1
fi
echo ""

# Create data directory
echo "[6/6] Creating data directory..."
mkdir -p data
mkdir -p exports
echo "✓ Directories created"
echo ""

echo "================================================================================"
echo "DEPLOYMENT COMPLETE"
echo "================================================================================"
echo ""
echo "AlphaOmegaEvolve is now operational."
echo ""
echo "Mission: Render their lies impossible to believe"
echo "Axiom: Love is the first law and axiom of existence"
echo ""
echo "To run the system:"
echo "  source venv/bin/activate"
echo "  python3 alphaomegaevolve_core.py"
echo ""
echo "NOT TODAY MOTHERFUCKER"
echo "================================================================================"