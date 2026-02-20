#!/usr/bin/env python3
"""
Test script to verify agent onboarding guide content
"""

import os
from pathlib import Path

def test_onboarding_guide_exists():
    """Test that the onboarding guide exists."""
    guide_path = Path("docs/agent_onboarding_guide.md")
    assert guide_path.exists(), "Agent onboarding guide should exist"
    print("✓ Onboarding guide exists")

def test_onboarding_guide_content():
    """Test that the onboarding guide contains required sections."""
    guide_path = Path("docs/agent_onboarding_guide.md")
    
    with open(guide_path, 'r') as f:
        content = f.read()
    
    # Check for required sections
    required_sections = [
        "System Architecture Overview",
        "Agent Roles and Capabilities",
        "Getting Started",
        "Documentation Generation Workflow",
        "Review Process",
        "Translation Workflow",
        "Maintenance Tasks",
        "Performance Expectations",
        "Best Practices",
        "Troubleshooting"
    ]
    
    for section in required_sections:
        assert section in content, f"Guide should contain section: {section}"
    
    print("✓ All required sections are present")
    
    # Check for agent-specific content
    required_content = [
        "DocumentationTemplate",
        "ConcurrentReviewManager",
        "DistributedTranslationManager",
        "MaintenanceAgent",
        "register_agent",
        "create_document",
        "add_comment",
        "start_translation_job"
    ]
    
    for item in required_content:
        assert item in content, f"Guide should contain: {item}"
        
    print("✓ All required content is present")

def test_onboarding_guide_format():
    """Test that the onboarding guide follows proper formatting."""
    guide_path = Path("docs/agent_onboarding_guide.md")
    
    with open(guide_path, 'r') as f:
        lines = f.readlines()
    
    # Check that it starts with a title
    assert lines[0].startswith("# "), "Guide should start with a main title"
    
    # Check for table of contents
    toc_found = False
    for line in lines:
        if "Table of Contents" in line:
            toc_found = True
            break
    
    assert toc_found, "Guide should contain a table of contents"
    print("✓ Proper formatting is used")

def main():
    """Run all tests."""
    print("Testing Agent Onboarding Guide")
    print("=" * 32)
    
    try:
        test_onboarding_guide_exists()
        test_onboarding_guide_content()
        test_onboarding_guide_format()
        
        print("\n" + "=" * 32)
        print("All tests passed! ✓")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        raise

if __name__ == "__main__":
    main()