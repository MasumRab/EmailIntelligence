#!/usr/bin/env python3
"""
Test script for the project configuration system.
Run this to verify that the configuration system works correctly.
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from setup.project_config import get_project_config, ProjectConfig

def test_config():
    """Test the project configuration system."""
    print("Testing Project Configuration System")
    print("=" * 40)

    # Test configuration loading
    config = get_project_config()
    print(f"Project root: {config.root_dir}")
    print(f"Backend path: {config.paths.backend}")
    print(f"Client path: {config.paths.client}")
    print(f"Python backend path: {config.paths.python_backend}")

    # Test critical files discovery
    critical_files = config.get_critical_files()
    print(f"\nCritical files ({len(critical_files)}):")
    for file in sorted(critical_files):
        print(f"  - {file}")

    # Test service discovery
    services = config.discover_services()
    print(f"\nDiscovered services ({len(services)}):")
    for service_name, service_info in services.items():
        print(f"  - {service_name}: {service_info}")

    # Test structure validation
    issues = config.validate_structure()
    if issues:
        print(f"\nStructure validation issues ({len(issues)}):")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print("\nStructure validation: PASSED")

    # Test service configurations
    print("\nService configurations:")
    for service_name in ["python_backend", "typescript_backend", "frontend"]:
        service_config = config.get_service_config(service_name)
        service_path = config.get_service_path(service_name)
        if service_config:
            exists = service_path.exists() if service_path else False
            print(f"  - {service_name}: {service_config['path']} ({'EXISTS' if exists else 'MISSING'})")
        else:
            print(f"  - {service_name}: NOT CONFIGURED")

    print("\nConfiguration test completed!")

if __name__ == "__main__":
    test_config()