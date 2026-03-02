"""
EmailIntelligence CLI - Main Entry Point

This module provides the main() function that serves as the CLI entry point.
"""

import sys

from cli.cli_class import EmailIntelligenceCLI
from cli.commands import create_parser, execute_command


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================


def main() -> None:
    """Main CLI entry point."""
    parser = create_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    # Initialize CLI
    cli = EmailIntelligenceCLI()

    try:
        # Execute command and print result
        result = execute_command(args, cli)
        print(result)  # Results are already JSON-serializable dicts
        
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        cli._error_exit(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
