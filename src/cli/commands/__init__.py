"""
CLI Commands Package

Organized by functional domains (git, task, analysis, infra, automation, agent).
"""

from .factory import CommandFactory
from .interface import Command
from .registry import CommandRegistry

# 1. Git Domain
from .git.analyze import AnalyzeCommand
from .git.resolve import ResolveCommand
from .git.rebase import PlanRebaseCommand
from .git.history import AnalyzeHistoryCommand
from .git.merge_smart import MergeSmartCommand
from .git.stash_resolve import StashResolveCommand
from .git.pr_extract import OrchExtractCommand

# 2. Analysis Domain
from .analysis.validate import ValidateCommand
from .analysis.compare import CompareCommand
from .analysis.code_audit import AnalyzeCodeCommand
from .analysis.import_audit import ImportAuditCommand

# 3. Infra Domain
from .infra.verify import VerifyCommand
from .infra.deploy import DeployCommand
from .infra.backup import BackupCommand

# 4. Task Domain
from .task.taskmaster import TaskmasterCommand
from .task.list_tasks import ListTasksCommand
from .task.analyze_tasks import AnalyzeTasksCommand
from .task.cluster_branches import ClusterBranchesCommand

# 5. Automation Domain
from .automation.monitor import MonitorCommand
from .automation.mcp_sync import MCPSyncCommand

# 6. Agent Domain
from .agent.scaffold import AgentScaffoldCommand
from .agent.rule_sync import RuleSyncCommand

__all__ = [
    "Command",
    "CommandFactory",
    "CommandRegistry",
    # Git
    "AnalyzeCommand",
    "ResolveCommand",
    "PlanRebaseCommand",
    "AnalyzeHistoryCommand",
    "MergeSmartCommand",
    "StashResolveCommand",
    "OrchExtractCommand",
    # Analysis
    "ValidateCommand",
    "CompareCommand",
    "AnalyzeCodeCommand",
    "ImportAuditCommand",
    # Infra
    "VerifyCommand",
    "DeployCommand",
    "BackupCommand",
    # Task
    "TaskmasterCommand",
    "ListTasksCommand",
    "AnalyzeTasksCommand",
    "ClusterBranchesCommand",
    # Automation
    "MonitorCommand",
    "MCPSyncCommand",
    # Agent
    "AgentScaffoldCommand",
    "RuleSyncCommand",
]
