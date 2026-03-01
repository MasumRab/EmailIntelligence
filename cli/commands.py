"""
EmailIntelligence CLI - Command Handlers

This module contains all CLI command handlers using argparse.
"""

import argparse
import asyncio
import json
import sys
from pathlib import Path
from typing import Any, Dict

from cli.cli_class import EmailIntelligenceCLI


# ============================================================================
# COMMAND HANDLERS
# ============================================================================


def setup_resolution(args: argparse.Namespace, cli: EmailIntelligenceCLI) -> Dict[str, Any]:
    """Handle setup-resolution command."""
    return cli.setup_resolution(
        pr_number=args.pr,
        source_branch=args.source_branch,
        target_branch=args.target_branch,
        constitution_files=args.constitution,
        spec_files=args.spec,
        dry_run=args.dry_run,
        push_to_target=args.push_to_target,
        no_resolution_branch=args.no_resolution_branch
    )


def push_resolution(args: argparse.Namespace, cli: EmailIntelligenceCLI) -> Dict[str, Any]:
    """Handle push-resolution command."""
    return cli.push_resolution_to_target(
        pr_number=args.pr,
        target_branch=args.target,
        confirmed=args.confirm,
        force=args.force
    )


def analyze_constitutional(args: argparse.Namespace, cli: EmailIntelligenceCLI) -> Dict[str, Any]:
    """Handle analyze-constitutional command."""
    return cli.analyze_constitutional(
        pr_number=args.pr,
        constitution_files=args.constitution,
        interactive=args.interactive
    )


def develop_strategy(args: argparse.Namespace, cli: EmailIntelligenceCLI) -> Dict[str, Any]:
    """Handle develop-spec-kit-strategy command."""
    return cli.develop_spec_kit_strategy(
        pr_number=args.pr,
        worktrees=args.worktrees,
        alignment_rules=args.alignment_rules,
        interactive=args.interactive
    )


def align_content(args: argparse.Namespace, cli: EmailIntelligenceCLI) -> Dict[str, Any]:
    """Handle align-content command."""
    return cli.align_content(
        pr_number=args.pr,
        strategy_file=args.strategy,
        dry_run=args.dry_run,
        preview_changes=args.preview_changes,
        interactive=args.interactive
    )


def validate_resolution(args: argparse.Namespace, cli: EmailIntelligenceCLI) -> Dict[str, Any]:
    """Handle validate-resolution command."""
    return cli.validate_resolution(
        pr_number=args.pr,
        comprehensive=args.comprehensive,
        quick=args.quick,
        test_suites=args.tests
    )


def auto_resolve(args: argparse.Namespace, cli: EmailIntelligenceCLI) -> Dict[str, Any]:
    """Handle auto-resolve command."""
    return asyncio.run(
        cli.auto_resolve_conflicts(
            pr_number=args.pr,
            strategy_file=args.strategy
        )
    )


def scan_all_branches(args: argparse.Namespace, cli: EmailIntelligenceCLI) -> Dict[str, Any]:
    """Handle scan-all-branches command."""
    result = cli.scan_all_branches(
        include_remotes=args.include_remotes,
        target_branches=args.targets,
        concurrency=args.concurrency,
        exclude_patterns=args.exclude,
        use_semantic=args.semantic
    )
    # Convert to dict for JSON output
    return {
        'scanned_at': result.scanned_at,
        'branches': result.branches,
        'target_branches': result.target_branches,
        'total_pairs': result.total_pairs,
        'pairs_with_conflicts': result.pairs_with_conflicts,
        'conflict_rate': result.conflict_rate,
        'total_conflicts': result.total_conflicts,
        'high_conflict_pairs': [
            {'source': r.source, 'target': r.target, 'count': r.conflict_count}
            for r in result.high_conflict_pairs
        ]
    }


def collect_pr_recommendations(args: argparse.Namespace, cli: EmailIntelligenceCLI) -> Dict[str, Any]:
    """Handle collect-pr-recommendations command."""
    return cli.collect_pr_recommendations(
        pr_number=args.pr,
        include_conflicts=args.include_conflicts,
        include_strategy=args.include_strategy,
        include_validation=args.include_validation
    )


# ============================================================================
# ARGUMENT PARSER SETUP
# ============================================================================


