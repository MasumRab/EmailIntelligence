@echo off
REM EmailIntelligence Launcher for Windows
REM Enhanced launcher with path resolution, conda support, and error handling

setlocal enabledelayedexpansion

REM Get the directory where this batch file is located
set "SCRIPT_DIR=%~dp0"
set "SCRIPT_DIR=%SCRIPT_DIR:~0,-1%"

REM Change to the script directory to ensure consistent execution
cd /d "%SCRIPT_DIR%"

REM Check if python is available
where python >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo ERROR: Python is not found in PATH. Please install Python 3.12+ and add it to your PATH.
    echo You can download Python from: https://python.org
    pause
    exit /b 1
)

REM Check Python version
python -c "import sys; sys.exit(0 if sys.version_info >= (3, 12) else 1)" >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo WARNING: Python version might be older than 3.12. Some features may not work correctly.
)

REM Check for conda
where conda >nul 2>nul
if %ERRORLEVEL% equ 0 (
    echo Conda detected. The launcher will handle environment activation automatically.
) else (
    echo No conda detected. Using virtual environment or system Python.
)

echo Starting EmailIntelligence Launcher...
echo Working directory: %SCRIPT_DIR%
echo Command: python launch.py %*

REM Execute launch.py with all arguments, properly handling paths with spaces
python launch.py %*

REM Capture the exit code
set LAUNCH_EXIT_CODE=%ERRORLEVEL%

if %LAUNCH_EXIT_CODE% neq 0 (
    echo.
    echo ERROR: Launcher exited with code %LAUNCH_EXIT_CODE%
    echo Check the output above for error details.
    echo.
    echo Common issues:
    echo - Missing dependencies: Run 'python launch.py --setup'
    echo - Port conflicts: Use --port option to specify different port
    echo - Permission issues: Run as administrator if needed
    echo.
    pause
) else (
    echo.
    echo EmailIntelligence launcher completed successfully.
)

exit /b %LAUNCH_EXIT_CODE%
