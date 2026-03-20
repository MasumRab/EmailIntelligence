"""
CLI Commands Package

Organized by functional domains (git, task, analysis, infra, automation, docs).
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
from .git.pr_extract import PRExtractCommand

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
    "PRExtractCommand",
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
]
