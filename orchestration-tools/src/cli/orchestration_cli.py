import argparse
import sys
from typing import Optional
from ..services.verification_service import VerificationService
from ..services.auth_service import AuthService
from ..services.git_service import GitService
from ..services.config_service import ConfigService
from ..lib.error_handling import logger


def main():
    """Main entry point for the orchestration CLI"""
    parser = argparse.ArgumentParser(
        description="Orchestration Tools Verification CLI",
        prog="orchestration-cli"
    )
    
    # Add subcommands
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Verify command
    verify_parser = subparsers.add_parser('verify', help='Run verification on changes')
    verify_parser.add_argument('--source-branch', type=str, help='Source branch name')
    verify_parser.add_argument('--target-branch', type=str, help='Target branch name')
    verify_parser.add_argument('--profile', type=str, help='Verification profile to use')
    
    # Status command
    status_parser = subparsers.add_parser('status', help='Check verification status')
    status_parser.add_argument('--branch', type=str, help='Branch to check status for')
    status_parser.add_argument('--verification-id', type=str, help='Specific verification ID to check')
    
    # Approve command
    approve_parser = subparsers.add_parser('approve', help='Approve verification results')
    approve_parser.add_argument('--verification-id', type=str, required=True, help='Verification ID to approve')
    approve_parser.add_argument('--comment', type=str, help='Approval comment')
    
    # Reject command
    reject_parser = subparsers.add_parser('reject', help='Reject verification results')
    reject_parser.add_argument('--verification-id', type=str, required=True, help='Verification ID to reject')
    reject_parser.add_argument('--comment', type=str, required=True, help='Rejection reason')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Initialize services
    auth_service = AuthService()
    git_service = GitService()
    config_service = ConfigService()
    verification_service = VerificationService(auth_service, git_service, config_service)
    
    try:
        if args.command == 'verify':
            _handle_verify_command(args, verification_service, git_service)
        elif args.command == 'status':
            _handle_status_command(args, verification_service)
        elif args.command == 'approve':
            _handle_approve_command(args, verification_service)
        elif args.command == 'reject':
            _handle_reject_command(args, verification_service)
        else:
            parser.print_help()
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)


def _handle_verify_command(args, verification_service, git_service):
    """Handle the verify command"""
    # Get current branch if not specified
    source_branch = args.source_branch or git_service.get_current_branch()
    target_branch = args.target_branch or "main"  # Default to main
    profile = args.profile
    
    print(f"Running verification: {source_branch} -> {target_branch}")
    
    # Run verification
    result = verification_service.run_verification(source_branch, target_branch, profile)
    
    print(f"Verification ID: {result.id}")
    print(f"Status: {result.status}")
    print(f"Profile: {result.profile}")
    if result.report:
        print(f"Report: {result.report}")


def _handle_status_command(args, verification_service):
    """Handle the status command"""
    if args.verification_id:
        result = verification_service.get_verification_result(args.verification_id)
        if result:
            print(f"Verification ID: {result.id}")
            print(f"Source Branch: {result.branch_name}")
            print(f"Target Branch: {result.target_branch}")
            print(f"Status: {result.status}")
            print(f"Review Status: {result.review_status}")
            print(f"Profile: {result.profile}")
            if result.report:
                print(f"Report: {result.report}")
        else:
            print(f"Verification {args.verification_id} not found")
    elif args.branch:
        # Get latest verification for branch
        print(f"Status for branch {args.branch}: Not implemented yet")
    else:
        print("Please specify either --verification-id or --branch")


def _handle_approve_command(args, verification_service):
    """Handle the approve command"""
    # In a real implementation, we would authenticate the user
    # For now, we'll simulate approval
    print(f"Approving verification {args.verification_id}")
    if args.comment:
        print(f"Comment: {args.comment}")
    print("Approval processed")


def _handle_reject_command(args, verification_service):
    """Handle the reject command"""
    # In a real implementation, we would authenticate the user
    # For now, we'll simulate rejection
    print(f"Rejecting verification {args.verification_id}")
    print(f"Reason: {args.comment}")
    print("Rejection processed")


if __name__ == "__main__":
    main()