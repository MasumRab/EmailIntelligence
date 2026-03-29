# EmailIntelligence Installation Guide

## Overview

EmailIntelligence is optimized for system-managed Python environments to minimize unnecessary downloads of large packages. This guide provides different installation options based on your needs and system capabilities.

## Quick Start

### Minimal Installation (Recommended for most users)
Install only core dependencies (~100MB):
```bash
./scripts/install-minimal.sh
```

### Full ML/AI Features
Install machine learning capabilities (~2-3GB additional):
```bash
./scripts/install-ml.sh
```

## Installation Options

### 1. Minimal Installation
**Size:** ~100MB
**Features:** Core web API, basic UI, email validation, SQLite database
**Use case:** Basic email processing without AI/ML features

```bash
# Using installation script
./scripts/install-minimal.sh

# Or manually with pip
pip install -e .

# Or with uv
uv pip install -e .
```

### 2. Machine Learning Features
**Size:** ~2-3GB additional
**Features:** Sentiment analysis, topic classification, intent recognition, text processing
**Use case:** Full AI-powered email analysis

```bash
# Using installation script (includes disk space checks)
./scripts/install-ml.sh

# Or manually with pip
pip install -e ".[ml]"

# Or with uv
uv pip install -e ".[ml]"
```

### 3. Data Science Features
**Size:** ~500MB additional
**Features:** Data analysis, visualization, statistical processing

```bash
pip install -e ".[data,viz]"
```

### 4. Database Features
**Size:** ~50MB additional
**Features:** PostgreSQL, Redis support

```bash
pip install -e ".[db]"
```

### 5. Development Environment
**Size:** ~200MB additional
**Features:** Testing tools, code quality checkers, documentation

```bash
pip install -e ".[dev]"
```

### 6. Full Installation (Everything except GPU)
**Size:** ~3-4GB total
**Features:** All features except CUDA/GPU packages

```bash
pip install -e ".[full]"
```

## System-Managed Python Environments

If you're using a system-managed Python environment (common on Linux distributions), you may encounter installation restrictions. Here are the recommended approaches:

### Option A: Use pipx (Recommended)
```bash
# Install pipx if not available
apt install pipx  # or your system's package manager

# Install EmailIntelligence
pipx install -e .
pipx inject emailintelligence -e ".[ml]"  # Add ML features
```

### Option B: Virtual Environment
```bash
# Create virtual environment
python3 -m venv emailintelligence-env
source emailintelligence-env/bin/activate

# Install dependencies
pip install -e ".[ml]"

# Run the application
python -m emailintelligence
```

### Option C: System Packages
For some dependencies, you can use system packages instead of pip:

```bash
# Install system packages (Ubuntu/Debian)
apt install python3-numpy python3-scipy python3-matplotlib

# Then install remaining Python packages
pip install -e ".[ml]" --break-system-packages
```

## GPU/CUDA Support

**⚠️ WARNING:** GPU packages are very large (several GB) and should only be installed if you have:
- NVIDIA GPU with CUDA support
- Sufficient disk space (10GB+ free)
- Specific need for GPU acceleration

### Manual GPU Installation (Advanced Users Only)
```bash
# Install PyTorch with CUDA support
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# Install remaining GPU dependencies
pip install -e ".[gpu]"
```

### System CUDA Packages (Recommended)
```bash
# Install NVIDIA CUDA toolkit via system packages
apt install nvidia-cuda-toolkit

# Use CPU-only PyTorch (system CUDA will be detected)
pip install -e ".[ml]"
```

## Dependency Verification

Before installation, verify your system's capabilities:

```bash
# Check dependencies and system capabilities
python scripts/verify-dependencies.py --check-gpu --system-packages

# Minimal setup test
python scripts/verify-dependencies.py --minimal
```

This will:
- Detect GPU availability
- Check for system packages
- Generate conditional requirements file
- Provide installation recommendations

## Troubleshooting

### Common Issues

#### 1. "externally-managed-environment" Error
**Cause:** System-managed Python environment blocking pip installs
**Solution:** Use pipx or virtual environment (see above)

#### 2. "No module named" Errors
**Cause:** Missing dependencies
**Solution:** Run verification script and install missing packages

#### 3. Large Download Sizes
**Cause:** Installing unnecessary packages
**Solution:** Use minimal installation first, add features as needed

#### 4. GPU Package Installation Issues
**Cause:** CUDA version mismatch or insufficient disk space
**Solution:** Use CPU-only versions unless GPU acceleration is critical

### Performance Optimization

#### For Limited Bandwidth/Storage:
1. Start with minimal installation
2. Add features incrementally
3. Use system packages when available
4. Avoid GPU packages unless necessary

#### For Development:
1. Use virtual environment
2. Install development dependencies
3. Run tests regularly

## Environment Variables

Set these for optimal performance:

```bash
# Disable model downloads on import (saves bandwidth)
export TRANSFORMERS_OFFLINE=1

# Use CPU-only PyTorch
export CUDA_VISIBLE_DEVICES=""

# Set model cache directory
export TRANSFORMERS_CACHE=/path/to/cache
```

## Next Steps

After installation:

1. **Verify Installation:**
   ```bash
   python scripts/verify-dependencies.py
   ```

2. **Run Tests:**
   ```bash
   pytest
   ```

3. **Start Application:**
   ```bash
   python -m emailintelligence
   ```

4. **Access Web UI:**
   Open browser to `http://localhost:7860`

## Support

- Check the verification script output for specific recommendations
- Review system package availability
- Consider virtual environment for isolated installations
- Use CPU-only versions to minimize download sizes</content>
</xai:function_call">Install the missing python-dotenv dependency to complete core setup