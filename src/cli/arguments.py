
"""
CLI arguments definition.
"""

import argparse

def create_parser() -> argparse.ArgumentParser:
    """
    Create the argument parser for the CLI.
    """
    parser = argparse.ArgumentParser(
        description="EmailIntelligence CLI - Intelligent Conflict Resolution"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Analyze command
    analyze_parser = subparsers.add_parser("analyze", help="Analyze repository conflicts")
    analyze_parser.add_argument("repo_path", help="Path to the repository")
    analyze_parser.add_argument("--pr", help="Pull Request ID (optional)")
    
    # Resolve command
    resolve_parser = subparsers.add_parser("resolve", help="Resolve a conflict")
    resolve_parser.add_argument("conflict_id", help="ID of the conflict to resolve")
    resolve_parser.add_argument("strategy_id", help="ID of the strategy to use")
    
    # Validate command
    validate_parser = subparsers.add_parser("validate", help="Run validation checks")

    # Analyze History command
    history_parser = subparsers.add_parser("analyze-history", help="Analyze git history")
    history_parser.add_argument("--branch", default="HEAD", help="Branch to analyze")
    history_parser.add_argument("--output", help="Output file for report")

    # Plan Rebase command
    rebase_parser = subparsers.add_parser("plan-rebase", help="Generate rebase plan")
    rebase_parser.add_argument("--branch", default="HEAD", help="Branch to plan rebase for")
    rebase_parser.add_argument("--output", required=True, help="Output file for rebase plan")
    
    return parser
