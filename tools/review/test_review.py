#!/usr/bin/env python3
"""
Test script for the Multi-Agent Code Review System
"""

import sys
from pathlib import Path

# Add project root to path
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

# Add tools to path
TOOLS_DIR = ROOT_DIR / "tools"
sys.path.insert(0, str(TOOLS_DIR))

from review import MultiAgentCodeReview


def test_review_system():
    """Test the review system with a small set of files."""
    print("Testing Multi-Agent Code Review System...")
    
    # Initialize the review system
    review_system = MultiAgentCodeReview()
    
    # Test with a small set of files
    test_files = [
        "launch.py",
        "backend/python_backend/main.py",
        "src/main.py"
    ]
    
    # Convert to absolute paths
    absolute_test_files = [str(ROOT_DIR / f) for f in test_files if (ROOT_DIR / f).exists()]
    
    if not absolute_test_files:
        print("No test files found. Using all Python files in the project.")
        absolute_test_files = None
    
    # Run the review
    results = review_system.run_review(absolute_test_files)
    
    # Generate and print report
    report = review_system.generate_report(results, format="console")
    print(report)
    
    # Save report
    review_system.save_report(report, "markdown", str(ROOT_DIR / "CODE_REVIEW_REPORT.md"))
    
    print("\nReview completed. Report saved to CODE_REVIEW_REPORT.md")


if __name__ == "__main__":
    test_review_system()