"""
Installation Service for EmailIntelligence Command Line Tools

This module provides cross-platform installation functionality for the EmailIntelligence
CLI tools, handling symlink creation, PATH management, and platform-specific differences.
"""

import os
import sys
import platform
import subprocess
import shutil
from pathlib import Path
from typing import Optional, List, Dict, Any
import json
import stat


class InstallationService:
    """
    Service for installing and managing EmailIntelligence command line tools.
    
    This service handles:
    - Platform-specific installation paths
    - Symlink creation and management
    - PATH environment variable checking
    - Installation verification
    - Shell configuration for different platforms
    """
    
    def __init__(self, project_root: Optional[Path] = None):
        """
        Initialize the InstallationService.
        
        Args:
            project_root: Path to the project root. If None, auto-detects from this file.
        """
        self.project_root = project_root or Path(__file__).parent.parent.parent.absolute()
        self.system = platform.system()
        self.home_dir = Path.home()
        
        # Platform-specific default paths
        if self.system == "Windows":
            self.default_bin_dir = self.home_dir / "AppData" / "Local" / "Programs" / "EmailIntelligence"
            self.shell_configs = {
                "cmd": self.home_dir / "AppData" / "Roaming" / "Microsoft" / "Command Prompt" / "cmdrc",
                "powershell": self.home_dir / "Documents" / "WindowsPowerShell" / "Microsoft.PowerShell_profile.ps1",
                "git_bash": self.home_dir / ".bashrc"
            }
        else:  # Unix-like systems (Linux, macOS)
            self.default_bin_dir = self.home_dir / ".local" / "bin"
            self.shell_configs = {
                "bash": self.home_dir / ".bashrc",
                "zsh": self.home_dir / ".zshrc",
                "fish": self.home_dir / ".config" / "fish" / "config.fish"
            }
    
    def get_python_executable(self) -> Path:
        """
        Get the Python executable path for the current environment.
        
        Returns:
            Path to the Python executable
        """
        return Path(sys.executable)
    
    def get_default_installation_path(self, tool_name: str) -> Path:
        """
        Get the default installation path for a given tool name.
        
        Args:
            tool_name: Name of the tool to install
            
        Returns:
            Path where the tool should be installed
        """
        return self.default_bin_dir / tool_name
    
    def create_installation_wrapper(self, target_path: Path, alias: str, python_executable: Path) -> str:
        """
        Create a platform-specific wrapper script for the tool.
        
        Args:
            target_path: Path where the wrapper will be created
            alias: Name of the tool/alias
            python_executable: Path to the Python executable
            
        Returns:
            Content for the wrapper script
        """
        tool_path = self.project_root / "src" / "cli" / "main.py"
        
        if self.system == "Windows":
            return f'''@echo off
"{python_executable}" "{tool_path}" %*
'''
        else:
            return f'''#!/bin/bash
"{python_executable}" "{tool_path}" "$@"
'''
    
    def install_tool(self, alias: str, bin_dir: Optional[Path] = None, force: bool = False) -> Dict[str, Any]:
        """
        Install a command line tool.
        
        Args:
            alias: Name/alias for the tool
            bin_dir: Directory to install to. If None, uses default.
            force: Whether to overwrite existing installation
            
        Returns:
            Dictionary with installation results and status
        """
        try:
            # Determine installation path
            if bin_dir is None:
                bin_dir = self.get_default_installation_path(alias)
            else:
                bin_dir = Path(bin_dir) / alias
            
            # Create installation result
            result = {
                "success": False,
                "tool_name": alias,
                "install_path": str(bin_dir),
                "bin_dir": str(bin_dir.parent),
                "messages": [],
                "warnings": [],
                "errors": []
            }
            
            # Create bin directory if it doesn't exist
            bin_dir.parent.mkdir(parents=True, exist_ok=True)
            
            # Check for existing installation
            if bin_dir.exists() and not force:
                result["warnings"].append(f"Installation already exists at {bin_dir}. Use --force to overwrite.")
                return result
            
            # Get Python executable
            python_executable = self.get_python_executable()
            
            # Create wrapper content
            wrapper_content = self.create_installation_wrapper(bin_dir, alias, python_executable)
            
            # Write wrapper
            with open(bin_dir, 'w') as f:
                f.write(wrapper_content)
            
            # Make executable on Unix systems
            if self.system != "Windows":
                os.chmod(bin_dir, 0o755)
            
            result["success"] = True
            result["messages"].append(f"Successfully installed '{alias}' to {bin_dir}")
            
            # Check PATH
            if not self._is_in_path(bin_dir.parent):
                result["warnings"].append(f"{bin_dir.parent} is not in your PATH.")
                result["messages"].extend(self._get_path_instructions(bin_dir.parent))
            
            # Verify installation
            if self.verify_installation(bin_dir):
                result["messages"].append(f"Installation verified successfully!")
            else:
                result["errors"].append("Installation verification failed.")
            
            return result
            
        except Exception as e:
            return {
                "success": False,
                "tool_name": alias,
                "errors": [f"Installation failed: {str(e)}"],
                "messages": [],
                "warnings": []
            }
    
    def _is_in_path(self, directory: Path) -> bool:
        """
        Check if a directory is in the PATH environment variable.
        
        Args:
            directory: Directory to check
            
        Returns:
            True if directory is in PATH, False otherwise
        """
        path_dirs = os.environ.get("PATH", "").split(os.pathsep)
        directory_str = str(directory)
        
        # Normalize paths for comparison
        directory_str = os.path.normpath(directory_str)
        
        for path_dir in path_dirs:
            if os.path.normpath(path_dir) == directory_str:
                return True
        
        return False
    
    def _get_path_instructions(self, bin_dir: Path) -> List[str]:
        """
        Get instructions for adding a directory to PATH based on the platform and shell.
        
        Args:
            bin_dir: Directory to add to PATH
            
        Returns:
            List of instruction strings
        """
        instructions = []
        
        if self.system == "Windows":
            instructions.append("You may need to add it to your PATH in:")
            instructions.append("1. System Properties > Environment Variables")
            instructions.append("2. Or open a new Command Prompt as Administrator and run:")
            instructions.append(f'   setx PATH "{bin_dir};%PATH%"')
        else:
            shell_name = self._detect_shell()
            if shell_name == "fish":
                instructions.append(f"Add this to your ~/.config/fish/config.fish:")
                instructions.append(f"set -gx PATH \"{bin_dir}\" $PATH")
            elif shell_name == "zsh":
                instructions.append("Add this to your ~/.zshrc:")
                instructions.append(f"export PATH=\"{bin_dir}:$PATH\"")
            else:  # bash or unknown
                instructions.append("Add this to your ~/.bashrc or ~/.bash_profile:")
                instructions.append(f"export PATH=\"{bin_dir}:$PATH\"")
        
        return instructions
    
    def _detect_shell(self) -> str:
        """
        Detect the current shell.
        
        Returns:
            Name of the current shell (bash, zsh, fish, powershell, cmd, etc.)
        """
        # Check if we're on Windows
        if self.system == "Windows":
            # Try to detect Windows shell
            parent_process = os.environ.get("COMSPEC", "cmd.exe")
            if "powershell" in parent_process.lower():
                return "powershell"
            else:
                return "cmd"
        else:
            # Check for Unix shells
            shell_var = os.environ.get("SHELL", "")
            if "fish" in shell_var:
                return "fish"
            elif "zsh" in shell_var:
                return "zsh"
            else:
                return "bash"
    
    def verify_installation(self, install_path: Path) -> bool:
        """
        Verify that an installation works correctly.
        
        Args:
            install_path: Path to the installed tool
            
        Returns:
            True if installation is working, False otherwise
        """
        try:
            # Test with --help
            result = subprocess.run(
                [str(install_path), "--help"], 
                capture_output=True, 
                text=True, 
                timeout=10
            )
            return result.returncode == 0
        except Exception:
            return False
    
    def list_installed_tools(self, bin_dir: Optional[Path] = None) -> List[str]:
        """
        List all installed EmailIntelligence tools.
        
        Args:
            bin_dir: Directory to search in. If None, uses default.
            
        Returns:
            List of installed tool names
        """
        if bin_dir is None:
            bin_dir = self.default_bin_dir
        
        tools = []
        if bin_dir.exists():
            for file_path in bin_dir.iterdir():
                if file_path.is_file() and not file_path.name.startswith('.'):
                    # Check if it's one of our known tools
                    if file_path.name in ["git-verifier", "kilocode", "email-intelligence"]:
                        tools.append(file_path.name)
        
        return tools
    
    def uninstall_tool(self, alias: str, bin_dir: Optional[Path] = None) -> Dict[str, Any]:
        """
        Uninstall a command line tool.
        
        Args:
            alias: Name/alias of the tool to uninstall
            bin_dir: Directory where tool is installed. If None, uses default.
            
        Returns:
            Dictionary with uninstallation results
        """
        try:
            if bin_dir is None:
                install_path = self.get_default_installation_path(alias)
            else:
                install_path = Path(bin_dir) / alias
            
            result = {
                "success": False,
                "tool_name": alias,
                "install_path": str(install_path),
                "messages": [],
                "errors": []
            }
            
            if not install_path.exists():
                result["errors"].append(f"Tool '{alias}' is not installed at {install_path}")
                return result
            
            # Remove the installation
            os.remove(install_path)
            
            result["success"] = True
            result["messages"].append(f"Successfully uninstalled '{alias}' from {install_path}")
            
            return result
            
        except Exception as e:
            return {
                "success": False,
                "tool_name": alias,
                "errors": [f"Uninstallation failed: {str(e)}"],
                "messages": []
            }
    
    def get_installation_info(self) -> Dict[str, Any]:
        """
        Get information about the current installation setup.
        
        Returns:
            Dictionary with installation information
        """
        return {
            "system": self.system,
            "python_executable": str(self.get_python_executable()),
            "default_bin_dir": str(self.default_bin_dir),
            "home_dir": str(self.home_dir),
            "project_root": str(self.project_root),
            "shell": self._detect_shell(),
            "installed_tools": self.list_installed_tools()
        }


def install_main_tools(project_root: Optional[Path] = None, 
                      bin_dir: Optional[Path] = None, 
                      force: bool = False) -> Dict[str, Any]:
    """
    Install the main EmailIntelligence CLI tools.
    
    Args:
        project_root: Path to the project root
        bin_dir: Directory to install to
        force: Whether to overwrite existing installations
        
    Returns:
        Dictionary with installation results for all tools
    """
    service = InstallationService(project_root)
    tools = ["git-verifier", "kilocode", "email-intelligence"]
    
    results = {}
    for tool in tools:
        results[tool] = service.install_tool(tool, bin_dir, force)
    
    return results


if __name__ == "__main__":
    # Test the installation service
    service = InstallationService()
    print("Installation Service Test")
    print("========================")
    print(f"System: {service.system}")
    print(f"Default bin dir: {service.default_bin_dir}")
    print(f"Project root: {service.project_root}")
    print(f"Python executable: {service.get_python_executable()}")
    
    # Show installation info
    info = service.get_installation_info()
    print(f"\nCurrent setup: {json.dumps(info, indent=2)}")