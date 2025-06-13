#!/bin/bash

# EmailIntelligence Launcher for Unix-based systems
# This shell script launches the EmailIntelligence application with the specified arguments

# Make the script executable if it's not already
if [ ! -x "$0" ]; then
    chmod +x "$0"
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed or not in PATH. Please install Python 3.8 or higher."
    exit 1
fi

# Define the virtual environment directory name
VENV_DIR="venv"

# Check if uv is installed
if command -v uv &> /dev/null; then
    echo "uv is installed. Using uv to create and manage the virtual environment."
    # Create the virtual environment using uv if it doesn't exist
    if [ ! -d "$VENV_DIR" ]; then
        uv venv "$VENV_DIR"
        if [ $? -ne 0 ]; then
            echo "Failed to create virtual environment with uv. Please check for errors."
            exit 1
        fi
    fi
    # Activate the virtual environment
    source "$VENV_DIR/bin/activate"
    # Install dependencies using uv pip
    uv pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "Failed to install dependencies with uv pip. Please check for errors."
        exit 1
    fi
else
    echo "uv is not installed. Falling back to python3 -m venv."
    # Check if the virtual environment directory exists
    if [ ! -d "$VENV_DIR" ]; then
        echo "Creating virtual environment using python3 -m venv."
        python3 -m venv "$VENV_DIR"
        if [ $? -ne 0 ]; then
            echo "Failed to create virtual environment with python3 -m venv. Please check for errors."
            exit 1
        fi
    fi
    # Activate the virtual environment
    source "$VENV_DIR/bin/activate"
    # Install dependencies using pip
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "Failed to install dependencies with pip. Please check for errors."
        exit 1
    fi
fi

# Execute the Python script
python3 launch.py "$@"

# Check if the script exited with an error
if [ $? -ne 0 ]; then
    echo
    echo "The application exited with an error. Please check the logs above."
    read -p "Press Enter to continue..."
fi

# Deactivate the virtual environment upon exiting
deactivate