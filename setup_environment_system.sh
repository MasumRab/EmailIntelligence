#!/bin/bash
# EmailIntelligence Environment Setup Script - System Package Priority
# Prefers system packages over pip installs where possible

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

echo "🚀 Setting up EmailIntelligence with system package priority..."

# Check if running as root/sudo
if [[ $EUID -eq 0 ]]; then
    log_error "This script should not be run as root. Please run as a regular user."
    exit 1
fi

# Update package list
log_info "📦 Updating package list..."
sudo apt update

# Install core system packages
log_info "🔧 Installing core system packages..."
sudo apt install -y \
    python3-dev \
    python3-pip \
    python3-venv \
    python3-setuptools \
    build-essential \
    git \
    curl \
    wget

# Install Python scientific stack from system packages
log_info "🧮 Installing Python scientific computing stack (system packages)..."
sudo apt install -y \
    python3-numpy \
    python3-scipy \
    python3-matplotlib \
    python3-pandas \
    python3-seaborn \
    python3-plotly \
    python3-scikit-learn \
    python3-joblib \
    python3-psutil

# Install Python web framework packages
log_info "🌐 Installing Python web framework packages..."
sudo apt install -y \
    python3-fastapi \
    python3-uvicorn \
    python3-pydantic \
    python3-multipart \
    python3-httpx \
    python3-dotenv

# Install Python utility packages
log_info "🛠️ Installing Python utility packages..."
sudo apt install -y \
    python3-bleach \
    python3-aiofiles \
    python3-sqlite3

# Install development tools
log_info "🔧 Installing development tools..."
sudo apt install -y \
    python3-black \
    python3-flake8 \
    python3-isort \
    python3-mypy \
    python3-pylint \
    python3-pytest \
    python3-pytest-asyncio

# Install additional system libraries needed for pip packages
log_info "📚 Installing additional system libraries..."
sudo apt install -y \
    libssl-dev \
    libffi-dev \
    libblas-dev \
    liblapack-dev \
    libatlas-base-dev \
    gfortran \
    libfreetype6-dev \
    libpng-dev \
    libjpeg-dev \
    libtiff-dev \
    libx11-dev \
    libxext-dev

# Create virtual environment for packages not available in system repos
log_info "🐍 Creating virtual environment for specialized packages..."
VENV_DIR="emailintelligence_venv"
if [[ -d "$VENV_DIR" ]]; then
    log_warning "Virtual environment already exists. Removing..."
    rm -rf "$VENV_DIR"
fi

python3 -m venv "$VENV_DIR"
source "$VENV_DIR/bin/activate"

# Upgrade pip in virtual environment
pip install --upgrade pip --quiet

# Install packages that are not available in Ubuntu system repos
log_info "🤖 Installing specialized AI/ML packages (pip only)..."

# PyTorch CPU (not available in Ubuntu repos)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu --quiet

# Hugging Face ecosystem
pip install transformers accelerate sentencepiece --quiet

# NLP packages
pip install nltk textblob --quiet

# Web/API packages not in Ubuntu repos
pip install gradio pyngrok email-validator --quiet

# Google API packages
pip install google-api-python-client google-auth google-auth-oauthlib --quiet

# Security and specialized packages
pip install RestrictedPython pydantic-settings aiosqlite --quiet

# Download NLTK data
log_info "📖 Downloading NLTK data..."
python -c "
import nltk
try:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
    print('NLTK data downloaded successfully')
except Exception as e:
    print(f'Warning: NLTK download failed: {e}')
"

# Create activation script
cat > activate_system.sh << 'ACTIVATE_EOF'
#!/bin/bash
# Activation script for EmailIntelligence system package environment

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$SCRIPT_DIR/emailintelligence_venv"

# Activate virtual environment if it exists
if [[ -d "$VENV_DIR" ]]; then
    source "$VENV_DIR/bin/activate"
    echo "✅ Virtual environment activated"
else
    echo "⚠️  Virtual environment not found - using system Python"
fi

# Set environment variables
export PYTHONPATH="$SCRIPT_DIR:$PYTHONPATH"

echo "✅ EmailIntelligence environment ready!"
echo "💡 To run the application: python launch.py"
echo "💡 To deactivate virtual environment: deactivate"

# Show versions
python3 -c "
import sys
print(f'System Python: {sys.version}')
try:
    import torch
    print(f'PyTorch: {torch.__version__} (CUDA: {torch.cuda.is_available()})')
except ImportError:
    print('PyTorch: Not available')
try:
    import numpy
    print(f'NumPy: {numpy.__version__}')
except ImportError:
    print('NumPy: Not available')
"
ACTIVATE_EOF

chmod +x activate_system.sh

# Test basic functionality
log_info "🧪 Testing basic functionality..."
python3 -c "
import sys
print('✅ System Python import test passed')

try:
    import numpy
    print('✅ NumPy (system) import test passed')
except ImportError as e:
    print(f'❌ NumPy import failed: {e}')

try:
    import torch
    print('✅ PyTorch (venv) import test passed')
except ImportError as e:
    print(f'❌ PyTorch import failed: {e}')

try:
    import fastapi
    print('✅ FastAPI (system) import test passed')
except ImportError as e:
    print(f'❌ FastAPI import failed: {e}')

try:
    import transformers
    print('✅ Transformers (venv) import test passed')
except ImportError as e:
    print(f'❌ Transformers import failed: {e}')
"

log_success "🎉 Environment setup complete!"
echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║               SYSTEM PACKAGE SETUP COMPLETE!                ║"
echo "╠══════════════════════════════════════════════════════════════╣"
echo "║                                                              ║"
echo "║  This setup prioritizes system packages for better          ║"
echo "║  integration and performance.                                ║"
echo "║                                                              ║"
echo "║  To activate the environment:                                ║"
echo "║  ./activate_system.sh                                        ║"
echo "║                                                              ║"
echo "║  To run the application:                                     ║"
echo "║  ./activate_system.sh && python launch.py                    ║"
echo "║                                                              ║"
echo "║  System packages installed: ~25 core packages                ║"
echo "║  Virtual environment packages: ~15 specialized packages      ║"
echo "║                                                              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Show package counts
echo "📊 Package Summary:"
echo "  System packages: $(dpkg -l | grep '^ii' | grep python3 | wc -l) Python packages"
echo "  Virtual environment: $VENV_DIR"
echo "  Total pip packages in venv: $(source $VENV_DIR/bin/activate && pip list | wc -l)"
