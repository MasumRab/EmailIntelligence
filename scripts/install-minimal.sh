#!/bin/bash
# Minimal Installation Script for EmailIntelligence
# Installs only core dependencies to minimize download size

set -e

echo "🚀 Installing EmailIntelligence (Minimal)"
echo "=========================================="
echo "This will install only core dependencies."
echo "Advanced features (ML, data science, etc.) will not be available."
echo ""

# Check if uv is available
if command -v uv &> /dev/null; then
    echo "📦 Using uv package manager..."
    uv pip install -e .
else
    echo "📦 Using pip package manager..."
    pip install -e .
fi

echo ""
echo "✅ Minimal installation complete!"
echo ""
echo "Core features available:"
echo "  • Web API (FastAPI)"
echo "  • Basic UI (Gradio)"
echo "  • Email validation"
echo "  • SQLite database"
echo ""
echo "To install additional features:"
echo "  pip install -e '.[ml]'        # Machine learning features"
echo "  pip install -e '.[data]'      # Data science features"
echo "  pip install -e '.[viz]'       # Visualization features"
echo "  pip install -e '.[full]'      # All features (except GPU)"
echo ""
echo "⚠️  GPU packages are NOT included - use system CUDA if needed"