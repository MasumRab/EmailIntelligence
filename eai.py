"""
EmailIntelligence CLI Entry Point.
"""

import asyncio
import sys
from src.cli.arguments import create_parser
from src.cli.commands import CLICommands
from src.utils.logger import get_logger

logger = get_logger(__name__)


async def main():
    """
    Main entry point.
    """
    parser = create_parser()
    args = parser.parse_args()

    commands = CLICommands()

    try:
        if args.command == "analyze":
            await commands.analyze(
                args.repo_path,
                getattr(args, "pr", None),
                getattr(args, "base_branch", None),
                getattr(args, "head_branch", None),
            )
        elif args.command == "resolve":
            await commands.resolve(args.conflict_id, args.strategy_id)
        elif args.command == "validate":
            await commands.validate()
        elif args.command == "analyze-history":
            await commands.analyze_history(args.branch, args.output)
        elif args.command == "plan-rebase":
            await commands.plan_rebase(args.branch, args.output)
        else:
            parser.print_help()

    except Exception as e:
        logger.error("Command failed", error=str(e))
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
