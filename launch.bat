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

REM Determine if conda should be used
set "USE_CONDA_FLAG="
set "CONDA_ENV_NAME_ARG="
for %%A in (%*) do (
    if /i "%%A"=="--use-conda" (
        set "USE_CONDA_FLAG=true"
    )
    if /i "%%A"=="--conda-env" (
        set "CONDA_ENV_NAME_ARG=true"
    )
)

set "CONDA_COMMAND="
if defined USE_CONDA_FLAG (
    where conda >nul 2>nul
    if %ERRORLEVEL% equ 0 (
        echo Conda detected and --use-conda flag is present. Attempting to run via conda.
        set "CONDA_ENV_TO_USE=base"
        REM Extract conda environment name if specified
        for /f "tokens=1,2" %%i in ("%*") do (
            if /i "%%i"=="--conda-env" (
                set "CONDA_ENV_TO_USE=%%j"
            )
        )
        echo Using conda environment: %CONDA_ENV_TO_USE%
        set "CONDA_COMMAND=conda run -n %CONDA_ENV_TO_USE% python launch.py %*"
    ) else (
        echo WARNING: --use-conda flag specified, but conda is not found. Falling back to standard python execution.
    )
) else if defined CONDA_ENV_NAME_ARG (
    where conda >nul 2>nul
    if %ERRORLEVEL% equ 0 (
        echo Conda detected and --conda-env flag is present. Attempting to run via conda.
        set "CONDA_ENV_TO_USE="
        REM Extract conda environment name if specified
        for /f "tokens=1,2" %%i in ("%*") do (
            if /i "%%i"=="--conda-env" (
                set "CONDA_ENV_TO_USE=%%j"
            )
        )
        if not defined CONDA_ENV_TO_USE (
            echo ERROR: --conda-env flag used without specifying an environment name. Falling back to standard python execution.
            set "CONDA_COMMAND="
        ) else (
            echo Using conda environment: %CONDA_ENV_TO_USE%
            set "CONDA_COMMAND=conda run -n %CONDA_ENV_TO_USE% python launch.py %*"
        )
    ) else (
        echo WARNING: --conda-env flag specified, but conda is not found. Falling back to standard python execution.
    )
)

if defined CONDA_COMMAND (
    echo Command: %CONDA_COMMAND%
    %CONDA_COMMAND%
) else (
    echo Command: python launch.py %*
    REM Execute launch.py with all arguments, properly handling paths with spaces
    python launch.py %*
)

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
