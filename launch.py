#!/usr/bin/env python3
"""
EmailIntelligence Launcher

This script provides a unified way to launch the EmailIntelligence application
with automatic environment setup, dependency management, and configuration.
It's inspired by the approach used in projects like Stable Diffusion WebUI.

Usage:
    python launch.py [arguments]

Arguments:
    --help                      Show this help message
    --no-venv                   Don't create or use a virtual environment
    --update-deps               Update dependencies before launching
    --skip-torch-cuda-test      Skip CUDA availability test for PyTorch
    --reinstall-torch           Reinstall PyTorch (useful for CUDA issues)
    --skip-python-version-check Skip Python version check
    --stage {dev,test,staging,prod}  Specify the application stage to run
    --port PORT                 Specify the port to run on (default: 8000)
    --host HOST                 Specify the host to run on (default: 127.0.0.1)
    --api-only                  Run only the API server without the frontend
    --frontend-only             Run only the frontend without the API server
    --debug                     Enable debug mode
    --no-download-nltk          Skip downloading NLTK data
    --skip-prepare              Skip preparation steps
    --skip-extensions           Skip loading extensions
    --no-half                   Disable half-precision for models
    --force-cpu                 Force CPU mode even if GPU is available
    --low-memory                Enable low memory mode
    --share                     Create a public URL
    --listen                    Make the server listen on network
    --ngrok NGROK               Use ngrok to create a tunnel, specify ngrok region
    --env-file FILE             Specify a custom .env file
"""

import os
import sys
import platform
import subprocess
import argparse
import shutil
import venv
import logging
import json
import time
import signal
import pkg_resources
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple, Union

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("launcher")

# Constants
PYTHON_MIN_VERSION = (3, 8)
PYTHON_MAX_VERSION = (3, 11)
VENV_DIR = "venv"
REQUIREMENTS_FILE = "requirements.txt"
TORCH_CUDA_REQUIRED = False  # Set to True if CUDA is required

# Project root directory
ROOT_DIR = Path(__file__).resolve().parent

def check_python_version() -> bool:
    """Check if the Python version is supported."""
    current_version = sys.version_info[:2]
    if current_version < PYTHON_MIN_VERSION:
        logger.error(f"Python {'.'.join(map(str, PYTHON_MIN_VERSION))} or higher is required")
        return False
    if current_version > PYTHON_MAX_VERSION:
        logger.warning(f"Python {'.'.join(map(str, current_version))} is not officially supported. "
                      f"Recommended version is {'.'.join(map(str, PYTHON_MAX_VERSION))} or lower.")
    return True

def is_venv_available() -> bool:
    """Check if a virtual environment is available."""
    venv_path = ROOT_DIR / VENV_DIR
    return venv_path.exists() and (venv_path / "Scripts" / "python.exe").exists() if os.name == 'nt' else \
           (venv_path / "bin" / "python").exists()

def create_venv() -> bool:
    """Create a virtual environment."""
    venv_path = ROOT_DIR / VENV_DIR
    if venv_path.exists():
        logger.info(f"Virtual environment already exists at {venv_path}")
        return True
    
    logger.info(f"Creating virtual environment at {venv_path}")
    try:
        venv.create(venv_path, with_pip=True)
        return True
    except Exception as e:
        logger.error(f"Failed to create virtual environment: {e}")
        return False

def get_python_executable() -> str:
    """Get the Python executable path."""
    if is_venv_available():
        if os.name == 'nt':
            return str(ROOT_DIR / VENV_DIR / "Scripts" / "python.exe")
        else:
            return str(ROOT_DIR / VENV_DIR / "bin" / "python")
    return sys.executable

def install_dependencies(update: bool = False) -> bool:
    """Install or update dependencies."""
    python = get_python_executable()
    requirements_path = ROOT_DIR / REQUIREMENTS_FILE
    
    if not requirements_path.exists():
        logger.error(f"Requirements file not found at {requirements_path}")
        return False
    
    cmd = [python, "-m", "pip", "install"]
    if update:
        cmd.append("--upgrade")
    cmd.extend(["-r", str(requirements_path)])
    
    logger.info(f"{'Updating' if update else 'Installing'} dependencies...")
    try:
        subprocess.check_call(cmd)
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to install dependencies: {e}")
        return False

