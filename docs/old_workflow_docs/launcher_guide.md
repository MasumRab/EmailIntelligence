<<<<<<< HEAD:docs/old_workflow_docs/launcher_guide.md
# EmailIntelligence Launcher

The EmailIntelligence Launcher is a unified way to run the EmailIntelligence application with automatic environment setup, dependency management, and configuration.

## Quick Start

### Cross-Platform

1. Run the setup command:
```bash
python launch.py --setup
```

2. Start the application:
```bash
python launch.py --stage dev
```

### Convenience Wrappers

- **Windows**: `launch.bat --stage dev`
- **Linux/macOS**: `./launch.sh --stage dev`

## Features

- **Automatic Environment Setup**: Creates a virtual environment and installs dependencies automatically.
- **Conda Environment Support**: Automatically detects and uses conda environments when available, with fallback to venv.
- **Multiple Stages**: Supports development and testing environments.
- **Extensions Support**: Install, update, and manage extensions.
- **Model Management**: Download, verify, and manage machine learning models.
- **Testing Framework**: Run unit tests, integration tests, and end-to-end tests.
- **Flexible Configuration**: Configure the application through command-line arguments or environment variables.

## Command-Line Arguments

### Environment Setup

- `--setup`: Run environment setup.
- `--force-recreate-venv`: Force recreation of the venv.

- `--use-conda`: Use Conda environment instead of venv.
- `--conda-env NAME`: Conda environment name to use (default: base).
- `--no-venv`: Don't create or use a virtual environment.
- `--update-deps`: Update dependencies before launching.
- `--skip-torch-cuda-test`: Skip CUDA availability test for PyTorch.
- `--reinstall-torch`: Reinstall PyTorch.
- `--skip-python-version-check`: Skip Python version check.
- `--no-download-nltk`: Skip downloading NLTK data.
- `--skip-prepare`: Skip all environment preparation steps.
- `--loglevel {DEBUG,INFO,WARNING,ERROR,CRITICAL}`: Set the logging level. Default is INFO.

### Application Stage

- `--stage {dev,test}`: Specify the application mode.
  - `dev`: For running the application (backend/frontend). (Default)
  - `test`: For running tests.

### Server Configuration

- `--port PORT`: Specify the port to run on (default: 8000)
- `--host HOST`: Specify the host to run on (default: 127.0.0.1)
- `--frontend-port PORT`: Specify the frontend port to run on (default: 5173)
- `--api-url URL`: Specify the API URL for the frontend
- `--api-only`: Run only the API server without the frontend
- `--frontend-only`: Run only the frontend without the API server
- `--debug`: Enable debug mode

### Testing Options

- `--coverage`: Generate coverage report when running tests
- `--unit`: Run unit tests
- `--integration`: Run integration tests
- `--e2e`: Run end-to-end tests
- `--performance`: Run performance tests
- `--security`: Run security tests

### Extensions and Models

- `--skip-extensions`: Skip loading extensions
- `--skip-models`: Skip downloading models
- `--install-extension URL`: Install an extension from a Git repository
- `--uninstall-extension NAME`: Uninstall an extension
- `--update-extension NAME`: Update an extension
- `--list-extensions`: List all extensions
- `--create-extension NAME`: Create a new extension template
- `--download-model URL`: Download a model from a URL
- `--model-name NAME`: Specify the model name for download
- `--list-models`: List all models
- `--delete-model NAME`: Delete a model

### Advanced Options

- `--no-half`: Disable half-precision for models
- `--force-cpu`: Force CPU mode even if GPU is available
- `--low-memory`: Enable low memory mode
- `--system-info`: Print detailed system, Python, and project configuration information then exit.

### Networking Options

- `--share`: Create a public URL
- `--listen`: Make the server listen on network
- `--ngrok REGION`: Use ngrok to create a tunnel, specify ngrok region

### Environment Configuration

- `--env-file FILE`: Specify a custom .env file

## Examples

### Running in Development Mode

```
python launch.py --stage dev
```

### Running Only the API Server

```
python launch.py --api-only
```

### Running Only the Frontend

```
python launch.py --frontend-only
```

### Running Tests

```
python launch.py --unit --coverage
```

### Installing an Extension

```
python launch.py --install-extension https://github.com/username/extension.git
```

### Listing Models

```
python launch.py --list-models
```

### Printing System Information

```
python launch.py --system-info
```

## Directory Structure

- `deployment/`: Contains scripts and modules used by `launch.py` for specific tasks like extension management (`extensions_manager.py`), model management (`models_manager.py`), and test execution (`test_stages.py`).
- `backend/extensions/`: Contains installed extensions.
- `models/`: Contains downloaded models.
- `venv/`: Contains the Python virtual environment created by `launch.py` (unless `--no-venv` is used).

## Creating Extensions

You can create a new extension template using the `--create-extension` argument:

```
python launch.py --create-extension my_extension
```

This will create a new extension template in the `backend/extensions/my_extension` directory with the following structure:

- `my_extension.py`: The main extension module
- `metadata.json`: Extension metadata
- `README.md`: Extension documentation
- `requirements.txt`: Extension dependencies

## Customizing the Launcher

You can customize the launcher by modifying the following files:

- `launch.py`: The main launcher script, which now integrates environment management.
- `deployment/test_stages.py`: Manages testing for different stages.

## Troubleshooting

### Virtual Environment Issues

If you encounter issues with the virtual environment (e.g., creation failures), you can try running with the `--no-venv` argument. Remember that this makes you responsible for installing all Python dependencies:

```
python launch.py --no-venv
```

### Conda Environment Issues

The launcher automatically detects and uses conda environments. If you want to use a specific conda environment:

```
python launch.py --conda-env myenv
```

If conda is not available or you prefer not to use it, the launcher will fall back to using venv or system Python.

### Dependency Issues

If you encounter issues with dependencies, try updating them:

```
python launch.py --update-deps
```

### PyTorch CUDA Issues

If you encounter issues with PyTorch CUDA, try reinstalling PyTorch:

```
python launch.py --reinstall-torch
```

### Other Issues

If you encounter other issues, try running with the `--debug` argument:

```
python launch.py --debug
```

Or check the system information:

```
python launch.py --system-info
```
=======
>>>>>>> scientific:docs/launcher_guide.md
