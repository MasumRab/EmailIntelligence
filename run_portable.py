
#!/usr/bin/env python3
"""
Portable Runner for Gmail AI Research Interface
Simple script to run the research interface anywhere
"""

import os
import sys
import subprocess
from pathlib import Path

def check_python():
    """Check Python version"""
    if sys.version_info < (3, 7):
        print("❌ Python 3.7+ required")
        sys.exit(1)
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")

def install_requirements():
    """Install minimal requirements"""
    packages = [
        "fastapi",
        "uvicorn[standard]", 
        "python-multipart",
        "jinja2"
    ]
    
    print("📦 Installing required packages...")
    for package in packages:
        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", 
                "--user", package
            ])
            print(f"✅ {package} installed")
        except subprocess.CalledProcessError:
            print(f"⚠️  Failed to install {package}")

def main():
    """Main runner function"""
    print("🔬 Gmail AI Research Interface - Portable Runner")
    print("=" * 50)
    
    # Check Python
    check_python()
    
    # Install requirements
    install_requirements()
    
    # Set environment
    os.environ["PYTHONPATH"] = str(Path(__file__).parent)
    
    # Run the interface
    print("\n🚀 Starting research interface...")
    try:
        import simple_research_ui
    except ImportError:
        print("❌ Failed to import research interface")
        print("Make sure simple_research_ui.py is in the same directory")
        sys.exit(1)

if __name__ == "__main__":
    main()
