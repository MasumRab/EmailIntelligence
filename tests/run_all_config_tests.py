#!/usr/bin/env python3
"""
Master test runner for all configuration file tests.
Runs both basic validation tests and edge case tests.
"""
import sys
from test_config_files_standalone import ConfigFileTests
from test_config_edge_cases import EdgeCaseTests


def main():
    """Run all configuration file tests."""
    print("\n" + "=" * 70)
    print("CONFIGURATION FILE TEST SUITE")
    print("=" * 70)
    print("\nTesting 24 changed configuration files:")
    print("  - 6 JSON config files")
    print("  - 1 YAML config file")
    print("  - 1 Bandit config file")
    print("  - 16 Markdown documentation files")
    print("")

    # Run basic validation tests
    print("\nPHASE 1: Basic Validation Tests")
    print("-" * 70)
    basic_runner = ConfigFileTests()
    basic_success = basic_runner.run_all_tests()

    # Run edge case tests
    print("\n\nPHASE 2: Edge Case & Integration Tests")
    print("-" * 70)
    edge_runner = EdgeCaseTests()
    edge_success = edge_runner.run_all_tests()

    # Overall summary
    print("\n\n" + "=" * 70)
    print("OVERALL TEST SUMMARY")
    print("=" * 70)

    total_passed = basic_runner.passed + edge_runner.passed
    total_failed = basic_runner.failed + edge_runner.failed
    total_skipped = basic_runner.skipped + edge_runner.skipped
    total_tests = total_passed + total_failed + total_skipped

    print(f"\nTotal Tests Run: {total_tests}")
    print(f"  ✓ Passed:  {total_passed}")
    print(f"  ✗ Failed:  {total_failed}")
    print(f"  ⊘ Skipped: {total_skipped}")

    if total_failed == 0:
        print("\n🎉 ALL TESTS PASSED! 🎉")
        print("\nAll configuration files are valid:")
        print("  ✓ JSON files have correct syntax and structure")
        print("  ✓ YAML files are properly formatted")
        print("  ✓ Markdown files have valid structure")
        print("  ✓ Security configurations are appropriate")
        print("  ✓ Permissions are correctly defined")
        print("  ✓ No hardcoded secrets detected")
        print("  ✓ Cross-file consistency validated")
    else:
        print("\n❌ SOME TESTS FAILED")
        print("\nReview the errors above for details.")

    print("=" * 70 + "\n")

    return basic_success and edge_success


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)