def check_torch_cuda() -> bool:
    """Check if PyTorch with CUDA is available."""
    python = get_python_executable()
    
    try:
        result = subprocess.run(
            [python, "-c", "import torch; print(torch.cuda.is_available())"],
            capture_output=True,
            text=True,
            check=True
        )
        is_available = result.stdout.strip() == "True"
        logger.info(f"PyTorch CUDA is {'available' if is_available else 'not available'}")
        return is_available
    except subprocess.CalledProcessError:
        logger.warning("Failed to check PyTorch CUDA availability")
        return False

def reinstall_torch() -> bool:
    """Reinstall PyTorch with CUDA support."""
    python = get_python_executable()
    
    # Uninstall existing PyTorch
    logger.info("Uninstalling existing PyTorch...")
    subprocess.run([python, "-m", "pip", "uninstall", "-y", "torch", "torchvision", "torchaudio"])
    
    # Install PyTorch with CUDA support
    logger.info("Installing PyTorch with CUDA support...")
    if os.name == 'nt':  # Windows
        cmd = f"{python} -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118"
    else:  # Linux/MacOS
        cmd = f"{python} -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118"
    
    try:
        subprocess.check_call(cmd, shell=True)
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to reinstall PyTorch: {e}")
        return False

def download_nltk_data() -> bool:
    """Download NLTK data."""
    python = get_python_executable()
    
    logger.info("Downloading NLTK data...")
    try:
        subprocess.check_call([
            python, "-c", 
            "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet')"
        ])
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to download NLTK data: {e}")
        return False

def prepare_environment(args: argparse.Namespace) -> bool:
    """Prepare the environment for running the application."""
    # Import environment manager
    from deployment.env_manager import env_manager
    
    # Check Python version
    if not args.skip_python_version_check and not env_manager.check_python_version():
        return False
    
    # Create virtual environment if needed
    if not args.no_venv and not env_manager.is_venv_available() and not env_manager.create_venv():
        return False
    
    # Install dependencies for the specified stage
    if not args.no_venv and not env_manager.setup_environment_for_stage(args.stage, args.update_deps):
        return False
    
    # Check PyTorch CUDA
    if TORCH_CUDA_REQUIRED and not args.skip_torch_cuda_test:
        # Get system info to check CUDA availability
        system_info = env_manager.get_system_info()
        if not system_info["cuda_available"]:
            if args.reinstall_torch:
                # Reinstall PyTorch with CUDA support
                env_manager.uninstall_package("torch")
                env_manager.uninstall_package("torchvision")
                env_manager.uninstall_package("torchaudio")
                
                if os.name == 'nt':  # Windows
                    env_manager.install_package("torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118")
                else:  # Linux/MacOS
                    env_manager.install_package("torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118")
            else:
                logger.warning("PyTorch CUDA is not available. Use --reinstall-torch to reinstall with CUDA support.")
    
    # Download NLTK data
    if not args.no_download_nltk:
        python = env_manager.get_python_executable()
        try:
            subprocess.check_call([
                python, "-c", 
                "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet')"
            ])
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to download NLTK data: {e}")
            return False
    
    # Load extensions if not skipped
    if not args.skip_extensions:
        from deployment.extensions import extensions_manager
        extensions_manager.load_extensions()
        extensions_manager.initialize_extensions()
    
    # Download models if needed
    if not args.skip_models:
        from deployment.models import models_manager
        if not models_manager.list_models():
            logger.info("No models found. Downloading default models...")
            models_manager.download_default_models()
    
    return True

