"""
This module contains the 'guide-dev' command implementation.
"""

from argparse import Namespace
from .command_interface import Command
from src.lib.workflow_context import WorkflowContextManager

class GuideDevCommand(Command):
    """
    A command to guide the user through the general development workflow.
    """

    def _get_current_branch(self) -> str:
        """
        Gets the current git branch name.
        """
        import subprocess
        return subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD']).decode('utf-8').strip()

    def get_description(self) -> str:
        """
        Get the description of the command.
        """
        return "Provides guided assistance for the general development workflow."

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
            guide.stage = "DEV_GUIDE_START"
            print("\nWelcome to the Development Workflow Guide.")
            print("This tool will help you follow the correct process for making changes.")
            
            while True:
                print("\nWhat do you want to do?")
                print("  1. Work on application code (e.g., in 'src/', 'client/')")
                print("  2. Modify a shared setup or configuration file (e.g., in 'setup/', '.flake8')")
                print("  q. Quit")
                
                choice = input("Enter your choice (1/2/q): ").strip()

                if choice == '1':
                    guide.stage = "APP_CODE_GUIDANCE"
                    print("\n--- Application Code Workflow ---")
                    print("✅ You can work on application code freely on any feature branch.")
                    print("The orchestration system will automatically keep your local setup files in sync.")
                    print("No special commands are needed. Happy coding!")
                    break
                elif choice == '2':
                    guide.stage = "ORCH_CODE_GUIDANCE"
                    print("\n--- Shared Config Workflow ---")
                    
                    try:
                        current_branch = self._get_current_branch()
                        
                        if current_branch == 'orchestration-tools':
                            guide.stage = "ORCH_CODE_SAFE"
                            print("✅ You are on the 'orchestration-tools' branch.")
                            print("It is safe to edit shared setup and configuration files here.")
                            print("Commit and push your changes to this branch, and they will be propagated automatically.")
                        else:
                            guide.stage = "ORCH_CODE_UNSAFE"
                            print(f"❌ You are currently on the '{current_branch}' branch, not 'orchestration-tools'.")
                            print("Changes to shared files on this branch will be overwritten by the sync hooks.")
                            print("\nRecommendation:")
                            print("  1. Stash your changes if you have any (`git stash`).")
                            print("  2. Switch to the correct branch (`git checkout orchestration-tools`).")
                            print("  3. Re-apply your changes if needed (`git stash pop`).")
                        break
                    except Exception as e:
                        print(f"\nCould not determine git branch. Error: {e}")
                        print("Please ensure you are in a git repository.")
                        return 1
                elif choice.lower() == 'q':
                    print("Exiting guide.")
                    break
                else:
                    print("Invalid choice. Please enter 1, 2, or q.")
        return 0
