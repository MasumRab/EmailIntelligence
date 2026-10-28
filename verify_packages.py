#!/usr/bin/env python3
"""
Package Verification Script
Checks which packages are available system-wide vs in virtual environment
"""

import sys
import subprocess
import importlib
from pathlib import Path

def run_command(cmd):
    """Run a command and return output"""
    try:
        # Use shell=False for security, ensure cmd is a list
        if isinstance(cmd, str):
            # For shell commands that need shell features, use shlex.split
            import shlex
            cmd = shlex.split(cmd)
        result = subprocess.run(cmd, shell=False, capture_output=True, text=True)
        return result.returncode == 0, result.stdout.strip()
    except Exception:
        return False, ""

def check_package_availability():
    """Check package availability in different contexts"""

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

    print("🔍 Checking package availability...")
    print("=" * 80)

    system_available = []
    venv_available = []
    not_available = []

    for package in packages_to_check:
        try:
            importlib.import_module(package.replace('.', '_') if '.' in package else package)
            # Check if it's from system or venv
            module = sys.modules[package.replace('.', '_') if '.' in package else package]
            module_path = getattr(module, '__file__', '')

            if module_path and 'site-packages' in module_path:
                if '/usr/' in module_path:
                    system_available.append(package)
                else:
                    venv_available.append(package)
            else:
                system_available.append(package)  # Assume system if unclear
        except ImportError:
            not_available.append(package)

    print(f"✅ System packages ({len(system_available)}):")
    for pkg in sorted(system_available):
        print(f"   • {pkg}")

    print(f"\n🐍 Virtual environment packages ({len(venv_available)}):")
    for pkg in sorted(venv_available):
        print(f"   • {pkg}")

    if not_available:
        print(f"\n❌ Not available ({len(not_available)}):")
        for pkg in sorted(not_available):
            print(f"   • {pkg}")

    print("\n" + "=" * 80)
    print(f"📊 Summary: {len(system_available)} system, {len(venv_available)} venv, {len(not_available)} missing")

    # Check virtual environment (try standard names)
    venv_names = ['./venv', './emailintelligence_env', './emailintelligence_venv']
    venv_found = False

    for venv_name in venv_names:
        venv_path = Path(venv_name)
        if venv_path.exists():
            print(f"✅ Virtual environment found: {venv_path.absolute()}")
            venv_found = True

            # Check pip packages in venv
            pip_exe = venv_path / "bin" / "pip"
            if pip_exe.exists():
                success, output = run_command([str(pip_exe), "list", "--format=freeze"])
                if success:
                    # Count lines in output
                    line_count = len([line for line in output.split('\n') if line.strip()])
                    print(f"📦 Virtual environment has {line_count} packages installed")
            else:
                success, output = run_command(f"source {venv_name}/bin/activate && pip list --format=freeze | wc -l")
            if success:
                print(f"📦 Virtual environment has {output} packages installed")
            break

    if not venv_found:
        print("⚠️  Virtual environment not found")

    # Check system packages
    success, output = run_command(["dpkg", "-l"])
    if success:
    # Count python3 packages manually
        lines = [line for line in output.split("\n") if line.startswith("ii") and "python3" in line]
        package_count = str(len(lines))
        print(f"📦 System has {package_count} Python packages installed")

if __name__ == "__main__":
    check_package_availability()
