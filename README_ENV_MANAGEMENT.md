# EmailIntelligence Python Environment Management

This document provides a summary of the Python Environment Management implementation for the EmailIntelligence project.

## Overview and Recommended Setup

The primary method for setting up and managing the Python environment for EmailIntelligence is through the main launcher script, `launch.py`. This script automates several key processes:

*   **Virtual Environment Creation**: Automatically creates a Python virtual environment (named `venv` by default) to isolate project dependencies.
*   **Dependency Installation**: Installs required Python packages from predefined requirements files.
*   **NLTK Data Download**: Ensures necessary NLTK (Natural Language Toolkit) data is available.
*   **Application Launching**: Serves as the main entry point to run the application, tests, and other utilities.

**Note on `setup_python.sh`:**
The shell script `scripts/setup_python.sh` is **DEPRECATED** and should no longer be used for environment setup. It is considered a **legacy script** and may be removed in future versions. **`launch.py` is the sole recommended and comprehensive tool for creating and managing the project's Python virtual environment and dependencies.** All users **must** prioritize using `launch.py` for a consistent and correct environment setup.

## Key Components Managed by `launch.py`

### 1. Unified Launcher System (`launch.py`)

`launch.py` is the central script for all environment and application management tasks. It handles:
- Command-line argument parsing.
- Orchestrating environment setup steps.
- Launching the application, backend, frontend, or tests.

*(Platform-specific launchers like `launch.bat` or `launch.sh` are thin wrappers that primarily invoke `python launch.py`)*

### 2. Environment Management (via `launch.py`)

`launch.py` directly manages the Python environment to ensure consistency:

- **Virtual Environment Management**:
    - Creates a virtual environment named `venv` in the project root if it doesn't exist (unless `--no-venv` is used).
    - Activates this venv for application execution.
- **Dependency Management Strategy**:
    - **Base Dependencies**:
        - `launch.py` first looks for `requirements_versions.txt`. If found, dependencies listed here (expected to be pinned versions) are installed.
        - If `requirements_versions.txt` is not found, it falls back to `requirements.txt` for base dependencies.
    - **Stage-Specific Dependencies**:
        - For `dev` stage (`--stage dev`): After base dependencies, packages from `requirements-dev.txt` are installed (if the file exists).
        - For `test` stage (`--stage test`): After base dependencies, packages from `requirements-test.txt` are installed (if the file exists).
    - The `--update-deps` flag forces an update (upgrade) of existing packages during installation.
- **Python Version Checking**: Ensures the Python version being used is within the supported range. Notably, `launch.py` now enforces the use of Python 3.11+ for the environment, aligning with the project's dependencies and configurations as specified in `pyproject.toml`.
- **NLTK Data Download**: Actively manages and automatically attempts to download required NLTK datasets (such as 'punkt', 'stopwords', 'wordnet') upon initial setup. If a download fails, an error will be logged. This can be skipped using the `--no-download-nltk` flag.
- **System Information**: The `--system-info` flag provides detailed diagnostics about the Python environment, OS, hardware, and project configuration.
- **Log Level Control**: The `--loglevel` flag allows users to set the verbosity of the launcher script (e.g., DEBUG, INFO, WARNING, ERROR).

**Behavior of `--no-venv`:**
If the `--no-venv` flag is used, `launch.py`:
1.  Will **not** create or use a virtual environment.
2.  Will **skip all Python dependency installation steps** (from `requirements.txt`, `requirements_versions.txt`, `requirements-dev.txt`, etc.).
Users who choose this option are fully responsible for ensuring their Python environment has all necessary dependencies installed and correctly configured. This option is generally intended for advanced users or specific deployment scenarios where manual environment management is preferred.

### 3. Extensions Framework

The extensions framework allows for modular enhancements to the application:

- **Extension Discovery**: Automatically discovers available extensions
- **Extension Lifecycle**: Handles loading, initialization, and shutdown of extensions
- **Extension Management**: Supports installing, updating, and uninstalling extensions
- **Configuration Management**: Provides configuration options for extensions

### 4. Models Management

The models management system handles machine learning models used by the application:

- **Model Download**: Downloads models from URLs
- **Model Verification**: Verifies model integrity using checksums
- **Model Configuration**: Manages configuration for different models
- **Model Lifecycle**: Handles loading and unloading of models

### 5. Application Execution

The application execution system runs the application in different modes and stages:

- **Development Mode**: Runs the application with hot-reloading for quick development
- **Testing Mode**: Runs the application in a testing environment
- **Staging Mode**: Runs the application in a staging environment
- **Production Mode**: Runs the application in a production environment

### 6. Testing Framework

The testing framework provides comprehensive testing capabilities:

- **Unit Testing**: Tests individual components
- **Integration Testing**: Tests component interactions
- **End-to-End Testing**: Tests the entire application
- **Performance Testing**: Tests application performance
- **Security Testing**: Tests application security

## Implementation Details

### Handling Complex Dependencies

While `launch.py` automates the installation of Python packages listed in the requirements files, some packages have more complex needs:

*   **Packages Requiring Compilation:**
    Some Python packages, like `scikit-learn`, include C extensions for performance. For most common operating systems and architectures, pre-compiled versions (binary wheels) are available and `pip` will install them automatically. However, if a compatible wheel is not available for your specific system (e.g., a less common Linux distribution, a new CPU architecture, or a very specific Python version), `pip` will attempt to compile the package from source. This compilation process requires system-level build tools.
    If you encounter errors during the installation of such packages, you may need to install these build tools. Common examples include:
    *   **Debian/Ubuntu Linux:** `sudo apt-get install build-essential python3-dev`
    *   **Fedora/RHEL Linux:** `sudo dnf groupinstall "Development Tools"` and `sudo dnf install python3-devel`
    *   **macOS:** Install Xcode Command Line Tools: `xcode-select --install`
    *   **Windows:** Install "Microsoft C++ Build Tools" from the Visual Studio Installer.

