"""
Fictionality Query Builder for GraphQL
Builds complex fictionality filtering queries, analytics, and trend analysis
"""

import json
import time
import structlog
from typing import Dict, List, Any, Optional, Union
from datetime import datetime, timedelta
from enum import Enum

from ..models.fictionality_models import FictionalityScore

logger = structlog.get_logger()


class FictionalityFilterType(Enum):
    """Types of fictionality filters"""
    SCORE_RANGE = "score_range"
    CONFIDENCE_LEVEL = "confidence_level"
    INDICATORS = "indicators"
    CONTENT_PATTERN = "content_pattern"
    TIME_RANGE = "time_range"
    PR_CONTEXT = "pr_context"
    CONFLICT_TYPE = "conflict_type"
    SEVERITY = "severity"


class FictionalityQueryBuilder:
    """Builder for complex fictionality filtering and analysis queries"""
    
    def __init__(self):
        self.filters = []
        self.sort_options = []
        self.aggregation_rules = {}
        self.time_window = None
        self.context_requirements = {}
    
    def add_score_range_filter(self, min_score: float = 0.0, max_score: float = 1.0):
        """Add fictionality score range filter"""
        self.filters.append({
            "type": FictionalityFilterType.SCORE_RANGE.value,
            "min_score": min_score,
            "max_score": max_score
        })
        return self
    
    def add_confidence_filter(self, confidence_levels: List[FictionalityScore]):
        """Add confidence level filter"""
        self.filters.append({
            "type": FictionalityFilterType.CONFIDENCE_LEVEL.value,
            "confidence_levels": [level.value for level in confidence_levels]
        })
        return self
    
    def add_indicators_filter(
        self, 
        include_indicators: List[str] = None, 
        exclude_indicators: List[str] = None
    ):
        """Add fictionality/realism indicators filter"""
        filter_data = {
            "type": FictionalityFilterType.INDICATORS.value
        }
        
        if include_indicators:
            filter_data["include_indicators"] = include_indicators
        
        if exclude_indicators:
            filter_data["exclude_indicators"] = exclude_indicators
        
        self.filters.append(filter_data)
        return self
    
    def add_content_pattern_filter(
        self, 
        text_pattern: str, 
        pattern_type: str = "contains"
    ):
        """Add content pattern filter"""
        self.filters.append({
            "type": FictionalityFilterType.CONTENT_PATTERN.value,
            "text_pattern": text_pattern,
            "pattern_type": pattern_type
        })
        return self
    
    def add_time_range_filter(
        self, 
        start_time: datetime = None, 
        end_time: datetime = None,
        period: str = None
    ):
        """Add time range filter"""
        if not start_time and not end_time and not period:
            # Default to last 30 days
            end_time = datetime.utcnow()
            start_time = end_time - timedelta(days=30)
        
        if period:
            end_time = datetime.utcnow()
            if period == "1d":
                start_time = end_time - timedelta(days=1)
            elif period == "7d":
                start_time = end_time - timedelta(days=7)
            elif period == "30d":
                start_time = end_time - timedelta(days=30)
            else:
                start_time = end_time - timedelta(days=30)  # Default
        
        self.time_window = {
            "start_time": start_time.isoformat() if start_time else None,
            "end_time": end_time.isoformat() if end_time else None,
            "period": period
        }
        return self
    
    def add_pr_context_filter(
        self, 
        pr_id: str = None,
        author: str = None,
        branch: str = None
    ):
        """Add PR context filter"""
        context_filter = {"type": FictionalityFilterType.PR_CONTEXT.value}
        
        if pr_id:
            context_filter["pr_id"] = pr_id
        if author:
            context_filter["author"] = author
        if branch:
            context_filter["branch"] = branch
        
        self.context_requirements.update(context_filter)
        return self
    
    def add_conflict_context_filter(
        self, 
        conflict_types: List[str] = None,
        severities: List[str] = None
    ):
        """Add conflict context filter"""
        filter_data = {"type": FictionalityFilterType.CONFLICT_TYPE.value}
        
        if conflict_types:
            filter_data["conflict_types"] = conflict_types
        
        if severities:
            filter_data["severities"] = severities
        
        self.filters.append(filter_data)
        return self
    
    def sort_by_score(self, ascending: bool = False):
        """Sort by fictionality score"""
        self.sort_options.append({
            "field": "fictionality_score",
            "direction": "asc" if ascending else "desc"
        })
        return self
    
    def sort_by_time(self, ascending: bool = False):
        """Sort by time"""
        self.sort_options.append({
            "field": "created_at",
            "direction": "asc" if ascending else "desc"
        })
        return self
    
    def add_aggregation(self, rule_type: str, field: str, **kwargs):
        """Add aggregation rule"""
        self.aggregation_rules[rule_type] = {
            "field": field,
            "parameters": kwargs
        }
        return self
    
    def build_query(self) -> Dict[str, Any]:
        """Build the final query dictionary"""
        query = {
            "filters": self.filters,
            "sort": self.sort_options,
            "aggregations": self.aggregation_rules,
            "time_window": self.time_window,
            "context_requirements": self.context_requirements,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # Remove empty fields
        query = {k: v for k, v in query.items() if v}
        
        logger.debug("Fictionality query built", query=query)
        return query


class FictionalityAnalyticsBuilder:
    """Builder for fictionality analytics and trend analysis"""
    
    def __init__(self):
        self.analysis_periods = []
        self.metric_calculations = {}
        self.trend_analysis = {}
        self.comparative_metrics = {}
    
    def add_period_analysis(self, period: str, label: str = None):
        """Add analysis for a specific time period"""
        self.analysis_periods.append({
            "period": period,
            "label": label or period
        })
        return self
    
    def add_fictionality_score_trend(self, include_percentiles: bool = True):
        """Add fictionality score trend analysis"""
        self.trend_analysis["fictionality_score"] = {
            "include_percentiles": include_percentiles,
            "buckets": [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
        }
        return self
    
    def add_confidence_distribution(self):
        """Add confidence level distribution analysis"""
        self.metric_calculations["confidence_distribution"] = {
            "type": "group_by",
            "field": "confidence_level"
        }
        return self
    
    def add_indicators_analysis(self, top_n: int = 10):
        """Add analysis of most common fictionality indicators"""
        self.metric_calculations["top_indicators"] = {
            "type": "most_common",
            "field": "fictionality_indicators",
            "limit": top_n
        }
        return self
    
    def add_performance_metrics(self):
        """Add processing performance metrics"""
        self.metric_calculations["performance"] = {
            "type": "statistics",
            "fields": ["processing_time", "tokens_used"],
            "statistics": ["mean", "median", "p95", "p99"]
        }
        return self
    
    def add_comparative_analysis(
        self, 
        comparison_type: str, 
        baseline_period: str = "7d"
    ):
        """Add comparative analysis against baseline period"""
        self.comparative_metrics[comparison_type] = {
            "baseline_period": baseline_period,
            "comparison_fields": ["average_score", "total_analyses", "high_fictionality_count"]
        }
        return self
    
    def build_analytics_query(self) -> Dict[str, Any]:
        """Build the analytics query"""
        query = {
            "analysis_periods": self.analysis_periods,
            "metric_calculations": self.metric_calculations,
            "trend_analysis": self.trend_analysis,
            "comparative_metrics": self.comparative_metrics,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        logger.debug("Fictionality analytics query built", query=query)
        return query


class FictionalityPRRecommendationBuilder:
    """Builder for PR recommendation queries based on fictionality analysis"""
    
    def __init__(self):
        self.recommendation_types = []
        self.risk_factors = {}
        self.optimization_targets = {}
    
    def add_conflict_risk_analysis(self):
        """Add analysis for conflict risk based on fictionality"""
        self.risk_factors["fictionality_indicators"] = {
            "high_impact_indicators": [
                "inconsistent_technical_details",
                "unrealistic_timelines",
                "vague_requirements",
                "generic_content"
            ],
            "risk_multipliers": {
                "HIGHLY_FICTIONAL": 2.0,
                "PROBABLY_FICTIONAL": 1.5,
                "UNCERTAIN": 1.1,
                "PROBABLY_REAL": 0.9,
                "HIGHLY_REAL": 0.8
            }
        }
        return self
    
    def add_resolution_confidence_analysis(self):
        """Add analysis for resolution confidence"""
        self.optimization_targets["confidence_factors"] = {
            "fictionality_penalty": {
                "score_threshold": 0.5,
                "penalty_per_0.1": 0.05
            },
            "validation_requirements": {
                "min_fictionality_score": 0.3,
                "max_fictionality_score": 0.7
            }
        }
        return self
    
    def add_automation_recommendation(self):
        """Add recommendations for automation vs manual intervention"""
        self.recommendation_types.append({
            "type": "automation_level",
            "criteria": {
                "fictionality_score": {
                    "min": 0.0,
                    "max": 0.4
                },
                "confidence_level": ["HIGHLY_REAL", "PROBABLY_REAL"],
                "required_validations": ["code_review", "test_coverage"]
            }
        })
        return self
    
    def add_reviewer_assignment_recommendation(self):
        """Add recommendations for reviewer assignment based on fictionality"""
        self.recommendation_types.append({
            "type": "reviewer_assignment",
            "criteria": {
                "fictionality_score": {
                    "min": 0.4,
                    "max": 0.8
                },
                "required_expertise": ["fictionality_analysis", "technical_validation"],
                "priority": "elevated"
            }
        })
        return self
    
    def build_recommendation_query(self) -> Dict[str, Any]:
        """Build the PR recommendation query"""
        query = {
            "recommendation_types": self.recommendation_types,
            "risk_factors": self.risk_factors,
            "optimization_targets": self.optimization_targets,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        logger.debug("PR recommendation query built", query=query)
        return query


# Utility functions for common fictionality queries
def create_fictionality_filter_query(
    min_score: float = 0.0,
    max_score: float = 1.0,
    confidence_levels: List[FictionalityScore] = None,
    pr_id: str = None,
    period: str = "7d"
) -> Dict[str, Any]:
    """Create a basic fictionality filter query"""
    builder = FictionalityQueryBuilder()
    builder.add_score_range_filter(min_score, max_score)
    builder.add_time_range_filter(period=period)
    
    if confidence_levels:
        builder.add_confidence_filter(confidence_levels)
    
    if pr_id:
        builder.add_pr_context_filter(pr_id=pr_id)
    
    return builder.build_query()


def create_fictionality_analytics_query(
    periods: List[str] = None,
    include_trends: bool = True
) -> Dict[str, Any]:
    """Create a fictionality analytics query"""
    builder = FictionalityAnalyticsBuilder()
    
    if not periods:
        periods = ["1d", "7d", "30d"]
    
    for period in periods:
        builder.add_period_analysis(period)
    
    if include_trends:
        builder.add_fictionality_score_trend()
        builder.add_confidence_distribution()
        builder.add_indicators_analysis()
        builder.add_performance_metrics()
        builder.add_comparative_analysis("period_comparison")
    
    return builder.build_analytics_query()


def create_pr_recommendation_query(pr_id: str) -> Dict[str, Any]:
    """Create PR recommendation query for a specific PR"""
    builder = FictionalityPRRecommendationBuilder()
    builder.add_conflict_risk_analysis()
    builder.add_resolution_confidence_analysis()
    builder.add_automation_recommendation()
    builder.add_reviewer_assignment_recommendation()
    
    query = builder.build_recommendation_query()
    query["pr_id"] = pr_id
    
    return query


# Export all builders
__all__ = [
    "FictionalityQueryBuilder",
    "FictionalityAnalyticsBuilder", 
    "FictionalityPRRecommendationBuilder",
    "create_fictionality_filter_query",
    "create_fictionality_analytics_query",
    "create_pr_recommendation_query"
]