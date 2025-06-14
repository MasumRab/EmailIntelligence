# === Configuration ===
# Specify your project's Conda environment name here if applicable
$PROJECT_CONDA_ENV_NAME = "base"
# Specify your project's venv directory name
$VENV_DIR = "venv"

# === Conda Environment Handling ===
$CONDA_ENV_ACTIVATED_BY_SCRIPT = $false
$VENV_ACTIVATED_BY_SCRIPT = $false
$PYTHON_EXE = "python"

# Check if Conda is available
$condaAvailable = $null -ne (Get-Command conda -ErrorAction SilentlyContinue)
if ($condaAvailable) {
    Write-Host "Conda is available."
    
    if ($PROJECT_CONDA_ENV_NAME -eq "base") {
        Write-Host "INFO: Project specific Conda environment name is set to the default 'base'."
        Write-Host "This script will not attempt to activate or create a specific Conda environment."
        Write-Host "If you wish to use a project-specific Conda environment, please edit this script"
        Write-Host "and set PROJECT_CONDA_ENV_NAME to your desired environment name."
        Write-Host "Falling back to checking for an existing active Conda environment or using standard venv."
    }
    
    # Check if already in a Conda environment
    if ($env:CONDA_DEFAULT_ENV) {
        Write-Host "Already in a Conda environment: $env:CONDA_DEFAULT_ENV"
        $PYTHON_EXE = Join-Path $env:CONDA_PREFIX "python.exe"
        Write-Host "Using Python from active Conda env: $PYTHON_EXE"
        
        if ($env:CONDA_DEFAULT_ENV -eq $PROJECT_CONDA_ENV_NAME) {
            Write-Host "Current Conda environment matches project environment. Using it."
        } else {
            if ($PROJECT_CONDA_ENV_NAME -ne "base") {
                Write-Host "Current Conda environment ($env:CONDA_DEFAULT_ENV) does not match project specific one ($PROJECT_CONDA_ENV_NAME)."
                Write-Host "Attempting to activate project Conda environment: $PROJECT_CONDA_ENV_NAME"
                
                try {
                    # In PowerShell, we need to use conda-hook to properly activate environments
                    & conda activate $PROJECT_CONDA_ENV_NAME
                    if ($LASTEXITCODE -eq 0) {
                        Write-Host "Successfully activated Conda environment: $PROJECT_CONDA_ENV_NAME"
                        $CONDA_ENV_ACTIVATED_BY_SCRIPT = $true
                        $PYTHON_EXE = Join-Path $env:CONDA_PREFIX "python.exe"
                        Write-Host "Using Python from newly activated Conda env: $PYTHON_EXE"
                    } else {
                        Write-Host "WARNING: Failed to activate Conda environment: $PROJECT_CONDA_ENV_NAME. Will use current Conda env: $env:CONDA_DEFAULT_ENV."
                        Write-Host "Please ensure it exists and Conda is configured correctly."
                    }
                } catch {
                    Write-Host "WARNING: Failed to activate Conda environment: $PROJECT_CONDA_ENV_NAME. Will use current Conda env: $env:CONDA_DEFAULT_ENV."
                    Write-Host "Please ensure it exists and Conda is configured correctly."
                }
            }
        }
    } else {
        if ($PROJECT_CONDA_ENV_NAME -ne "base") {
            Write-Host "Not in a Conda environment. Attempting to activate project Conda environment: $PROJECT_CONDA_ENV_NAME"
            
            try {
                & conda activate $PROJECT_CONDA_ENV_NAME
                if ($LASTEXITCODE -eq 0) {
                    Write-Host "Successfully activated Conda environment: $PROJECT_CONDA_ENV_NAME"
                    $CONDA_ENV_ACTIVATED_BY_SCRIPT = $true
                    $PYTHON_EXE = Join-Path $env:CONDA_PREFIX "python.exe"
                    Write-Host "Using Python from Conda env: $PYTHON_EXE"
                } else {
                    Write-Host "WARNING: Failed to activate Conda environment: $PROJECT_CONDA_ENV_NAME."
                    Write-Host "Attempting to create the Conda environment..."
                    
                    & conda create -n $PROJECT_CONDA_ENV_NAME python=3.9 -y
                    if ($LASTEXITCODE -eq 0) {
                        Write-Host "Successfully created Conda environment: $PROJECT_CONDA_ENV_NAME."
                        Write-Host "Attempting to activate the newly created environment..."
                        
                        & conda activate $PROJECT_CONDA_ENV_NAME
                        if ($LASTEXITCODE -eq 0) {
                            $CONDA_ENV_ACTIVATED_BY_SCRIPT = $true
                            $PYTHON_EXE = Join-Path $env:CONDA_PREFIX "python.exe"
                            Write-Host "Successfully activated newly created Conda environment: $PROJECT_CONDA_ENV_NAME"
                            Write-Host "Using Python from Conda env: $PYTHON_EXE"
                        } else {
                            Write-Host "WARNING: Failed to activate newly created Conda environment: $PROJECT_CONDA_ENV_NAME."
                            Write-Host "Falling back to standard venv."
                        }
                    } else {
                        Write-Host "WARNING: Failed to create Conda environment: $PROJECT_CONDA_ENV_NAME."
                        Write-Host "It might not exist or Conda needs setup."
                        Write-Host "Falling back to standard venv."
                    }
                }
            } catch {
                Write-Host "WARNING: Error occurred while working with Conda environment: $_"
                Write-Host "Falling back to standard venv."
            }
        }
    }
} else {
    Write-Host "Conda is not available or not in PATH."
}