def run_application(args: argparse.Namespace) -> int:
    """Run the application with the specified arguments."""
    # Import run application module
    from deployment.run_app import run_app
    
    # Set up environment variables
    env = {}
    if args.env_file:
        env_file = Path(args.env_file)
        if env_file.exists():
            logger.info(f"Loading environment variables from {env_file}")
            with open(env_file, "r") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        key, value = line.split("=", 1)
                        env[key] = value
    
    # Run the application in the specified mode
    if args.api_only:
        return 0 if run_app.run_api_only(args.host, args.port, args.debug, args.stage) else 1
    elif args.frontend_only:
        return 0 if run_app.run_frontend_only(args.host, args.frontend_port, args.api_url, args.stage) else 1
    elif args.stage == "dev":
        return 0 if run_app.run_dev_mode(args.host, args.port, args.frontend_port, args.debug) else 1
    elif args.stage == "test":
        # Import test stages module
        from deployment.test_stages import test_stages
        return 0 if test_stages.run_tests_for_stage(args.stage, args.coverage, args.debug) else 1
    elif args.stage == "staging":
        return 0 if run_app.run_staging_mode() else 1
    elif args.stage == "prod":
        return 0 if run_app.run_production_mode() else 1
    else:
        logger.error(f"Unknown stage: {args.stage}")
        return 1

def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="EmailIntelligence Launcher")
    
    # Environment setup arguments
    parser.add_argument("--no-venv", action="store_true", help="Don't create or use a virtual environment")
    parser.add_argument("--update-deps", action="store_true", help="Update dependencies before launching")
    parser.add_argument("--skip-torch-cuda-test", action="store_true", help="Skip CUDA availability test for PyTorch")
    parser.add_argument("--reinstall-torch", action="store_true", help="Reinstall PyTorch (useful for CUDA issues)")
    parser.add_argument("--skip-python-version-check", action="store_true", help="Skip Python version check")
    parser.add_argument("--no-download-nltk", action="store_true", help="Skip downloading NLTK data")
    parser.add_argument("--skip-prepare", action="store_true", help="Skip preparation steps")
    
    # Application stage
    parser.add_argument("--stage", choices=["dev", "test", "staging", "prod"], default="dev",
                        help="Specify the application stage to run")
    
    # Server configuration
    parser.add_argument("--port", type=int, default=8000, help="Specify the port to run on (default: 8000)")
    parser.add_argument("--host", type=str, default="127.0.0.1", help="Specify the host to run on (default: 127.0.0.1)")
    parser.add_argument("--frontend-port", type=int, default=5173, help="Specify the frontend port to run on (default: 5173)")
    parser.add_argument("--api-url", type=str, help="Specify the API URL for the frontend")
    parser.add_argument("--api-only", action="store_true", help="Run only the API server without the frontend")
    parser.add_argument("--frontend-only", action="store_true", help="Run only the frontend without the API server")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    
    # Testing options
    parser.add_argument("--coverage", action="store_true", help="Generate coverage report when running tests")
    parser.add_argument("--unit", action="store_true", help="Run unit tests")
    parser.add_argument("--integration", action="store_true", help="Run integration tests")
    parser.add_argument("--e2e", action="store_true", help="Run end-to-end tests")
    parser.add_argument("--performance", action="store_true", help="Run performance tests")
    parser.add_argument("--security", action="store_true", help="Run security tests")
    
    # Extensions and models
    parser.add_argument("--skip-extensions", action="store_true", help="Skip loading extensions")
    parser.add_argument("--skip-models", action="store_true", help="Skip downloading models")
    parser.add_argument("--install-extension", type=str, help="Install an extension from a Git repository")
    parser.add_argument("--uninstall-extension", type=str, help="Uninstall an extension")
    parser.add_argument("--update-extension", type=str, help="Update an extension")
    parser.add_argument("--list-extensions", action="store_true", help="List all extensions")
    parser.add_argument("--create-extension", type=str, help="Create a new extension template")
    
    # Model options
    parser.add_argument("--download-model", type=str, help="Download a model from a URL")
    parser.add_argument("--model-name", type=str, help="Specify the model name for download")
    parser.add_argument("--list-models", action="store_true", help="List all models")
    parser.add_argument("--delete-model", type=str, help="Delete a model")
    
    # Advanced options
    parser.add_argument("--no-half", action="store_true", help="Disable half-precision for models")
    parser.add_argument("--force-cpu", action="store_true", help="Force CPU mode even if GPU is available")
    parser.add_argument("--low-memory", action="store_true", help="Enable low memory mode")
    parser.add_argument("--system-info", action="store_true", help="Print system information")
    
    # Networking options
    parser.add_argument("--share", action="store_true", help="Create a public URL")
    parser.add_argument("--listen", action="store_true", help="Make the server listen on network")
    parser.add_argument("--ngrok", type=str, help="Use ngrok to create a tunnel, specify ngrok region")
    
    # Environment configuration
    parser.add_argument("--env-file", type=str, help="Specify a custom .env file")
    
    return parser.parse_args()

