"""
CLI Commands Package

Organized by functional domains (git, task, analysis, infra, automation, docs).
"""

from .factory import CommandFactory
from .interface import Command
from .registry import CommandRegistry

# Domain-specific commands
from .git.analyze import AnalyzeCommand
from .git.resolve import ResolveCommand
from .git.rebase import PlanRebaseCommand
from .git.history import AnalyzeHistoryCommand
from .analysis.validate import ValidateCommand
from .analysis.compare import CompareCommand
from .infra.verify import VerifyCommand
from .task.taskmaster import TaskmasterCommand
from .task.list_tasks import ListTasksCommand
from .task.analyze_tasks import AnalyzeTasksCommand
from .task.cluster_branches import ClusterBranchesCommand

__all__ = [
    "Command",
    "CommandFactory",
    "CommandRegistry",
    "AnalyzeCommand",
    "ResolveCommand",
    "PlanRebaseCommand",
    "AnalyzeHistoryCommand",
    "ValidateCommand",
    "CompareCommand",
    "VerifyCommand",
    "TaskmasterCommand",
    "ListTasksCommand",
    "AnalyzeTasksCommand",
    "ClusterBranchesCommand",
]
