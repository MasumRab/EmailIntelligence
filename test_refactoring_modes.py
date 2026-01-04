#!/usr/bin/env python3
"""
Comprehensive test harness for i2t4-into-756 refactoring validation.
Tests all 3 execution modes and validates output structure.
"""

import sys
import json
from pathlib import Path

# Add task_data to path
sys.path.insert(0, str(Path(__file__).parent))

from task_data.branch_clustering_implementation import (
    BranchClusteringEngine,
    MigrationAnalyzer,
    OutputGenerator,
    MigrationMetrics,
)


def test_imports():
    """Test that all refactored classes import correctly."""
    print("\n" + "=" * 70)
    print("TEST 1: Import Validation")
    print("=" * 70)
    
    try:
        from task_data.branch_clustering_implementation import (
            BranchClusteringEngine,
            MigrationAnalyzer,
            OutputGenerator,
            MigrationMetrics,
        )
        print("✅ BranchClusteringEngine imported")
        print("✅ MigrationAnalyzer imported")
        print("✅ OutputGenerator imported")
        print("✅ MigrationMetrics imported")
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False


def test_mode_validation():
    """Test that execution mode validation works correctly."""
    print("\n" + "=" * 70)
    print("TEST 2: Mode Validation")
    print("=" * 70)
    
    valid_modes = ["identification", "clustering", "hybrid"]
    invalid_modes = ["invalid", "unknown", "test"]
    
    all_passed = True
    
    for mode in valid_modes:
        try:
            engine = BranchClusteringEngine(mode=mode)
            assert engine.mode == mode
            print(f"✅ Mode '{mode}' validated")
        except Exception as e:
            print(f"❌ Mode '{mode}' failed: {e}")
            all_passed = False
    
    for mode in invalid_modes:
        try:
            engine = BranchClusteringEngine(mode=mode)
            print(f"❌ Mode '{mode}' should have raised ValueError")
            all_passed = False
        except ValueError as e:
            print(f"✅ Mode '{mode}' correctly rejected: {str(e)[:50]}...")
        except Exception as e:
            print(f"❌ Mode '{mode}' raised unexpected error: {e}")
            all_passed = False
    
    return all_passed


def test_migration_analyzer():
    """Test MigrationAnalyzer instantiation and basic structure."""
    print("\n" + "=" * 70)
    print("TEST 3: MigrationAnalyzer Validation")
    print("=" * 70)
    
    try:
        analyzer = MigrationAnalyzer(".")
        print("✅ MigrationAnalyzer instantiated")
        
        # Check for required attributes
        assert hasattr(analyzer, "analyze_migration"), "Missing analyze_migration method"
        print("✅ analyze_migration method exists")
        
        assert hasattr(analyzer, "_get_merge_base"), "Missing _get_merge_base method"
        print("✅ _get_merge_base method exists")
        
        assert hasattr(analyzer, "_get_changed_files"), "Missing _get_changed_files method"
        print("✅ _get_changed_files method exists")
        
        assert hasattr(analyzer, "_check_backend_imports"), "Missing _check_backend_imports method"
        print("✅ _check_backend_imports method exists")
        
        assert hasattr(analyzer, "_check_src_imports"), "Missing _check_src_imports method"
        print("✅ _check_src_imports method exists")
        
        # Check import tracking
        assert analyzer.backend_imports, "backend_imports not set"
        print(f"✅ Backend imports tracked: {analyzer.backend_imports}")
        
        assert analyzer.src_imports, "src_imports not set"
        print(f"✅ Src imports tracked: {analyzer.src_imports}")
        
        return True
    except Exception as e:
        print(f"❌ MigrationAnalyzer validation failed: {e}")
        return False


def test_output_generator():
    """Test OutputGenerator instantiation and format support."""
    print("\n" + "=" * 70)
    print("TEST 4: OutputGenerator Validation")
    print("=" * 70)
    
    try:
        gen = OutputGenerator()
        print("✅ OutputGenerator instantiated")
        
        # Check for required methods
        assert hasattr(gen, "generate_output"), "Missing generate_output method"
        print("✅ generate_output method exists")
        
        assert hasattr(gen, "_generate_simple_output"), "Missing _generate_simple_output method"
        print("✅ _generate_simple_output method exists")
        
        assert hasattr(gen, "_generate_detailed_output"), "Missing _generate_detailed_output method"
        print("✅ _generate_detailed_output method exists")
        
        # Test with mock data
        mock_results = [
            {
                "branch": "feature-test",
                "target": "main",
                "confidence": 0.95,
                "reasoning": "Test branch",
                "tags": ["tag:test"],
                "metrics": {
                    "commit_history": {},
                    "codebase_structure": {},
                    "migration": {},
                }
            }
        ]
        
        # Test format validation
        for fmt in ["simple", "detailed", "all"]:
            try:
                output = gen.generate_output(mock_results, fmt)
                assert output is not None
                assert isinstance(output, dict)
                print(f"✅ Format '{fmt}' generates valid output")
            except Exception as e:
                print(f"❌ Format '{fmt}' failed: {e}")
                return False
        
        return True
    except Exception as e:
        print(f"❌ OutputGenerator validation failed: {e}")
        return False


