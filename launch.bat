@echo off
setlocal enabledelayedexpansion

:: EmailIntelligence Launcher for Windows
:: This batch file launches the EmailIntelligence application with the specified arguments

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed or not in PATH. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

:: Pass all arguments to the Python script
python launch.py %*

:: Check if the script exited with an error
if %errorlevel% neq 0 (
    echo.
    echo The application exited with an error. Please check the logs above.
    pause
)

endlocal