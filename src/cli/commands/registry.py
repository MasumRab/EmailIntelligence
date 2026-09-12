"""
Command Registry Module

Manages registration and discovery of commands.
Provides centralized command management for the CLI system.
"""

from typing import Dict, List, Type

from .factory import CommandFactory
from .interface import Command


class CommandRegistry:
    """
    Registry for managing and discovering commands.

    This registry provides:
    - Command registration and discovery
    - Agent assignment tracking
    - Command metadata management
    - Integration with the command factory
    """

    def __init__(self, factory: CommandFactory):
        """
        Initialize the command registry.

        Args:
            factory: The command factory to use for command creation
        """
        self._factory = factory
        self._agent_assignments: Dict[str, str] = {}
        self._command_metadata: Dict[str, Dict] = {}

    def register_command(
        self, command_class: Type[Command], agent: str = "system"
    ) -> None:
        """
        Register a command class with the registry.

        Args:
            command_class: The command class to register
            agent: Agent responsible for this command (for coordination)
        """
        self._factory.register_command(command_class)

        # Create temporary instance to get metadata
        command_instance = command_class()
        command_name = command_instance.name

        # Store agent assignment
        self._agent_assignments[command_name] = agent

        # Store metadata
        self._command_metadata[command_name] = {
            "description": command_instance.description,
            "agent": agent,
            "class": command_class.__name__,
            "module": command_class.__module__,
        }

    def get_command(self, command_name: str) -> Command:
        """
        Get a command instance by name.

        Args:
            command_name: Name of the command to retrieve

        Returns:
            Command instance

        Raises:
            ValueError: If command is not registered
        """
        command = self._factory.create_command(command_name)
        if command is None:
            raise ValueError(f"Command '{command_name}' is not registered")
        return command

    def get_agent_for_command(self, command_name: str) -> str:
        """
        Get the agent assigned to a command.

        Args:
            command_name: Name of the command

        Returns:
            Agent name or 'system' if not assigned
        """
        return self._agent_assignments.get(command_name, "system")

    def get_commands_by_agent(self, agent: str) -> List[str]:
        """
        Get all commands assigned to a specific agent.

        Args:
            agent: Agent name

        Returns:
            List of command names
        """
        return [
            cmd
            for cmd, cmd_agent in self._agent_assignments.items()
            if cmd_agent == agent
        ]

    def get_all_commands(self) -> Dict[str, Dict]:
        """
        Get metadata for all registered commands.

        Returns:
            Dict mapping command names to metadata
        """
        return self._command_metadata.copy()

    def has_command(self, command_name: str) -> bool:
        """
        Check if a command is registered.

        Args:
            command_name: Name of the command

        Returns:
            True if registered, False otherwise
        """
        return self._factory.has_command(command_name)

    def get_available_commands(self) -> Dict[str, str]:
        """
        Get all available commands with descriptions.

        Returns:
            Dict mapping command names to descriptions
        """
        return self._factory.get_available_commands()

    def get_registry_status(self) -> Dict:
        """
        Get comprehensive registry status for debugging/monitoring.

        Returns:
            Dict with registry statistics and assignments
        """
        agent_counts = {}
        for agent in self._agent_assignments.values():
            agent_counts[agent] = agent_counts.get(agent, 0) + 1

        return {
            "total_commands": len(self._command_metadata),
            "agents": list(agent_counts.keys()),
            "agent_counts": agent_counts,
            "commands_by_agent": {
                agent: self.get_commands_by_agent(agent)
                for agent in agent_counts.keys()
            },
        }
