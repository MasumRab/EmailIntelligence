@echo off
setlocal enabledelayedexpansion

:: === Configuration ===
:: Specify your project's Conda environment name here if applicable
set "PROJECT_CONDA_ENV_NAME=your_conda_env_name"
:: Specify your project's venv directory name
set "VENV_DIR=venv"

:: === PowerShell Detection ===
:: Check if running in PowerShell (powershell.exe or pwsh.exe)
set "IS_POWERSHELL="
echo "%COMSPEC%" | findstr /I /C:"powershell.exe" >nul && set "IS_POWERSHELL=1"
echo "%COMSPEC%" | findstr /I /C:"pwsh.exe" >nul && set "IS_POWERSHELL=1"
if defined IS_POWERSHELL (
    echo Running in PowerShell.
)

:: === Conda Environment Handling ===
set "CONDA_ENV_ACTIVATED_BY_SCRIPT="
set "VENV_ACTIVATED_BY_SCRIPT="
set "PYTHON_EXE=python"

:: Check if Conda is available
where conda >nul 2>&1
if %errorlevel% equ 0 (
    echo Conda is available.
    if /I "%PROJECT_CONDA_ENV_NAME%" == "your_conda_env_name" (
        echo INFO: Project specific Conda environment name is set to the default placeholder 'your_conda_env_name'.
        echo This script will not attempt to activate or create this specific Conda environment.
        echo If you wish to use a project-specific Conda environment, please edit this script
        echo and set PROJECT_CONDA_ENV_NAME to your desired environment name.
        echo Falling back to checking for an existing active Conda environment or using standard venv.
    )
    :: Check if already in a Conda environment
    if defined CONDA_DEFAULT_ENV (
        echo Already in a Conda environment: %CONDA_DEFAULT_ENV%
        set "PYTHON_EXE=%CONDA_PREFIX%\python.exe"
        echo Using Python from active Conda env: %PYTHON_EXE%
        if /I "%CONDA_DEFAULT_ENV%"=="%PROJECT_CONDA_ENV_NAME%" (
            echo Current Conda environment matches project environment. Using it.
        ) else (
            if "%PROJECT_CONDA_ENV_NAME%" NEQ "your_conda_env_name" (
                echo Current Conda environment (%CONDA_DEFAULT_ENV%) does not match project specific one (%PROJECT_CONDA_ENV_NAME%).
                echo Attempting to activate project Conda environment: %PROJECT_CONDA_ENV_NAME%
                call conda activate "%PROJECT_CONDA_ENV_NAME%"
                if !errorlevel! neq 0 (
                    echo WARNING: Failed to activate Conda environment: %PROJECT_CONDA_ENV_NAME%. Will use current Conda env: %CONDA_DEFAULT_ENV%.
                    echo Please ensure it exists and Conda is configured correctly.
                ) else (
                    echo Successfully activated Conda environment: %PROJECT_CONDA_ENV_NAME%
                    set "CONDA_ENV_ACTIVATED_BY_SCRIPT=1"
                    set "PYTHON_EXE=%CONDA_PREFIX%\python.exe"
                    echo Using Python from newly activated Conda env: %PYTHON_EXE%
                )
            )
        )
    ) else (
        if "%PROJECT_CONDA_ENV_NAME%" NEQ "your_conda_env_name" (
            echo Not in a Conda environment. Attempting to activate project Conda environment: %PROJECT_CONDA_ENV_NAME%
            call conda activate "%PROJECT_CONDA_ENV_NAME%"
            if !errorlevel! neq 0 (
                echo WARNING: Failed to activate Conda environment: %PROJECT_CONDA_ENV_NAME%.
                echo Attempting to create the Conda environment...
                call conda create -n "%PROJECT_CONDA_ENV_NAME%" python=3.9 -y
                if !errorlevel! neq 0 (
                    echo WARNING: Failed to create Conda environment: %PROJECT_CONDA_ENV_NAME%.
                    echo It might not exist or Conda needs setup (e.g., conda init for your shell).
                    echo Falling back to standard venv.
                    set "PROJECT_CONDA_ENV_NAME=your_conda_env_name"
                ) else (
                    echo Successfully created Conda environment: %PROJECT_CONDA_ENV_NAME%.
                    echo Attempting to activate the newly created environment...
                    call conda activate "%PROJECT_CONDA_ENV_NAME%"
                    if !errorlevel! neq 0 (
                        echo WARNING: Failed to activate newly created Conda environment: %PROJECT_CONDA_ENV_NAME%.
                        echo Falling back to standard venv.
                        set "PROJECT_CONDA_ENV_NAME=your_conda_env_name"
                    ) else (
                        set "CONDA_ENV_ACTIVATED_BY_SCRIPT=1"
                        set "PYTHON_EXE=%CONDA_PREFIX%\python.exe"
                        echo Successfully activated newly created Conda environment: %PROJECT_CONDA_ENV_NAME%
                        echo Using Python from Conda env: %PYTHON_EXE%
                    )
                )
            ) else (
                set "CONDA_ENV_ACTIVATED_BY_SCRIPT=1"
                set "PYTHON_EXE=%CONDA_PREFIX%\python.exe"
                echo Successfully activated Conda environment: %PROJECT_CONDA_ENV_NAME%
                echo Using Python from Conda env: %PYTHON_EXE%
            )
        )
    )
) else (
    echo Conda is not available or not in PATH.
)

