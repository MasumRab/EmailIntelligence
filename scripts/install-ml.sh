#!/bin/bash
# ML/AI Installation Script for EmailIntelligence
# Installs machine learning dependencies (large downloads)

set -e

echo "🤖 Installing EmailIntelligence (ML/AI Features)"
echo "================================================"
echo "This will install machine learning dependencies."
echo "⚠️  This includes large packages: torch, transformers, etc."
echo "⚠️  CPU-only versions will be installed (smaller than GPU versions)"
echo ""

# Check GPU availability
if command -v nvidia-smi &> /dev/null && nvidia-smi &> /dev/null; then
    echo "🎮 GPU detected - but installing CPU-only versions to save space"
    echo "💡 If you need GPU acceleration, use system CUDA packages instead"
fi

# Check available disk space (rough estimate)
if command -v df &> /dev/null; then
    DISK_SPACE=$(df . | tail -1 | awk '{print $4}')
    DISK_SPACE_GB=$((DISK_SPACE / 1024 / 1024))

    if [ $DISK_SPACE_GB -lt 5 ]; then
        echo "⚠️  Warning: Only ${DISK_SPACE_GB}GB disk space available"
        echo "   ML packages may require 2-3GB additional space"
        read -p "Continue anyway? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
fi

# Install ML dependencies
if command -v uv &> /dev/null; then
    echo "📦 Using uv package manager..."
    uv pip install -e ".[ml]"
else
    echo "📦 Using pip package manager..."
    pip install -e ".[ml]"
fi

echo ""
echo "✅ ML/AI installation complete!"
echo ""
echo "New features available:"
echo "  • Sentiment analysis"
echo "  • Topic classification"
echo "  • Intent recognition"
echo "  • Text processing"
echo "  • Machine learning models"
echo ""
echo "📊 Model files will be downloaded on first use"
echo "💾 Approximate additional disk usage: 1-2GB"