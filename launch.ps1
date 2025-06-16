# EmailIntelligence Launcher for PowerShell
# This script identifies a Python interpreter and executes launch.py.
# All environment setup (venv, dependencies) is handled by launch.py.

# Ensure launch.py exists
if (-not (Test-Path "launch.py")) {
    Write-Error "Error: launch.py not found in the current directory."
    exit 1
}

$PythonExecutable = ""
$PythonPrefixArgs = "" # For arguments like -3.11 for py.exe

# 1. Try py -3.11
$PyPath = Get-Command py -ErrorAction SilentlyContinue
if ($PyPath) {
    try {
        & py -3.11 --version *>$null # Suppress output, check exit code
        if ($LASTEXITCODE -eq 0) {
            $PythonExecutable = "py"
            $PythonPrefixArgs = "-3.11"
            Write-Host "Found py -3.11"
        }
    } catch {
        # py -3.11 might not be a valid version, or py.exe is misconfigured
        Write-Host "py -3.11 check failed or version not supported by py.exe."
    }
}

# 2. Fallback to python3.11
if (-not $PythonExecutable) {
    $Python311Path = Get-Command python3.11 -ErrorAction SilentlyContinue
    if ($Python311Path) {
        $PythonExecutable = "python3.11"
        Write-Host "Found python3.11"
    }
}

# 3. Fallback to python
if (-not $PythonExecutable) {
    $PythonPath = Get-Command python -ErrorAction SilentlyContinue
    if ($PythonPath) {
        # Further check if this 'python' is Python 3. We can't be certain it's 3.11 here.
        # launch.py itself will re-execute if this python is not 3.11.
        $PythonExecutable = "python"
        Write-Host "Found python"
    }
}

if (-not $PythonExecutable) {
    Write-Error "Error: Python (3.11 recommended) not found in PATH."
    Write-Error "Please install Python 3.11 and ensure it's accessible via 'py -3.11', 'python3.11', or 'python'."
    # Read-Host "Press Enter to exit..." # Consider for interactive sessions
    exit 1
}

Write-Host "Using Python interpreter: $PythonExecutable $PythonPrefixArgs"
if ($PythonPrefixArgs) {
    & $PythonExecutable $PythonPrefixArgs launch.py $args
} else {
    & $PythonExecutable launch.py $args
}

$ExitCode = $LASTEXITCODE
if ($ExitCode -ne 0) {
    Write-Host ""
    Write-Host "The application exited with error code: $ExitCode."
    # Read-Host "Press Enter to continue..." # Consider for interactive sessions
}

exit $ExitCode
