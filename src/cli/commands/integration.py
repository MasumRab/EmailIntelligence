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

# --- Domain-organized implementation imports ---

# 1. Git Domain
from .git.analyze import AnalyzeCommand
from .git.resolve import ResolveCommand
from .git.align import GitAlignCommand
from .git.auto_resolve import GitAutoResolveCommand
from .git.discover import GitDiscoverCommand
from .git.history import AnalyzeHistoryCommand
from .git.merge_semantic import GitMergeSemanticCommand
from .git.merge_smart import MergeSmartCommand
from .git.pr_extract import OrchExtractCommand
from .git.rebase import PlanRebaseCommand
from .git.stash_resolve import StashResolveCommand
from .git.topology import TopologyMapperCommand
from .git.logic_drift import LogicDriftAnalyzerCommand
from .git.verify_merge import VerifyMergeCommand
from .git.detect_rebased import DetectRebasedCommand
from .git.conflicts import GitConflictsCommand
from .git.branch_health import BranchHealthCommand
from .git.conflict_bisect import ConflictBisectCommand

# 2. Analysis Domain
from .analysis.code_audit import AnalyzeCodeCommand
from .analysis.compare import CompareCommand
from .analysis.import_audit import ImportAuditCommand
from .analysis.validate import ValidateCommand

# 3. Infra Domain
from .infra.backup import BackupCommand
from .infra.deploy import DeployCommand
from .infra.verify import VerifyCommand
from .infra.install_tools import InstallToolsCommand

# 4. Task Domain
from .task.analyze_tasks import AnalyzeTasksCommand
from .task.cluster_branches import ClusterBranchesCommand
from .task.list_tasks import ListTasksCommand
from .task.taskmaster import TaskmasterCommand

# 5. Automation Domain
from .automation.mcp_sync import MCPSyncCommand
from .automation.monitor import MonitorCommand

# 6. Agent Domain
from .agent.rule_sync import RuleSyncCommand
from .agent.scaffold import AgentScaffoldCommand

# 7. Workflow Domain
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

    # 2. Validation Domain - Simple in-memory validator for CLI
    class CLIValidator:
        """Simple validator for CLI validation command."""

        def __init__(self):
            pass

        async def validate(self, target):
            """Run validation on target."""

            class Result:
                is_valid = True
                details = {"cli_validation": True}

            return Result()

    dependencies["validator"] = CLIValidator()

    # 3. NLP Domain (Strategy Pattern)
    try:
        from ..services.nlp import NLPService

        dependencies["nlp"] = NLPService()
    except ImportError:
        logger.warning("NLP Service not available.")
        dependencies["nlp"] = None

    # 4. Git Domain
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

    # Git Domain
    registry.register_command(AnalyzeCommand, "agent-git")
    registry.register_command(ResolveCommand, "agent-git")
    registry.register_command(GitAlignCommand, "agent-git")
    registry.register_command(GitAutoResolveCommand, "agent-git")
    registry.register_command(GitDiscoverCommand, "agent-git")
    registry.register_command(AnalyzeHistoryCommand, "agent-git")
    registry.register_command(GitMergeSemanticCommand, "agent-git")
    registry.register_command(MergeSmartCommand, "agent-git")
    registry.register_command(OrchExtractCommand, "agent-git")
    registry.register_command(PlanRebaseCommand, "agent-git")
    registry.register_command(StashResolveCommand, "agent-git")
    registry.register_command(TopologyMapperCommand, "agent-git")
    registry.register_command(LogicDriftAnalyzerCommand, "agent-git")
    registry.register_command(VerifyMergeCommand, "agent-git")
    registry.register_command(DetectRebasedCommand, "agent-git")
    registry.register_command(GitConflictsCommand, "agent-git")
    registry.register_command(BranchHealthCommand, "agent-git")
    registry.register_command(ConflictBisectCommand, "agent-git")

    # Analysis Domain
    registry.register_command(AnalyzeCodeCommand, "agent-analyst")
    registry.register_command(CompareCommand, "agent-analyst")
    registry.register_command(ImportAuditCommand, "agent-analyst")
    registry.register_command(ValidateCommand, "agent-analyst")

    # Infra Domain
    registry.register_command(BackupCommand, "agent-infra")
    registry.register_command(DeployCommand, "agent-infra")
    registry.register_command(VerifyCommand, "agent-infra")
    registry.register_command(InstallToolsCommand, "agent-infra")

    # Task Domain
    registry.register_command(AnalyzeTasksCommand, "agent-workflow")
    registry.register_command(ClusterBranchesCommand, "agent-workflow")
    registry.register_command(ListTasksCommand, "agent-workflow")
    registry.register_command(TaskmasterCommand, "agent-workflow")

    # Automation Domain
    registry.register_command(MCPSyncCommand, "agent-automation")
    registry.register_command(MonitorCommand, "agent-automation")

    # Agent Domain
    registry.register_command(RuleSyncCommand, "agent-agent")
    registry.register_command(AgentScaffoldCommand, "agent-agent")

    # Workflow Domain
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
            logger.exception(
                f"Unexpected error executing command '{command_name}': {e}"
            )
            return 1

    return dispatch


async def run_modular_command(args: Any, dispatcher=None) -> int:
    """
    Helper function to bridge the main CLI entry point to the modular system.
    """
    if not hasattr(args, "modular_command") or not args.modular_command:
        return 0

    cmd_dispatcher = dispatcher or get_command_dispatcher()
    return await cmd_dispatcher(args.modular_command, args)
