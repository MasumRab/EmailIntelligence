"""
Fictionality analysis models for EmailIntelligence
"""

from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

from .graph_entities import Node


class FictionalityScore(str, Enum):
    """Fictionality confidence levels"""
    HIGHLY_FICTIONAL = "HIGHLY_FICTIONAL"
    PROBABLY_FICTIONAL = "PROBABLY_FICTIONAL"
    UNCERTAIN = "UNCERTAIN"
    PROBABLY_REAL = "PROBABLY_REAL"
    HIGHLY_REAL = "HIGHLY_REAL"


class FictionalityAnalysis(Node):
    """
    Fictionality analysis model extending base Node
    
    Provides comprehensive fictionality analysis for conflicts and PRs
    """
    # Core fictionality metrics
    fictionality_score: float = Field(
        ..., 
        ge=0.0, 
        le=1.0, 
        description="Fictionality score (0.0-1.0) where 0.0 is highly real and 1.0 is highly fictional"
    )
    confidence_level: FictionalityScore = Field(
        ..., 
        description="Confidence categorization based on score"
    )
    
    # Analysis details
    text_content: str = Field(
        ..., 
        description="Content analyzed for fictionality"
    )
    analysis_features: Dict[str, float] = Field(
        default_factory=dict, 
        description="Analysis features (technical_consistency, realism_of_requirements, etc.)"
    )
    fictionality_indicators: List[str] = Field(
        default_factory=list, 
        description="Fictionality indicators found in content"
    )
    realism_indicators: List[str] = Field(
        default_factory=list, 
        description="Realism indicators found in content"
    )
    
    # Metadata
    model: str = Field(
        ..., 
        description="AI model used for analysis"
    )
    processing_time: float = Field(
        ..., 
        description="Processing time in seconds"
    )
    tokens_used: int = Field(
        ..., 
        description="Total tokens consumed"
    )
    reasoning: Optional[str] = Field(
        None, 
        description="Detailed reasoning for fictionality assessment"
    )
    
    # Integration with existing systems
    conflict_id: Optional[str] = Field(
        None, 
        description="Associated conflict ID"
    )
    pr_id: Optional[str] = Field(
        None, 
        description="Associated PR ID"
    )
    resolution_impact: Optional[str] = Field(
        None, 
        description="Impact on resolution strategy"
    )
    strategy_adjustments: List[str] = Field(
        default_factory=list, 
        description="Suggested strategy adjustments"
    )
    
    # Analysis configuration
    analysis_depth: str = Field(
        default="standard", 
        description="Analysis depth: quick, standard, deep"
    )
    custom_threshold: Optional[float] = Field(
        None, 
        description="Custom threshold used for analysis"
    )


class FictionalityContext(BaseModel):
    """
    Context data for fictionality analysis
    """
    pr_data: Dict[str, Any] = Field(
        ..., 
        description="Pull request data"
    )
    conflict_data: Dict[str, Any] = Field(
        ..., 
        description="Conflict data"
    )
    content_to_analyze: str = Field(
        ..., 
        description="Content to be analyzed"
    )
    analysis_depth: str = Field(
        default="standard", 
        description="Analysis depth preference"
    )
    include_strategies: bool = Field(
        default=True, 
        description="Whether to include strategy recommendations"
    )
    custom_threshold: Optional[float] = Field(
        None, 
        description="Custom fictionality threshold"
    )


class FictionalityMetrics(BaseModel):
    """
    Fictionality analysis metrics and statistics
    """
    total_analyses: int = Field(
        ..., 
        description="Total number of analyses performed"
    )
    high_fictionality_count: int = Field(
        ..., 
        description="Count of high fictionality analyses (score >= 0.8)"
    )
    uncertain_count: int = Field(
        ..., 
        description="Count of uncertain analyses (0.4 <= score < 0.6)"
    )
    low_fictionality_count: int = Field(
        ..., 
        description="Count of low fictionality analyses (score < 0.4)"
    )
    average_score: float = Field(
        ..., 
        description="Average fictionality score across all analyses"
    )
    average_processing_time: float = Field(
        ..., 
        description="Average processing time in seconds"
    )
    cache_hit_rate: float = Field(
        ..., 
        description="Cache hit rate for fictionality analysis"
    )
    fictionality_distribution: Dict[str, int] = Field(
        default_factory=dict, 
        description="Distribution of fictionality scores"
    )


class FictionalitySummary(BaseModel):
    """
    Summary of fictionality analysis for a specific PR or overall
    """
    total_analyses: int = Field(
        ..., 
        description="Total analyses performed"
    )
    high_fictionality_count: int = Field(
        ..., 
        description="High fictionality analyses count"
    )
    uncertain_count: int = Field(
        ..., 
        description="Uncertain fictionality analyses count"
    )
    low_fictionality_count: int = Field(
        ..., 
        description="Low fictionality analyses count"
    )
    average_score: float = Field(
        ..., 
        description="Average fictionality score"
    )
    recent_analyses: List[FictionalityAnalysis] = Field(
        ..., 
        description="Most recent analyses"
    )
    trends: List[Dict[str, Any]] = Field(
        default_factory=list, 
        description="Trend data points"
    )


