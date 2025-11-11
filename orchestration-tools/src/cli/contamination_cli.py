"""
CLI Command for Context Contamination Prevention
"""
import argparse
from typing import Optional
from ..services.verification_service import VerificationService
from ..services.auth_service import AuthService
from ..services.git_service import GitService
from ..services.config_service import ConfigService


def main():
    """Main entry point for context contamination CLI"""
    parser = argparse.ArgumentParser(
        description="Context Contamination Prevention CLI",
        prog="contamination-cli"
    )
    
    # Add subcommands
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Analyze context boundaries command
    analyze_parser = subparsers.add_parser('analyze', help='Analyze context boundaries')
    analyze_parser.add_argument('--component', type=str, help='Component to analyze (optional)')
    
    # Detect contamination points command
    detect_parser = subparsers.add_parser('detect', help='Detect contamination points')
    detect_parser.add_argument('--component', type=str, help='Component to check for contamination (optional)')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Initialize services
    auth_service = AuthService()
    git_service = GitService()
    config_service = ConfigService()
    verification_service = VerificationService(auth_service, git_service, config_service)
    
    try:
        if args.command == 'analyze':
            _handle_analyze_command(args)
        elif args.command == 'detect':
            _handle_detect_command(args)
        else:
            parser.print_help()
    except Exception as e:
        print(f"Error: {str(e)}")


def _handle_analyze_command(args):
    """Handle the analyze context boundaries command"""
    print("Analyzing context boundaries...")
    if args.component:
        print(f"Checking component: {args.component}")
    else:
        print("Checking all components")
    # In a real implementation, this would call the actual services


def _handle_detect_command(args):
    """Handle the detect contamination points command"""
    print("Detecting contamination points...")
    if args.component:
        print(f"Checking component: {args.component}")
    else:
        print("Checking all components")
    # In a real implementation, this would call the actual services


if __name__ == "__main__":
    main()