# === Standard Venv Handling (if no Conda environment is active or activated by script) ===
if (-not $env:CONDA_DEFAULT_ENV -and -not $CONDA_ENV_ACTIVATED_BY_SCRIPT) {
    Write-Host "Proceeding with standard venv setup."
    
    $pythonAvailable = $null -ne (Get-Command python -ErrorAction SilentlyContinue)
    if (-not $pythonAvailable) {
        $venvPythonPath = Join-Path $VENV_DIR "Scripts\python.exe"
        if (-not (Test-Path $venvPythonPath)) {
            Write-Host "Python is not installed, not in PATH, and no venv Python found. Please install Python 3.8 or higher."
            Read-Host "Press Enter to exit"
            exit 1
        }
    }
    
    $activatePs1Path = Join-Path $VENV_DIR "Scripts\Activate.ps1"
    if (Test-Path $activatePs1Path) {
        Write-Host "Activating venv for PowerShell..."
        try {
            & $activatePs1Path
            $VENV_ACTIVATED_BY_SCRIPT = $true
            $PYTHON_EXE = Join-Path (Get-Location) "$VENV_DIR\Scripts\python.exe"
            Write-Host "PowerShell venv activation successful."
        } catch {
            Write-Host "PowerShell venv activation failed: $_"
        }
    } else {
        Write-Host "$activatePs1Path not found. Cannot activate for PowerShell."
    }
    
    # Create venv and install dependencies if not already in an active Conda environment
    # And if venv activation (or attempt) was made
    if ($VENV_ACTIVATED_BY_SCRIPT) {
        $uvAvailable = $null -ne (Get-Command uv -ErrorAction SilentlyContinue)
        if ($uvAvailable) {
            Write-Host "uv is installed. Using uv."
            $pyvenvCfgPath = Join-Path $VENV_DIR "pyvenv.cfg"
            if (-not (Test-Path $pyvenvCfgPath)) {
                Write-Host "Creating virtual environment using uv..."
                & uv venv $VENV_DIR --python $PYTHON_EXE
                if ($LASTEXITCODE -ne 0) {
                    Write-Host "Failed to create venv with uv."
                    Read-Host "Press Enter to exit"
                    exit 1
                }
            }
            Write-Host "Installing dependencies with uv..."
            & uv pip install -r requirements.txt
            if ($LASTEXITCODE -ne 0) {
                Write-Host "Failed to install deps with uv."
                Read-Host "Press Enter to exit"
                exit 1
            }
        } else {
            Write-Host "uv not found. Falling back to python -m venv and pip."
            $pyvenvCfgPath = Join-Path $VENV_DIR "pyvenv.cfg"
            if (-not (Test-Path $pyvenvCfgPath)) {
                Write-Host "Creating virtual environment using python -m venv."
                & $PYTHON_EXE -m venv $VENV_DIR
                if ($LASTEXITCODE -ne 0) {
                    Write-Host "Failed to create venv."
                    Read-Host "Press Enter to exit"
                    exit 1
                }
            }
            Write-Host "Installing dependencies with pip..."
            & $PYTHON_EXE -m pip install -r requirements.txt
            if ($LASTEXITCODE -ne 0) {
                Write-Host "Failed to install deps."
                Read-Host "Press Enter to exit"
                exit 1
            }
        }
    } else {
        if (-not $env:CONDA_DEFAULT_ENV) {
            Write-Host "WARNING: Could not activate venv. Python from PATH will be used if available."
        }
    }
}

# === Execute the Application ===
Write-Host "Using Python executable: $PYTHON_EXE"
Write-Host "Launching application: $PYTHON_EXE launch.py $args"
& $PYTHON_EXE launch.py $args

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "The application exited with an error."
    Read-Host "Press Enter to continue"
}

# === Deactivation ===
# Note: In PowerShell, environment changes persist after the script ends,
# so we don't need to explicitly deactivate environments.
# The user can manually run 'conda deactivate' or 'deactivate' if needed.