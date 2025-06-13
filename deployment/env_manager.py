#!/usr/bin/env python3
"""
Environment Manager for EmailIntelligence

This module provides functions for managing the Python environment,
including virtual environment creation, dependency management,
and environment configuration.
"""

import os
import sys
import subprocess
import logging
import venv
import pkg_resources
import platform
import json
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple, Union

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("env-manager")

# Constants
PYTHON_MIN_VERSION = (3, 8)
PYTHON_MAX_VERSION = (3, 11)
VENV_DIR = "venv"
REQUIREMENTS_FILE = "requirements.txt"
DEV_REQUIREMENTS_FILE = "requirements-dev.txt"
TEST_REQUIREMENTS_FILE = "requirements-test.txt"

# Project root directory
ROOT_DIR = Path(__file__).resolve().parent.parent

class EnvironmentManager:
    """Manages the Python environment for EmailIntelligence."""
    
    def __init__(self, root_dir: Path = ROOT_DIR):
        """Initialize the environment manager."""
        self.root_dir = root_dir
        self.venv_dir = root_dir / VENV_DIR
    
    def check_python_version(self) -> bool:
        """Check if the Python version is supported."""
        current_version = sys.version_info[:2]
        if current_version < PYTHON_MIN_VERSION:
            logger.error(f"Python {'.'.join(map(str, PYTHON_MIN_VERSION))} or higher is required")
            return False
        if current_version > PYTHON_MAX_VERSION:
            logger.warning(f"Python {'.'.join(map(str, current_version))} is not officially supported. "
                          f"Recommended version is {'.'.join(map(str, PYTHON_MAX_VERSION))} or lower.")
        return True
    
    def is_venv_available(self) -> bool:
        """Check if a virtual environment is available."""
        if os.name == 'nt':  # Windows
            return self.venv_dir.exists() and (self.venv_dir / "Scripts" / "python.exe").exists()
        else:  # Unix-based systems
            return self.venv_dir.exists() and (self.venv_dir / "bin" / "python").exists()
    
    def create_venv(self) -> bool:
        """Create a virtual environment."""
        if self.venv_dir.exists():
            logger.info(f"Virtual environment already exists at {self.venv_dir}")
            return True
        
        logger.info(f"Creating virtual environment at {self.venv_dir}")
        try:
            venv.create(self.venv_dir, with_pip=True)
            return True
        except Exception as e:
            logger.error(f"Failed to create virtual environment: {e}")
            return False
    
    def get_python_executable(self) -> str:
        """Get the Python executable path."""
        if self.is_venv_available():
            if os.name == 'nt':  # Windows
                return str(self.venv_dir / "Scripts" / "python.exe")
            else:  # Unix-based systems
                return str(self.venv_dir / "bin" / "python")
        return sys.executable
    
    def install_requirements(self, requirements_file: str = REQUIREMENTS_FILE, update: bool = False) -> bool:
        """Install or update requirements from a file."""
        python = self.get_python_executable()
        requirements_path = self.root_dir / requirements_file
        
        if not requirements_path.exists():
            logger.error(f"Requirements file not found at {requirements_path}")
            return False
        
        cmd = [python, "-m", "pip", "install"]
        if update:
            cmd.append("--upgrade")
        cmd.extend(["-r", str(requirements_path)])
        
        logger.info(f"{'Updating' if update else 'Installing'} dependencies from {requirements_file}...")
        try:
            subprocess.check_call(cmd)
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to install dependencies: {e}")
            return False
    
    def install_package(self, package: str, version: Optional[str] = None, update: bool = False) -> bool:
        """Install or update a specific package."""
        python = self.get_python_executable()
        
        package_spec = package
        if version:
            package_spec = f"{package}=={version}"
        
        cmd = [python, "-m", "pip", "install"]
        if update:
            cmd.append("--upgrade")
        cmd.append(package_spec)
        
        logger.info(f"{'Updating' if update else 'Installing'} package {package_spec}...")
        try:
            subprocess.check_call(cmd)
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to install package {package_spec}: {e}")
            return False
    
    def uninstall_package(self, package: str) -> bool:
        """Uninstall a specific package."""
        python = self.get_python_executable()
        
        cmd = [python, "-m", "pip", "uninstall", "-y", package]
        
        logger.info(f"Uninstalling package {package}...")
        try:
            subprocess.check_call(cmd)
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to uninstall package {package}: {e}")
            return False
    
    def list_installed_packages(self) -> List[str]:
        """List all installed packages."""
        python = self.get_python_executable()
        
        cmd = [python, "-m", "pip", "list", "--format=json"]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            packages = json.loads(result.stdout)
            return [f"{pkg['name']}=={pkg['version']}" for pkg in packages]
        except (subprocess.CalledProcessError, json.JSONDecodeError) as e:
            logger.error(f"Failed to list installed packages: {e}")
            return []
    
    def check_package_installed(self, package: str) -> bool:
        """Check if a package is installed."""
        python = self.get_python_executable()
        
        cmd = [python, "-c", f"import {package}; print('Package found')"]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            return result.returncode == 0
        except Exception:
            return False
    
    def setup_environment_for_stage(self, stage: str, update: bool = False) -> bool:
        """Set up the environment for a specific stage."""
        # Install base requirements
        if not self.install_requirements(REQUIREMENTS_FILE, update):
            return False
        
        # Install stage-specific requirements
        if stage == "dev":
            if Path(self.root_dir / DEV_REQUIREMENTS_FILE).exists():
                if not self.install_requirements(DEV_REQUIREMENTS_FILE, update):
                    return False
        elif stage == "test":
            if Path(self.root_dir / TEST_REQUIREMENTS_FILE).exists():
                if not self.install_requirements(TEST_REQUIREMENTS_FILE, update):
                    return False
        
        return True
    
    def run_python_script(self, script_path: Union[str, Path], args: List[str] = None, env: Dict[str, str] = None) -> int:
        """Run a Python script with the specified arguments."""
        python = self.get_python_executable()
        script_path = Path(script_path)
        
        if not script_path.exists():
            logger.error(f"Script not found at {script_path}")
            return 1
        
        cmd = [python, str(script_path)]
        if args:
            cmd.extend(args)
        
        # Set environment variables
        env_vars = os.environ.copy()
        env_vars["PYTHONPATH"] = str(self.root_dir)
        if env:
            env_vars.update(env)
        
        logger.info(f"Running script: {' '.join(cmd)}")
        return subprocess.call(cmd, env=env_vars)
    
    def get_system_info(self) -> Dict[str, Any]:
        """Get system information."""
        python = self.get_python_executable()
        
        # Get Python version
        python_version = platform.python_version()
        
        # Get OS information
        os_info = {
            "system": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
            "machine": platform.machine()
        }
        
        # Get installed packages
        packages = self.list_installed_packages()
        
        # Check for CUDA
        cuda_available = False
        try:
            result = subprocess.run(
                [python, "-c", "import torch; print(torch.cuda.is_available())"],
                capture_output=True,
                text=True,
                check=True
            )
            cuda_available = result.stdout.strip() == "True"
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass
        
        return {
            "python_version": python_version,
            "os_info": os_info,
            "packages": packages,
            "cuda_available": cuda_available,
            "virtual_env": self.is_venv_available()
        }
    
    def print_system_info(self) -> None:
        """Print system information."""
        info = self.get_system_info()
        
        print("\n=== System Information ===")
        print(f"Python Version: {info['python_version']}")
        print(f"Operating System: {info['os_info']['system']} {info['os_info']['release']} ({info['os_info']['machine']})")
        print(f"Virtual Environment: {'Active' if info['virtual_env'] else 'Not Active'}")
        print(f"CUDA Available: {'Yes' if info['cuda_available'] else 'No'}")
        
        print("\n=== Installed Packages ===")
        for package in sorted(info['packages']):
            print(f"  {package}")
        
        print("\n")

# Create a singleton instance
env_manager = EnvironmentManager()

if __name__ == "__main__":
    # If run directly, print system information
    env_manager.print_system_info()