def main() -> int:
    """Main entry point."""
    # Parse arguments
    args = parse_arguments()
    
    # Handle special commands
    
    # System information
    if args.system_info:
        from deployment.env_manager import env_manager
        env_manager.print_system_info()
        return 0
    
    # Extensions management
    if args.list_extensions:
        from deployment.extensions import extensions_manager
        extensions_manager.load_extensions()
        extensions = extensions_manager.list_extensions()
        
        print(f"Found {len(extensions)} extensions:")
        for extension in extensions:
            print(f"  {extension['name']} - {'Enabled' if extension['enabled'] else 'Disabled'}")
            print(f"    Path: {extension['path']}")
            print(f"    Loaded: {extension['loaded']}")
            print(f"    Description: {extension['metadata'].get('description', 'No description')}")
            print()
        
        return 0
    
    if args.install_extension:
        from deployment.extensions import extensions_manager
        success = extensions_manager.install_extension(args.install_extension)
        return 0 if success else 1
    
    if args.uninstall_extension:
        from deployment.extensions import extensions_manager
        success = extensions_manager.uninstall_extension(args.uninstall_extension)
        return 0 if success else 1
    
    if args.update_extension:
        from deployment.extensions import extensions_manager
        success = extensions_manager.update_extension(args.update_extension)
        return 0 if success else 1
    
    if args.create_extension:
        from deployment.extensions import extensions_manager
        success = extensions_manager.create_extension_template(args.create_extension)
        return 0 if success else 1
    
    # Models management
    if args.list_models:
        from deployment.models import models_manager
        models = models_manager.list_models()
        
        print(f"Found {len(models)} models:")
        for model in models:
            print(f"  {model}")
            
            # Print the model configuration if available
            config = models_manager.get_model_config(model)
            if config:
                print(f"    Configuration:")
                for key, value in config.items():
                    print(f"      {key}: {value}")
            
            print()
        
        return 0
    
    if args.download_model and args.model_name:
        from deployment.models import models_manager
        success = models_manager.download_model(args.download_model, args.model_name)
        return 0 if success else 1
    
    if args.delete_model:
        from deployment.models import models_manager
        success = models_manager.delete_model(args.delete_model)
        return 0 if success else 1
    
    # Testing options
    if args.unit or args.integration or args.e2e or args.performance or args.security:
        from deployment.test_stages import test_stages
        
        success = True
        
        if args.unit:
            success = test_stages.run_unit_tests(args.coverage, args.debug) and success
        
        if args.integration:
            success = test_stages.run_integration_tests(args.coverage, args.debug) and success
        
        if args.e2e:
            success = test_stages.run_e2e_tests(True, args.debug) and success
        
        if args.performance:
            success = test_stages.run_performance_tests(60, 10, args.debug) and success
        
        if args.security:
            success = test_stages.run_security_tests(f"http://{args.host}:{args.port}", args.debug) and success
        
        return 0 if success else 1
    
    # Prepare environment
    if not args.skip_prepare and not prepare_environment(args):
        return 1
    
    # Run application
    return run_application(args)

if __name__ == "__main__":
    sys.exit(main())