*   **Packages with Post-Install Downloads (e.g., `pyngrok`):**
    Some packages, like `pyngrok`, download additional binaries or data the first time they are run, rather than during the `pip install` process. For instance, `pyngrok` downloads the `ngrok` executable when you first attempt to create a tunnel (e.g., when using the `--share` flag in `launch.py`).
    `launch.py` facilitates the use of such packages. If `pyngrok` (or a similar package) fails to download its necessary components due to network issues or permissions, it will raise an error when its functionality is invoked, and `launch.py` will log this error. Ensure your system has internet connectivity and appropriate permissions for the package to save its components (usually within the Python environment's site-packages directory or a user-specific cache directory).

### Launcher Script Features (Relevant to Environment)

`launch.py` offers several command-line arguments to control its behavior regarding environment setup:

- **`--no-venv`**: Skips virtual environment creation/use and all Python dependency installations.
- **`--update-deps`**: Forces an update of dependencies during installation.
- **`--skip-python-version-check`**: Bypasses the Python version compatibility check.
- **`--no-download-nltk`**: Skips the automatic download of NLTK data.
- **`--system-info`**: Prints detailed system and environment information and exits.
- **`--loglevel {DEBUG,INFO,WARNING,ERROR,CRITICAL}`**: Sets the logging verbosity for the launcher.

*(For a full list of launcher arguments, see `LAUNCHER.md` or run `python launch.py --help`)*

<!-- The section below is intentionally commented out as env_manager.py no longer exists and its functionalities are integrated into launch.py -->
<!--
### Environment Manager Features (Legacy - Integrated into launch.py)

The functionality previously associated with a separate `env_manager.py` is now directly integrated into `launch.py`. These include:

- Python Version Checking
- Virtual Environment Creation (directory named `venv`)
- Dependency Installation (from `requirements_versions.txt`, `requirements.txt`, `requirements-dev.txt`, `requirements-test.txt`)
- System Information gathering
-->

### Extensions Framework Features

The extensions framework provides the following features:

- **Extension Discovery**: Automatically discovers available extensions
- **Extension Loading**: Loads extensions at runtime
- **Extension Initialization**: Initializes extensions with configuration
- **Extension Shutdown**: Properly shuts down extensions
- **Extension Management**: Installs, updates, and uninstalls extensions
- **Extension Configuration**: Manages configuration for extensions

### Models Management Features

The models management system provides the following features:

- **Model Download**: Downloads models from URLs
- **Model Verification**: Verifies model integrity using checksums
- **Model Configuration**: Manages configuration for different models
- **Model Listing**: Lists available models
- **Model Deletion**: Deletes models when no longer needed

### Application Execution Features

The application execution system provides the following features:

- **Development Mode**: Runs with hot-reloading for quick development
- **Testing Mode**: Runs in a testing environment
- **Staging Mode**: Runs in a staging environment
- **Production Mode**: Runs in a production environment
- **API-Only Mode**: Runs only the API server
- **Frontend-Only Mode**: Runs only the frontend

### Testing Framework Features

The testing framework provides the following features:

- **Unit Testing**: Tests individual components
- **Integration Testing**: Tests component interactions
- **End-to-End Testing**: Tests the entire application
- **Performance Testing**: Tests application performance
- **Security Testing**: Tests application security
- **Coverage Reporting**: Generates test coverage reports

## Usage Examples

### Setting up the environment and running in Development Mode

```bash
python launch.py --stage dev
```

### Running Tests

```bash
python launch.py --unit --coverage
```

### Managing Extensions

```bash
python launch.py --list-extensions
python launch.py --install-extension https://github.com/username/extension.git
python launch.py --create-extension my_extension
```

### Managing Models

```bash
python launch.py --list-models
python launch.py --download-model https://example.com/models/sentiment.zip --model-name sentiment
```

### System Information

```bash
python launch.py --system-info
```

### Running with a specific log level (e.g., debug)
```bash
python launch.py --loglevel DEBUG --stage dev
```

## Benefits of This Approach

1. **Consistency**: Ensures consistent environment and execution across different machines and stages
2. **Modularity**: Allows for easy extension and customization through the extension system
3. **Simplicity**: Provides a simple, unified interface for running the application
4. **Flexibility**: Supports different stages, modes, and configurations
5. **Maintainability**: Separates concerns into different modules for easier maintenance
6. **Testability**: Includes comprehensive testing support for different stages

## Extension System

The extension system allows for modular enhancements to the application. Extensions are discovered automatically and loaded at runtime. Each extension can provide additional functionality or modify existing functionality.

### Extension Structure

An extension consists of the following files:

- **Main Module**: Contains the extension code
- **Metadata File**: Contains information about the extension
- **README File**: Contains documentation for the extension
- **Requirements File**: Contains dependencies for the extension

### Extension Lifecycle

Extensions go through the following lifecycle:

1. **Discovery**: Extensions are discovered in the extensions directory
2. **Loading**: Extension modules are loaded into memory
3. **Initialization**: Extensions are initialized with configuration
4. **Execution**: Extensions provide functionality during application execution
5. **Shutdown**: Extensions are properly shut down when the application exits

### Creating Extensions

New extensions can be created using the `--create-extension` argument:

```bash
python launch.py --create-extension my_extension
```

This creates a template for a new extension with the necessary files.

## Conclusion

The environment management system, centered around `launch.py`, provides a robust and automated way to ensure consistent Python environments for the EmailIntelligence project. Users are encouraged to rely on `launch.py` for setup and execution.
This implementation integrates functionalities previously handled by separate modules, streamlining the process.