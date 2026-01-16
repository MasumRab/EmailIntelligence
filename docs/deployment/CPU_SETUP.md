# CPU-Only Setup (NVIDIA-Free)

This guide explains how to set up EmailIntelligence without NVIDIA/CUDA dependencies for CPU-only operation.

## Problem

By default, installing `transformers` and `accelerate` pulls in PyTorch with CUDA support, which includes many NVIDIA packages even on systems without GPUs.

## Solution

### 1. Install CPU-Only PyTorch First

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install CPU-only PyTorch
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

### 2. Install HuggingFace Libraries

```bash
# Install transformers and accelerate (they will use the CPU PyTorch)
pip install transformers accelerate
```

### 3. Verify CPU-Only Setup

```bash
python -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}')"
# Should print: CUDA available: False
```

## Configuration Files

### requirements-cpu.txt
```
torch>=2.4.0
torchvision>=0.19.0
torchaudio>=2.4.0
```

### requirements.txt (modified)
```
# AI/ML packages (CPU versions - CUDA-free)
# Note: PyTorch CPU-only versions are installed via setup scripts
transformers[torch]>=4.40.0  # CPU-only, no CUDA dependencies
accelerate>=0.30.0
sentencepiece>=0.2.0
scikit-learn>=1.5.0
joblib>=1.5.1

# Data science
pandas>=2.0.0
numpy>=1.26.0
matplotlib>=3.8.0
seaborn>=0.13.0
scipy>=1.11.0
plotly>=5.18.0

# NLP
nltk>=3.9.1
textblob>=0.19.0

# Web and API
httpx>=0.28.1
gradio>=4.0.0
pyngrok>=0.7.0
email-validator>=2.2.0

# Google APIs
google-api-python-client>=2.172.0
google-auth>=2.40.3
google-auth-oauthlib>=1.2.2

# Security and utilities
bleach>=6.0.0
python-dotenv>=1.1.0
pydantic-settings>=2.0.0
psutil>=6.0.0
aiosqlite>=0.19.0
RestrictedPython>=8.0
```

## Setup Scripts

All setup scripts (`setup_environment*.sh`) have been updated to use CPU-only PyTorch:

```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

## Benefits

- ✅ **No NVIDIA dependencies**: Completely CUDA-free setup
- ✅ **Smaller installation**: Fewer packages to download/install
- ✅ **Faster setup**: No large CUDA libraries
- ✅ **Broader compatibility**: Works on any CPU system
- ✅ **Reduced memory usage**: CPU-only PyTorch is lighter

## Performance Notes

- **Transformers**: Will work but may be slower on CPU vs GPU
- **Accelerate**: Will use CPU acceleration features
- **Training**: Possible but much slower than GPU
- **Inference**: Works well for smaller models

## Troubleshooting

If you accidentally install CUDA versions:

```bash
# Remove CUDA PyTorch
pip uninstall torch torchvision torchaudio

# Install CPU-only versions
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

## Alternative: Use Conda

Conda makes CPU-only installation easier:

```bash
conda create -n emailintel python=3.12
conda activate emailintel
conda install pytorch torchvision torchaudio cpuonly -c pytorch
pip install transformers accelerate
```