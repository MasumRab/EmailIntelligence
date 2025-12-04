# Conda Installation Guide for EmailIntelligence

This guide provides instructions for setting up the EmailIntelligence project using conda with CPU-only packages, utilizing the optimal channels for each package.

## Prerequisites

- Install [Anaconda](https://www.anaconda.com/products/distribution) or [Miniconda](https://docs.conda.io/en/latest/miniconda.html)
- Open Anaconda Prompt or terminal with conda available

## Step-by-Step Installation

### 1. Create a New Conda Environment

```bash
conda create -n emailintelligence python=3.10
conda activate emailintelligence
```

### 2. Configure Conda Channels (Recommended Order)

For optimal package resolution, configure channels with the recommended priority:

```bash

# Add channels in order of priority
conda config --add channels pytorch
conda config --add channels conda-forge
conda config --add channels defaults

# Show current channel priority
conda config --show channels
```

### 3. Install PyTorch with CPU-only Support

```bash

# Install PyTorch with CPU-only support from PyTorch's conda channel
conda install pytorch torchvision torchaudio cpuonly -c pytorch
```

### 4. Install Intel-Optimized Libraries (Optional)

For improved performance on Intel hardware, you can install Intel's optimized packages separately:
```bash

# Note: The 'intel' channel is not available in this guide due to access restrictions

# You may manually install Intel-optimized packages if available in other channels
```

### 5. Install Other Dependencies via Conda with Appropriate Channels

Install packages using the best available channel for each:

```bash

# Core AI/ML libraries
conda install -c huggingface transformers -c conda-forge accelerate

# NLP libraries
conda install -c conda-forge nltk textblob

# Web framework
conda install -c conda-forge fastapi uvicorn -c gradio gradio

# Utilities
conda install -c conda-forge python-dotenv psutil structlog redis

# Google APIs
conda install -c conda-forge google-api-python-client google-auth google-auth-oauthlib

# Email processing
conda install -c conda-forge email-validator

# Development and testing
conda install -c conda-forge pytest pytest-asyncio

# Additional utilities
conda install -c conda-forge bleach pyotp qrcode RestrictedPython aiosqlite aiofiles pydantic pydantic-settings python-multipart httpx pyngrok
```

### 6. Install Remaining Dependencies via Pip

If any packages fail to install via conda, you can install them with pip:

```bash

# Only run this if conda installation failed for any packages
pip install pydantic>=2.11.5 pydantic-settings>=2.0.0 python-multipart>=0.0.20 httpx>=0.28.1 pyngrok>=0.7.0
```

## Alternative: Complete Pip Installation in Conda Environment

If you prefer to use pip for all packages in your conda environment:

1. Create and activate the environment:
```bash
conda create -n emailintelligence python=3.10
conda activate emailintelligence
```

2. Install PyTorch with CPU-only support:
```bash
conda install pytorch torchvision torchaudio cpuonly -c pytorch
```

3. Install all remaining packages from requirements.txt (after installing CPU-only PyTorch):
```bash

# Note: Most packages should already be installed via conda

# This is only if some packages couldn't be installed via conda
pip install -r setup/requirements.txt
```

## Verification

To verify the installation, run:

```bash
python -c "import torch; print(f'PyTorch version: {torch.__version__}'); print(f'CPU available: {torch.cuda.is_available()}')"
```

To verify all required packages can be imported:

```bash
python -c "
import transformers
import accelerate
import nltk
import textblob
import fastapi
import pydantic
import uvicorn
import gradio
import sklearn
import joblib
import RestrictedPython
import aiosqlite
import aiofiles
import redis
import googleapiclient.discovery
import google.auth
import google.auth.transport.requests
import httplib2
import email_validator
import pytest
import bleach
import dotenv
import psutil
import pyotp
import qrcode
import structlog
print('All packages successfully imported!')
"
```

You should see that CUDA is not available since we installed CPU-only packages, which is the desired behavior.

## Troubleshooting

### If you encounter package conflicts:
1. Try installing packages one by one to identify the conflicting package
2. Consider using the alternative installation method (pip in conda environment)

### If packages are not found in conda:
- First try searching with `conda search <package_name>`
- If not available, install with pip as shown in the installation steps

### Minimizing pip installations:
- Most packages in requirements.txt can now be installed via conda
- Only use pip if conda installation fails for specific packages

### Channel-specific troubleshooting:
- For PyTorch packages: ensure the PyTorch channel is prioritized: `conda install -c pytorch <package>`
- For conda-forge packages: use: `conda install -c conda-forge <package>`

### Environment management:
- To deactivate the environment: `conda deactivate`
- To remove the environment: `conda env remove -n emailintelligence`
- To list all environments: `conda env list`
