#!/usr/bin/env python3
"""
Command Line Interface for Session Management

This script provides a CLI for managing development sessions
in the Taskmaster project.
"""

import argparse
import sys
from pathlib import Path

# Add the .qwen directory to the path to import session_manager
sys.path.insert(0, str(Path(__file__).parent))

from session_manager import SessionManager, initialize_session_manager


def cmd_start_session(args):
    """Start a new development session."""
    sm = initialize_session_manager()
    
    # Get goals from command line or prompt user
    if args.goals:
        goals = [goal.strip() for goal in args.goals.split(',')]
    else:
        print("Enter your session goals (press Enter twice to finish):")
        goals = []
        while True:
            goal = input("> ").strip()
            if not goal:
                break
            goals.append(goal)
    
    if not goals:
        print("No goals provided. Starting session without specific goals.")
        goals = []
    
    session_info = sm.start_session(goals=goals)
    print(f"✓ Started session: {session_info['session_id']}")
    print(f"• Project: {session_info['project_path']}")
    print(f"• Goals: {session_info['goals']}")


def cmd_end_session(args):
    """End the current development session."""
    sm = initialize_session_manager()
    session_id = sm.end_session()
    
    if session_id:
        print(f"✓ Ended session: {session_id}")
    else:
        print("⚠ No active session to end")


def cmd_show_session(args):
    """Show information about the current session."""
    sm = initialize_session_manager()
    session_info = sm.get_current_session()
    
    if session_info:
        print(f"Session ID: {session_info['session_id']}")
        print(f"Start Time: {session_info['start_time']}")
        print(f"Project: {session_info['project_path']}")
        print(f"Status: {session_info['status']}")
        print(f"Goals: {session_info['goals']}")
    else:
        print("No session information available")


def cmd_show_context(args):
    """Show the current project context."""
    sm = initialize_session_manager()
    context = sm.get_project_context()
    
    print("Project Context:")
    print(f"  QWEN.md found: {'Yes' if 'qwem_md_content' in context else 'No'}")
    print(f"  Pending handoffs: {len(context.get('pending_handoffs', []))}")
    print(f"  Command history entries: {len(context.get('command_history', []))}")


def main():
    parser = argparse.ArgumentParser(description="Session Management for Taskmaster")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Start session command
    start_parser = subparsers.add_parser('start', help='Start a new development session')
    start_parser.add_argument('--goals', '-g', help='Comma-separated list of session goals')
    start_parser.set_defaults(func=cmd_start_session)
    
    # End session command
    end_parser = subparsers.add_parser('end', help='End the current development session')
    end_parser.set_defaults(func=cmd_end_session)
    
    # Show session command
    show_parser = subparsers.add_parser('show', help='Show current session information')
    show_parser.set_defaults(func=cmd_show_session)
    
    # Show context command
    context_parser = subparsers.add_parser('context', help='Show project context')
    context_parser.set_defaults(func=cmd_show_context)
    
    # Parse arguments
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()