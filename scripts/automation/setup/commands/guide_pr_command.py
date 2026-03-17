"""
This module contains the 'guide-pr' command implementation.
"""

from argparse import Namespace
from .command_interface import Command
from src.lib.workflow_context import WorkflowContextManager

class GuidePrCommand(Command):
    """
    A command to guide the user through the PR resolution workflow.
    """

    def get_description(self) -> str:
        """
        Get the description of the command.
        """
        return "Provides guided assistance for the PR resolution workflow."

    def validate_args(self) -> bool:
        """
        Validate the arguments for the command.
        """
        # No specific arguments to validate for this command yet.
        return True

    def execute(self) -> int:
        """
        Execute the command.
        """
        with WorkflowContextManager() as guide:
            guide.stage = "PR_GUIDE_START"
            print("\nWelcome to the PR Resolution Workflow Guide.")
            print("This tool will help you follow the correct process for merging branches.")

            while True:
                print("\nWhat kind of branch are you merging?")
                print("  1. A branch with changes to shared setup/config files (an 'orchestration' change).")
                print("  2. A branch with only application code changes (e.g., in 'src/', 'client/').")
                print("  q. Quit")

                choice = input("Enter your choice (1/2/q): ").strip()

                if choice == '1':
                    guide.stage = "ORCH_MERGE_GUIDANCE"
                    print("\n--- Orchestration Change Merge Workflow ---")
                    print("❌ DO NOT use a standard 'git merge' for this.")
                    print("To safely merge these changes into the 'orchestration-tools' branch, you must use the reverse sync script.")
                    print("\nRecommended Command:")
                    print("  ./scripts/reverse_sync_orchestration.sh <your-branch-name> <commit-sha>")
                    print("\nThis ensures that your approved setup changes are correctly applied to the source of truth.")
                    break
                elif choice == '2':
                    guide.stage = "APP_MERGE_GUIDANCE"
                    print("\n--- Application Feature Merge Workflow ---")
                    print("✅ This is a standard feature merge.")
                    print("You can use 'git merge' to merge your branch into 'main' or 'scientific'.")
                    print("\nRecommendation:")
                    print("  1. Ensure your feature branch is up to date with the target branch (`git pull origin main`).")
                    print("  2. Checkout the target branch (`git checkout main`).")
                    print("  3. Merge your feature branch (`git merge feature/your-feature`).")
                    print("  4. Run the full validation suite as outlined in 'final_merge_approach.md' before pushing the merge.")
                    break
                elif choice.lower() == 'q':
                    print("Exiting guide.")
                    break
                else:
                    print("Invalid choice. Please enter 1, 2, or q.")
        return 0
