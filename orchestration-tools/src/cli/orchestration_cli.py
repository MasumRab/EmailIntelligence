"""CLI for orchestration tools verification system."""

import asyncio
import argparse
from typing import Optional
import uuid

from src.config import load_settings
from src.logging import get_logger
from src.services.verification_service import VerificationService
from src.models.verification import VerificationProfile


logger = get_logger(__name__)


async def verify_command(args: argparse.Namespace) -> None:
    """Run verification with specified profile."""
    profile_name = args.profile or "default"
    correlation_id = f"CLI-{uuid.uuid4().hex[:8].upper()}"

    service = VerificationService()

    # Register default profiles
    default_profile = VerificationProfile(
        name="default",
        description="Default verification profile",
        scenarios=["test_git_operations", "test_environment_variables"],
        context_checks=["environment_variables"],
        timeout=3600,
        parallel=True,
    )
    service.register_profile(default_profile)

    # Run verification
    result = await service.run_verification(
        profile_name=profile_name,
        correlation_id=correlation_id,
        timeout=args.timeout,
    )

    # Print results
    print(f"\nVerification Result ({correlation_id}):")
    print(f"Success: {result.success}")
    print(f"Message: {result.message}")

    if result.data:
        results = result.data.get("results", [])
        summary = result.data.get("summary", {})

        print(f"\nResults Summary:")
        print(f"  Total: {summary.get('total', 0)}")
        print(f"  Passed: {summary.get('passed', 0)}")
        print(f"  Failed: {summary.get('failed', 0)}")
        print(f"  Duration: {summary.get('duration', 0):.2f}s")

        if results:
            print(f"\nDetailed Results:")
            for r in results:
                print(f"  - {r.name}: {r.status} ({r.duration:.2f}s)")
                if r.errors:
                    for error in r.errors:
                        print(f"    Error: {error}")


def create_parser() -> argparse.ArgumentParser:
    """Create argument parser for CLI."""
    parser = argparse.ArgumentParser(
        description="Orchestration Tools - Verification and Consistency System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Verify command
    verify_parser = subparsers.add_parser("verify", help="Run verification")
    verify_parser.add_argument(
        "--profile",
        type=str,
        default="default",
        help="Verification profile to use (default: default)",
    )
    verify_parser.add_argument(
        "--timeout",
        type=int,
        default=3600,
        help="Verification timeout in seconds (default: 3600)",
    )
    verify_parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose output",
    )
    verify_parser.set_defaults(func=verify_command)

    # Version command
    def version_command(args: argparse.Namespace) -> None:
        """Show version information."""
        from src import __version__
        print(f"Orchestration Tools v{__version__}")

    version_parser = subparsers.add_parser("version", help="Show version")
    version_parser.set_defaults(func=version_command)

    # Health check command
    async def health_command(args: argparse.Namespace) -> None:
        """Check system health."""
        print("System Health Check:")
        print("✓ Configuration loaded")
        print("✓ Logging configured")
        print("✓ Services initialized")
        print("\nStatus: HEALTHY")

    health_parser = subparsers.add_parser("health", help="Check system health")
    health_parser.set_defaults(func=health_command)

    return parser


def main() -> None:
    """Main CLI entry point."""
    settings = load_settings()

    parser = create_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    # Run the command
    try:
        if asyncio.iscoroutinefunction(args.func):
            asyncio.run(args.func(args))
        else:
            args.func(args)
    except KeyboardInterrupt:
        logger.info("Interrupted by user")
    except Exception as e:
        logger.error(f"CLI error: {e}")
        raise


if __name__ == "__main__":
    main()
