"""
GraphQL schema definitions using Graphene
"""

import graphene
from graphene import ObjectType, String, Int, Float, Boolean, List, Field, Enum, DateTime
from typing import List as TypeList

# Import our models
from ..models.graph_entities import (
    PRStatus, ConflictType, ConflictSeverity, ResolutionStrategy,
    ResolutionMethod, ChangeType
)
from ..models.fictionality_models import FictionalityScore


# GraphQL Enums
class PRStatusEnum(Enum):
    OPEN = PRStatus.OPEN
    IN_REVIEW = PRStatus.IN_REVIEW
    CONFLICT_DETECTED = PRStatus.CONFLICT_DETECTED
    RESOLVING = PRStatus.RESOLVING
    READY_TO_MERGE = PRStatus.READY_TO_MERGE
    MERGED = PRStatus.MERGED
    CLOSED = PRStatus.CLOSED
    BLOCKED = PRStatus.BLOCKED


class ConflictTypeEnum(Enum):
    MERGE_CONFLICT = ConflictType.MERGE_CONFLICT
    DEPENDENCY_CONFLICT = ConflictType.DEPENDENCY_CONFLICT
    ARCHITECTURE_VIOLATION = ConflictType.ARCHITECTURE_VIOLATION
    TEST_FAILURE = ConflictType.TEST_FAILURE
    CODE_STYLE_VIOLATION = ConflictType.CODE_STYLE_VIOLATION
    SECURITY_VIOLATION = ConflictType.SECURITY_VIOLATION
    PERFORMANCE_ISSUE = ConflictType.PERFORMANCE_ISSUE


class ConflictSeverityEnum(Enum):
    CRITICAL = ConflictSeverity.CRITICAL
    HIGH = ConflictSeverity.HIGH
    MEDIUM = ConflictSeverity.MEDIUM
    LOW = ConflictSeverity.LOW
    INFO = ConflictSeverity.INFO


class ResolutionStrategyEnum(Enum):
    AUTOMATIC = ResolutionStrategy.AUTOMATIC
    SEMI_AUTOMATIC = ResolutionStrategy.SEMI_AUTOMATIC
    MANUAL = ResolutionStrategy.MANUAL
    REQUIRES_REVIEW = ResolutionStrategy.REQUIRES_REVIEW
    BLOCKED = ResolutionStrategy.BLOCKED


class ResolutionMethodEnum(Enum):
    AI_RESOLVED = ResolutionMethod.AI_RESOLVED
    SUGGESTED_MERGE = ResolutionMethod.SUGGESTED_MERGE
    REBASE_REQUIRED = ResolutionMethod.REBASE_REQUIRED
    MANUAL_INTERVENTION = ResolutionMethod.MANUAL_INTERVENTION
    ARCHITECTURE_REFACTOR = ResolutionMethod.ARCHITECTURE_REFACTOR


# Fictionality Enums
class FictionalityScoreEnum(Enum):
    HIGHLY_FICTIONAL = FictionalityScore.HIGHLY_FICTIONAL
    PROBABLY_FICTIONAL = FictionalityScore.PROBABLY_FICTIONAL
    UNCERTAIN = FictionalityScore.UNCERTAIN
    PROBABLY_REAL = FictionalityScore.PROBABLY_REAL
    HIGHLY_REAL = FictionalityScore.HIGHLY_REAL


# GraphQL Types
class ConflictType(ObjectType):
    """GraphQL type for Conflict"""
    id = String(required=True)
    type = Field(ConflictTypeEnum, required=True)
    severity = Field(ConflictSeverityEnum, required=True)
    description = String(required=True)
    affected_files = List(String)
    affected_commits = List(String)
    detected_at = DateTime(required=True)
    created_at = DateTime(required=True)
    updated_at = DateTime(required=True)


