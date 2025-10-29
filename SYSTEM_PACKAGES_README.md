# EmailIntelligence System Package Requirements

This document outlines the system-wide packages required for the EmailIntelligence project and provides setup instructions.

## Setup Approaches

### Option 1: System Package Priority (Recommended)
Uses Ubuntu system packages where possible for better integration and automatic updates.

**Benefits:**
- ✅ Automatic security updates
- ✅ Better system integration
- ✅ Reduced disk usage
- ✅ Optimized performance
- ✅ No version conflicts

**Usage:**
```bash
./setup_environment_system.sh
./activate_system.sh
```

### Option 2: Virtual Environment Only
Installs everything via pip in isolated virtual environment.

**Usage:**
```bash
./setup_environment.sh  # or ./setup_environment_wsl.sh for WSL
```

### Option 3: Manual Installation
Follow the detailed instructions below.

## System Packages (Install with apt)

The following Debian/Ubuntu packages should be installed system-wide:

### Core Python Development
- `python3-dev` - Python development headers
- `python3-pip` - Python package installer
- `python3-venv` - Python virtual environment support
- `python3-setuptools` - Python package building
- `python3-wheel` - Python wheel support

### Build Tools
- `build-essential` - Essential build tools (gcc, make, etc.)
- `gfortran` - Fortran compiler for scientific computing

### SSL and Cryptography
- `libssl-dev` - SSL development libraries
- `libffi-dev` - Foreign function interface
- `libbz2-dev`, `liblzma-dev`, `libreadline-dev` - Compression and readline support

### Scientific Computing Libraries
- `libblas-dev` - Basic Linear Algebra Subprograms
- `liblapack-dev` - Linear Algebra PACKage
- `libatlas-base-dev` - Automatically Tuned Linear Algebra Software

### Graphics and Imaging
- `libfreetype6-dev` - FreeType font library
- `libpng-dev` - PNG image library
- `libjpeg-dev` - JPEG image library
- `libtiff-dev` - TIFF image library
- `libx11-dev`, `libxext-dev` - X11 development libraries

### Development Tools
- `git` - Version control
- `curl`, `wget` - Network utilities

## Python Packages (Install in Virtual Environment)

The following Python packages should be installed in a virtual environment, NOT system-wide:

### Core Web Framework
- FastAPI, Uvicorn, Pydantic - Web framework and validation

### AI/ML (CPU Versions)
- PyTorch (CPU-only from pytorch.org/whl/cpu)
- Transformers, Accelerate - Hugging Face ecosystem
- Scikit-learn, Joblib - Machine learning

### Data Science
- Pandas, NumPy, Matplotlib, Seaborn, SciPy, Plotly

### NLP
- NLTK, TextBlob

### Web and APIs
- HTTPX, Gradio, Pyngrok, Email-validator

### Google APIs
- google-api-python-client, google-auth, google-auth-oauthlib

### Utilities
- Bleach, python-dotenv, psutil, aiosqlite, RestrictedPython

## Installation Instructions

### Option 1: Automated Setup
```bash
# Run the automated setup script
./setup_environment.sh
```

### Option 2: Manual Setup
```bash
# Install system packages
sudo apt update
sudo apt install python3-dev python3-pip python3-venv build-essential libssl-dev libffi-dev libblas-dev liblapack-dev libfreetype6-dev libpng-dev git curl wget

# Set up environment using the project's standard launcher
python launch.py --setup

# This creates a venv and installs all dependencies using uv
# CPU PyTorch is automatically installed for lightweight deployment

# Alternative manual setup (not recommended):
# python3 -m venv venv
# source venv/bin/activate
# pip install uv
# uv pip install -e .
uv sync  # Standard dependency management
```

## Important Notes

1. **Do NOT install Python packages system-wide** - This can break system Python and cause conflicts
2. **Use virtual environments** - Always work within a virtual environment
3. **PyTorch CPU-only** - The setup ensures CPU-only PyTorch installation to avoid NVIDIA dependencies
4. **NLTK data** - Some packages require downloading additional data (handled in setup script)

## Troubleshooting

### Externally Managed Environment Error
If you get "externally-managed-environment" error, you're trying to install packages system-wide. Use a virtual environment instead.

### PyTorch CUDA Issues
If PyTorch tries to install CUDA versions, use the `--index-url https://download.pytorch.org/whl/cpu` flag.

### Permission Issues
Use `sudo` only for `apt install` commands, never for `pip install`.

## Verification

After setup, verify your installation:

```bash
# Check package availability
python3 verify_packages.py

# Test basic functionality
python3 -c "import numpy, torch, fastapi; print('Core packages working!')"
```

## Package Distribution

The system prioritizes **25+ system packages** for core functionality and uses **15 specialized packages** in virtual environment for AI/ML components not available in Ubuntu repositories.
