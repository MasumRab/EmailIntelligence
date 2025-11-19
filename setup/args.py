"""
Argument parsing for the EmailIntelligence launcher.

This module handles all command-line argument parsing logic,
including both modern command pattern and legacy argument support.
"""

import argparse
import sys
from typing import Any


def _add_common_args(parser: argparse.ArgumentParser) -> None:
    """Add common arguments to subcommand parsers."""
    parser.add_argument(
        "--loglevel",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default="INFO",
        help="Set the logging level.",
    )
    parser.add_argument("--debug", action="store_true", help="Enable debug mode.")


def _add_legacy_args(parser: argparse.ArgumentParser) -> None:
    """Add legacy arguments for backward compatibility."""
    # Environment Setup
    parser.add_argument(
        "--force-recreate-venv",
        action="store_true",
        help="Force recreation of the venv.",
    )
    parser.add_argument(
        "--use-conda",
        action="store_true",
        help="Use Conda environment instead of venv.",
    )
    parser.add_argument(
        "--conda-env",
        type=str,
        default="base",
        help="Conda environment name to use (default: base).",
    )
    parser.add_argument(
        "--no-venv",
        action="store_true",
        help="Don't create or use a virtual environment.",
    )
    parser.add_argument(
        "--update-deps",
        action="store_true",
        help="Update dependencies before launching.",
    )
    parser.add_argument(
        "--skip-torch-cuda-test",
        action="store_true",
        help="Skip CUDA availability test for PyTorch.",
    )
    parser.add_argument(
        "--reinstall-torch", action="store_true", help="Reinstall PyTorch."
    )
    parser.add_argument(
        "--skip-python-version-check",
        action="store_true",
        help="Skip Python version check.",
    )
    parser.add_argument(
        "--no-download-nltk", action="store_true", help="Skip downloading NLTK data."
    )
    parser.add_argument(
        "--skip-prepare",
        action="store_true",
        help="Skip all environment preparation steps.",
    )

    # Application Configuration
    parser.add_argument(
        "--port", type=int, default=8000, help="Specify the port to run on."
    )
    parser.add_argument(
        "--host", type=str, default="127.0.0.1", help="Specify the host to run on."
    )
    parser.add_argument(
        "--frontend-port",
        type=int,
        default=5173,
        help="Specify the frontend port to run on.",
    )
    parser.add_argument(
        "--api-url", type=str, help="Specify the API URL for the frontend."
    )
    parser.add_argument(
        "--api-only",
        action="store_true",
        help="Run only the API server without the frontend.",
    )
    parser.add_argument(
        "--frontend-only",
        action="store_true",
        help="Run only the frontend without the API server.",
    )
    parser.add_argument("--env-file", type=str, help="Specify a custom .env file.")

    # Testing Options
    parser.add_argument(
        "--coverage",
        action="store_true",
        help="Generate coverage report when running tests.",
    )
    parser.add_argument("--unit", action="store_true", help="Run unit tests.")
    parser.add_argument(
        "--integration", action="store_true", help="Run integration tests."
    )
    parser.add_argument("--e2e", action="store_true", help="Run end-to-end tests.")
    parser.add_argument(
        "--performance", action="store_true", help="Run performance tests."
    )
    parser.add_argument("--security", action="store_true", help="Run security tests.")

    # Extensions and Models
    parser.add_argument(
        "--skip-extensions", action="store_true", help="Skip loading extensions."
    )
    parser.add_argument(
        "--skip-models", action="store_true", help="Skip downloading models."
    )

    # Advanced Options
    parser.add_argument(
        "--system-info", action="store_true", help="Print system information then exit."
    )
    parser.add_argument("--share", action="store_true", help="Create a public URL.")
    parser.add_argument(
        "--listen", action="store_true", help="Make the server listen on network."
    )
    parser.add_argument(
        "--ngrok", type=str, help="Use ngrok to create a tunnel, specify ngrok region."
    )


def create_argument_parser() -> argparse.ArgumentParser:
    """Create the main argument parser with all subcommands."""
    parser = argparse.ArgumentParser(
        description="EmailIntelligence Unified Launcher",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    # Add subcommands
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Setup command
    setup_parser = subparsers.add_parser(
        "setup", help="Set up the development environment"
    )
    _add_common_args(setup_parser)

    # Run command
    run_parser = subparsers.add_parser(
        "run", help="Run the EmailIntelligence application"
    )
    _add_common_args(run_parser)
    run_parser.add_argument(
        "--dev", action="store_true", help="Run in development mode"
    )

    # Test command
    test_parser = subparsers.add_parser("test", help="Run tests")
    _add_common_args(test_parser)
    test_parser.add_argument("--unit", action="store_true", help="Run unit tests")
    test_parser.add_argument(
        "--integration", action="store_true", help="Run integration tests"
    )
    test_parser.add_argument("--e2e", action="store_true", help="Run end-to-end tests")
    test_parser.add_argument(
        "--performance", action="store_true", help="Run performance tests"
    )
    test_parser.add_argument(
        "--security", action="store_true", help="Run security tests"
    )
    test_parser.add_argument(
        "--coverage", action="store_true", help="Generate coverage report"
    )
    test_parser.add_argument(
        "--continue-on-error",
        action="store_true",
        help="Continue running tests even if some fail",
    )

    # Check command for orchestration-tools branch
    check_parser = subparsers.add_parser(
        "check", help="Run checks for orchestration environment"
    )
    _add_common_args(check_parser)
    check_parser.add_argument(
        "--critical-files", action="store_true", help="Check for critical orchestration files"
    )
    check_parser.add_argument(
        "--env", action="store_true", help="Check orchestration environment"
    )

    # Legacy argument parsing for backward compatibility
    parser.add_argument(
        "--setup", action="store_true", help="Set up the environment (legacy)"
    )
    parser.add_argument(
        "--stage",
        choices=["dev", "test"],
        default="dev",
        help="Application mode (legacy)",
    )

    # Add all legacy arguments for backward compatibility
    _add_legacy_args(parser)

    return parser


def parse_arguments(args: list[str] = None) -> argparse.Namespace:
    """
    Parse command line arguments.

    Args:
        args: List of arguments to parse (defaults to sys.argv[1:])

    Returns:
        Parsed arguments namespace
    """
    parser = create_argument_parser()
    return parser.parse_args(args or sys.argv[1:])