class ConflictResolutionType(ObjectType):
    """GraphQL type for Conflict Resolution"""
    id = String(required=True)
    method = Field(ResolutionMethodEnum, required=True)
    description = String(required=True)
    applied_at = DateTime(required=True)
    confidence = Float(required=True)
    ai_generated = Boolean(required=True)


class AIAnalysisType(ObjectType):
    """GraphQL type for AI Analysis"""
    id = String(required=True)
    conflict_type = String(required=True)
    complexity = Float(required=True)
    resolution_suggestions = List(String)
    estimated_time = Int(required=True)
    confidence = Float(required=True)
    model = String(required=True)
    created_at = DateTime(required=True)
    # AI-specific fields
    overall_assessment = String()
    risk_level = String()
    detailed_analysis = graphene.JSONString()
    processing_time = Float()
    tokens_used = Int()
    ai_error = String()
    fallback_used = Boolean()


class ResolutionSuggestionType(ObjectType):
    """GraphQL type for AI Resolution Suggestions"""
    id = String(required=True)
    name = String(required=True)
    approach = String(required=True)
    complexity = Int(required=True)
    time_estimate = Int(required=True)
    confidence = Float(required=True)
    risk_level = String()
    steps = List(String)
    code_changes = String()
    testing_plan = String()
    rollback_plan = String()
    success_criteria = List(String)
    potential_blockers = List(String)
    ai_generated = Boolean(required=True)
    created_at = DateTime(required=True)
    analysis_id = String()


class AIHealthReportType(ObjectType):
    """GraphQL type for AI Health Report"""
    timestamp = DateTime(required=True)
    overall_status = String(required=True)
    current_metrics = graphene.JSONString(required=True)
    service_health = graphene.JSONString(required=True)
    trends = graphene.JSONString()
    recent_alerts = List(graphene.JSONString)
    usage_analytics = graphene.JSONString()
    recommendations = List(String)


class AIProcessingTaskType(ObjectType):
    """GraphQL type for AI Processing Tasks"""
    id = String(required=True)
    task_type = String(required=True)
    status = String(required=True)
    priority = String(required=True)
    created_at = DateTime(required=True)
    started_at = DateTime()
    completed_at = DateTime()
    error = String()
    result = graphene.JSONString()
    retry_count = Int(required=True)
    max_retries = Int(required=True)


class AILogType(ObjectType):
    """GraphQL type for AI Operation Logs"""
    id = String(required=True)
    operation_type = String(required=True)
    pr_id = String()
    status = String(required=True)
    duration = Float()
    tokens_used = Int()
    cost_estimate = Float()
    timestamp = DateTime(required=True)
    metadata = graphene.JSONString()


class PullRequestType(ObjectType):
    """GraphQL type for Pull Request"""
    id = String(required=True)
    title = String(required=True)
    description = String()
    source_branch = String(required=True)
    target_branch = String(required=True)
    status = Field(PRStatusEnum, required=True)
    conflicts = List(ConflictType)
    complexity = Float(required=True)
    estimated_resolution_time = Int(required=True)
    created_at = DateTime(required=True)
    updated_at = DateTime(required=True)
    # AI-specific fields
    ai_analysis = List(AIAnalysisType)
    ai_suggestions = List(ResolutionSuggestionType)
    processing_tasks = List(AIProcessingTaskType)


class PRResolutionType(ObjectType):
    """GraphQL type for PR Resolution"""
    id = String(required=True)
    strategy = Field(ResolutionStrategyEnum, required=True)
    description = String(required=True)
    applied_at = DateTime(required=True)
    success = Boolean(required=True)
    feedback = String()


# Response Types
class ProcessResultType(ObjectType):
    """GraphQL type for Process Result"""
    success = Boolean(required=True)
    message = String(required=True)
    processing_time = Float(required=True)
    conflicts_detected = Int(required=True)


class EscalationResultType(ObjectType):
    """GraphQL type for Escalation Result"""
    success = Boolean(required=True)
    escalated_to = String(required=True)
    reason = String(required=True)


