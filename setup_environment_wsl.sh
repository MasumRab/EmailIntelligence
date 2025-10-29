#!/bin/bash
# EmailIntelligence Environment Setup Script for Ubuntu WSL
# Optimized for Windows Subsystem for Linux environment

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

echo "🚀 Setting up EmailIntelligence development environment for Ubuntu WSL..."

# Check if running in WSL
if [[ ! -f /proc/version ]] || ! grep -q "Microsoft" /proc/version && ! grep -q "microsoft" /proc/version; then
    log_warning "This script is optimized for WSL. You appear to be running on native Linux."
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Check if running as root/sudo
if [[ $EUID -eq 0 ]]; then
    log_error "This script should not be run as root. Please run as a regular user."
    exit 1
fi

# Detect Ubuntu version
UBUNTU_VERSION=$(lsb_release -rs 2>/dev/null || echo "unknown")
log_info "Detected Ubuntu version: $UBUNTU_VERSION"

# Update package list with retry logic
log_info "📦 Updating package list..."
for i in {1..3}; do
    if sudo apt update; then
        break
    else
        log_warning "apt update failed (attempt $i/3), retrying in 5 seconds..."
        sleep 5
    fi
done

# Install system packages optimized for WSL
log_info "🔧 Installing system packages for WSL..."

# Core packages
sudo apt install -y \
    python3-dev \
    python3-pip \
    python3-venv \
    python3-setuptools \
    python3-wheel \
    build-essential \
    software-properties-common

# SSL and development libraries
sudo apt install -y \
    libssl-dev \
    libffi-dev \
    libbz2-dev \
    liblzma-dev \
    libreadline-dev \
    libsqlite3-dev \
    zlib1g-dev

# Scientific computing libraries (optimized for WSL)
sudo apt install -y \
    libblas-dev \
    liblapack-dev \
    libatlas-base-dev \
    gfortran \
    libopenblas-dev \
    python3-numpy \
    python3-scipy \
    python3-matplotlib \
    python3-pandas \
    python3-seaborn \
    python3-plotly \
    python3-scikit-learn \
    python3-joblib

# Graphics and imaging libraries
sudo apt install -y \
    libfreetype6-dev \
    libpng-dev \
    libjpeg-dev \
    libtiff-dev \
    libx11-dev \
    libxext-dev \
    libxcb1-dev \
    libxrandr-dev \
    libxss1

# Web framework and utilities (system packages)
sudo apt install -y \
    python3-fastapi \
    python3-uvicorn \
    python3-pydantic \
    python3-multipart \
    python3-httpx \
    python3-dotenv \
    python3-bleach \
    python3-psutil \
    python3-plotly \
    python3-seaborn

# Development tools (system packages)
sudo apt install -y \
    python3-black \
    python3-flake8 \
    python3-isort \
    python3-mypy \
    python3-pylint \
    python3-pytest \
    python3-pytest-asyncio

# Additional WSL-specific packages
sudo apt install -y \
    git \
    curl \
    wget \
    unzip \
    x11-apps \
    xvfb \
    libgtk-3-dev \
    libgirepository1.0-dev \
    gir1.2-gtk-3.0

# Use system Python 3.12+ (default in Ubuntu 24.04+)
PYTHON_CMD="python3"

log_success "System packages installed successfully!"

# Create virtual environment with specific Python version
log_info "🐍 Creating Python virtual environment..."
VENV_DIR="emailintelligence_env"
if [[ -d "$VENV_DIR" ]]; then
    log_warning "Virtual environment already exists. Removing..."
    rm -rf "$VENV_DIR"
fi

$PYTHON_CMD -m venv --system-site-packages "$VENV_DIR"
source "$VENV_DIR/bin/activate"

# Verify virtual environment
if [[ "$VIRTUAL_ENV" != "$(pwd)/$VENV_DIR" ]]; then
    log_error "Failed to activate virtual environment"
    exit 1
fi

log_success "Virtual environment created and activated"

# Upgrade pip with better error handling
log_info "⬆️ Upgrading pip..."
pip install --upgrade pip --quiet

# Install PyTorch CPU with WSL optimizations
log_info "🧠 Installing PyTorch CPU version (optimized for WSL)..."
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu --quiet

# Verify PyTorch installation
python -c "import torch; print(f'PyTorch version: {torch.__version__}'); print(f'CUDA available: {torch.cuda.is_available()}')"

# Install core packages first (for better dependency resolution)
log_info "📚 Installing core Python packages..."
pip install --quiet \
    pydantic-settings>=2.0.0

# Install AI/ML packages
log_info "🤖 Installing AI/ML packages..."
pip install --quiet \
    transformers>=4.40.0 \
    accelerate>=0.30.0 \
    sentencepiece>=0.2.0

# Install data science packages (remaining pip-only packages)
log_info "📊 Installing data science packages..."
# Note: pandas, numpy, matplotlib, seaborn, scipy, plotly installed via system packages

# Install NLP packages
log_info "📖 Installing NLP packages..."
pip install --quiet \
    nltk>=3.9.1 \
    textblob>=0.19.0

