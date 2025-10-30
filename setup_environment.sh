#!/bin/bash
# EmailIntelligence Environment Setup Script
# This script sets up the development environment following project guidelines
# Uses uv for fast, reliable Python package management


set -e  # Exit on any error

echo "🚀 Setting up EmailIntelligence development environment..."

# Check if running as root/sudo
if [[ $EUID -eq 0 ]]; then
   echo "❌ This script should not be run as root. Please run as a regular user."
   exit 1
fi

# Update package list
echo "📦 Updating package list..."
sudo apt update

# Install system packages
echo "🔧 Installing system packages..."
sudo apt install -y \
    python3-dev \
    python3-pip \
    python3-venv \
    python3-setuptools \
    python3-wheel \
    build-essential \
    libssl-dev \
    libffi-dev \
    libbz2-dev \
    liblzma-dev \
    libreadline-dev \
    libsqlite3-dev \
    libblas-dev \
    liblapack-dev \
    libatlas-base-dev \
    gfortran \
    libfreetype6-dev \
    libpng-dev \
    libjpeg-dev \
    libtiff-dev \
    git \
    curl \
    wget

echo "✅ System packages installed successfully!"

# Install uv package manager
echo "📦 Installing uv package manager..."
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.cargo/bin:$PATH"

# Use the project's standard setup
echo "🐍 Setting up Python environment with uv..."
python launch.py --setup


# Download NLTK data
echo "📖 Downloading NLTK data..."
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"

echo "🎉 Environment setup complete!"
echo ""
echo "To activate the virtual environment in future sessions:"
echo "  source venv/bin/activate"
echo ""
echo "To run the application:"
echo "  python launch.py"
echo ""
echo "For development:"
echo "  python launch.py --dev"