class TrendPointType(ObjectType):
    """GraphQL type for Trend Point"""
    timestamp = DateTime(required=True)
    value = Float(required=True)
    label = String(required=True)


class WorkloadAnalysisType(ObjectType):
    """GraphQL type for Workload Analysis"""
    current_prs = Int(required=True)
    average_resolution_time = Float(required=True)
    expertise_score = Float(required=True)
    conflict_rate = Float(required=True)


class PatternType(ObjectType):
    """GraphQL type for Pattern"""
    pattern_type = String(required=True)
    frequency = Int(required=True)
    description = String(required=True)
    confidence = Float(required=True)


class SystemHealthType(ObjectType):
    """GraphQL type for System Health"""
    status = String(required=True)
    services = graphene.JSONString(required=True)
    timestamp = DateTime(required=True)
    uptime = Float(required=True)


# Fictionality Types
class FictionalityAnalysisType(ObjectType):
    """GraphQL type for Fictionality Analysis"""
    id = String(required=True)
    conflict_id = String()
    pr_id = String()
    fictionality_score = Float(required=True)
    confidence_level = Field(FictionalityScoreEnum, required=True)
    text_content = String(required=True)
    analysis_features = graphene.JSONString()
    fictionality_indicators = List(String, required=True)
    realism_indicators = List(String, required=True)
    model = String(required=True)
    processing_time = Float(required=True)
    tokens_used = Int(required=True)
    reasoning = String()
    resolution_impact = String()
    strategy_adjustments = List(String, required=True)
    analysis_depth = String()
    custom_threshold = Float()
    created_at = DateTime(required=True)
    updated_at = DateTime(required=True)


class FictionalityMetricsType(ObjectType):
    """GraphQL type for Fictionality Metrics"""
    total_analyses = Int(required=True)
    high_fictionality_count = Int(required=True)
    uncertain_count = Int(required=True)
    low_fictionality_count = Int(required=True)
    average_score = Float(required=True)
    average_processing_time = Float(required=True)
    cache_hit_rate = Float(required=True)
    fictionality_distribution = graphene.JSONString()


class FictionalitySummaryType(ObjectType):
    """GraphQL type for Fictionality Summary"""
    total_analyses = Int(required=True)
    high_fictionality_count = Int(required=True)
    uncertain_count = Int(required=True)
    low_fictionality_count = Int(required=True)
    average_score = Float(required=True)
    recent_analyses = List(FictionalityAnalysisType, required=True)
    trends = graphene.JSONString()


class FictionalityHealthReportType(ObjectType):
    """GraphQL type for Fictionality Health Report"""
    status = String(required=True)
    healthy = Boolean(required=True)
    services = graphene.JSONString(required=True)
    timestamp = DateTime(required=True)
    uptime = Float(required=True)
    metrics = Field(FictionalityMetricsType, required=True)
class FictionalityAnalyticsType(ObjectType):
    """GraphQL type for Fictionality Analytics"""
    total_analyses = Int(required=True)
    average_fictionality_score = Float(required=True)
    high_fictionality_percentage = Float(required=True)
    low_fictionality_percentage = Float(required=True)
    trend_direction = String(required=True)
    top_fictionality_indicators = List(String, required=True)
    analysis_distribution = graphene.JSONString()
    performance_metrics = graphene.JSONString()


class ConflictWithFictionalityType(ObjectType):
    """GraphQL type for Conflict with Fictionality Analysis"""
    id = String(required=True)
    type = String(required=True)
    severity = String(required=True)
    description = String(required=True)
    affected_files = List(String)
    fictionality_analysis_id = String()
    fictionality_score = Float()
    fictionality_indicators = List(String)
    fictionality_confidence = String()
    fictionality_analysis = Field(FictionalityAnalysisType)


