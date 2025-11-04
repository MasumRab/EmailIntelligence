#!/bin/bash

echo "Cleaning up virtual environment (venv)..."
rm -rf venv

echo "Cleaning up Python cache (__pycache__) directories..."
find . -type d -name "__pycache__" -exec rm -rf {} +

echo "Cleaning up typescript log file..."
rm -f typescript

echo "Cleanup complete."
