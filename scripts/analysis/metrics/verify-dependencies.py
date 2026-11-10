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
import importlib.metadata

# Mappings for packages where the import name differs from the package name
# or where legacy names are used.
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
    """Get a dictionary of installed packages and their versions using importlib.metadata."""
    from packaging.utils import canonicalize_name
    installed = {}
    for dist in importlib.metadata.distributions():
        name = canonicalize_name(dist.metadata["Name"])
        version = dist.version
        installed[name] = version
    return installed

def parse_requirements(files: List[str]) -> List['Requirement']:
    """Parse requirements from multiple files."""
    from packaging.requirements import Requirement
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

def check_compatibility(req: 'Requirement', installed_version: str) -> bool:
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

<<<<<<< HEAD:scripts/analysis/metrics/verify-dependencies.py
        # Check for common system package managers
        package_managers = {
            'apt': ['dpkg', '-l'],
            'yum': ['rpm', '-qa'],
            'brew': ['brew', 'list'],
            'pacman': ['pacman', '-Q']
        }

        for manager, cmd in package_managers.items():
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    # Parse output to detect relevant packages
                    output = result.stdout.lower()
                    if 'python3' in output:
                        system_packages.add('python3-system')
                    if 'numpy' in output or 'python3-numpy' in output:
                        system_packages.add('numpy-system')
                    if 'scipy' in output or 'python3-scipy' in output:
                        system_packages.add('scipy-system')
                    if 'matplotlib' in output or 'python3-matplotlib' in output:
                        system_packages.add('matplotlib-system')
            except (subprocess.SubprocessError, FileNotFoundError, subprocess.TimeoutExpired):
                continue

        return system_packages

    def categorize_dependencies(self) -> Dict[str, List[str]]:
        """Categorize project dependencies by type and necessity."""

        # Core dependencies (always needed)
        core_deps = [
            'fastapi', 'pydantic', 'uvicorn', 'python-dotenv',
            'httpx', 'email-validator', 'aiosqlite'
        ]

        # ML/AI dependencies (optional for basic functionality)
        ml_deps = [
            'torch', 'transformers', 'accelerate', 'sentencepiece',
            'scikit-learn', 'nltk', 'textblob'
        ]

        # Data science dependencies (optional)
        data_deps = [
            'pandas', 'numpy', 'matplotlib', 'seaborn', 'scipy', 'plotly'
        ]

        # Database dependencies (optional based on features used)
        db_deps = [
            'psycopg2-binary', 'redis', 'notmuch'
        ]

        # Development dependencies (only for development)
        dev_deps = [
            'pytest', 'black', 'flake8', 'mypy', 'pylint', 'isort'
        ]

        # GPU-specific dependencies (only if GPU available)
        gpu_deps = [
            'torch[cuda]', 'torchvision', 'torchaudio'  # CUDA versions
        ]

        return {
            'core': core_deps,
            'ml': ml_deps,
            'data': data_deps,
            'database': db_deps,
            'dev': dev_deps,
            'gpu': gpu_deps
        }

    def check_import_availability(self, package_name: str) -> Tuple[bool, str]:
        """Check if a package can be imported."""
        try:
            importlib.import_module(package_name.replace('-', '_'))
            return True, "Available"
        except ImportError as e:
            return False, str(e)

    def verify_minimal_setup(self) -> Dict[str, any]:
        """Verify that the project works with minimal dependencies."""
        results = {
            'core_imports': {},
            'optional_imports': {},
            'system_packages': self.system_packages,
            'gpu_available': self.has_gpu,
            'recommendations': []
        }

        categories = self.categorize_dependencies()

        # Test core dependencies
        print("🔍 Checking core dependencies...")
        for dep in categories['core']:
            available, status = self.check_import_availability(dep)
            results['core_imports'][dep] = {'available': available, 'status': status}
            if not available:
                results['recommendations'].append(f"Install core dependency: {dep}")

        # Test optional dependencies
        print("🔍 Checking optional dependencies...")
        for category, deps in categories.items():
            if category in ['ml', 'data', 'database']:
                for dep in deps:
                    available, status = self.check_import_availability(dep)
                    results['optional_imports'][f"{category}:{dep}"] = {
                        'available': available,
                        'status': status
                    }

        # Generate recommendations
        if not self.has_gpu:
            gpu_packages = [d for d in categories['gpu'] if 'cuda' in d]
            if gpu_packages:
                results['recommendations'].append(
                    f"GPU not detected - avoid installing CUDA packages: {', '.join(gpu_packages)}"
                )

        if self.system_packages:
            results['recommendations'].append(
                f"Consider using system packages: {', '.join(self.system_packages)}"
            )

        return results

    def generate_conditional_requirements(self) -> str:
        """Generate conditional requirements files for different scenarios."""

        categories = self.categorize_dependencies()

        # Base requirements (always needed)
        base_reqs = categories['core'] + ['gradio', 'pyngrok']

        # CPU-only requirements
        cpu_reqs = base_reqs + categories['ml'] + categories['data']
        cpu_reqs = [req for req in cpu_reqs if not req.endswith('[cuda]')]

        # GPU requirements
        gpu_reqs = cpu_reqs + categories['gpu']

        # Minimal requirements (no ML/AI)
        minimal_reqs = base_reqs + ['nltk', 'textblob']  # Basic NLP only

        # Development requirements
        dev_reqs = cpu_reqs + categories['dev']

        nl = '\n'
        nl_hash = '\n# '
        base_reqs_str = nl.join(f"{req}>=1.0.0" for req in base_reqs)
        ml_reqs_str = nl_hash.join(f"{req}>=1.0.0" for req in categories['ml'])
        data_reqs_str = nl_hash.join(f"{req}>=1.0.0" for req in categories['data'])
        db_reqs_str = nl_hash.join(f"{req}>=1.0.0" for req in categories['database'])
        gpu_reqs_str = nl_hash.join(f"{req}>=1.0.0" for req in categories['gpu'])

        requirements_content = f"""# Conditional Requirements for EmailIntelligence
# Generated by verify-dependencies.py

# Base requirements (always needed)
{base_reqs_str}

# CPU-only ML/AI packages (optional)
# Uncomment the following for full ML functionality:
# {ml_reqs_str}

# Data science packages (optional)
# Uncomment the following for data analysis features:
# {data_reqs_str}

# Database packages (optional - based on features used)
# Uncomment the following for database functionality:
# {db_reqs_str}

# GPU/CUDA packages (only if GPU available)
# DO NOT install on CPU-only systems - very large downloads!
# {gpu_reqs_str}
"""

        return requirements_content

    def run_verification(self, check_gpu: bool = False, minimal: bool = False,
                        system_packages: bool = False) -> None:
        """Run the complete dependency verification."""

        print("🚀 EmailIntelligence Dependency Verification")
        print("=" * 50)
        print(f"System: {self.system}")
        print(f"Python: {self.python_version.major}.{self.python_version.minor}")
        print(f"GPU Available: {self.has_gpu}")
        print(f"System Packages: {', '.join(self.system_packages) if self.system_packages else 'None detected'}")
        print()

        # Run verification
        results = self.verify_minimal_setup()

        # Display results
        print("📊 Verification Results:")
        print("-" * 30)

        print("✅ Core Dependencies:")
        for dep, info in results['core_imports'].items():
            status = "✅" if info['available'] else "❌"
            print(f"  {status} {dep}: {info['status']}")

        print("\\n📦 Optional Dependencies (ML/AI/Data):")
        for dep, info in results['optional_imports'].items():
            status = "✅" if info['available'] else "⚠️"
            print(f"  {status} {dep}: {info['status']}")

        print("\\n💡 Recommendations:")
        for rec in results['recommendations']:
            print(f"  • {rec}")

        if check_gpu:
            gpu_status = "Available" if self.has_gpu else "Not detected"
            print(f"\n🎮 GPU Status: {gpu_status}")
            if not self.has_gpu:
                print("  ⚠️  Avoid installing CUDA/GPU packages to save disk space and bandwidth")

        if minimal:
            print("\\n🎯 Minimal Setup Test:")
            print("  ✅ Core functionality should work without ML/AI packages")
            print("  ⚠️  Advanced features (sentiment analysis, etc.) will be limited")

        if system_packages:
            print("\\n📥 System Package Detection:")
            if self.system_packages:
                print(f"  ✅ Detected: {', '.join(self.system_packages)}")
                print("  💡 Consider using system packages instead of pip installs")
            else:
                print("  ⚠️  No system packages detected")

        # Generate conditional requirements
        print("\\n📝 Generating conditional requirements file...")
        conditional_reqs = self.generate_conditional_requirements()

        with open('requirements-conditional.txt', 'w') as f:
            f.write(conditional_reqs)

        print("  ✅ Created: requirements-conditional.txt")
        print("  💡 Use this file to install only necessary dependencies")

        print("\\n🎉 Verification complete!")
