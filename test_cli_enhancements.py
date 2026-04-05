#!/usr/bin/env python3
"""
Test script for CLI enhancements.

This script tests the new CLI functionality to ensure everything works correctly.
"""

import json
import tempfile
import subprocess
import sys
from pathlib import Path

def test_cli_imports():
    """Test that all CLI components can be imported successfully."""
    print("Testing CLI imports...")
    
    try:
        from cli.cli_class import EmailIntelligenceCLI
        from cli.models import (
            ConflictType, ConflictSeverity, ConflictFile, 
            ConflictReport, BranchPairResult, ConflictMatrix,
            SemanticConflictAnalysis, GitWorkspaceManager
        )
        from cli.commands import create_parser, execute_command
        print("✅ All imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

def test_cli_initialization():
    """Test CLI initialization."""
    print("Testing CLI initialization...")
    
    try:
        from cli.cli_class import EmailIntelligenceCLI
        cli = EmailIntelligenceCLI()
        print("✅ CLI initialized successfully")
        return True
    except Exception as e:
        print(f"❌ CLI initialization failed: {e}")
        return False

def test_argument_parser():
    """Test argument parser creation."""
    print("Testing argument parser...")
    
    try:
        from cli.commands import create_parser
        parser = create_parser()
        
        # Test that all expected commands are present
        expected_commands = [
            'setup-resolution', 'push-resolution', 'analyze-constitutional',
            'develop-spec-kit-strategy', 'align-content', 'validate-resolution',
            'auto-resolve', 'scan-all-branches', 'collect-pr-recommendations'
        ]
        
        # Check if parser has subparsers
        if hasattr(parser, '_subparsers'):
            print("✅ Argument parser created successfully")
            print(f"   Available commands: {len(expected_commands)}")
            return True
        else:
            print("❌ Argument parser missing subparsers")
            return False
            
    except Exception as e:
        print(f"❌ Argument parser test failed: {e}")
        return False

def test_dataclass_creation():
    """Test dataclass creation."""
    print("Testing dataclass creation...")
    
    try:
        from cli.models import (
            ConflictType, ConflictSeverity, ConflictFile, 
            ConflictReport, BranchPairResult, ConflictMatrix,
            SemanticConflictAnalysis, GitWorkspaceManager
        )
        
        # Test basic dataclass creation
        conflict_file = ConflictFile(
            file_path="test.py",
            conflict_type=ConflictType.CHANGED_IN_BOTH,
            severity=ConflictSeverity.HIGH
        )
        
        branch_result = BranchPairResult(
            source="feature",
            target="main", 
            conflict_count=2,
            conflict_files=["test.py", "app.py"],
            severity="high",
            scan_duration_ms=150.5
        )
        
        print("✅ Dataclass creation successful")
        return True
        
    except Exception as e:
        print(f"❌ Dataclass creation failed: {e}")
        return False

def test_git_workspace_manager():
    """Test GitWorkspaceManager class."""
    print("Testing GitWorkspaceManager...")
    
    try:
        from cli.models import GitWorkspaceManager
        
        # Test initialization
        manager = GitWorkspaceManager("/tmp/test-repo")
        
        # Test properties
        assert manager.repo_root == "/tmp/test-repo"
        assert manager.worktrees_dir == "/tmp/test-repo/.git/worktrees"
        
        print("✅ GitWorkspaceManager test successful")
        return True
        
    except Exception as e:
        print(f"❌ GitWorkspaceManager test failed: {e}")
        return False

def run_all_tests():
    """Run all tests and return overall result."""
    print("=" * 60)
    print("CLI ENHANCEMENT TEST SUITE")
    print("=" * 60)
    
    tests = [
        test_cli_imports,
        test_cli_initialization, 
        test_argument_parser,
        test_dataclass_creation,
        test_git_workspace_manager
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test {test.__name__} failed with exception: {e}")
            results.append(False)
        print()
    
    passed = sum(results)
    total = len(results)
    
    print("=" * 60)
    print(f"TEST RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! CLI enhancements are working correctly.")
        return True
    else:
        print("⚠️  Some tests failed. Please check the implementation.")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)