:: === Standard Venv Handling (if no Conda environment is active or activated by script) ===
if not defined CONDA_DEFAULT_ENV and not defined CONDA_ENV_ACTIVATED_BY_SCRIPT (
    echo Proceeding with standard venv setup.
    where python >nul 2>&1
    if %errorlevel% neq 0 (
        if not exist "%VENV_DIR%\Scripts\python.exe" (
            echo Python is not installed, not in PATH, and no venv Python found. Please install Python 3.8 or higher.
            pause
            exit /b 1
        )
    )

    set "ACTIVATION_SUCCESSFUL="
    if defined IS_POWERSHELL (
        if exist "%VENV_DIR%\Scripts\Activate.ps1" (
            echo Activating venv for PowerShell...
            set "ACTIVATION_STATUS="
            FOR /F "tokens=*" %%i IN ('powershell -NoProfile -ExecutionPolicy Bypass -Command "& ""%CD%\%VENV_DIR%\Scripts\Activate.ps1""; if ($?) { Write-Host ""PS_ACTIVATE_SUCCESS"" }"') DO SET "ACTIVATION_STATUS=%%i"
            if "!ACTIVATION_STATUS!"=="PS_ACTIVATE_SUCCESS" (
                echo PowerShell venv activation successful.
                set "VENV_ACTIVATED_BY_SCRIPT=1"
                set "PYTHON_EXE=%CD%\%VENV_DIR%\Scripts\python.exe"
            ) else (
                echo PowerShell venv activation failed or script did not confirm success.
            )
        ) else (
            echo %VENV_DIR%\Scripts\Activate.ps1 not found. Cannot activate for PowerShell.
        )
    ) else (
        if exist "%VENV_DIR%\Scripts\activate.bat" (
            echo Activating venv for Command Prompt...
            call "%VENV_DIR%\Scripts\activate.bat"
            set "VENV_ACTIVATED_BY_SCRIPT=1"
            set "PYTHON_EXE=%CD%\%VENV_DIR%\Scripts\python.exe"
        ) else (
             echo %VENV_DIR%\Scripts\activate.bat not found. Cannot activate for Command Prompt.
        )
    )

    :: Create venv and install dependencies if not already in an active Conda environment
    :: And if venv activation (or attempt) was made
    if defined VENV_ACTIVATED_BY_SCRIPT (
        where uv >nul 2>&1
        if %errorlevel% equ 0 (
            echo uv is installed. Using uv.
            if not exist "%VENV_DIR%\pyvenv.cfg" ( :: More reliable venv check
                uv venv "%VENV_DIR%" --python "%PYTHON_EXE%"
                if !errorlevel! neq 0 (
                    echo Failed to create venv with uv.
                    pause
                    exit /b 1
                )
            )
            echo Installing dependencies with uv...
            uv pip install -r requirements.txt
            if !errorlevel! neq 0 (
                echo Failed to install deps with uv.
                pause
                exit /b 1
            )
        ) else (
            echo uv not found. Falling back to python -m venv and pip.
             if not exist "%VENV_DIR%\pyvenv.cfg" ( :: More reliable venv check
                echo Creating virtual environment using python -m venv.
                "%PYTHON_EXE%" -m venv "%VENV_DIR%"
                if !errorlevel! neq 0 (
                    echo Failed to create venv.
                    pause
                    exit /b 1
                )
            )
            echo Installing dependencies with pip...
            "%PYTHON_EXE%" -m pip install -r requirements.txt
            if !errorlevel! neq 0 (
                echo Failed to install deps.
                pause
                exit /b 1
            )
        )
    ) else (
        if not defined CONDA_DEFAULT_ENV (
             echo WARNING: Could not activate venv. Python from PATH will be used if available.
        )
    )
)


:: === Execute the Application ===
echo Using Python executable: %PYTHON_EXE%
echo Launching application: %PYTHON_EXE% launch.py %*
%PYTHON_EXE% launch.py %*

if %errorlevel% neq 0 (
    echo.
    echo The application exited with an error.
    pause
)

:: === Deactivation ===
if defined CONDA_ENV_ACTIVATED_BY_SCRIPT (
    echo Deactivating Conda environment...
    call conda deactivate
)
:: Venv deactivation from batch is tricky for PowerShell context as it runs in sub-shell.
:: For cmd.exe, deactivate.bat is called if venv was activated by script.
if defined VENV_ACTIVATED_BY_SCRIPT and not defined IS_POWERSHELL (
    if exist "%VENV_DIR%\Scripts\deactivate.bat" (
        echo Deactivating venv...
        call "%VENV_DIR%\Scripts\deactivate.bat"
    )
)

endlocal