def create_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser."""
    parser = argparse.ArgumentParser(
        description="EmailIntelligence CLI - AI-powered git worktree-based conflict resolution tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Setup resolution workspace
  eai setup-resolution --pr 123 --source-branch feature/auth --target-branch main

  # Analyze constitutional compliance
  eai analyze-constitutional --pr 123 --constitution ./constitutions/auth.yaml

  # Develop resolution strategy
  eai develop-spec-kit-strategy --pr 123 --worktrees --interactive

  # Execute content alignment
  eai align-content --pr 123 --interactive --checkpoint-each-step

  # Validate resolution
  eai validate-resolution --pr 123 --comprehensive

  # Scan all branches for conflicts
  eai scan-all-branches --targets main develop

  # Collect PR recommendations
  eai collect-pr-recommendations --pr 123
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Setup resolution command
    _add_setup_resolution_parser(subparsers)
    
    # Push resolution command
    _add_push_resolution_parser(subparsers)
    
    # Analyze constitutional command
    _add_analyze_constitutional_parser(subparsers)
    
    # Develop strategy command
    _add_develop_strategy_parser(subparsers)
    
    # Align content command
    _add_align_content_parser(subparsers)
    
    # Validate resolution command
    _add_validate_resolution_parser(subparsers)
    
    # Auto-resolve command
    _add_auto_resolve_parser(subparsers)
    
    # Scan all branches command
    _add_scan_all_branches_parser(subparsers)
    
    # Collect PR recommendations command
    _add_collect_pr_recommendations_parser(subparsers)
    
    # Version command
    subparsers.add_parser('version', help='Show version information')

    return parser


def _add_setup_resolution_parser(subparsers) -> None:
    """Add setup-resolution subcommand."""
    setup_parser = subparsers.add_parser('setup-resolution', help='Setup resolution workspace')
    setup_parser.add_argument('--pr', type=int, required=True, help='Pull request number')
    setup_parser.add_argument('--source-branch', required=True, help='Source branch with conflicts')
    setup_parser.add_argument('--target-branch', required=True, help='Target branch for merging')
    setup_parser.add_argument('--constitution', action='append', help='Constitution file(s)')
    setup_parser.add_argument('--spec', action='append', help='Specification file(s)')
    setup_parser.add_argument('--dry-run', action='store_true', help='Preview setup without creating worktrees')
    setup_parser.add_argument('--push-to-target', action='store_true', 
                             help='Push resolved changes directly to target branch instead of creating PR')
    setup_parser.add_argument('--no-resolution-branch', action='store_true',
                             help='Skip creating resolution branch, use existing branches directly')


def _add_push_resolution_parser(subparsers) -> None:
    """Add push-resolution subcommand."""
    push_parser = subparsers.add_parser('push-resolution', 
                                       help='Push resolved changes directly to target branch')
    push_parser.add_argument('--pr', type=int, required=True, help='Pull request number')
    push_parser.add_argument('--target', type=str, 
                            help='Target branch to push to (default: stored target)')
    push_parser.add_argument('--confirm', action='store_true', 
                            help='Skip confirmation prompt')
    push_parser.add_argument('--force', action='store_true', 
                            help='Use force push (--force-with-lease)')


def _add_analyze_constitutional_parser(subparsers) -> None:
    """Add analyze-constitutional subcommand."""
    analyze_parser = subparsers.add_parser('analyze-constitutional', help='Analyze conflicts against constitution')
    analyze_parser.add_argument('--pr', type=int, required=True, help='Pull request number')
    analyze_parser.add_argument('--constitution', action='append', help='Constitution file(s) to analyze against')
    analyze_parser.add_argument('--interactive', action='store_true', help='Enable interactive analysis mode')


def _add_develop_strategy_parser(subparsers) -> None:
    """Add develop-spec-kit-strategy subcommand."""
    strategy_parser = subparsers.add_parser('develop-spec-kit-strategy', help='Develop spec-kit resolution strategy')
    strategy_parser.add_argument('--pr', type=int, required=True, help='Pull request number')
    strategy_parser.add_argument('--worktrees', action='store_true', help='Use worktree-based analysis')
    strategy_parser.add_argument('--alignment-rules', help='Path to alignment rules file')
    strategy_parser.add_argument('--interactive', action='store_true', help='Enable interactive strategy development')
    strategy_parser.add_argument('--review-required', action='store_true', help='Require team review')


def _add_align_content_parser(subparsers) -> None:
    """Add align-content subcommand."""
    align_parser = subparsers.add_parser('align-content', help='Execute content alignment')
    align_parser.add_argument('--pr', type=int, required=True, help='Pull request number')
    align_parser.add_argument('--strategy', help='Path to strategy JSON file')
    align_parser.add_argument('--dry-run', action='store_true', help='Preview alignment without applying changes')
    align_parser.add_argument('--preview-changes', action='store_true', help='Show preview of changes')
    align_parser.add_argument('--interactive', action='store_true', help='Interactive alignment with confirmation')
    align_parser.add_argument('--checkpoint-each-step', action='store_true', help='Checkpoint after each step')


def _add_validate_resolution_parser(subparsers) -> None:
    """Add validate-resolution subcommand."""
    validate_parser = subparsers.add_parser('validate-resolution', help='Validate completed resolution')
    validate_parser.add_argument('--pr', type=int, required=True, help='Pull request number')
    validate_parser.add_argument('--comprehensive', action='store_true', help='Run comprehensive validation')
    validate_parser.add_argument('--quick', action='store_true', help='Run quick validation check')
    validate_parser.add_argument('--tests', help='Specific test suites to run (comma-separated)')


def _add_auto_resolve_parser(subparsers) -> None:
    """Add auto-resolve subcommand."""
    auto_resolve_parser = subparsers.add_parser('auto-resolve', help='Automatically resolve conflicts')
    auto_resolve_parser.add_argument('--pr', type=int, required=True, help='Pull request number')
    auto_resolve_parser.add_argument('--strategy', help='Path to strategy file')


def _add_scan_all_branches_parser(subparsers) -> None:
    """Add scan-all-branches subcommand."""
    scan_parser = subparsers.add_parser('scan-all-branches', 
                                       help='Scan all branch pairs for conflicts')
    scan_parser.add_argument('--include-remotes', action='store_true', default=True,
                            help='Include remote branches in scan (default: True)')
    scan_parser.add_argument('--targets', nargs='+', default=['main'],
                            help='Target branches to analyze against (default: main)')
    scan_parser.add_argument('--concurrency', type=int, default=4,
                            help='Number of parallel scans (default: 4)')
    scan_parser.add_argument('--exclude', nargs='*', 
                            help='Branch patterns to exclude (default: main develop HEAD)')
    scan_parser.add_argument('--semantic', action='store_true', default=False,
                            help='Enable semantic conflict analysis (default: False)')


def _add_collect_pr_recommendations_parser(subparsers) -> None:
    """Add collect-pr-recommendations subcommand."""
    rec_parser = subparsers.add_parser('collect-pr-recommendations', 
                                       help='Collect all recommendations for a PR')
    rec_parser.add_argument('--pr', type=int, required=True, help='Pull request number')
    rec_parser.add_argument('--include-conflicts', action='store_true', default=True,
                           help='Include conflict recommendations (default: True)')
    rec_parser.add_argument('--include-strategy', action='store_true', default=True,
                           help='Include strategy recommendations (default: True)')
    rec_parser.add_argument('--include-validation', action='store_true', default=True,
                           help='Include validation recommendations (default: True)')


# ============================================================================
# COMMAND DISPATCHER
# ============================================================================


# Map of command names to handler functions
COMMAND_HANDLERS = {
    'setup-resolution': setup_resolution,
    'push-resolution': push_resolution,
    'analyze-constitutional': analyze_constitutional,
    'develop-spec-kit-strategy': develop_strategy,
    'align-content': align_content,
    'validate-resolution': validate_resolution,
    'auto-resolve': auto_resolve,
    'scan-all-branches': scan_all_branches,
    'collect-pr-recommendations': collect_pr_recommendations,
}


def execute_command(args: argparse.Namespace, cli: EmailIntelligenceCLI) -> Dict[str, Any]:
    """Execute the command based on parsed arguments."""
    handler = COMMAND_HANDLERS.get(args.command)
    if handler:
        return handler(args, cli)
    return {"error": f"Unknown command: {args.command}"}


# ============================================================================
# EXPORTS
# ============================================================================

__all__ = [
    'create_parser',
    'execute_command',
    'COMMAND_HANDLERS',
]