# Input models for mutations
class FictionalityAnalysisRequest(BaseModel):
    """
    Input for fictionality analysis request
    """
    pr_id: str = Field(
        ..., 
        description="Pull request ID"
    )
    conflict_id: str = Field(
        ..., 
        description="Conflict ID"
    )
    content: str = Field(
        ..., 
        description="Content to analyze"
    )
    analysis_type: str = Field(
        default="comprehensive", 
        description="Type of analysis: quick, standard, comprehensive"
    )
    priority: str = Field(
        default="normal", 
        description="Priority level: low, normal, high, critical"
    )


class BatchFictionalityAnalysisRequest(BaseModel):
    """
    Input for batch fictionality analysis
    """
    requests: List[FictionalityAnalysisRequest] = Field(
        ..., 
        description="List of analysis requests"
    )
    max_concurrent: int = Field(
        default=3, 
        description="Maximum concurrent analyses"
    )


class FictionalityAnalysisOptions(BaseModel):
    """
    Options for fictionality analysis
    """
    include_features: bool = Field(
        default=True, 
        description="Include detailed features in analysis"
    )
    include_indicators: bool = Field(
        default=True, 
        description="Include fictionality/realism indicators"
    )
    include_strategies: bool = Field(
        default=True, 
        description="Include strategy recommendations"
    )
    custom_threshold: Optional[float] = Field(
        None, 
        description="Custom fictionality threshold"
    )
    analysis_depth: str = Field(
        default="standard", 
        description="Analysis depth: quick, standard, deep"
    )


# Response models
class FictionalityAnalysisResult(BaseModel):
    """
    Result of fictionality analysis operation
    """
    success: bool = Field(
        ..., 
        description="Analysis success status"
    )
    analysis: Optional[FictionalityAnalysis] = Field(
        None, 
        description="Completed analysis result"
    )
    error: Optional[str] = Field(
        None, 
        description="Error message if analysis failed"
    )
    processing_time: float = Field(
        ..., 
        description="Total processing time"
    )
    cached: bool = Field(
        default=False, 
        description="Whether result was served from cache"
    )


class BatchFictionalityAnalysisResult(BaseModel):
    """
    Result of batch fictionality analysis
    """
    success: bool = Field(
        ..., 
        description="Overall batch success status"
    )
    analyses: List[FictionalityAnalysisResult] = Field(
        ..., 
        description="Individual analysis results"
    )
    total_processing_time: float = Field(
        ..., 
        description="Total batch processing time"
    )
    successful_count: int = Field(
        ..., 
        description="Number of successful analyses"
    )
    failed_count: int = Field(
        ..., 
        description="Number of failed analyses"
    )
    cached_count: int = Field(
        ..., 
        description="Number of cached results served"
    )


class FictionalityHealthReport(BaseModel):
    """
    Health report for fictionality analysis service
    """
    status: str = Field(
        ..., 
        description="Overall service status"
    )
    healthy: bool = Field(
        ..., 
        description="Service health status"
    )
    services: Dict[str, Any] = Field(
        ..., 
        description="Individual service health"
    )
    timestamp: datetime = Field(
        default_factory=datetime.utcnow, 
        description="Health check timestamp"
    )
    uptime: float = Field(
        ..., 
        description="Service uptime in seconds"
    )
    metrics: FictionalityMetrics = Field(
        ..., 
        description="Current service metrics"
    )


# Extended models for integration
class ConflictWithFictionality(BaseModel):
    """
    Enhanced Conflict model with fictionality support
    """
    id: str = Field(..., description="Conflict ID")
    type: str = Field(..., description="Conflict type")
    severity: str = Field(..., description="Conflict severity")
    description: str = Field(..., description="Conflict description")
    affected_files: List[str] = Field(default_factory=list, description="Affected file paths")
    
    # Fictionality extensions
    fictionality_analysis_id: Optional[str] = Field(
        None, 
        description="Associated fictionality analysis ID"
    )
    fictionality_score: Optional[float] = Field(
        None, 
        description="Cached fictionality score"
    )
    fictionality_indicators: List[str] = Field(
        default_factory=list, 
        description="Fictionality indicators"
    )
    fictionality_confidence: Optional[str] = Field(
        None, 
        description="Fictionality confidence level"
    )
    
    # Relationships
    fictionality_analysis: Optional[FictionalityAnalysis] = Field(
        None, 
        description="Related fictionality analysis"
    )


class PullRequestWithFictionality(BaseModel):
    """
    Enhanced PullRequest model with fictionality metrics
    """
    id: str = Field(..., description="PR ID")
    title: str = Field(..., description="PR title")
    description: Optional[str] = Field(None, description="PR description")
    source_branch: str = Field(..., description="Source branch")
    target_branch: str = Field(..., description="Target branch")
    status: str = Field(..., description="PR status")
    complexity: float = Field(default=0.0, description="Complexity score")
    
    # Fictionality extensions
    fictionality_metrics: Dict[str, float] = Field(
        default_factory=dict, 
        description="Fictionality metrics"
    )
    fictionality_flags: List[str] = Field(
        default_factory=list, 
        description="Fictionality flags"
    )
    high_fictionality_conflicts: int = Field(
        default=0, 
        description="Number of high fictionality conflicts"
    )
    uncertain_fictionality_conflicts: int = Field(
        default=0, 
        description="Number of uncertain fictionality conflicts"
    )
    average_fictionality_score: float = Field(
        default=0.0, 
        description="Average fictionality score across conflicts"
    )
    
    # Relationships
    fictionality_analyses: List[str] = Field(
        default_factory=list, 
        description="Related fictionality analysis IDs"
    )