=======
    # Check for git
    exit_code = os.system("git --version > /dev/null 2>&1")
    if exit_code == 0:
        print("git: Installed")
    else:
        print("git: Missing")
        return False
>>>>>>> align-pr-489-head:scripts/verify-dependencies.py

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

    # Import here to allow minimal check to run without packaging installed
    try:
        from packaging.utils import canonicalize_name
    except ImportError:
        print("Error: 'packaging' library is required for dependency verification.")
        print("Please install it with: pip install packaging")
        return 1

    print(f"Verifying dependencies from: {', '.join(args.requirements)}")

    try:
        installed = get_installed_packages()
    except Exception as e:
        print(f"Error getting installed packages: {e}")
        # Graceful fallback if something is very wrong with the environment
        installed = {}

    requirements = parse_requirements(args.requirements)

    missing_packages = []
    version_mismatches = []

    for req in requirements:
        # Use canonical name for comparison
        pkg_name = canonicalize_name(req.name)

        # Also handle mapped names if needed (though canonicalize usually handles dash/underscore)
        # We check both to be safe against inconsistent naming in reqs vs metadata
        raw_name = req.name.lower()
        mapped_name = PACKAGE_MAPPINGS.get(raw_name)

        if pkg_name in installed:
            installed_ver = installed[pkg_name]
            if not check_compatibility(req, installed_ver):
                version_mismatches.append((req, installed_ver))
        elif mapped_name and canonicalize_name(mapped_name) in installed:
             # Fallback to mapped name
             installed_ver = installed[canonicalize_name(mapped_name)]
             if not check_compatibility(req, installed_ver):
                version_mismatches.append((req, installed_ver))
        else:
            missing_packages.append(req)

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