# Install web and API packages
log_info "🌐 Installing web and API packages..."
pip install --quiet \
    gradio>=4.0.0 \
    pyngrok>=0.7.0 \
    email-validator>=2.2.0

# Install Google API packages
log_info "🔐 Installing Google API packages..."
pip install --quiet \
    google-api-python-client>=2.172.0 \
    google-auth>=2.40.3 \
    google-auth-oauthlib>=1.2.2

# Install utility packages (remaining pip-only packages)
log_info "🛠️ Installing utility packages..."
pip install --quiet \
    aiosqlite>=0.19.0 \
    RestrictedPython>=8.0

# Install development tools (remaining pip-only packages)
log_info "🔧 Installing development tools..."
# Note: black, flake8, isort, mypy, pylint, pytest, pytest-asyncio installed via system packages

# Download NLTK data with error handling
log_info "📖 Downloading NLTK data..."
python -c "
import nltk
import ssl
try:
    # Handle SSL issues in WSL
    ssl._create_default_https_context = ssl._create_unverified_context
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
    print('NLTK data downloaded successfully')
except Exception as e:
    print(f'Warning: NLTK download failed: {e}')
"

# Create activation script for future use
cat > activate_env.sh << 'ACTIVATE_EOF'
#!/bin/bash
# Activation script for EmailIntelligence environment

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$SCRIPT_DIR/emailintelligence_env"

# Check if virtual environment exists
if [[ ! -d "$VENV_DIR" ]]; then
    echo "❌ Virtual environment not found. Run setup_environment_wsl.sh first."
    exit 1
fi

# Activate virtual environment
source "$VENV_DIR/bin/activate"

# Set environment variables for WSL
export PYTHONPATH="$SCRIPT_DIR:$PYTHONPATH"
export MPLBACKEND='Agg'  # Use non-interactive backend for matplotlib in WSL
export DISPLAY=:0  # Set display for GUI applications

echo "✅ EmailIntelligence environment activated!"
echo "💡 To run the application: python launch.py"
echo "💡 To deactivate: deactivate"

# Show Python and key packages versions
python -c "
import sys
print(f'Python: {sys.version}')
try:
    import torch
    print(f'PyTorch: {torch.__version__} (CUDA: {torch.cuda.is_available()})')
except ImportError:
    print('PyTorch: Not available')
"
ACTIVATE_EOF

chmod +x activate_env.sh

# Create WSL-specific configuration
cat > wsl_config.sh << 'WSL_EOF'
#!/bin/bash
# WSL-specific configuration for EmailIntelligence

# Enable X11 forwarding for GUI applications
export DISPLAY=:0
export LIBGL_ALWAYS_INDIRECT=1

# Set matplotlib backend for WSL
export MPLBACKEND='Agg'

# Optimize for WSL performance
export PYTHONDONTWRITEBYTECODE=1
export PYTHONUNBUFFERED=1

# Set up proper file permissions for WSL
umask 022

# Add local bin to PATH if it exists
if [[ -d "$HOME/.local/bin" ]]; then
    export PATH="$HOME/.local/bin:$PATH"
fi
WSL_EOF

chmod +x wsl_config.sh

# Test basic functionality
log_info "🧪 Testing basic functionality..."
python -c "
import sys
print('✅ Python import test passed')

try:
    import torch
    print('✅ PyTorch import test passed')
except ImportError as e:
    print(f'❌ PyTorch import failed: {e}')
    sys.exit(1)

try:
    import fastapi
    print('✅ FastAPI import test passed')
except ImportError as e:
    print(f'❌ FastAPI import failed: {e}')
    sys.exit(1)

try:
    import transformers
    print('✅ Transformers import test passed')
except ImportError as e:
    print(f'❌ Transformers import failed: {e}')
    sys.exit(1)
"

log_success "🎉 Environment setup complete!"
echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                    SETUP COMPLETE!                           ║"
echo "╠══════════════════════════════════════════════════════════════╣"
echo "║                                                              ║"
echo "║  To activate the environment in new terminals:              ║"
echo "║  ./activate_env.sh                                           ║"
echo "║                                                              ║"
echo "║  To run the application:                                     ║"
echo "║  ./activate_env.sh && python launch.py                       ║"
echo "║                                                              ║"
echo "║  For WSL GUI applications, ensure X11 server is running     ║"
echo "║  on Windows (VcXsrv, MobaXterm, etc.)                        ║"
echo "║                                                              ║"
echo "║  Virtual environment: ./emailintelligence_env/              ║"
echo "║  Configuration: ./wsl_config.sh                              ║"
echo "║                                                              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Show environment info
echo "📊 Environment Information:"
echo "  Ubuntu Version: $UBUNTU_VERSION"
echo "  Python Version: $($PYTHON_CMD --version)"
echo "  Virtual Environment: $(pwd)/$VENV_DIR"
echo "  PyTorch CPU: $(python -c "import torch; print(torch.__version__)" 2>/dev/null || echo "Not installed")"
