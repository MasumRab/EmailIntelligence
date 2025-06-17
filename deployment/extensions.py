#!/usr/bin/env python3
"""
Extensions Manager for EmailIntelligence

This module provides functions for managing extensions,
including loading, enabling, disabling, and updating extensions.
"""

import importlib
import inspect
import json
import logging
import os
import pkgutil
import subprocess
import sys
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("extensions")

# Project root directory
ROOT_DIR = Path(__file__).resolve().parent.parent


class Extension:
    """Represents an extension for the EmailIntelligence application."""

    def __init__(self, name: str, path: Path, metadata: Dict[str, Any]):
        """Initialize the extension."""
        self.name = name
        self.path = path
        self.metadata = metadata
        self.module = None
        self.enabled = metadata.get("enabled", True)

    def load(self) -> bool:
        """Load the extension module."""
        try:
            # Add the extension directory to the Python path
            sys.path.insert(0, str(self.path.parent))

            # Import the extension module
            self.module = importlib.import_module(self.path.stem)

            # Remove the extension directory from the Python path
            sys.path.pop(0)

            return True
        except ImportError as e:
            logger.error(f"Failed to load extension {self.name}: {e}")
            return False

    def initialize(self) -> bool:
        """Initialize the extension."""
        if not self.module:
            return False

        try:
            # Check if the module has an initialize function
            if hasattr(self.module, "initialize"):
                self.module.initialize()

            return True
        except Exception as e:
            logger.error(f"Failed to initialize extension {self.name}: {e}")
            return False

    def shutdown(self) -> bool:
        """Shutdown the extension."""
        if not self.module:
            return False

        try:
            # Check if the module has a shutdown function
            if hasattr(self.module, "shutdown"):
                self.module.shutdown()

            return True
        except Exception as e:
            logger.error(f"Failed to shutdown extension {self.name}: {e}")
            return False

    def get_info(self) -> Dict[str, Any]:
        """Get information about the extension."""
        return {
            "name": self.name,
            "path": str(self.path),
            "enabled": self.enabled,
            "metadata": self.metadata,
            "loaded": self.module is not None,
        }


