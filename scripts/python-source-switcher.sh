#!/bin/bash
# Python Source Switcher - Quick way to switch between Python installations
# Add to ~/.bashrc or ~/.zshrc

# Current active python
alias py-current='which python && python --version'

# Switch to Mise Python (current default)
py-mise() {
    export PATH="$HOME/.local/share/mise/installs/python/3.12.13/bin:$PATH"
    echo "Switched to Mise Python: $(python --version)"
}

# Switch to Conda Python  
py-conda() {
    source ~/miniconda3/etc/profile.d/conda.sh
    conda activate base
    echo "Switched to Conda Python: $(python --version)"
}

# Switch to System Python
py-system() {
    export PATH=/usr/bin:$PATH
    echo "Switched to System Python: $(python --version)"
}

# Show all available Python sources
py-sources() {
    echo "=== Available Python Sources ==="
    echo ""
    echo "Mise (current):"
    echo "  → $(which python 2>/dev/null || echo 'not in PATH')"
    echo "  → $(python --version 2>/dev/null || echo 'not available')"
    echo ""
    echo "Conda:"
    echo "  → ~/miniconda3/bin/python"
    echo "  → $(~/miniconda3/bin/python --version 2>/dev/null || echo 'not available')"
    echo ""
    echo "System:"
    echo "  → /usr/bin/python3"
    echo "  → $(/usr/bin/python3 --version 2>/dev/null || echo 'not available')"
}

# Quick install with specific source
pip-mise() {
    $HOME/.local/share/mise/installs/python/3.12.13/bin/pip "$@"
}

pip-conda() {
    ~/miniconda3/bin/pip "$@"
}

pip-system() {
    /usr/bin/pip3 "$@"
}
