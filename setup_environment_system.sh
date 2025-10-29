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
    python3-sklearn \
    python3-joblib \
    python3-psutil \
    python3-sentencepiece

# Install Python web framework packages
log_info "🌐 Installing Python web framework packages..."
sudo apt install -y \
    python3-uvicorn \
    python3-pydantic \
    python3-multipart \
    python3-httpx \
    python3-dotenv \
    python3-email-validator
# Note: python3-fastapi installed via pip as system package is outdated

# Install Python utility packages
log_info "🛠️ Installing Python utility packages..."
sudo apt install -y \
    python3-bleach \
    python3-aiofiles \
    python3-sqlite3 \
    python3-aiosqlite \
    python3-restrictedpython
# Note: aiosqlite, RestrictedPython installed via system packages

# Install development tools
log_info "🔧 Installing development tools..."
sudo apt install -y \
    python3-flake8 \
    python3-isort \
    python3-mypy \
    python3-pytest \
    python3-pytest-asyncio
# Note: python3-black, python3-pylint installed via pip as system packages are outdated

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

python3 -m venv --system-site-packages "$VENV_DIR"
source "$VENV_DIR/bin/activate"

# Upgrade pip in virtual environment
log_info "⬆️ Upgrading pip..."
pip install --upgrade pip --timeout 120

# Install packages that are not available in Ubuntu system repos
log_info "🤖 Installing specialized AI/ML packages (pip only)..."

# PyTorch CPU (not available in Ubuntu repos)
log_info "🧠 Installing PyTorch CPU version..."
log_info "   ⏳ This may take several minutes depending on your internet connection..."
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu --timeout 300

# Hugging Face ecosystem
log_info "🤖 Installing AI/ML packages..."
log_info "   ⏳ This may take several minutes depending on your internet connection..."
pip install transformers accelerate --timeout 600
# Note: sentencepiece installed via system packages

# NLP packages
sudo apt install -y \
    python3-nltk
pip install textblob --quiet
# Note: nltk installed via system packages

# Web/API packages
sudo apt install -y \
    python3-plotly \
    python3-seaborn
log_info "🌐 Installing web and API packages..."
log_info "   ⏳ This may take a few minutes depending on your internet connection..."
pip install gradio pyngrok fastapi --timeout 300
# Note: plotly, seaborn, email-validator installed via system packages

# Google API packages
sudo apt install -y \
    python3-googleapi \
    python3-google-auth \
    python3-google-auth-httplib2 \
    python3-google-auth-oauthlib
log_info "🔐 Installing Google API client..."
log_info "   ⏳ This may take a minute..."
pip install google-api-python-client --timeout 300
# Note: google-auth, google-auth-oauthlib installed via system packages

# Security and specialized packages
pip install pydantic-settings --timeout 120
# Note: RestrictedPython, aiosqlite installed via system packages

# Verify system package versions
log_info "🔍 Verifying system package versions..."
python -c "
import nltk
import plotly
import seaborn
import email_validator
import aiosqlite
import RestrictedPython
print(f'nltk version: {nltk.__version__}')
print(f'plotly version: {plotly.__version__}')
print(f'seaborn version: {seaborn.__version__}')
print(f'aiosqlite version: {aiosqlite.__version__}')
print(f'RestrictedPython version: {RestrictedPython.__version__ if hasattr(RestrictedPython, \"__version__\") else \"unknown\"}')
"

# Download NLTK data
log_info "📖 Downloading NLTK data..."
python -c "
import nltk
import ssl
try:
    # Handle SSL issues in some environments
    ssl._create_default_https_context = ssl._create_unverified_context
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
    print('NLTK data downloaded successfully')
except Exception as e:
    print(f'Warning: NLTK download failed: {e}')

# Verify sentencepiece installation
try:
    import sentencepiece
    print(f'sentencepiece version: {sentencepiece.__version__}')
except ImportError:
    # sentencepiece might not have __version__ attribute
    import sentencepiece as spm
    print('sentencepiece imported successfully')
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

# Final compatibility check
log_info "🔍 Running final compatibility check..."
python -c "
import sys
success = True

# Check core packages
try:
    import torch
    print('✅ PyTorch import: OK')
except ImportError:
    print('❌ PyTorch import: FAILED')
    success = False

try:
    import fastapi
    print('✅ FastAPI import: OK')
except ImportError:
    print('❌ FastAPI import: FAILED')
    success = False

try:
    import transformers
    print('✅ Transformers import: OK')
except ImportError:
    print('❌ Transformers import: FAILED')
    success = False

# Check system packages
try:
    import nltk
    print('✅ NLTK import: OK')
except ImportError:
    print('❌ NLTK import: FAILED')
    success = False

try:
    import plotly
    print('✅ Plotly import: OK')
except ImportError:
    print('❌ Plotly import: FAILED')
    success = False

try:
    import seaborn
    print('✅ Seaborn import: OK')
except ImportError:
    print('❌ Seaborn import: FAILED')
    success = False

try:
    import aiosqlite
    print('✅ Aiosqlite import: OK')
except ImportError:
    print('❌ Aiosqlite import: FAILED')
    success = False

try:
    import RestrictedPython
    print('✅ RestrictedPython import: OK')
except ImportError:
    print('❌ RestrictedPython import: FAILED')
    success = False

try:
    import sentencepiece
    print('✅ SentencePiece import: OK')
except ImportError:
    print('❌ SentencePiece import: FAILED')
    success = False

try:
    import google.auth
    print('✅ Google Auth import: OK')
except ImportError:
    print('❌ Google Auth import: FAILED')
    success = False

try:
    import email_validator
    print('✅ Email Validator import: OK')
except ImportError:
    print('❌ Email Validator import: FAILED')
    success = False

if not success:
    print('⚠️  Some packages failed to import, check installation logs.')
    sys.exit(1)
else:
    print('✅ All packages imported successfully!')
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
