#!/usr/bin/env python3
"""
Dependency Verification and Testing Script

This script verifies that project dependencies work correctly in system-managed
Python environments while minimizing unnecessary downloads of large packages.

Usage:
    python scripts/verify-dependencies.py [--check-gpu] [--minimal] [--system-packages]

Options:
    --check-gpu      Check for GPU availability and CUDA dependencies
    --minimal        Test with minimal dependency set (no ML/AI packages)
    --system-packages Check if system packages can be used instead of pip installs
"""

import sys
import subprocess
import importlib
import platform
from typing import Dict, List, Set, Tuple

class DependencyVerifier:
    """Verify and test project dependencies for system-managed Python environments."""

    def __init__(self):
        self.system = platform.system().lower()
        self.python_version = sys.version_info
        self.has_gpu = self._check_gpu_availability()
        self.system_packages = self._detect_system_packages()

    def _check_gpu_availability(self) -> bool:
        """Check if GPU/CUDA is available on the system."""
        try:
            # Check for NVIDIA GPU
            result = subprocess.run(['nvidia-smi'], capture_output=True, text=True)
            if result.returncode == 0:
                return True
        except (subprocess.SubprocessError, FileNotFoundError):
            pass

        try:
            # Check for CUDA
            import torch
            return torch.cuda.is_available()
        except ImportError:
            pass

        return False

    def _detect_system_packages(self) -> Set[str]:
        """Detect available system packages that could replace pip installs."""
        system_packages = set()

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

        requirements_content = f"""# Conditional Requirements for EmailIntelligence
# Generated by verify-dependencies.py

# Base requirements (always needed)
{"\\n".join(f"{req}>=1.0.0" for req in base_reqs)}

# CPU-only ML/AI packages (optional)
# Uncomment the following for full ML functionality:
# {"\\n# ".join(f"{req}>=1.0.0" for req in categories['ml'])}

# Data science packages (optional)
# Uncomment the following for data analysis features:
# {"\\n# ".join(f"{req}>=1.0.0" for req in categories['data'])}

# Database packages (optional - based on features used)
# Uncomment the following for database functionality:
# {"\\n# ".join(f"{req}>=1.0.0" for req in categories['database'])}

# GPU/CUDA packages (only if GPU available)
# DO NOT install on CPU-only systems - very large downloads!
# {"\\n# ".join(f"{req}>=1.0.0" for req in categories['gpu'])}
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
            print(f"\\n🎮 GPU Status: {'Available' if self.has_gpu else 'Not detected'}")
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


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Verify EmailIntelligence dependencies")
    parser.add_argument('--check-gpu', action='store_true',
                       help='Check for GPU availability and CUDA dependencies')
    parser.add_argument('--minimal', action='store_true',
                       help='Test with minimal dependency set (no ML/AI packages)')
    parser.add_argument('--system-packages', action='store_true',
                       help='Check if system packages can be used instead of pip installs')

    args = parser.parse_args()

    verifier = DependencyVerifier()
    verifier.run_verification(
        check_gpu=args.check_gpu,
        minimal=args.minimal,
        system_packages=args.system_packages
    )


if __name__ == '__main__':
    main()