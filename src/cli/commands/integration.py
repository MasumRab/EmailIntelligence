"""
CLI Commands Integration Module - Bridge Pattern Edition

Provides centralized factory setup, command registration, and CLI dispatch.
This module acts as the Bridge between the Abstraction (Orchestration Process) 
and the Implementation (Discrete CLI Commands).
"""

import asyncio
import logging
from typing import Any, Dict, Optional

from .factory import CommandFactory
from .registry import CommandRegistry
from .interface import Command

# Implementation imports
from .analyze_command import AnalyzeCommand
from .resolve_command import ResolveCommand
from .validate_command import ValidateCommand
from .analyze_history_command import AnalyzeHistoryCommand
from .plan_rebase_command import PlanRebaseCommand
from .guide import GuideCommand

logger = logging.getLogger(__name__)

def create_default_dependencies() -> Dict[str, Any]:
    """
    Creates and returns the default dependencies for CLI commands.
    Implements Dependency Injection following SOLID principles.
    """
    dependencies = {}

    # 1. Security Domain (Proxy Pattern)
    try:
        from ...core.security import SecurityValidator, SecureFileSystemProxy
        validator = SecurityValidator()
        dependencies["security_validator"] = validator
        dependencies["fs_proxy"] = SecureFileSystemProxy(validator)
    except ImportError:
        logger.warning("Security modules not available. Using fallback placeholders.")
        dependencies["security_validator"] = None
        dependencies["fs_proxy"] = None

    # 2. NLP Domain (Strategy Pattern)
    try:
        from ..services.nlp import NLPService
        dependencies["nlp"] = NLPService()
    except ImportError:
        logger.warning("NLP Service not available.")
        dependencies["nlp"] = None

    # 3. Git Domain
    try:
        from ..git.worktree import WorktreeManager
        dependencies["worktree_manager"] = WorktreeManager()
    except ImportError:
        dependencies["worktree_manager"] = None

    return dependencies

def get_command_registry(factory: Optional[CommandFactory] = None) -> CommandRegistry:
    """
    Initializes and returns the CommandRegistry with all commands registered.
    """
    cmd_factory = factory or CommandFactory(create_default_dependencies())
    registry = CommandRegistry(cmd_factory)

    # Register all commands with domain assignments
    # (Mapping Abstractions to Implementations)
    registry.register_command(AnalyzeCommand, "agent-analyst")
    registry.register_command(ResolveCommand, "agent-resolver")
    registry.register_command(ValidateCommand, "agent-validator")
    registry.register_command(AnalyzeHistoryCommand, "agent-analyst")
    registry.register_command(PlanRebaseCommand, "agent-planner")
    registry.register_command(GuideCommand, "agent-workflow")

    return registry

def get_command_dispatcher(registry: Optional[CommandRegistry] = None):
    """
    Returns a dispatcher function for executing modular commands.
    """
    cmd_registry = registry or get_command_registry()

    async def dispatch(command_name: str, args: Any) -> int:
        try:
            command = cmd_registry.get_command(command_name)
            if not command:
                print(f"Error: Command '{command_name}' not found.")
                return 1
            return await command.execute(args)
        except Exception as e:
            logger.exception(f"Unexpected error executing command '{command_name}': {e}")
            return 1

    return dispatch

async def run_modular_command(args: Any, dispatcher = None) -> int:
    """
    Helper function to bridge the main CLI entry point to the modular system.
    """
    if not hasattr(args, "modular_command") or not args.modular_command:
        return 0

    cmd_dispatcher = dispatcher or get_command_dispatcher()
    return await cmd_dispatcher(args.modular_command, args)
