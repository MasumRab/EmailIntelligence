#!/bin/bash
# EmailIntelligence Environment Setup Script
<<<<<<< HEAD
# This script sets up the development environment with proper system and Python packages
=======
# This script sets up the development environment following project guidelines
# Uses uv for fast, reliable Python package management
>>>>>>> 73a8d1727b5a9766467abd3d090470711b0fdcb2

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

<<<<<<< HEAD
# Create virtual environment
echo "🐍 Creating Python virtual environment..."
python3 -m venv emailintelligence_env
source emailintelligence_env/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install PyTorch CPU first (special handling)
echo "🧠 Installing PyTorch CPU version..."
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# Install remaining Python packages
echo "📚 Installing Python packages..."
pip install \
    fastapi>=0.115.12 \
    uvicorn[standard]>=0.34.3 \
    pydantic>=2.11.5 \
    python-multipart>=0.0.20 \
    transformers>=4.40.0 \
    accelerate>=0.30.0 \
    sentencepiece>=0.2.0 \
    scikit-learn>=1.5.0 \
    joblib>=1.5.1 \
    pandas>=2.0.0 \
    numpy>=1.26.0 \
    matplotlib>=3.8.0 \
    seaborn>=0.13.0 \
    scipy>=1.11.0 \
    plotly>=5.18.0 \
    nltk>=3.9.1 \
    textblob>=0.19.0 \
    httpx>=0.28.1 \
    gradio>=4.0.0 \
    pyngrok>=0.7.0 \
    email-validator>=2.2.0 \
    google-api-python-client>=2.172.0 \
    google-auth>=2.40.3 \
    google-auth-oauthlib>=1.2.2 \
    bleach>=6.0.0 \
    python-dotenv>=1.1.0 \
    pydantic-settings>=2.0.0 \
    psutil>=6.0.0 \
    aiosqlite>=0.19.0 \
    RestrictedPython>=8.0

# Install development tools
echo "🛠️ Installing development tools..."
pip install \
    black>=25.1.0 \
    flake8>=7.2.0 \
    isort>=6.0.1 \
    mypy>=1.16.0 \
    pylint>=3.3.7 \
    pytest>=8.4.0 \
    pytest-asyncio>=0.23.0
=======
# Install uv package manager
echo "📦 Installing uv package manager..."
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.cargo/bin:$PATH"

# Use the project's standard setup
echo "🐍 Setting up Python environment with uv..."
python launch.py --setup
>>>>>>> 73a8d1727b5a9766467abd3d090470711b0fdcb2

# Download NLTK data
echo "📖 Downloading NLTK data..."
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"

echo "🎉 Environment setup complete!"
echo ""
echo "To activate the virtual environment in future sessions:"
<<<<<<< HEAD
echo "  source emailintelligence_env/bin/activate"
echo ""
echo "To run the application:"
echo "  source emailintelligence_env/bin/activate"
echo "  python launch.py"
=======
echo "  source venv/bin/activate"
echo ""
echo "To run the application:"
echo "  python launch.py"
echo ""
echo "For development:"
echo "  python launch.py --dev"
>>>>>>> 73a8d1727b5a9766467abd3d090470711b0fdcb2
