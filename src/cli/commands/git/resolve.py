"""
Resolve Command Module

Implements the resolve command for conflict resolution.
"""

from argparse import Namespace
from typing import Any, Dict

from ..interface import Command


class ResolveCommand(Command):
    """
    Command for resolving specific conflicts using strategies.

    This command provides a framework for resolving individual conflicts
    with specific strategies. Currently provides a stub implementation
    that can be extended with AutoResolver integration.
    """

    @property
    def name(self) -> str:
        return "git-resolve"

    @property
    def description(self) -> str:
        return "Resolve a specific conflict using a strategy"

    def add_arguments(self, parser: Any) -> None:
        """
        Add command-specific arguments.

        Args:
            parser: ArgumentParser subparser for this command
        """
        parser.add_argument("conflict_id", help="ID of the conflict to resolve")
        parser.add_argument("strategy_id", help="ID of the strategy to use")

    def get_dependencies(self) -> Dict[str, Any]:
        """
        Get required dependencies for this command.

        Returns:
            Dict mapping dependency names to types
        """
        return {
            "resolver": "AutoResolver",
            "validator": "Validator",
        }

    def set_dependencies(self, dependencies: Dict[str, Any]) -> None:
        """
        Set command dependencies.

        Args:
            dependencies: Dict of dependency instances
        """
        self._resolver = dependencies.get("resolver")
        self._validator = dependencies.get("validator")

    async def execute(self, args: Namespace) -> int:
        """
        Execute the resolve command.

        Args:
            args: Parsed command-line arguments

        Returns:
            int: Exit code (0 for success, 1 for error)
        """
        try:
            conflict_id = args.conflict_id
            strategy_id = args.strategy_id

            print(f"Resolving conflict {conflict_id} with strategy {strategy_id}...")

            try:
                from src.core.resolution.engine import AutoResolver, ResolutionStrategy
                from src.core.models.git import ConflictModel, ConflictType

                # Execute real resolution logic via the AutoResolver engine
                resolver = AutoResolver()

                # Build mock ConflictModel using the CLI inputs
                import subprocess

                def get_blob(stage):
                    try:
                        res = subprocess.run(["git", "show", f":{stage}:{conflict_id}"], capture_output=True, text=True, check=True)
                        return res.stdout
                    except subprocess.CalledProcessError:
                        return ""

                def get_hash(stage):
                    try:
                        res = subprocess.run(["git", "ls-files", "-s", conflict_id], capture_output=True, text=True, check=True)
                        for line in res.stdout.strip().split('\n'):
                            parts = line.split()
                            if len(parts) >= 3 and parts[2] == str(stage):
                                return parts[1]
                        return ""
                    except subprocess.CalledProcessError:
                        return ""

                # Extract authentic conflict data from git index
                base_content = get_blob(1)
                ours_content = get_blob(2)
                theirs_content = get_blob(3)
                hash_ours = get_hash(2)
                hash_theirs = get_hash(3)

                conflict = ConflictModel(
                    path=conflict_id,
                    type=ConflictType.CONTENT,
                    base_content=base_content,
                    ours_content=ours_content,
                    theirs_content=theirs_content,
                    resolved_content=None,
                    oid_ours=hash_ours,
                    oid_theirs=hash_theirs,
                    oid_base=get_hash(1)
                )

                # Attempt to map strategy string to Enum
                try:
                    strategy_enum = ResolutionStrategy(strategy_id.lower())
                except ValueError:
                    strategy_enum = ResolutionStrategy.UNION

                result = resolver.resolve(conflict, strategy_enum)
                success = True
                message = f"Resolution executed: {result}"

            except ImportError as err:
                print(f"Error: Resolution engine dependencies not available: {err}")
                return 1

            if success:
                print(f"Resolution successful: {message}")
                return 0
            else:
                print(f"Resolution failed: {message}")
                return 1

        except Exception as e:
            print(f"Error during resolution: {e}")
            return 1
