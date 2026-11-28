#!/usr/bin/env python3
"""
Performance Testing Script for EmailIntelligence Dependencies

This script analyzes installation performance without actually installing packages.
It estimates download sizes, installation times, and disk usage for different
dependency configurations.
"""

import json
import time
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Any
import requests


class PerformanceTester:
    """Test installation performance for different dependency sets."""

    def __init__(self):
        self.package_sizes = self._load_package_sizes()
        self.test_results = {}

    def _load_package_sizes(self) -> Dict[str, int]:
        """Load approximate package sizes in MB."""
        # Approximate sizes based on common installations
        return {
            # Core dependencies
            'fastapi': 15,
            'pydantic': 25,
            'uvicorn': 8,
            'python-dotenv': 2,
            'httpx': 12,
            'email-validator': 3,
            'aiosqlite': 2,
            'gradio': 45,
            'pyngrok': 5,

            # ML dependencies
            'torch': 1800,  # CPU version
            'torch[cuda]': 3500,  # CUDA version
            'transformers': 1200,
            'accelerate': 150,
            'sentencepiece': 25,
            'scikit-learn': 85,
            'nltk': 12,
            'textblob': 8,

            # Data science
            'pandas': 35,
            'numpy': 25,
            'scipy': 45,
            'matplotlib': 35,
            'seaborn': 15,
            'plotly': 45,

            # Database
            'psycopg2-binary': 8,
            'redis': 5,
            'notmuch': 12,

            # Development
            'pytest': 25,
            'black': 8,
            'flake8': 5,
            'mypy': 35,
            'pylint': 25,
            'isort': 5,
        }

    def get_dependency_sets(self) -> Dict[str, List[str]]:
        """Get different dependency configurations to test."""
        return {
            'minimal': [
                'fastapi', 'pydantic', 'uvicorn', 'python-dotenv',
                'httpx', 'email-validator', 'aiosqlite', 'gradio', 'pyngrok'
            ],
            'ml-cpu': [
                'fastapi', 'pydantic', 'uvicorn', 'python-dotenv', 'httpx',
                'email-validator', 'aiosqlite', 'gradio', 'pyngrok',
                'torch', 'transformers', 'accelerate', 'sentencepiece',
                'scikit-learn', 'nltk', 'textblob'
            ],
            'ml-gpu': [
                'fastapi', 'pydantic', 'uvicorn', 'python-dotenv', 'httpx',
                'email-validator', 'aiosqlite', 'gradio', 'pyngrok',
                'torch[cuda]', 'transformers', 'accelerate', 'sentencepiece',
                'scikit-learn', 'nltk', 'textblob'
            ],
            'data-science': [
                'fastapi', 'pydantic', 'uvicorn', 'python-dotenv', 'httpx',
                'email-validator', 'aiosqlite', 'gradio', 'pyngrok',
                'pandas', 'numpy', 'scipy', 'matplotlib', 'seaborn', 'plotly'
            ],
            'full-cpu': [
                'fastapi', 'pydantic', 'uvicorn', 'python-dotenv', 'httpx',
                'email-validator', 'aiosqlite', 'gradio', 'pyngrok',
                'torch', 'transformers', 'accelerate', 'sentencepiece',
                'scikit-learn', 'nltk', 'textblob',
                'pandas', 'numpy', 'scipy', 'matplotlib', 'seaborn', 'plotly',
                'psycopg2-binary', 'redis', 'notmuch'
            ],
            'development': [
                'fastapi', 'pydantic', 'uvicorn', 'python-dotenv', 'httpx',
                'email-validator', 'aiosqlite', 'gradio', 'pyngrok',
                'torch', 'transformers', 'accelerate', 'sentencepiece',
                'scikit-learn', 'nltk', 'textblob',
                'pandas', 'numpy', 'scipy', 'matplotlib', 'seaborn', 'plotly',
                'psycopg2-binary', 'redis', 'notmuch',
                'pytest', 'black', 'flake8', 'mypy', 'pylint', 'isort'
            ]
        }

    def estimate_installation_time(self, packages: List[str], bandwidth_mbps: int = 50) -> Dict[str, Any]:
        """Estimate installation time based on package sizes and bandwidth."""
        total_size_mb = sum(self.package_sizes.get(pkg, 10) for pkg in packages)
        total_size_gb = total_size_mb / 1024

        # Estimate download time (bandwidth in MB/s)
        bandwidth_mbs = (bandwidth_mbps * 1024 * 1024) / (8 * 1024 * 1024)  # Convert Mbps to MB/s
        download_time_seconds = total_size_mb / bandwidth_mbs if bandwidth_mbs > 0 else 0

        # Estimate installation time (rough heuristic: 2 seconds per 100MB)
        install_time_seconds = (total_size_mb / 100) * 2

        # Estimate disk usage (actual installed size is ~2-3x download size)
        installed_size_mb = total_size_mb * 2.5
        installed_size_gb = installed_size_mb / 1024

        return {
            'download_size_mb': total_size_mb,
            'download_size_gb': total_size_gb,
            'installed_size_mb': installed_size_mb,
            'installed_size_gb': installed_size_gb,
            'download_time_seconds': download_time_seconds,
            'download_time_minutes': download_time_seconds / 60,
            'install_time_seconds': install_time_seconds,
            'install_time_minutes': install_time_seconds / 60,
            'total_time_seconds': download_time_seconds + install_time_seconds,
            'total_time_minutes': (download_time_seconds + install_time_seconds) / 60,
            'bandwidth_assumed_mbps': bandwidth_mbps,
            'package_count': len(packages)
        }

    def check_system_resources(self) -> Dict[str, Any]:
        """Check current system resources."""
        try:
            # Check disk space
            result = subprocess.run(['df', '.'], capture_output=True, text=True)
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                if len(lines) >= 2:
                    parts = lines[1].split()
                    if len(parts) >= 4:
                        disk_free_kb = int(parts[3])
                        disk_free_gb = disk_free_kb / (1024 * 1024)
                    else:
                        disk_free_gb = 0
                else:
                    disk_free_gb = 0
            else:
                disk_free_gb = 0
        except:
            disk_free_gb = 0

        try:
            # Check memory
            with open('/proc/meminfo', 'r') as f:
                mem_lines = f.readlines()
                mem_total_kb = int(mem_lines[0].split()[1])
                mem_free_kb = int([l for l in mem_lines if 'MemFree' in l][0].split()[1])
                mem_total_gb = mem_total_kb / (1024 * 1024)
                mem_free_gb = mem_free_kb / (1024 * 1024)
        except:
            mem_total_gb = mem_free_gb = 0

        return {
            'disk_free_gb': disk_free_gb,
            'memory_total_gb': mem_total_gb,
            'memory_free_gb': mem_free_gb
        }

    def run_performance_tests(self) -> Dict[str, Any]:
        """Run performance tests for all dependency sets."""
        print("🚀 EmailIntelligence Performance Testing")
        print("=" * 50)

        dependency_sets = self.get_dependency_sets()
        system_resources = self.check_system_resources()

        print("📊 System Resources:")
        print(f"  💾 Disk Free: {system_resources['disk_free_gb']:.1f}GB")
        print(f"  🧠 Memory Total: {system_resources['memory_total_gb']:.1f}GB")
        print(f"  🧠 Memory Free: {system_resources['memory_free_gb']:.1f}GB")
        print()

        results = {
            'system_resources': system_resources,
            'dependency_sets': {},
            'recommendations': []
        }

        for name, packages in dependency_sets.items():
            print(f"🔍 Testing {name} configuration...")
            estimates = self.estimate_installation_time(packages)

            results['dependency_sets'][name] = {
                'packages': packages,
                'estimates': estimates
            }

            print(f"  📦 Packages: {len(packages)}")
            print(f"  💾 Download: {estimates['download_size_gb']:.1f}GB")
            print(f"  💾 Installed: {estimates['installed_size_gb']:.1f}GB")
            print(f"  ⏱️  Total Time: {estimates['total_time_minutes']:.1f} minutes")
            print(f"  📡 Assumed bandwidth: {estimates['bandwidth_assumed_mbps']} Mbps")
            print()

            # Check if system has enough resources
            if estimates['installed_size_gb'] > system_resources['disk_free_gb']:
                results['recommendations'].append(
                    f"⚠️  {name} requires {estimates['installed_size_gb']:.1f}GB disk space, "
                    f"but only {system_resources['disk_free_gb']:.1f}GB available"
                )

        # Generate recommendations
        print("💡 Recommendations:")
        for rec in results['recommendations']:
            print(f"  {rec}")

        if not results['recommendations']:
            print("  ✅ All configurations should fit within system resources")

        print()
        print("🎯 Performance Summary:")
        minimal = results['dependency_sets']['minimal']['estimates']
        full = results['dependency_sets']['development']['estimates']

        savings_gb = full['download_size_gb'] - minimal['download_size_gb']
        savings_time = full['total_time_minutes'] - minimal['total_time_minutes']

        print(f"  💰 Minimal vs Full savings: {savings_gb:.1f}GB download, {savings_time:.1f} minutes")
        print(f"  🎯 Minimal installation: {minimal['download_size_gb']:.1f}GB, {minimal['total_time_minutes']:.1f} min")
        print(f"  📦 Full installation: {full['download_size_gb']:.1f}GB, {full['total_time_minutes']:.1f} min")

        return results

    def save_results(self, results: Dict[str, Any], output_file: str = 'performance-results.json'):
        """Save performance test results to file."""
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"  ✅ Results saved to {output_file}")


def main():
    """Main entry point."""
    tester = PerformanceTester()
    results = tester.run_performance_tests()
    tester.save_results(results)


if __name__ == '__main__':
    main()
