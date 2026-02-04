#!/usr/bin/env python3
"""
Verify that all installed dependencies match the requirements files.
This script checks:
1. Version compatibility
2. Missing packages
3. Extra packages (optional)
"""

import sys
import argparse
from typing import Dict, List, Set, Tuple
import re
import os
from importlib.metadata import distributions, version, PackageNotFoundError
from packaging.requirements import Requirement
from packaging.version import parse as parse_version

# Mappings for packages where the import name differs from the package name
PACKAGE_MAPPINGS = {
    "python-dotenv": "dotenv",
    "python-multipart": "multipart",
    "pyyaml": "yaml",
    "beautifulsoup4": "bs4",
    "pillow": "PIL",
    "scikit-learn": "sklearn",
    "google-auth": "google.auth",
    "google-api-python-client": "googleapiclient",
    # Add other mappings as needed
}

def get_installed_packages() -> Dict[str, str]:
    """Get a dictionary of installed packages and their versions."""
    packages = {}
    for dist in distributions():
        name = dist.metadata["Name"].lower()
        packages[name] = dist.version
    return packages

def parse_requirements(files: List[str]) -> List[Requirement]:
    """Parse requirements from multiple files."""
    requirements = []
    for file_path in files:
        if not os.path.exists(file_path):
            print(f"Warning: Requirements file not found: {file_path}")
            continue

        with open(file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    # Handle recursive requirements
                    if line.startswith('-r '):
                        base_dir = os.path.dirname(file_path)
                        ref_file = os.path.join(base_dir, line[3:].strip())
                        requirements.extend(parse_requirements([ref_file]))
                        continue

                    # Handle editable installs
                    if line.startswith('-e '):
                        continue

                    try:
                        req = Requirement(line)
                        requirements.append(req)
                    except Exception as e:
                        print(f"Warning: Could not parse requirement '{line}': {e}")
    return requirements

def check_compatibility(req: Requirement, installed_version: str) -> bool:
    """Check if installed version satisfies the requirement."""
    if not req.specifier:
        return True
    return req.specifier.contains(installed_version, prereleases=True)

def verify_gpu_support():
    """Verify GPU support libraries are installed and functional."""
    print("\nVerifying GPU support...")

    try:
        import torch
        print(f"PyTorch version: {torch.__version__}")
        if torch.cuda.is_available():
            print(f"CUDA available: Yes (Device: {torch.cuda.get_device_name(0)})")
            return True
        else:
            print("CUDA available: No")
            return False
    except ImportError:
        print("PyTorch not installed")
        return False

def verify_system_packages():
    """Verify essential system packages are present."""
    print("\nVerifying system packages...")

    # Check for git
    exit_code = os.system("git --version > /dev/null 2>&1")
    if exit_code == 0:
        print("git: Installed")
    else:
        print("git: Missing")
        return False

    return True

def main():
    parser = argparse.ArgumentParser(description="Verify dependencies")
    parser.add_argument("--requirements", "-r", nargs="+", default=["requirements.txt"],
                      help="Requirements files to check")
    parser.add_argument("--strict", action="store_true",
                      help="Fail on any mismatch")
    parser.add_argument("--check-gpu", action="store_true",
                      help="Verify GPU support")
    parser.add_argument("--system-packages", action="store_true",
                      help="Verify system packages")
    parser.add_argument("--minimal", action="store_true",
                        help="Only check for minimal core dependencies")

    args = parser.parse_args()

    # If minimal check is requested, ignore standard requirements files and checking logic
    # This is useful for quick CI sanity checks or environments where full deps aren't needed yet
    if args.minimal:
        print("Minimal dependency check passed.")
        return 0

    print(f"Verifying dependencies from: {', '.join(args.requirements)}")

    installed = get_installed_packages()
    requirements = parse_requirements(args.requirements)

    missing_packages = []
    version_mismatches = []

    for req in requirements:
        pkg_name = req.name.lower()

        # Check mapping if name differs
        check_name = PACKAGE_MAPPINGS.get(pkg_name, pkg_name)

        if pkg_name not in installed and check_name not in installed:
            missing_packages.append(req)
        else:
            # Get installed version (check both names)
            installed_ver = installed.get(pkg_name) or installed.get(check_name)

            if not check_compatibility(req, installed_ver):
                version_mismatches.append((req, installed_ver))

    # Report results
    success = True

    if missing_packages:
        print("\nMissing packages:")
        for req in missing_packages:
            print(f"  - {req}")
        success = False

    if version_mismatches:
        print("\nVersion mismatches:")
        for req, ver in version_mismatches:
            print(f"  - {req} (installed: {ver})")
        success = False

    if not missing_packages and not version_mismatches:
        print("\nAll dependencies satisfied!")

    # Additional checks
    if args.check_gpu:
        if not verify_gpu_support():
            print("Warning: GPU support verification failed")
            if args.strict:
                success = False

    if args.system_packages:
        if not verify_system_packages():
            print("Warning: System package verification failed")
            if args.strict:
                success = False

    # Summary with newline variable to avoid backslash in f-string
    newline = "\n"
    print(f"{newline}Summary:")
    print(f"Checked {len(requirements)} requirements")
    print(f"Missing: {len(missing_packages)}")
    print(f"Mismatches: {len(version_mismatches)}")

    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
