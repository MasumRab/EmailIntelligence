#!/usr/bin/env python3
"""
Quick Start Guide: Production-Ready Task Validator

This script demonstrates the basic usage of the production-ready task validator
with security fixes, atomic operations, and robust error handling.
"""

import os
import json
from pathlib import Path

def create_sample_task_file():
    """Create a sample task file for testing"""
    sample_tasks = {
        "tasks": [
            {
                "id": 1,
                "title": "Sample Task 1",
                "status": "pending",
                "description": "This is a sample task for testing"
            },
            {
                "id": 2,
                "title": "Sample Task 2", 
                "status": "in-progress",
                "dependencies": [1]
            },
            {
                "id": 3,
                "title": "Sample Task 3",
                "status": "completed"
            }
        ]
    }
    
    with open('sample_tasks.json', 'w') as f:
        json.dump(sample_tasks, f, indent=2)
    
    print("✓ Created sample_tasks.json")

def create_corrupted_task_file():
    """Create a corrupted task file to demonstrate validation"""
    corrupted_content = """{
    "tasks": [
        {
            "id": 1,
            "title": "Corrupted Task",
            "status": "invalid_status"
        },
        {
            "title": "Missing ID Task",
            "status": "pending"
        }
    ]
}"""
    
    with open('corrupted_tasks.json', 'w') as f:
        f.write(corrupted_content)
    
    print("✓ Created corrupted_tasks.json")

def demonstrate_basic_usage():
    """Demonstrate basic usage of the validator"""
    print("\n" + "="*60)
    print("DEMONSTRATING BASIC USAGE")
    print("="*60)
    
    print("\n1. Validating a single file:")
    print("   python task_validator_fixer_production.py sample_tasks.json")
    
    print("\n2. Validating and auto-fixing a file:")
    print("   python task_validator_fixer_production.py corrupted_tasks.json --auto-fix")
    
    print("\n3. Batch processing multiple files:")
    print("   python task_validator_fixer_production.py --batch sample_tasks.json corrupted_tasks.json")
    
    print("\n4. Finding and validating all task files in project:")
    print("   python task_validator_fixer_production.py --find-all")

def demonstrate_advanced_usage():
    """Demonstrate advanced usage features"""
    print("\n" + "="*60)
    print("ADVANCED USAGE FEATURES")
    print("="*60)
    
    print("\n• Validate only (no fixes):")
    print("  python task_validator_fixer_production.py tasks.json --validate-only")
    
    print("\n• Specify project root:")
    print("  python task_validator_fixer_production.py tasks.json --project-root /path/to/project")
    
    print("\n• Process with specific file pattern:")
    print("  (This would be done programmatically in a script)")

def show_security_features():
    """Highlight security features"""
    print("\n" + "="*60)
    print("KEY SECURITY FEATURES")
    print("="*60)
    
    features = [
        "✓ Path validation prevents directory traversal attacks",
        "✓ File size limits prevent resource exhaustion",
        "✓ Atomic operations prevent file corruption",
        "✓ Automatic backups before modifications",
        "✓ Thread-safe file operations",
        "✓ Input validation and sanitization",
        "✓ Merge conflict detection",
        "✓ Working directory restriction"
    ]
    
    for feature in features:
        print(f"  {feature}")

def main():
    """Main demonstration function"""
    print("Production-Ready Task Validator - Quick Start Guide")
    print("="*60)
    
    # Create sample files
    create_sample_task_file()
    create_corrupted_task_file()
    
    # Show security features
    show_security_features()
    
    # Demonstrate usage
    demonstrate_basic_usage()
    demonstrate_advanced_usage()
    
    print("\n" + "="*60)
    print("NEXT STEPS")
    print("="*60)
    print("1. Review the security analysis documentation")
    print("2. Test with your actual task files")
    print("3. Integrate into your CI/CD pipeline")
    print("4. Configure for your specific project needs")
    
    print(f"\nFiles created in current directory:")
    print(f"  - sample_tasks.json (valid tasks)")
    print(f"  - corrupted_tasks.json (invalid tasks for testing)")
    print(f"  - task_validator_fixer_production.py (the validator script)")
    print(f"  - task_validator_fixer_security_analysis.md (security details)")
    print(f"  - task_validator_fixer_security_summary.md (security summary)")

if __name__ == "__main__":
    main()