class FictionalityFilterResultType(ObjectType):
    """GraphQL type for Fictionality Filter Results"""
    conflicts = List(ConflictWithFictionalityType, required=True)
    total_count = Int(required=True)
    filters_applied = graphene.JSONString()



# Input Types
class CreatePRInputType(graphene.InputObjectType):
    """GraphQL input type for creating PR"""
    title = String(required=True)
    description = String()
    source_branch = String(required=True)
    target_branch = String(required=True)
    author_id = String(required=True)


class UpdatePRStatusInputType(graphene.InputObjectType):
    """GraphQL input type for updating PR status"""
    pr_id = String(required=True)
    status = Field(PRStatusEnum, required=True)


class ResolveConflictInputType(graphene.InputObjectType):
    """GraphQL input type for resolving conflicts"""
    conflict_id = String(required=True)
    method = Field(ResolutionMethodEnum, required=True)
    description = String(required=True)


# Fictionality Input Types
class FictionalityAnalysisRequestType(graphene.InputObjectType):
    """GraphQL input type for fictionality analysis request"""
    pr_id = String(required=True)
    conflict_id = String(required=True)
    content = String(required=True)
    analysis_type = String(default_value="comprehensive")
    priority = String(default_value="normal")


class FictionalityAnalysisOptionsType(graphene.InputObjectType):
    """GraphQL input type for fictionality analysis options"""
    include_features = Boolean(default_value=True)
    include_indicators = Boolean(default_value=True)
    include_strategies = Boolean(default_value=True)
    custom_threshold = Float()
    analysis_depth = String(default_value="standard")


# Query Type
class Query(ObjectType):
    """GraphQL Query type"""
    
    # PR Management
    pull_request = Field(PullRequestType, id=String(required=True))
    pull_requests = List(
        PullRequestType,
        status=Field(PRStatusEnum),
        author=String(),
        assigned=Boolean(),
        limit=Int(default_value=50),
        offset=Int(default_value=0)
    )
    
    # Graph Traversal
    pr_conflicts = List(ConflictType, pr_id=String(required=True))
    pr_dependencies = List(PullRequestType, pr_id=String(required=True))
    similar_prs = List(PullRequestType, pr_id=String(required=True), limit=Int(default_value=10))
    
    # Analytics
    pr_complexity = Float(pr_id=String(required=True))
    resolution_time = Int(pr_id=String(required=True))
    conflict_trends = List(TrendPointType, period=String(required=True))
    
    # Developer Insights
    developer_workload = Field(WorkloadAnalysisType, developer_id=String(required=True))
    conflict_patterns = List(PatternType, developer_id=String(required=True))
    
    # System
    system_health = Field(SystemHealthType)
    
    # Conflict Management
    conflicts = List(
        ConflictType,
        severity=Field(ConflictSeverityEnum),
        conflict_type=Field(ConflictTypeEnum),
        limit=Int(default_value=50)
    )
    
    # AI Analysis
    ai_analysis = List(AIAnalysisType, pr_id=String(required=True))
    ai_suggestions = List(ResolutionSuggestionType, analysis_id=String(required=True))
    ai_health_report = Field(AIHealthReportType)
    ai_processing_tasks = List(AIProcessingTaskType, status=String())
    ai_logs = List(AILogType, pr_id=String(), operation_type=String(), limit=Int(default_value=50))
    
    # AI Performance
    ai_performance_analysis = graphene.JSONString(hours=Int(default_value=24))
    circuit_breaker_status = graphene.JSONString()
    ai_metrics = graphene.JSONString()
    
    # Fictionality Analysis
    fictionality_analysis = Field(FictionalityAnalysisType, id=String(required=True))
    fictionality_analyses = List(
        FictionalityAnalysisType,
        conflict_id=String(),
        pr_id=String(),
        min_score=Float(),
        max_score=Float(),
        confidence=FictionalityScoreEnum(),
        limit=Int(default_value=50),
        offset=Int(default_value=0)
    )
    fictionality_metrics = Field(FictionalityMetricsType, pr_id=String(), period=String(default_value="7d"))
    fictionality_summary = Field(FictionalitySummaryType, pr_id=String())
    fictionality_trends = List(TrendPointType, period=String(default_value="30d"))
    fictionality_health_report = Field(FictionalityHealthReportType)
    fictionality_analytics = Field(FictionalityAnalyticsType, pr_id=String(), period=String(default_value="30d"))
    fictionality_filter_conflicts = Field(FictionalityFilterResultType, 
                                        min_score=Float(), max_score=Float(), 
                                        confidence_levels=List(FictionalityScoreEnum), 
                                        include_indicators=List(String), 
                                        exclude_indicators=List(String), 
                                        pr_id=String(), limit=Int(default_value=50), 
                                        offset=Int(default_value=0))