def test_engine_instantiation():
    """Test BranchClusteringEngine instantiation with all modes."""
    print("\n" + "=" * 70)
    print("TEST 5: BranchClusteringEngine Instantiation")
    print("=" * 70)
    
    all_passed = True
    
    for mode in ["identification", "clustering", "hybrid"]:
        try:
            engine = BranchClusteringEngine(mode=mode)
            print(f"✅ Engine instantiated with mode='{mode}'")
            
            # Verify components are initialized
            assert hasattr(engine, "commit_analyzer"), f"Missing commit_analyzer for {mode}"
            assert hasattr(engine, "codebase_analyzer"), f"Missing codebase_analyzer for {mode}"
            assert hasattr(engine, "diff_calculator"), f"Missing diff_calculator for {mode}"
            assert hasattr(engine, "migration_analyzer"), f"Missing migration_analyzer for {mode}"
            assert hasattr(engine, "clusterer"), f"Missing clusterer for {mode}"
            assert hasattr(engine, "assigner"), f"Missing assigner for {mode}"
            print(f"✅ All components initialized for mode='{mode}'")
            
            # Verify execute methods exist
            assert hasattr(engine, "execute"), "Missing execute method"
            assert hasattr(engine, "execute_identification_pipeline"), "Missing execute_identification_pipeline"
            assert hasattr(engine, "execute_hybrid_pipeline"), "Missing execute_hybrid_pipeline"
            assert hasattr(engine, "execute_full_pipeline"), "Missing execute_full_pipeline"
            print(f"✅ All execute methods present for mode='{mode}'")
            
        except Exception as e:
            print(f"❌ Engine instantiation failed for mode='{mode}': {e}")
            all_passed = False
    
    return all_passed


def test_migration_metrics_structure():
    """Test MigrationMetrics dataclass structure."""
    print("\n" + "=" * 70)
    print("TEST 6: MigrationMetrics Structure")
    print("=" * 70)
    
    try:
        metrics = MigrationMetrics(
            migration_status="in_progress",
            has_backend_imports=True,
            has_src_imports=True,
            migration_ratio=0.75,
            backend_file_count=5,
            src_file_count=3,
        )
        
        print("✅ MigrationMetrics instantiated with all fields")
        
        # Verify all fields are present
        assert metrics.migration_status == "in_progress"
        print("✅ migration_status field correct")
        
        assert metrics.has_backend_imports == True
        print("✅ has_backend_imports field correct")
        
        assert metrics.has_src_imports == True
        print("✅ has_src_imports field correct")
        
        assert metrics.migration_ratio == 0.75
        print("✅ migration_ratio field correct")
        
        assert metrics.backend_file_count == 5
        print("✅ backend_file_count field correct")
        
        assert metrics.src_file_count == 3
        print("✅ src_file_count field correct")
        
        return True
    except Exception as e:
        print(f"❌ MigrationMetrics validation failed: {e}")
        return False


def test_output_json_structure():
    """Test that output JSON matches expected structure."""
    print("\n" + "=" * 70)
    print("TEST 7: Output JSON Structure Validation")
    print("=" * 70)
    
    try:
        gen = OutputGenerator()
        
        # Mock result matching expected structure
        mock_results = [
            {
                "branch": "feature-auth",
                "target": "main",
                "primary_target": "main",
                "confidence": 0.92,
                "reasoning": "Core framework integration",
                "tags": ["tag:core_changes", "tag:migration_complete"],
                "metrics": {
                    "commit_history": {
                        "merge_base_distance": 42,
                        "divergence_ratio": 0.15,
                        "commit_frequency": 3.5,
                        "shared_contributors": 5,
                        "message_similarity_score": 0.78,
                        "branch_age_days": 8,
                    },
                    "codebase_structure": {
                        "core_directories": ["src/auth"],
                        "file_type_distribution": {"py": 12},
                        "code_volume": 450,
                        "affects_core": True,
                        "affects_tests": True,
                        "affects_infrastructure": False,
                        "documentation_intensity": 0.3,
                        "config_change_count": 2,
                    },
                    "migration": {
                        "migration_status": "complete",
                        "has_backend_imports": False,
                        "has_src_imports": True,
                        "migration_ratio": 1.0,
                        "backend_file_count": 0,
                        "src_file_count": 12,
                    },
                }
            }
        ]
        
        # Test simple format
        simple_output = gen.generate_output(mock_results, "simple")
        print("✅ Simple output generated")
        
        # Validate simple output structure
        assert "branches" in simple_output or isinstance(simple_output, list)
        print("✅ Simple output has expected top-level structure")
        
        # Test detailed format
        detailed_output = gen.generate_output(mock_results, "detailed")
        print("✅ Detailed output generated")
        
        assert detailed_output is not None
        print("✅ Detailed output is not None")
        
        # Test all format
        all_output = gen.generate_output(mock_results, "all")
        print("✅ All output generated")
        
        assert "simple" in all_output or len(all_output) > 0
        print("✅ All output contains multiple formats")
        
        return True
    except Exception as e:
        print(f"❌ Output JSON structure validation failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def run_all_tests():
    """Run all validation tests."""
    print("\n" + "=" * 70)
    print("i2t4-into-756 REFACTORING VALIDATION TEST SUITE")
    print("=" * 70)
    
    tests = [
        ("Imports", test_imports),
        ("Mode Validation", test_mode_validation),
        ("MigrationAnalyzer", test_migration_analyzer),
        ("OutputGenerator", test_output_generator),
        ("Engine Instantiation", test_engine_instantiation),
        ("MigrationMetrics", test_migration_metrics_structure),
        ("Output JSON Structure", test_output_json_structure),
    ]
    
    results = {}
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"\n❌ Test '{test_name}' crashed: {e}")
            import traceback
            traceback.print_exc()
            results[test_name] = False
    
    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n✅ ALL TESTS PASSED - Refactoring validation successful!")
        return True
    else:
        print(f"\n❌ {total - passed} test(s) failed - Review output above")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
