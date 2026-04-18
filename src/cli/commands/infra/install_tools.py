"""
Install Tools Command Module

Implements the install-tools command for installing CLI dependencies.
"""

from argparse import Namespace
from typing import Any, Dict

from ..interface import Command


class InstallToolsCommand(Command):
    """
    Command for installing and managing EmailIntelligence CLI tools.

    This command wraps the InstallationService to handle tool installation,
    PATH management, and verification.
    """

    def __init__(self):
        self._service = None

    @property
    def name(self) -> str:
        return "install-tools"

    @property
    def description(self) -> str:
        return "Install and manage CLI tool dependencies"

    def add_arguments(self, parser: Any) -> None:
        """Add command-specific arguments."""
        parser.add_argument(
            "--tool",
            type=str,
            help="Specific tool to install (git-verifier, kilocode, email-intelligence)",
        )
        parser.add_argument("--bin-dir", type=str, help="Directory to install tools to")
        parser.add_argument(
            "--force", action="store_true", help="Overwrite existing installation"
        )
        parser.add_argument("--list", action="store_true", help="List installed tools")
        parser.add_argument(
            "--info", action="store_true", help="Show installation information"
        )
        parser.add_argument("--uninstall", type=str, help="Uninstall a specific tool")

    def get_dependencies(self) -> Dict[str, Any]:
        """Return required dependencies."""
        return {}

    def set_dependencies(self, deps: Dict[str, Any]) -> None:
        """Set dependencies for the command."""
        pass

    async def execute(self, args: Namespace) -> int:
        """Execute the install-tools command."""
        try:
            from pathlib import Path
            from src.services.installation_service import (
                InstallationService,
                install_main_tools,
            )

            bin_dir = Path(args.bin_dir) if args.bin_dir else None

            if args.list:
                service = InstallationService()
                tools = service.list_installed_tools(bin_dir)
                print("\n=== Installed Tools ===")
                if tools:
                    for tool in tools:
                        print(f"  - {tool}")
                else:
                    print("No tools installed.")
                print("=" * 26)
                return 0

            if args.info:
                service = InstallationService()
                info = service.get_installation_info()
                print("\n=== Installation Info ===")
                print(f"System: {info['system']}")
                print(f"Shell: {info['shell']}")
                print(f"Python: {info['python_executable']}")
                print(f"Default bin dir: {info['default_bin_dir']}")
                print(f"Project root: {info['project_root']}")
                print(f"Installed tools: {info['installed_tools'] or 'None'}")
                print("=" * 26)
                return 0

            if args.uninstall:
                service = InstallationService()
                result = service.uninstall_tool(args.uninstall, bin_dir)
                print(f"\n=== Uninstall Result ===")
                print(f"Tool: {result['tool_name']}")
                print(f"Success: {result['success']}")
                for msg in result["messages"]:
                    print(f"  {msg}")
                for err in result["errors"]:
                    print(f"  ERROR: {err}")
                print("=" * 26)
                return 0 if result["success"] else 1

            if args.tool:
                service = InstallationService()
                result = service.install_tool(args.tool, bin_dir, args.force)
                print(f"\n=== Install Result ===")
                print(f"Tool: {result['tool_name']}")
                print(f"Success: {result['success']}")
                for msg in result["messages"]:
                    print(f"  {msg}")
                for warn in result["warnings"]:
                    print(f"  WARNING: {warn}")
                for err in result["errors"]:
                    print(f"  ERROR: {err}")
                print("=" * 26)
                return 0 if result["success"] else 1

            result = install_main_tools(None, bin_dir, args.force)
            print("\n=== Install Results ===")
            all_success = True
            for tool, res in result.items():
                print(f"\n{tool}:")
                print(f"  Success: {res['success']}")
                for msg in res["messages"]:
                    print(f"    {msg}")
                for warn in res["warnings"]:
                    print(f"    WARNING: {warn}")
                for err in res["errors"]:
                    print(f"    ERROR: {err}")
                if not res["success"]:
                    all_success = False
            print("=" * 26)
            return 0 if all_success else 1

        except Exception as e:
            print(f"Error during installation: {e}")
            return 1