# Mutation Type
class Mutation(ObjectType):
    """GraphQL Mutation type"""
    
    # PR Processing
    create_pr = Field(PullRequestType, input=CreatePRInputType(required=True))
    update_pr_status = Field(PullRequestType, input=UpdatePRStatusInputType(required=True))
    resolve_conflict = Field(ConflictResolutionType, input=ResolveConflictInputType(required=True))
    
    # Batch Operations
    batch_process_prs = List(ProcessResultType, pr_ids=List(String, required=True))
    
    # Manual Interventions
    escalate_pr = Field(EscalationResultType, pr_id=String(required=True), reason=String(required=True))
    add_manual_resolution = Field(PRResolutionType, pr_id=String(required=True), resolution=String(required=True))
    
    # AI Processing
    analyze_conflict_with_ai = Field(AIAnalysisType, pr_id=String(required=True), conflict_id=String(required=True))
    generate_resolution_suggestions = List(ResolutionSuggestionType, analysis_id=String(required=True))
    validate_solution_with_ai = graphene.JSONString(
        solution=String(required=True),
        context=graphene.JSONString(required=True)
    )
    assess_pr_complexity_ai = graphene.JSONString(pr_id=String(required=True))
    
    # AI Management
    cancel_ai_task = Boolean(task_id=String(required=True))
    retry_ai_task = Boolean(task_id=String(required=True))
    clear_ai_cache = Boolean()
    trigger_ai_health_check = Field(AIHealthReportType)
    
    # AI Monitoring
    start_ai_monitoring = Boolean()
    stop_ai_monitoring = Boolean()
    update_ai_settings = Boolean(
        rate_limit_rpm=Int(),
        cache_ttl=Int(),
        temperature=Float(),
        circuit_breaker_threshold=Int()
    )
    
    # Fictionality Analysis
    analyze_fictionality = Field(
        FictionalityAnalysisType,
        pr_id=String(required=True),
        conflict_id=String(required=True),
        content=String(required=True),
        analysis_options=FictionalityAnalysisOptionsType()
    )
    batch_analyze_fictionality = List(
        FictionalityAnalysisType,
        requests=List(FictionalityAnalysisRequestType, required=True),
        max_concurrent=Int(default_value=3)
    )
    update_fictionality_settings = Boolean(
        sensitivity=Float(),
        cache_ttl=Int(),
        custom_prompts=graphene.JSONString()
    )
    clear_fictionality_cache = Int(pattern=String())
    prefetch_fictionality_analysis = Boolean(pr_id=String(required=True))


# Subscription Type
class Subscription(ObjectType):
    """GraphQL Subscription type for real-time updates"""
    
    pr_status_changed = Field(PRStatusEnum, pr_id=String(required=True))
    conflict_detected = Field(ConflictType, pr_id=String(required=True))
    resolution_completed = Field(PRResolutionType, pr_id=String(required=True))
    system_health = Field(SystemHealthType)


# Main Schema
schema = graphene.Schema(query=Query, mutation=Mutation, subscription=Subscription)