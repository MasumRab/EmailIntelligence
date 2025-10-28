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
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout.strip()
    except Exception:
        return False, ""

def check_package_availability():
    """Check package availability in different contexts"""
<<<<<<< HEAD
    
=======

>>>>>>> origin/feature-dashboard-stats-endpoint
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
<<<<<<< HEAD
    
    print("🔍 Checking package availability...")
    print("=" * 80)
    
    system_available = []
    venv_available = []
    not_available = []
    
=======

    print("🔍 Checking package availability...")
    print("=" * 80)

    system_available = []
    venv_available = []
    not_available = []

>>>>>>> origin/feature-dashboard-stats-endpoint
    for package in packages_to_check:
        try:
            importlib.import_module(package.replace('.', '_') if '.' in package else package)
            # Check if it's from system or venv
            module = sys.modules[package.replace('.', '_') if '.' in package else package]
            module_path = getattr(module, '__file__', '')
<<<<<<< HEAD
            
=======

>>>>>>> origin/feature-dashboard-stats-endpoint
            if module_path and 'site-packages' in module_path:
                if '/usr/' in module_path:
                    system_available.append(package)
                else:
                    venv_available.append(package)
            else:
                system_available.append(package)  # Assume system if unclear
        except ImportError:
            not_available.append(package)
<<<<<<< HEAD
    
    print(f"✅ System packages ({len(system_available)}):")
    for pkg in sorted(system_available):
        print(f"   • {pkg}")
    
    print(f"\n🐍 Virtual environment packages ({len(venv_available)}):")
    for pkg in sorted(venv_available):
        print(f"   • {pkg}")
    
=======

    print(f"✅ System packages ({len(system_available)}):")
    for pkg in sorted(system_available):
        print(f"   • {pkg}")

    print(f"\n🐍 Virtual environment packages ({len(venv_available)}):")
    for pkg in sorted(venv_available):
        print(f"   • {pkg}")

>>>>>>> origin/feature-dashboard-stats-endpoint
    if not_available:
        print(f"\n❌ Not available ({len(not_available)}):")
        for pkg in sorted(not_available):
            print(f"   • {pkg}")
<<<<<<< HEAD
    
    print("\n" + "=" * 80)
    print(f"📊 Summary: {len(system_available)} system, {len(venv_available)} venv, {len(not_available)} missing")
    
=======

    print("\n" + "=" * 80)
    print(f"📊 Summary: {len(system_available)} system, {len(venv_available)} venv, {len(not_available)} missing")

>>>>>>> origin/feature-dashboard-stats-endpoint
    # Check virtual environment (try both possible names)
    venv_names = ['./emailintelligence_env', './emailintelligence_venv', './venv']
    venv_found = False

    for venv_name in venv_names:
        venv_path = Path(venv_name)
        if venv_path.exists():
            print(f"✅ Virtual environment found: {venv_path.absolute()}")
            venv_found = True

            # Check pip packages in venv
            success, output = run_command(f"source {venv_name}/bin/activate && pip list --format=freeze | wc -l")
            if success:
                print(f"📦 Virtual environment has {output} packages installed")
            break

    if not venv_found:
        print("⚠️  Virtual environment not found")
<<<<<<< HEAD
    
=======

>>>>>>> origin/feature-dashboard-stats-endpoint
    # Check system packages
    success, output = run_command("dpkg -l | grep '^ii' | grep python3 | wc -l")
    if success:
        print(f"📦 System has {output} Python packages installed")

if __name__ == "__main__":
    check_package_availability()
