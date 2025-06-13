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

:: Define the virtual environment directory name
set "VENV_DIR=venv"

:: Check if uv is installed
uv --version >nul 2>&1
if %errorlevel% equ 0 (
    echo uv is installed. Using uv to create and manage the virtual environment.
    :: Create the virtual environment using uv if it doesn't exist
    if not exist "%VENV_DIR%" (
        uv venv "%VENV_DIR%"
        if !errorlevel! neq 0 (
            echo Failed to create virtual environment with uv. Please check for errors.
            pause
            exit /b 1
        )
    )
    :: Activate the virtual environment
    call "%VENV_DIR%\Scripts\activate.bat"
    :: Install dependencies using uv pip
    uv pip install -r requirements.txt
    if !errorlevel! neq 0 (
        echo Failed to install dependencies with uv pip. Please check for errors.
        pause
        exit /b 1
    )
) else (
    echo uv is not installed. Falling back to python -m venv.
    :: Check if the virtual environment directory exists
    if not exist "%VENV_DIR%" (
        echo Creating virtual environment using python -m venv.
        python -m venv "%VENV_DIR%"
        if !errorlevel! neq 0 (
            echo Failed to create virtual environment with python -m venv. Please check for errors.
            pause
            exit /b 1
        )
    )
    :: Activate the virtual environment
    call "%VENV_DIR%\Scripts\activate.bat"
    :: Install dependencies using pip
    pip install -r requirements.txt
    if !errorlevel! neq 0 (
        echo Failed to install dependencies with pip. Please check for errors.
        pause
        exit /b 1
    )
)

:: Execute the Python script
python launch.py %*

:: Check if the script exited with an error
if %errorlevel% neq 0 (
    echo.
    echo The application exited with an error. Please check the logs above.
    pause
)

:: Deactivate the virtual environment upon exiting
call "%VENV_DIR%\Scripts\deactivate.bat"

endlocal