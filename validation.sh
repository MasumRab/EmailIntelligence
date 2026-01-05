#!/bin/bash
# Run all code quality checks for EmailIntelligence

set -e  # Exit on error

echo "=================================================="
echo "Running Code Quality Validation"
echo "=================================================="

echo -e "\n[1/4] Running Black (Formatting)..."
if python -m black src tests --check --line-length=100; then
    echo "✅ Black passed"
else
    echo "❌ Black failed"
    exit 1
fi

echo -e "\n[2/4] Running Ruff (Linting)..."
if python -m ruff check src tests; then
    echo "✅ Ruff passed"
else
    echo "❌ Ruff failed"
    exit 1
fi

echo -e "\n[3/4] Running Flake8 (Style)..."
if python -m flake8 src tests --max-line-length=100 --extend-ignore=E203,W503; then
    echo "✅ Flake8 passed"
else
    echo "❌ Flake8 failed"
    exit 1
fi

echo -e "\n[4/4] Running Pytest (Unit Tests)..."
if python -m pytest; then
    echo "✅ Tests passed"
else
    echo "❌ Tests failed"
    exit 1
fi

echo -e "\n🎉 All validation checks passed successfully!"
