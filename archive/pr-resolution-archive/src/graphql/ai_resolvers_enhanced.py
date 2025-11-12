"""
AI resolver implementations for GraphQL with Fictionality Integration
Enhanced AI resolvers that integrate fictionality analysis into conflict resolution
"""

import asyncio
import time
import structlog
from typing import Dict, List, Any, Optional

from .schema import (
    AIAnalysisType, ResolutionSuggestionType, AIHealthReportType,
    AIProcessingTaskType, AILogType
)
from ..ai.client import get_openai_client
from ..ai.analysis import get_conflict_analyzer
from ..ai.processing import get_ai_processor
from ..ai.monitoring import get_ai_monitor
from ..ai.fictionality_analyzer import get_fictionality_analyzer
from ..database.data_access import pr_dao, conflict_dao

logger = structlog.get_logger()


class EnhancedAIResolvers:
    """Enhanced AI-related GraphQL resolvers with fictionality integration"""
    
    @staticmethod
    async def resolve_analyze_conflict_with_ai(root, info, pr_id, conflict_id):
        """Resolver for triggering AI conflict analysis with fictionality integration"""
        start_time = time.time()
        try:
            analyzer = await get_conflict_analyzer()
            processor = await get_ai_processor()
            
            # Get PR and conflict data
            pr_data = await pr_dao.get_pr(pr_id)
            conflict_data = await conflict_dao.get_conflict(conflict_id)
            
            if not pr_data or not conflict_data:
                raise Exception(f"PR {pr_id} or conflict {conflict_id} not found")
            
            # Check for existing fictionality analysis
            fictionality_analysis = None
            fictionality_context = None
            try:
                fictionality_analyzer = await get_fictionality_analyzer()
                
                # Create content to analyze
                content_to_analyze = f"""
                PR Title: {pr_data.get('title', '') if isinstance(pr_data, dict) else pr_data.title}
                Conflict Description: {conflict_data.get('description', '') if isinstance(conflict_data, dict) else getattr(conflict_data, 'description', '')}
                Conflict Type: {conflict_data.get('type', '') if isinstance(conflict_data, dict) else getattr(conflict_data, 'type', '')}
                """
                
                from ..models.fictionality_models import FictionalityContext
                fictionality_context = FictionalityContext(
                    pr_data=pr_data.dict() if hasattr(pr_data, 'dict') else pr_data,
                    conflict_data=conflict_data.dict() if hasattr(conflict_data, 'dict') else conflict_data,
                    content_to_analyze=content_to_analyze,
                    analysis_depth="standard",
                    include_strategies=True
                )
                
                # Try to get cached fictionality analysis or perform new one
                cache_key = f"fictionality:{pr_id}:{conflict_id}:{hash(content_to_analyze)}"
                fictionality_result = await fictionality_analyzer.analyze_fictionality(
                    fictionality_context, cache_key=cache_key
                )
                
                if fictionality_result.success:
                    fictionality_analysis = fictionality_result.analysis
                    logger.info("Fictionality analysis retrieved for AI analysis", 
                               pr_id=pr_id, conflict_id=conflict_id,
                               fictionality_score=fictionality_analysis.fictionality_score)
                
            except Exception as e:
                logger.warning("Failed to get fictionality analysis for AI analysis", 
                             pr_id=pr_id, conflict_id=conflict_id, error=str(e))
            
            # Submit analysis task with fictionality context
            task_payload = {
                "pr_id": pr_id,
                "conflict_id": conflict_id,
                "pr_data": pr_data.dict() if hasattr(pr_data, 'dict') else pr_data,
                "conflict_data": conflict_data.dict() if hasattr(conflict_data, 'dict') else conflict_data
            }
            
            # Add fictionality context if available
            if fictionality_analysis:
                task_payload["fictionality_analysis"] = {
                    "score": fictionality_analysis.fictionality_score,
                    "confidence_level": fictionality_analysis.confidence_level.value,
                    "indicators": fictionality_analysis.fictionality_indicators,
                    "reasoning": fictionality_analysis.reasoning
                }
            
            # Submit task with appropriate priority based on fictionality
            priority = "HIGH" if fictionality_analysis and fictionality_analysis.fictionality_score > 0.6 else "NORMAL"
            from ..ai.processing import TaskPriority
            task_priority = TaskPriority.HIGH if priority == "HIGH" else TaskPriority.NORMAL
            
            task_id = await processor.submit_task(
                task_type="analyze_conflict",
                payload=task_payload,
                priority=task_priority
            )
            
            logger.info("AI conflict analysis submitted", 
                       pr_id=pr_id,
                       conflict_id=conflict_id,
                       task_id=task_id,
                       has_fictionality=bool(fictionality_analysis),
                       fictionality_score=fictionality_analysis.fictionality_score if fictionality_analysis else None,
                       priority=priority,
                       duration=time.time() - start_time)
            
            # Return a placeholder analysis with fictionality context
            analysis = {
                "id": f"analysis_{task_id}",
                "conflict_type": conflict_data.get('type', '') if isinstance(conflict_data, dict) else getattr(conflict_data, 'type', ''),
                "complexity": 5.0,
                "resolution_suggestions": [],
                "estimated_time": 60,
                "confidence": 0.8,
                "model": "gpt-4",
                "created_at": time.time(),
                "overall_assessment": "Analysis submitted for processing",
                "risk_level": "MEDIUM"
            }
            
            # Add fictionality context to analysis if available
            if fictionality_analysis:
                fictionality_score = fictionality_analysis.fictionality_score
                analysis["fictionality_score"] = fictionality_score
                analysis["fictionality_confidence"] = fictionality_analysis.confidence_level.value
                analysis["fictionality_indicators"] = fictionality_analysis.fictionality_indicators
                
                if fictionality_score > 0.6:
                    analysis["risk_level"] = "HIGH"
                    analysis["confidence"] *= 0.8  # Reduce confidence for high fictionality
                    analysis["resolution_suggestions"] = [
                        "Fictionality concerns detected - recommend manual review",
                        "Verify content authenticity before proceeding",
                        "Consider additional validation steps",
                        "May require re-evaluation of problem statement"
                    ]
                    analysis["overall_assessment"] = (
                        f"High fictionality score detected ({fictionality_score:.2f}) - "
                        "proceed with additional caution and manual validation. "
                        f"Key concerns: {', '.join(fictionality_analysis.fictionality_indicators[:3])}"
                    )
                elif fictionality_score > 0.4:
                    analysis["risk_level"] = "MEDIUM"
                    analysis["confidence"] *= 0.95
                    analysis["resolution_suggestions"].append(
                        "Fictionality assessment suggests some uncertainty - verify problem context"
                    )
            
            return analysis
            
        except Exception as e:
            logger.error("Failed to analyze conflict with AI", 
                        pr_id=pr_id, conflict_id=conflict_id, error=str(e))
            raise
    
    @staticmethod
    async def resolve_generate_resolution_suggestions(root, info, analysis_id):
        """Resolver for generating AI resolution suggestions with fictionality awareness"""
        start_time = time.time()
        try:
            analyzer = await get_conflict_analyzer()
            processor = await get_ai_processor()
            
            # Get analysis details (would normally fetch from database)
            # For now, we'll generate suggestions that consider fictionality
            
            # Check if analysis has fictionality context
            fictionality_context = None
            try:
                # Would normally get analysis from database
                # For now, we'll simulate fictionality check
                fictionality_context = {"fictionality_score": 0.3, "indicators": []}
            except Exception as e:
                logger.warning("Failed to get fictionality context for suggestions", 
                             analysis_id=analysis_id, error=str(e))
            
            # Submit suggestion generation task with fictionality context
            task_payload = {
                "analysis_id": analysis_id,
                "analysis": {"id": analysis_id, "complexity": 5.0},
                "fictionality_context": fictionality_context
            }
            
            task_id = await processor.submit_task(
                task_type="generate_suggestions",
                payload=task_payload,
                priority=TaskPriority.NORMAL
            )
            
            logger.info("AI resolution suggestions generation submitted", 
                       analysis_id=analysis_id,
                       task_id=task_id,
                       has_fictionality=bool(fictionality_context),
                       duration=time.time() - start_time)
            
            # Generate base suggestions
            suggestions = [
                {
                    "id": f"suggestion_{task_id}_1",
                    "name": "Manual Merge with Review",
                    "approach": "Manual resolution with code review and validation",
                    "complexity": 6,
                    "time_estimate": 90,
                    "confidence": 0.7,
                    "risk_level": "MEDIUM",
                    "steps": ["Review conflicts", "Apply changes", "Test", "Code review"],
                    "ai_generated": True,
                    "created_at": time.time(),
                    "analysis_id": analysis_id
                }
            ]
            
            # Add fictionality-aware suggestions
            if fictionality_context and fictionality_context.get("fictionality_score", 0) > 0.5:
                fictionality_suggestion = {
                    "id": f"suggestion_{task_id}_fic",
                    "name": "Fictionality-Aware Resolution",
                    "approach": "Address fictionality concerns before resolution",
                    "complexity": 7,
                    "time_estimate": 120,
                    "confidence": 0.6,
                    "risk_level": "HIGH",
                    "steps": [
                        "Verify problem statement authenticity",
                        "Validate conflict description with stakeholders",
                        "Confirm technical requirements",
                        "Manual conflict resolution with validation"
                    ],
                    "ai_generated": True,
                    "created_at": time.time(),
                    "analysis_id": analysis_id
                }
                suggestions.append(fictionality_suggestion)
            
            return suggestions
            
        except Exception as e:
            logger.error("Failed to generate resolution suggestions", 
                        analysis_id=analysis_id, error=str(e))
            raise


# Integration with existing AI resolvers
def enhance_ai_resolvers():
    """Enhance existing AI resolvers with fictionality integration"""
    try:
        from .ai_resolvers import AIResolvers
        
        # Replace the original resolve_analyze_conflict_with_ai with enhanced version
        AIResolvers.resolve_analyze_conflict_with_ai = EnhancedAIResolvers.resolve_analyze_conflict_with_ai
        AIResolvers.resolve_generate_resolution_suggestions = EnhancedAIResolvers.resolve_generate_resolution_suggestions
        
        logger.info("AI resolvers enhanced with fictionality integration")
        return True
    except Exception as e:
        logger.error("Failed to enhance AI resolvers", error=str(e))
        return False


# Apply enhancement when module is imported
enhance_ai_resolvers()