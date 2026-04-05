"""
Verify Command Module

Implements a command for verifying package availability across system and venv.
Ported from verify_packages.py.
"""

import importlib
import sys
import subprocess
from argparse import Namespace
from pathlib import Path
from typing import Any, Dict, List

from ..interface import Command


class VerifyCommand(Command):
    """
    Command for verifying package availability in different contexts.
    
    Checks which packages are available system-wide vs in the virtual environment
    and identifies any missing critical dependencies.
    """

    def __init__(self):
        self._security_validator = None

    @property
    def name(self) -> str:
        return "env-verify"

    @property
    def description(self) -> str:
        return "Verify package availability and environment health"

    def add_arguments(self, parser: Any) -> None:
        """Add command-specific arguments."""
        parser.add_argument(
            "--list-all", 
            action="store_true", 
            help="List all checked packages, not just missing ones"
        )
        parser.add_argument(
            "--venv-path", 
            help="Specify a custom path to the virtual environment"
        )

    def get_dependencies(self) -> Dict[str, Any]:
        """Get required dependencies."""
        return {
            "security_validator": "SecurityValidator"
        }

    def set_dependencies(self, dependencies: Dict[str, Any]) -> None:
        """Set command dependencies."""
        self._security_validator = dependencies.get("security_validator")

    async def execute(self, args: Namespace) -> int:
        """Execute the verify command."""
        packages_to_check = [
            # Core scientific
            'numpy', 'scipy', 'matplotlib', 'pandas', 'seaborn', 'plotly', 'sklearn', 'joblib',
            # Web framework
            'fastapi', 'uvicorn', 'pydantic', 'httpx', 'dotenv',
            # AI/ML
            'torch', 'transformers', 'accelerate', 'sentencepiece',
            # NLP
            'nltk', 'textblob',
            # Web/API
            'gradio', 'pyngrok',
            # Google
            'googleapiclient', 'google.auth', 'google_auth_oauthlib',
            # Utils
            'bleach', 'psutil', 'aiosqlite', 'RestrictedPython'
        ]

        print("🔍 Analyzing package environment...")
        print("=" * 60)

        results = self._check_packages(packages_to_check)
        
        if args.list_all:
            self._print_results(results)
        else:
            self._print_summary(results)
            
        # Check venv
        venv_found = await self._check_venv(args.venv_path)
        if not venv_found:
            print("⚠️  No standard virtual environment detected.")
            
        print("=" * 60)
        return 0

    def _check_packages(self, packages: List[str]) -> Dict[str, List[str]]:
        """Check availability of specified packages."""
        system = []
        venv = []
        missing = []

        for package in packages:
            try:
                # Handle nested packages (e.g., googleapiclient)
                pkg_name = package.split('.')[0]
                importlib.import_module(pkg_name)
                
                module = sys.modules.get(pkg_name)
                module_path = getattr(module, '__file__', '')

                if module_path and 'site-packages' in module_path:
                    if '/usr/' in module_path or '/lib/' in module_path:
                        system.append(package)
                    else:
                        venv.append(package)
                else:
                    system.append(package)
            except ImportError:
                missing.append(package)
        
        return {
            "system": system,
            "venv": venv,
            "missing": missing
        }

    def _print_results(self, results: Dict[str, List[str]]) -> None:
        """Print detailed package availability."""
        for context, pkgs in [("System", results["system"]), ("Venv", results["venv"])]:
            if pkgs:
                print(f"✅ {context} packages ({len(pkgs)}):")
                for pkg in sorted(pkgs):
                    print(f"   • {pkg}")
        
        if results["missing"]:
            print(f"\n❌ Missing packages ({len(results['missing'])}):")
            for pkg in sorted(results["missing"]):
                print(f"   • {pkg}")

    def _print_summary(self, results: Dict[str, List[str]]) -> None:
        """Print a concise summary of package availability."""
        print(f"Status: {len(results['system'])} system, {len(results['venv'])} venv, {len(results['missing'])} missing")
        if results["missing"]:
            print(f"Action required: Install missing packages: {', '.join(results['missing'])}")

    async def _check_venv(self, custom_path: str = None) -> bool:
        """Check for virtual environment presence and status."""
        venv_names = [custom_path] if custom_path else ['./venv', './.venv', './env']
        
        for venv_name in venv_names:
            if not venv_name: continue
            
            path = Path(venv_name)
            if path.exists() and path.is_dir():
                # Security check: Ensure path is within project root
                if self._security_validator:
                    is_safe, error = self._security_validator.validate_path_security(str(path.absolute()))
                    if not is_safe:
                        print(f"⚠️  Security Warning: Venv path '{venv_name}' is outside project root: {error}")
                        continue

                print(f"✅ Virtual environment detected: {path.absolute()}")
                
                # Try to count packages using pip in that venv
                pip_exe = path / "bin" / "pip"
                if pip_exe.exists():
                    try:
                        result = subprocess.run(
                            [str(pip_exe), "list", "--format=freeze"],
                            capture_output=True, text=True, check=False
                        )
                        if result.returncode == 0:
                            count = len([line for line in result.stdout.split('\n') if line.strip()])
                            print(f"📦 Packages in venv: {count}")
                    except Exception:
                        pass
                return True
        return False
