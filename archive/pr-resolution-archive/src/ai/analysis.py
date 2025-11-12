"""
Conflict analysis engine with AI integration
"""

import asyncio
import json
import structlog
import time
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime

from .client import get_openai_client
from .prompts import PromptTemplates
from .interfaces import AIProvider
from ..models.graph_entities import ConflictType, ConflictSeverity
from ..utils.caching import cache_manager

logger = structlog.get_logger()


class ConflictAnalyzer(AIProvider):
    """
    AI-powered conflict analysis engine
    """
    
    def __init__(self):
        self.client = None
        self.analysis_cache_ttl = 3600  # 1 hour
    
    async def initialize(self) -> bool:
        """Initialize the analysis engine"""
        try:
            self.client = await get_openai_client()
            logger.info("Conflict analyzer initialized")
            return True
        except Exception as e:
            logger.error("Failed to initialize conflict analyzer", error=str(e))
            return False
    
    async def analyze_conflict(
        self, 
        pr_data: Dict[str, Any], 
        conflict_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Analyze conflicts using AI and return comprehensive analysis
        """
        try:
            if not self.client:
                raise Exception("Analyzer not initialized")
            
            # Create cache key
            cache_key = self._generate_cache_key("analyze_conflict", pr_data, conflict_data)
            cached_result = cache_manager.get(cache_key)
            
            if cached_result:
                logger.debug("Returning cached conflict analysis", cache_key=cache_key)
                return cached_result
            
            # Prepare analysis request
            messages = PromptTemplates.analyze_conflict_prompt(pr_data, conflict_data)
            
            # Make AI request
            response = await self.client.chat_completion(
                messages=messages,
                temperature=0.1,  # Low temperature for consistent analysis
                max_tokens=2000
            )
            
            # Parse AI response
            analysis = self._parse_ai_response(response)
            
            # Enhance analysis with metadata
            enhanced_analysis = {
                **analysis,
                "id": f"analysis_{int(time.time())}",
                "pr_id": pr_data.get("id"),
                "conflicts_analyzed": len(conflict_data.get("conflicts", [])),
                "model_used": self.client.client.api_key and "gpt-4" or "unknown",
                "timestamp": datetime.utcnow().isoformat(),
                "processing_time": response.get("response_time", 0),
                "tokens_used": response.get("usage", {}).get("total_tokens", 0)
            }
            
            # Cache the result
            cache_manager.set(cache_key, {"pr_data": pr_data, "conflict_data": conflict_data}, enhanced_analysis)
            
            logger.info("Conflict analysis completed",
                       pr_id=pr_data.get("id"),
                       complexity=analysis.get("complexity_score", 0),
                       confidence=analysis.get("confidence_score", 0))
            
            return enhanced_analysis
            
        except Exception as e:
            logger.error("Conflict analysis failed", pr_id=pr_data.get("id"), error=str(e))
            # Return fallback analysis
            return self._create_fallback_analysis(pr_data, conflict_data, str(e))
    
    async def generate_resolution_suggestions(
        self, 
        analysis: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Generate resolution suggestions based on analysis
        """
        try:
            if not self.client:
                raise Exception("Analyzer not initialized")
            
            # Create context for resolution suggestions
            context = {
                "team_size": analysis.get("team_context", {}).get("size", 5),
                "experience_level": "intermediate",
                "timeline": "standard",
                "priority": "medium"
            }
            
            # Prepare prompt
            messages = PromptTemplates.resolution_suggestion_prompt(analysis, context)
            
            # Make AI request
            response = await self.client.chat_completion(
                messages=messages,
                temperature=0.2,  # Low temperature for consistent suggestions
                max_tokens=1500
            )
            
            # Parse AI response
            suggestions = self._parse_ai_response(response)
            
            # Enhance suggestions with metadata
            enhanced_suggestions = []
            for i, suggestion in enumerate(suggestions.get("strategies", [])):
                enhanced_suggestion = {
                    **suggestion,
                    "id": f"suggestion_{int(time.time())}_{i}",
                    "analysis_id": analysis.get("id"),
                    "created_at": datetime.utcnow().isoformat(),
                    "ai_generated": True
                }
                enhanced_suggestions.append(enhanced_suggestion)
            
            logger.info("Resolution suggestions generated",
                       analysis_id=analysis.get("id"),
                       suggestion_count=len(enhanced_suggestions))
            
            return enhanced_suggestions
            
        except Exception as e:
            logger.error("Resolution suggestion generation failed", analysis_id=analysis.get("id"), error=str(e))
            return self._create_fallback_suggestions(analysis, str(e))
    
    async def assess_complexity(
        self, 
        pr_data: Dict[str, Any]
    ) -> float:
        """
        Assess complexity of PR changes
        """
        try:
            if not self.client:
                raise Exception("Analyzer not initialized")
            
            # Get dependency information
            dependency_data = await self._get_dependency_info(pr_data)
            
            # Prepare analysis request
            messages = PromptTemplates.complexity_assessment_prompt(pr_data, dependency_data)
            
            # Make AI request
            response = await self.client.chat_completion(
                messages=messages,
                temperature=0.1,  # Low temperature for consistent assessment
                max_tokens=1000
            )
            
            # Parse AI response
            assessment = self._parse_ai_response(response)
            
            complexity = assessment.get("overall_complexity", 5.0)
            
            logger.info("Complexity assessment completed",
                       pr_id=pr_data.get("id"),
                       complexity=complexity)
            
            return complexity
            
        except Exception as e:
            logger.error("Complexity assessment failed", pr_id=pr_data.get("id"), error=str(e))
            return self._assess_complexity_heuristic(pr_data)
    
    async def validate_solution(
        self, 
        solution: str, 
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Validate proposed solution using AI
        """
        try:
            if not self.client:
                raise Exception("Analyzer not initialized")
            
            # Prepare validation request
            messages = PromptTemplates.solution_validation_prompt(
                context.get("conflict", {}),
                solution,
                context.get("code_context", {})
            )
            
            # Make AI request
            response = await self.client.chat_completion(
                messages=messages,
                temperature=0.1,  # Low temperature for consistent validation
                max_tokens=1500
            )
            
            # Parse AI response
            validation = self._parse_ai_response(response)
            
            # Enhance validation with metadata
            enhanced_validation = {
                **validation,
                "solution": solution,
                "validation_id": f"validation_{int(time.time())}",
                "validated_at": datetime.utcnow().isoformat(),
                "ai_validated": True
            }
            
            logger.info("Solution validation completed",
                       validation_id=enhanced_validation["validation_id"],
                       result=validation.get("validation_result", "UNKNOWN"))
            
            return enhanced_validation
            
        except Exception as e:
            logger.error("Solution validation failed", error=str(e))
            return self._create_fallback_validation(solution, str(e))
    
    def _parse_ai_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse AI response and extract JSON content
        """
        try:
            content = response.get("choices", [{}])[0].get("message", {}).get("content", "")
            
            # Try to extract JSON from the response
            if content.strip().startswith("{"):
                return json.loads(content)
            else:
                # Try to find JSON in the content
                start_idx = content.find("{")
                end_idx = content.rfind("}") + 1
                
                if start_idx != -1 and end_idx != -1:
                    json_content = content[start_idx:end_idx]
                    return json.loads(json_content)
                else:
                    raise Exception("No JSON found in AI response")
                    
        except json.JSONDecodeError as e:
            logger.error("Failed to parse AI response as JSON", 
                        response=content[:200], error=str(e))
            return {"error": f"Failed to parse AI response: {str(e)}"}
        except Exception as e:
            logger.error("Unexpected error parsing AI response", error=str(e))
            return {"error": f"Unexpected error: {str(e)}"}
    
    def _generate_cache_key(self, operation: str, *args) -> str:
        """
        Generate cache key for request
        """
        import hashlib
        content = f"{operation}_{str(args)}"
        return hashlib.md5(content.encode()).hexdigest()
    
    async def _get_dependency_info(self, pr_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get dependency information for PR files
        """
        # This would typically query the database for file dependencies
        # For now, return a simplified version
        files = pr_data.get("files", [])
        return {
            "files": [{"path": f, "dependencies": []} for f in files],
            "total_dependencies": 0,
            "circular_dependencies": []
        }
    
    def _assess_complexity_heuristic(self, pr_data: Dict[str, Any]) -> float:
        """
        Heuristic complexity assessment when AI is not available
        """
        file_count = len(pr_data.get("files", []))
        lines_changed = pr_data.get("lines_changed", 0)
        
        # Simple heuristic based on file count and lines changed
        complexity = min(10.0, (file_count * 0.5) + (lines_changed / 1000))
        return max(1.0, complexity)
    
    def _create_fallback_analysis(
        self, 
        pr_data: Dict[str, Any], 
        conflict_data: Dict[str, Any], 
        error: str
    ) -> Dict[str, Any]:
        """
        Create fallback analysis when AI fails
        """
        return {
            "id": f"fallback_analysis_{int(time.time())}",
            "pr_id": pr_data.get("id"),
            "overall_assessment": f"Analysis failed: {error}",
            "complexity_score": self._assess_complexity_heuristic(pr_data),
            "estimated_resolution_time": 120,  # Default 2 hours
            "confidence_score": 0.3,  # Low confidence for fallback
            "risk_level": "MEDIUM",
            "detailed_analysis": {
                "dependency_conflicts": "Unable to analyze due to AI service failure",
                "semantic_conflicts": "Unable to analyze due to AI service failure",
                "merge_conflicts": "Unable to analyze due to AI service failure",
                "architectural_impact": "Unable to analyze due to AI service failure"
            },
            "resolution_strategies": [
                {
                    "strategy": "Manual Analysis",
                    "description": "Requires manual analysis of conflicts",
                    "complexity": 7,
                    "time_estimate": 180,
                    "risk_level": "HIGH",
                    "confidence": 0.5
                }
            ],
            "ai_error": error,
            "fallback_used": True,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def _create_fallback_suggestions(
        self, 
        analysis: Dict[str, Any], 
        error: str
    ) -> List[Dict[str, Any]]:
        """
        Create fallback suggestions when AI fails
        """
        complexity = analysis.get("complexity_score", 5)
        
        suggestions = [
            {
                "id": f"fallback_suggestion_{int(time.time())}_1",
                "name": "Manual Review Required",
                "approach": "Manual code review and conflict resolution",
                "complexity": min(10, complexity + 2),
                "time_estimate": complexity * 30,
                "confidence": 0.5,
                "ai_error": error,
                "fallback_used": True
            }
        ]
        
        return suggestions
    
    def _create_fallback_validation(
        self, 
        solution: str, 
        error: str
    ) -> Dict[str, Any]:
        """
        Create fallback validation when AI fails
        """
        return {
            "validation_id": f"fallback_validation_{int(time.time())}",
            "validation_result": "CONDITIONAL",
            "confidence_score": 0.3,
            "detailed_assessment": {
                "technical_correctness": {
                    "score": 0.5,
                    "feedback": "Unable to validate due to AI service failure"
                },
                "code_quality": {
                    "score": 0.5,
                    "feedback": "Unable to validate due to AI service failure"
                }
            },
            "recommendations": ["Manual review required", "Extensive testing needed"],
            "potential_issues": [
                {
                    "issue": "AI validation unavailable",
                    "severity": "MEDIUM",
                    "likelihood": 0.8,
                    "mitigation": "Manual testing and code review"
                }
            ],
            "overall_feedback": f"Validation failed: {error}",
            "ai_error": error,
            "fallback_used": True
        }
    
    async def health_check(self) -> Dict[str, Any]:
        """
        Check analyzer health
        """
        try:
            if not self.client:
                return {"status": "not_initialized", "healthy": False}
            
            ai_health = await self.client.health_check()
            
            return {
                "status": "healthy" if ai_health.get("healthy") else "unhealthy",
                "healthy": ai_health.get("healthy", False),
                "ai_service": ai_health,
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            return {
                "status": "error",
                "healthy": False,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }


# Global analyzer instance
conflict_analyzer = ConflictAnalyzer()


async def get_conflict_analyzer() -> ConflictAnalyzer:
    """Get initialized conflict analyzer"""
    if not conflict_analyzer.client:
        await conflict_analyzer.initialize()
    return conflict_analyzer