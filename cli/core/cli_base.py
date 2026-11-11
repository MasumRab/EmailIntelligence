"""
CLI Base Class - Core infrastructure for EmailIntelligence CLI
"""
import asyncio
import logging
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

# Constitutional Engine integration
try:
    from resolution import ConstitutionalEngine
except ImportError:
    ConstitutionalEngine = None

# Git Operations integration
try:
    from git.conflict_detector import GitConflictDetector
except ImportError:
    GitConflictDetector = None

try:
    from core.conflict_models import Conflict, ConflictBlock, ConflictTypeExtended, RiskLevel
except ImportError:
    Conflict = ConflictBlock = ConflictTypeExtended = RiskLevel = None

try:
    from analysis.conflict_analyzer import ConflictAnalyzer
except ImportError:
    ConflictAnalyzer = None

# Additional imports for interface-based architecture
try:
    from analysis.constitutional.analyzer import ConstitutionalAnalyzer
except ImportError:
    ConstitutionalAnalyzer = None

try:
    from resolution.auto_resolver import AutoResolver
except ImportError:
    AutoResolver = None

try:
    from resolution.semantic_merger import SemanticMerger
except ImportError:
    SemanticMerger = None

try:
    from strategy.generator import StrategyGenerator
except ImportError:
    StrategyGenerator = None

try:
    from strategy.risk_assessor import RiskAssessor
except ImportError:
    RiskAssessor = None

try:
    from validation.validator import Validator
except ImportError:
    Validator = None

try:
    import yaml
except ImportError:
    yaml = None

# Use absolute imports from the cli package
from cli.conflict import ConflictDetector
from cli.exceptions import (
    BranchNotFoundError,
    GitOperationError,
    MergeTreeError,
    PushOperationError,
)
from cli.models import (
    BranchPairResult,
    ConflictMatrix,
    ConflictReport,
    ConflictSeverity,
    ConflictType,
    SemanticConflictAnalysis,
    GitWorkspaceManager,
)
from cli.semantic import SemanticConflictDetector
from cli.workspace import RobustWorkspaceManager


# ============================================================================
# LOGGING HELPERS
# ============================================================================

def _setup_logger(name: str) -> logging.Logger:
    """Setup a logger with consistent formatting."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter('%(message)s'))
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger


# ============================================================================
# BASE CLI CLASS - Core Infrastructure
# ============================================================================

class EmailIntelligenceCLIBase:
    """Base CLI class with core infrastructure - extracted from god class"""

    def __init__(self):
        self.repo_root = Path.cwd()
        self.worktrees_dir = self.repo_root / ".git" / "worktrees"
        self.resolution_branches_dir = self.repo_root / "resolution-workspace"
        self.config_file = self.repo_root / ".emailintelligence" / "config.yaml"
        self.constitutions_dir = self.repo_root / ".emailintelligence" / "constitutions"
        self.strategies_dir = self.repo_root / ".emailintelligence" / "strategies"

        self.logger = _setup_logger("EmailIntelligenceCLI")
        self.remote = "origin"  # Default remote

        # Create necessary directories
        self._ensure_directories()

        # Load configuration
        self.config = self._load_config()

        # Initialize Constitutional Engine
        if ConstitutionalEngine:
            self.constitutional_engine = ConstitutionalEngine(
                constitution_file=self.config.get('constitutional_framework', {}).get('default_constitution_file')
            )
        else:
            self.constitutional_engine = None
        # Lazy initialization flag
        self._constitutional_engine_initialized = False

        # Initialize Conflict Detector
        self.conflict_detector = ConflictDetector(self.repo_root)

        # Initialize Workspace Manager with fallback support
        self.workspace_manager = RobustWorkspaceManager(self.repo_root)

        # Initialize Conflict Analyzer
        self.conflict_analyzer = ConflictAnalyzer()

        # Initialize additional components for interface-based architecture
        if ConstitutionalAnalyzer:
            self.constitutional_analyzer = ConstitutionalAnalyzer()
        else:
            self.constitutional_analyzer = None
        
        if AutoResolver:
            self.auto_resolver = AutoResolver()
        else:
            self.auto_resolver = None
            
        if SemanticMerger:
            self.semantic_merger = SemanticMerger()
        else:
            self.semantic_merger = None
            
        if StrategyGenerator:
            self.strategy_generator = StrategyGenerator()
        else:
            self.strategy_generator = None
            
        if RiskAssessor:
            self.risk_assessor = RiskAssessor()
        else:
            self.risk_assessor = None
            
        if Validator:
            self.validator = Validator()
        else:
            self.validator = None

        # Initialize git repository check
        self._check_git_repository()

    # ============================================================================
    # LOGGING METHODS
    # ============================================================================

    def _info(self, message: str) -> None:
        """Log info message."""
        self.logger.info(message)

    def _warn(self, message: str) -> None:
        """Log warning message."""
        self.logger.warning(f"⚠️  {message}")

    def _error(self, message: str) -> None:
        """Log error message."""
        self.logger.error(f"❌ {message}")

    def _success(self, message: str) -> None:
        """Log success message."""
        self.logger.info(f"✅ {message}")

    def _error_exit(self, message: str) -> None:
        """Log error and exit."""
        self._error(message)
        sys.exit(1)

    # ============================================================================
    # INFRASTRUCTURE METHODS
    # ============================================================================

    def _ensure_directories(self) -> None:
        """Ensure required directories exist."""
        directories = [
            self.worktrees_dir,
            self.resolution_branches_dir,
            self.constitutions_dir,
            self.strategies_dir,
        ]
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from config file."""
        if self.config_file.exists():
            with open(self.config_file) as f:
                if yaml:
                    return yaml.safe_load(f) or {}
        return {}

    def _check_git_repository(self) -> None:
        """Verify we're in a git repository."""
        if not (self.repo_root / ".git").exists():
            self._error_exit("Not a git repository")
