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

# Pass all arguments to the Python script
python3 launch.py "$@"

# Check if the script exited with an error
if [ $? -ne 0 ]; then
    echo
    echo "The application exited with an error. Please check the logs above."
    read -p "Press Enter to continue..."
fi