class ExtensionsManager:
    """Manages extensions for the EmailIntelligence application."""

    def __init__(
        self, root_dir: Path = ROOT_DIR, python_executable: Optional[str] = None
    ):
        """Initialize the extensions manager."""
        self.root_dir = root_dir
        self.extensions_dir = root_dir / "extensions"
        self.extensions: Dict[str, Extension] = {}
        self.python_executable = (
            python_executable if python_executable else sys.executable
        )

    def set_python_executable(self, python_executable: str):
        """Set the Python executable path."""
        self.python_executable = python_executable

    def discover_extensions(self) -> List[Extension]:
        """Discover available extensions."""
        if not self.extensions_dir.exists():
            logger.info(f"Extensions directory not found at {self.extensions_dir}")
            return []

        extensions = []

        # Iterate through subdirectories in the extensions directory
        for ext_dir in self.extensions_dir.iterdir():
            if not ext_dir.is_dir():
                continue

            # Check if the extension has a metadata file
            metadata_file = ext_dir / "metadata.json"
            if not metadata_file.exists():
                logger.warning(
                    f"Extension {ext_dir.name} does not have a metadata.json file"
                )
                continue

            # Load the metadata
            try:
                with open(metadata_file, "r") as f:
                    metadata = json.load(f)
            except json.JSONDecodeError as e:
                logger.error(
                    f"Failed to parse metadata for extension {ext_dir.name}: {e}"
                )
                continue

            # Check if the extension has a main module
            main_module = ext_dir / f"{ext_dir.name}.py"
            if not main_module.exists():
                logger.warning(f"Extension {ext_dir.name} does not have a main module")
                continue

            # Create the extension
            extension = Extension(ext_dir.name, main_module, metadata)
            extensions.append(extension)

        return extensions

    def load_extensions(self) -> bool:
        """Load all available extensions."""
        extensions = self.discover_extensions()
        all_loaded = True

        for extension in extensions:
            if extension.enabled:
                if extension.load():
                    self.extensions[extension.name] = extension
                    logger.info(f"Loaded extension: {extension.name}")
                else:
                    logger.error(f"Failed to load extension: {extension.name}")
                    all_loaded = False

        return all_loaded

    def initialize_extensions(self) -> bool:
        """Initialize all loaded extensions with detailed error feedback."""
        import traceback

        all_initialized = True
        failed_extensions = []
        for name, extension in self.extensions.items():
            if extension.enabled:
                try:
                    if extension.initialize():
                        logger.info(f"Initialized extension: {name}")
                    else:
                        logger.error(
                            f"Failed to initialize extension: {name} (no exception raised)"
                        )
                        all_initialized = False
                        failed_extensions.append(name)
                except Exception as e:
                    logger.error(
                        f"Exception during initialization of extension '{name}': {e}",
                        exc_info=True,
                    )
                    all_initialized = False
                    failed_extensions.append(name)
        if failed_extensions:
            logger.error(
                f"Extensions failed to initialize: {', '.join(failed_extensions)}"
            )
        return all_initialized

    def shutdown_extensions(self) -> bool:
        """Shutdown all loaded extensions."""
        for name, extension in self.extensions.items():
            if extension.enabled:
                if extension.shutdown():
                    logger.info(f"Shutdown extension: {name}")
                else:
                    logger.error(f"Failed to shutdown extension: {name}")

        return True

    def get_extension(self, name: str) -> Optional[Extension]:
        """Get an extension by name."""
        return self.extensions.get(name)

    def enable_extension(self, name: str) -> bool:
        """Enable an extension."""
        extension = self.get_extension(name)
        if not extension:
            logger.error(f"Extension not found: {name}")
            return False

        extension.enabled = True

        # Update the metadata file
        metadata_file = extension.path.parent / "metadata.json"
        try:
            with open(metadata_file, "r") as f:
                metadata = json.load(f)

            metadata["enabled"] = True

            with open(metadata_file, "w") as f:
                json.dump(metadata, f, indent=4)

            return True
        except (json.JSONDecodeError, IOError) as e:
            logger.error(f"Failed to update metadata for extension {name}: {e}")
            return False

    def disable_extension(self, name: str) -> bool:
        """Disable an extension."""
        extension = self.get_extension(name)
        if not extension:
            logger.error(f"Extension not found: {name}")
            return False

        extension.enabled = False

        # Update the metadata file
        metadata_file = extension.path.parent / "metadata.json"
        try:
            with open(metadata_file, "r") as f:
                metadata = json.load(f)

            metadata["enabled"] = False

            with open(metadata_file, "w") as f:
                json.dump(metadata, f, indent=4)

            return True
        except (json.JSONDecodeError, IOError) as e:
            logger.error(f"Failed to update metadata for extension {name}: {e}")
            return False

    def install_extension(self, url: str) -> bool:
        """Install an extension from a Git repository."""
        if not self.extensions_dir.exists():
            self.extensions_dir.mkdir(parents=True)

        # Extract the extension name from the URL
        name = url.split("/")[-1].replace(".git", "")

        # Check if the extension is already installed
        if (self.extensions_dir / name).exists():
            logger.error(f"Extension already installed: {name}")
            return False

        # Clone the repository
        try:
            subprocess.check_call(
                ["git", "clone", url, str(self.extensions_dir / name)]
            )

            # Check if the extension has a requirements.txt file
            requirements_file = self.extensions_dir / name / "requirements.txt"
            if requirements_file.exists():
                # Install the requirements
                python = self.python_executable
                subprocess.check_call(
                    [python, "-m", "pip", "install", "-r", str(requirements_file)]
                )

            logger.info(f"Installed extension: {name}")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to install extension {name}: {e}")
            return False

    def uninstall_extension(self, name: str) -> bool:
        """Uninstall an extension."""
        extension_dir = self.extensions_dir / name
        if not extension_dir.exists():
            logger.error(f"Extension not found: {name}")
            return False

        # Remove the extension from the loaded extensions
        if name in self.extensions:
            extension = self.extensions[name]
            extension.shutdown()
            del self.extensions[name]

        # Remove the extension directory
        try:
            import shutil

            shutil.rmtree(extension_dir)

            logger.info(f"Uninstalled extension: {name}")
            return True
        except Exception as e:
            logger.error(f"Failed to uninstall extension {name}: {e}")
            return False

    def update_extension(self, name: str) -> bool:
        """Update an extension."""
        extension_dir = self.extensions_dir / name
        if not extension_dir.exists():
            logger.error(f"Extension not found: {name}")
            return False

        # Pull the latest changes
        try:
            subprocess.check_call(["git", "pull"], cwd=str(extension_dir))

            # Check if the extension has a requirements.txt file
            requirements_file = extension_dir / "requirements.txt"
            if requirements_file.exists():
                # Install the requirements
                python = self.python_executable
                subprocess.check_call(
                    [python, "-m", "pip", "install", "-r", str(requirements_file)]
                )

            logger.info(f"Updated extension: {name}")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to update extension {name}: {e}")
            return False

    def list_extensions(self) -> List[Dict[str, Any]]:
        """List all extensions."""
        return [extension.get_info() for extension in self.extensions.values()]

    def create_extension_template(self, name: str) -> bool:
        """Create a template for a new extension."""
        if not self.extensions_dir.exists():
            self.extensions_dir.mkdir(parents=True)

        # Check if the extension already exists
        extension_dir = self.extensions_dir / name
        if extension_dir.exists():
            logger.error(f"Extension already exists: {name}")
            return False

        # Create the extension directory
        extension_dir.mkdir()

        # Create the metadata file
        metadata = {
            "name": name,
            "version": "0.1.0",
            "description": "A new extension for EmailIntelligence",
            "author": "Your Name",
            "email": "your.email@example.com",
            "enabled": True,
            "dependencies": [],
        }

        with open(extension_dir / "metadata.json", "w") as f:
            json.dump(metadata, f, indent=4)

        # Create the main module
        with open(extension_dir / f"{name}.py", "w") as f:
            f.write(
                f"""#!/usr/bin/env python3
\"\"\"
{name} Extension for EmailIntelligence

This extension provides additional functionality for the EmailIntelligence application.
\"\"\"

import logging

# Configure logging
logger = logging.getLogger(__name__)

def initialize():
    \"\"\"Initialize the extension.\"\"\"
    logger.info(f"Initializing {name} extension")

def shutdown():
    \"\"\"Shutdown the extension.\"\"\"
    logger.info(f"Shutting down {name} extension")

# Add your extension code here
"""
            )

        # Create a README file
        with open(extension_dir / "README.md", "w") as f:
            f.write(
                f"""# {name} Extension

This extension provides additional functionality for the EmailIntelligence application.

## Installation

1. Clone this repository into the `extensions` directory of your EmailIntelligence installation:
   ```
   cd /path/to/EmailIntelligence/extensions
   git clone https://github.com/yourusername/{name}.git
   ```

2. Restart the EmailIntelligence application.

## Usage

Describe how to use your extension here.

## License

This extension is licensed under the MIT License. See the LICENSE file for details.
"""
            )

        # Create a requirements.txt file
        with open(extension_dir / "requirements.txt", "w") as f:
            f.write("# Add your dependencies here\n")

        logger.info(f"Created extension template: {name}")
        return True


# Create a singleton instance
extensions_manager = ExtensionsManager()

if __name__ == "__main__":
    # If run directly, list all extensions
    extensions_manager.load_extensions()
    extensions = extensions_manager.list_extensions()

    print(f"Found {len(extensions)} extensions:")
    for extension in extensions:
        print(
            f"  {extension['name']} - {'Enabled' if extension['enabled'] else 'Disabled'}"
        )
        print(f"    Path: {extension['path']}")
        print(f"    Loaded: {extension['loaded']}")
        print(
            f"    Description: {extension['metadata'].get('description', 'No description')}"
        )
        print()
