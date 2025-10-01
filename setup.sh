#!/bin/bash

# EmailIntelligence Setup Script
# This script sets up both Python backend and Node.js frontend environments

set -e  # Exit on any error

echo "🚀 Setting up EmailIntelligence application..."

# Check if we're in the right directory
if [ ! -f "pyproject.toml" ]; then
    echo "❌ Error: pyproject.toml not found. Please run this script from the EmailIntelligence root directory."
    exit 1
fi

# 1. Python Backend Setup
echo "🐍 Setting up Python backend environment..."

# Check Python version
python_version=$(python3 --version 2>&1 | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "📋 Detected Python version: $python_version"

if ! python3 -c "import sys; exit(0 if sys.version_info >= (3, 11) else 1)" 2>/dev/null; then
    echo "❌ Error: Python 3.11+ is required. Current version: $python_version"
    exit 1
fi

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "📦 Creating Python virtual environment..."
    python3 -m venv venv
else
    echo "📦 Virtual environment already exists"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install uv if not present
if ! command -v uv &> /dev/null; then
    echo "📥 Installing uv package manager..."
    pip install uv
fi

# Install Python dependencies
echo "📥 Installing Python dependencies with uv..."
uv sync

# 2. Node.js Frontend Setup
echo "🌐 Setting up Node.js frontend environment..."

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Error: Node.js is not installed. Please install Node.js 18+ first."
    echo "Visit: https://nodejs.org/"
    exit 1
fi

# Check Node.js version
node_version=$(node --version | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$node_version" -lt 18 ]; then
    echo "❌ Error: Node.js 18+ is required. Current version: $(node --version)"
    exit 1
fi

# Check if npm is available
if ! command -v npm &> /dev/null; then
    echo "❌ Error: npm is not installed. Please install npm."
    exit 1
fi

# Install frontend dependencies
echo "📥 Installing frontend dependencies..."
cd client
npm install
cd ..

# 3. Verify setup
echo "✅ Verifying setup..."

# Test Python imports
echo "🧪 Testing Python backend..."
source venv/bin/activate
python3 -c "
import sys
sys.path.append('.')
try:
    from backend.main import app
    print('✅ Backend imports successful')
except Exception as e:
    print(f'❌ Backend import error: {e}')
    sys.exit(1)
"

# Test frontend build
echo "🧪 Testing frontend build..."
cd client
if npm run build > /dev/null 2>&1; then
    echo "✅ Frontend build successful"
else
    echo "❌ Frontend build failed"
    exit 1
fi
cd ..

echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "📋 Next steps:"
echo "1. Activate Python environment: source venv/bin/activate"
echo "2. Start backend server: python3 backend/main.py"
echo "3. In another terminal, start frontend: cd client && npm run dev"
echo ""
echo "🌐 Access the application at:"
echo "   - Backend API: http://localhost:8000"
echo "   - Frontend: http://localhost:5173"
echo ""