"""
EmailIntelligence CLI - Main CLI Class (Compatibility Wrapper)

This module provides a compatibility wrapper around the new modular CLI structure.
"""

from cli.core import (
    EmailIntelligenceCLIBase,
    WorkflowOrchestrator,
    ConflictResolver,
    BranchManager,
    WorkspaceManager,
    GitOperations,
    ConfigManager,
    ConstitutionalAnalyzer,
    StrategyGenerator,
    ContentAligner,
    Validator,
    ResolutionManager,
)

# Main CLI class that composes all the modular components
class EmailIntelligenceCLI(EmailIntelligenceCLIBase):
    """Main CLI class - compatibility wrapper for the new modular structure"""
    
    def __init__(self):
        super().__init__()
        
        # Initialize all modular components
        self.workflow_orchestrator = WorkflowOrchestrator(self)
        self.conflict_resolver = ConflictResolver(self)
        self.branch_manager = BranchManager(self)
        self.workspace_manager_module = WorkspaceManager(self)
        self.git_operations = GitOperations(self)
        self.config_manager = ConfigManager(self)
        self.constitutional_analyzer_module = ConstitutionalAnalyzer(self)
        self.strategy_generator = StrategyGenerator(self)
        self.content_aligner = ContentAligner(self)
        self.validator = Validator(self)
        self.resolution_manager = ResolutionManager(self)
    
    # ============================================================================
    # DELEGATE METHODS - Forward calls to appropriate modules
    # ============================================================================
    
    def scan_all_branches(self, **kwargs):
        return self.workflow_orchestrator.scan_all_branches(**kwargs)
    
    def setup_resolution(self, **kwargs):
        return self.resolution_manager.setup_resolution(**kwargs)
    
    def push_resolution_to_target(self, **kwargs):
        return self.resolution_manager.push_resolution_to_target(**kwargs)
    
    def analyze_constitutional(self, **kwargs):
        return self.constitutional_analyzer_module.analyze_constitutional(**kwargs)
    
    def develop_spec_kit_strategy(self, **kwargs):
        return self.strategy_generator.develop_spec_kit_strategy(**kwargs)
    
    def align_content(self, **kwargs):
        return self.content_aligner.align_content(**kwargs)
    
    def validate_resolution(self, **kwargs):
        return self.validator.validate_resolution(**kwargs)
    
    def collect_pr_recommendations(self, **kwargs):
        return self.resolution_manager.collect_pr_recommendations(**kwargs)
    
    async def auto_resolve_conflicts(self, **kwargs):
        # Would delegate to auto resolver
        return {"status": "auto_resolved"}

# Expose the old API for backward compatibility
__all__ = ['EmailIntelligenceCLI']
