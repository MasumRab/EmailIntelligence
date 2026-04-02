#!/usr/bin/env python3
"""
Test script for the enhanced error reporting system.
"""

import asyncio
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core.enhanced_error_reporting import (
    EnhancedErrorReporter,
    ErrorSeverity,
    ErrorCategory,
    create_error_context,
    log_error,
    get_error_statistics,
    get_recent_errors
)

async def test_enhanced_error_reporting():
    """Test the enhanced error reporting system."""
    print("Testing enhanced error reporting system...")

    # Initialize error reporter
    error_reporter = EnhancedErrorReporter()

    # Test logging a simple error
    print("Testing simple error logging...")
    error_id1 = error_reporter.log_error(
        "Test error message",
        severity=ErrorSeverity.WARNING,
        category=ErrorCategory.VALIDATION
    )
    print(f"Logged error with ID: {error_id1}")

    # Test logging an exception
    print("Testing exception logging...")
    try:
        raise ValueError("Test exception for error reporting")
    except Exception as e:
        error_id2 = error_reporter.log_error(
            e,
            severity=ErrorSeverity.ERROR,
            category=ErrorCategory.DATA,
            context=create_error_context(
                component="test_component",
                operation="test_operation",
                user_id="test_user_123"
            ),
            details={"test_field": "test_value", "number": 42}
        )
        print(f"Logged exception with ID: {error_id2}")

    # Test logging with context
    print("Testing error logging with context...")
    context = create_error_context(
        component="database_manager",
        operation="get_email_by_id",
        request_id="req_abc123",
        additional_context={"email_id": 12345}
    )

    error_id3 = error_reporter.log_error(
        "Database connection failed",
        severity=ErrorSeverity.CRITICAL,
        category=ErrorCategory.INTEGRATION,
        context=context
    )
    print(f"Logged contextual error with ID: {error_id3}")

    # Test error statistics
    print("Testing error statistics...")
    stats = error_reporter.get_error_stats()
    print(f"Error statistics: {stats}")

    # Test retrieving recent errors
    print("Testing recent errors retrieval...")
    recent_errors = error_reporter.get_recent_errors()
    print(f"Found {len(recent_errors)} recent errors")

    # Test filtering by category
    print("Testing error filtering by category...")
    data_errors = error_reporter.get_errors_by_category(ErrorCategory.DATA)
    print(f"Found {len(data_errors)} data errors")

    # Test filtering by severity
    print("Testing error filtering by severity...")
    critical_errors = error_reporter.get_errors_by_severity(ErrorSeverity.CRITICAL)
    print(f"Found {len(critical_errors)} critical errors")

    # Test convenience functions
    print("Testing convenience functions...")
    error_id4 = log_error(
        "Convenience function test error",
        severity=ErrorSeverity.INFO,
        category=ErrorCategory.UNKNOWN
    )
    print(f"Logged error with convenience function: {error_id4}")

    # Test global statistics
    global_stats = get_error_statistics()
    print(f"Global error statistics: {global_stats}")

    print("Enhanced error reporting system test completed successfully!")

if __name__ == "__main__":
    asyncio.run(test_enhanced_error_reporting())