"""
Command-line interface for context control.
"""

import argparse
from .core import ContextController


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="Agent Context Control CLI")
    parser.add_argument("--branch", help="Branch name to get context for")
    parser.add_argument("--agent-id", default="cli", help="Agent ID")
    parser.add_argument("--validate", action="store_true", help="Validate the context instead of displaying it")

    args = parser.parse_args()

    controller = ContextController()
    context = controller.get_context_for_branch(branch_name=args.branch, agent_id=args.agent_id)

    if args.validate:
        result = controller.validate_context(context)
        print("✅ Context validation passed" if result else "❌ Context validation failed")
    else:
        print(f"Branch: {context.branch_name or 'unknown'}")
        print(f"Environment: {context.environment_type}")
        print(f"Profile ID: {context.profile_id}")
        print(f"Agent ID: {context.agent_id}")
        print(f"Accessible files: {len(context.accessible_files)}")
        print(f"Restricted files: {len(context.restricted_files)}")


if __name__ == "__main__":
    main()