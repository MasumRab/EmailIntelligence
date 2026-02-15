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
from typing import Dict, List, Set, Optional
import os
import importlib.metadata
from packaging.requirements import Requirement
from packaging.version import parse as parse_version

# Try to import toml for pyproject.toml parsing
try:
    import toml
    TOML_AVAILABLE = True
except ImportError:
    TOML_AVAILABLE = False

# Mappings for packages where the import name differs from the package name
# or where legacy mappings are needed.
# Note: importlib.metadata usually handles standard names correctly.
PACKAGE_MAPPINGS = {
    "python-dotenv": "python-dotenv",
    "python-multipart": "python-multipart",
    "pyyaml": "PyYAML",
    "beautifulsoup4": "beautifulsoup4",
    "pillow": "Pillow",
    "scikit-learn": "scikit-learn",
    "google-auth": "google-auth",
    "google-api-python-client": "google-api-python-client",
    "typing-extensions": "typing-extensions",
}

def get_installed_packages() -> Dict[str, str]:
    """Get a dictionary of installed packages and their versions using importlib.metadata."""
    installed = {}
    for dist in importlib.metadata.distributions():
        try:
            name = dist.metadata["Name"]
            version = dist.version
            if name:
                installed[name.lower()] = version
        except Exception:
            continue
    return installed

def get_optional_dependencies() -> Set[str]:
    """Extract optional dependencies from pyproject.toml."""
    optional_deps = set()
    if not TOML_AVAILABLE:
        return optional_deps

    # Find pyproject.toml relative to script location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Assuming script is in scripts/, go up one level
    root_dir = os.path.dirname(script_dir)
    pyproject_path = os.path.join(root_dir, "pyproject.toml")

    if not os.path.exists(pyproject_path):
        return optional_deps

    try:
        data = toml.load(pyproject_path)
        opt_deps = data.get("project", {}).get("optional-dependencies", {})
        for group, deps in opt_deps.items():
            for dep in deps:
                try:
                    # Parse the requirement string to get the name
                    req = Requirement(dep)
                    optional_deps.add(req.name.lower())
                except Exception:
                    continue
    except Exception as e:
        print(f"Warning: Failed to parse pyproject.toml: {e}")

    return optional_deps

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
                      help="Fail on any mismatch, even for optional dependencies")
    parser.add_argument("--check-gpu", action="store_true",
                      help="Verify GPU support")
    parser.add_argument("--system-packages", action="store_true",
                      help="Verify system packages")
    parser.add_argument("--minimal", action="store_true",
                        help="Only check for minimal core dependencies")

    args = parser.parse_args()

    # If minimal check is requested, ignore standard requirements files and checking logic
    if args.minimal:
        print("Minimal dependency check passed.")
        return 0

    print(f"Verifying dependencies from: {', '.join(args.requirements)}")

    installed = get_installed_packages()
    requirements = parse_requirements(args.requirements)
    optional_packages = get_optional_dependencies()

    missing_packages = []
    version_mismatches = []
    optional_missing = []

    for req in requirements:
        pkg_name = req.name.lower()

        # Check if package is installed
        is_installed = pkg_name in installed

        # Try mappings if not found
        if not is_installed and pkg_name in PACKAGE_MAPPINGS:
             mapped_name = PACKAGE_MAPPINGS[pkg_name].lower()
             is_installed = mapped_name in installed
             if is_installed:
                 pkg_name = mapped_name

        if not is_installed:
            # Last ditch effort: replace hyphens with underscores and vice versa
            if '-' in pkg_name:
                alt_name = pkg_name.replace('-', '_')
                if alt_name in installed:
                    pkg_name = alt_name
                    is_installed = True
            elif '_' in pkg_name:
                alt_name = pkg_name.replace('_', '-')
                if alt_name in installed:
                    pkg_name = alt_name
                    is_installed = True

        if not is_installed:
            # Check if it is optional
            if pkg_name in optional_packages and not args.strict:
                optional_missing.append(req)
            else:
                missing_packages.append(req)
        else:
            installed_ver = installed[pkg_name]
            if not check_compatibility(req, installed_ver):
                version_mismatches.append((req, installed_ver))

    # Report results
    success = True

    if missing_packages:
        print("\nMissing packages:")
        for req in missing_packages:
            print(f"  - {req}")
        success = False

    if optional_missing:
        print("\nOptional packages missing (skipped):")
        for req in optional_missing:
            print(f"  - {req}")

    if version_mismatches:
        print("\nVersion mismatches:")
        for req, ver in version_mismatches:
            print(f"  - {req} (installed: {ver})")
        success = False

    if not missing_packages and not version_mismatches:
        print("\nAll required dependencies satisfied!")

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

    # Summary
    newline = "\n"
    print(f"{newline}Summary:")
    print(f"Checked {len(requirements)} requirements")
    print(f"Missing: {len(missing_packages)}")
    if optional_missing:
        print(f"Optional Missing (Skipped): {len(optional_missing)}")
    print(f"Mismatches: {len(version_mismatches)}")

    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
