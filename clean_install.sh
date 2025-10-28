#!/bin/bash
echo "Activating fresh virtual environment..."
source venv/bin/activate

echo "Upgrading pip..."
pip install --upgrade pip

echo "Installing CPU-only PyTorch packages..."
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

echo "Installing other required packages..."
pip install -r requirements.txt

echo "Installation complete!"
echo "To activate: source venv/bin/activate"
