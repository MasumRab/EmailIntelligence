"""
CLI Commands Package

Organized by functional domains (git, task, analysis, agent).

Every command in this package implements the ``Command`` interface defined in
``interface.py``. Without that module and this package ``__init__``, the
command modules are unimportable: each one starts with ``from ..interface
import Command``, so the whole tree raised ``ModuleNotFoundError`` before these
files existed.
"""

from .agent.rule_sync import RuleSyncCommand
from .agent.scaffold import AgentScaffoldCommand
from .analysis.code_audit import AnalyzeCodeCommand
from .analysis.compare import CompareCommand
from .analysis.import_audit import ImportAuditCommand
from .analysis.validate import ValidateCommand
from .factory import CommandFactory
from .git.analyze import AnalyzeCommand
from .git.history import AnalyzeHistoryCommand
from .git.merge_smart import MergeSmartCommand
from .git.pr_extract import OrchExtractCommand
from .git.rebase import PlanRebaseCommand
from .git.resolve import ResolveCommand
from .git.stash_resolve import StashResolveCommand
from .interface import Command
from .registry import CommandRegistry
from .task.analyze_tasks import AnalyzeTasksCommand
from .task.cluster_branches import ClusterBranchesCommand
from .task.list_tasks import ListTasksCommand
from .task.taskmaster import TaskmasterCommand

__all__ = [
    "AgentScaffoldCommand",
    "AnalyzeCodeCommand",
    "AnalyzeCommand",
    "AnalyzeHistoryCommand",
    "AnalyzeTasksCommand",
    "ClusterBranchesCommand",
    "Command",
    "CommandFactory",
    "CommandRegistry",
    "CompareCommand",
    "ImportAuditCommand",
    "ListTasksCommand",
    "MergeSmartCommand",
    "OrchExtractCommand",
    "PlanRebaseCommand",
    "ResolveCommand",
    "RuleSyncCommand",
    "StashResolveCommand",
    "TaskmasterCommand",
    "ValidateCommand",
]
