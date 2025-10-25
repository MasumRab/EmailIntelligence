@echo off
setlocal

:: EmailIntelligence Launcher for Windows
:: This script identifies a Python interpreter and executes launch.py.
:: All environment setup (venv, dependencies) is handled by launch.py.

:: Ensure launch.py exists
if not exist "launch.py" (
    echo Error: launch.py not found in the current directory.
    pause
    exit /B 1
)

set "PYTHON_TO_RUN="
set "PYTHON_ARGS="

:: 1. Try py -3.11
where py >nul 2>&1
if %errorlevel% equ 0 (
    py -3.11 --version >nul 2>&1
    if %errorlevel% equ 0 (
        set "PYTHON_TO_RUN=py"
        set "PYTHON_ARGS=-3.11"
    )
)

:: 2. Fallback to python3.11 if py -3.11 not successful
if not defined PYTHON_TO_RUN (
    where python3.11 >nul 2>&1
    if %errorlevel% equ 0 (
        set "PYTHON_TO_RUN=python3.11"
    )
)

:: 3. Fallback to python if python3.11 not successful
if not defined PYTHON_TO_RUN (
    where python >nul 2>&1
    if %errorlevel% equ 0 (
        set "PYTHON_TO_RUN=python"
    )
)

if not defined PYTHON_TO_RUN (
    echo Error: Python (3.11 recommended) not found.
    echo Please install Python 3.11 and ensure it's in PATH (accessible via 'py -3.11', 'python3.11', or 'python').
    pause
    exit /B 1
)

echo Using Python interpreter: %PYTHON_TO_RUN% %PYTHON_ARGS%
if defined PYTHON_ARGS (
    %PYTHON_TO_RUN% %PYTHON_ARGS% launch.py %*
) else (
    %PYTHON_TO_RUN% launch.py %*
)

set "EXIT_CODE=%errorlevel%"
if %EXIT_CODE% neq 0 (
    echo.
    echo The application exited with error code: %EXIT_CODE%.
    pause
)

endlocal
exit /B %EXIT_CODE%
