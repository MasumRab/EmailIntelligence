"""
CLI Command for Goal-Task Consistency Verification
"""
import argparse
from typing import Optional
from ..services.verification_service import VerificationService
from ..services.auth_service import AuthService
from ..services.git_service import GitService
from ..services.config_service import ConfigService


def main():
    """Main entry point for consistency verification CLI"""
    parser = argparse.ArgumentParser(
        description="Goal-Task Consistency Verification CLI",
        prog="consistency-cli"
    )
    
    # Add subcommands
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Verify goal-task alignment command
    verify_parser = subparsers.add_parser('verify-alignment', help='Verify goal-task alignment')
    verify_parser.add_argument('--goal-id', type=str, required=True, help='Goal ID to verify')
    verify_parser.add_argument('--task-id', type=str, help='Task ID to verify (optional, if not provided, checks all tasks for the goal)')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Initialize services
    auth_service = AuthService()
    git_service = GitService()
    config_service = ConfigService()
    verification_service = VerificationService(auth_service, git_service, config_service)
    
    try:
        if args.command == 'verify-alignment':
            _handle_verify_alignment_command(args)
        else:
            parser.print_help()
    except Exception as e:
        print(f"Error: {str(e)}")


def _handle_verify_alignment_command(args):
    """Handle the verify alignment command"""
    print(f"Verifying goal-task alignment for goal: {args.goal_id}")
    if args.task_id:
        print(f"Checking specific task: {args.task_id}")
    else:
        print("Checking all tasks related to the goal")
    # In a real implementation, this would call the actual services


if __name__ == "__main__":
    main()