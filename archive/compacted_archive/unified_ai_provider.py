"""
Unified AI Provider - Single interface for all AI operations
"""

from fictionality_analyzer import FictionalityAnalyzer
from conflict_analyzer import ConflictAnalyzer


class UnifiedAIProvider:
    def __init__(self):
        self.fictionality = FictionalityAnalyzer()
        self.conflict = ConflictAnalyzer()
        self.initialized = False
    
    async def initialize(self):
        """Initialize all analyzers"""
        if self.initialized:
            return True
        
        try:
            # Initialize clients (simplified)
            self.fictionality.client = "initialized"
            self.conflict.client = "initialized"
            self.initialized = True
            return True
        except Exception:
            return False
    
    async def analyze_fictionality(self, content, context=None):
        """Analyze content for fictionality"""
        if not self.initialized:
            await self.initialize()
        
        ctx = context or {}
        ctx["content"] = content
        return await self.fictionality.analyze(ctx)
    
    async def analyze_conflict(self, pr_data, conflict_data):
        """Analyze conflicts"""
        if not self.initialized:
            await self.initialize()
        
        ctx = {"pr_data": pr_data, "conflict_data": conflict_data}
        return await self.conflict.analyze(ctx)
    
    async def batch_analyze(self, operations):
        """Batch process multiple operations"""
        results = []
        for op in operations:
            if op["type"] == "fictionality":
                result = await self.analyze_fictionality(op["content"], op.get("context"))
            elif op["type"] == "conflict":
                result = await self.analyze_conflict(op["pr_data"], op["conflict_data"])
            else:
                result = {"error": "Unknown operation type"}
            results.append(result)
        return {"total": len(operations), "results": results}


# Global instance
ai_provider = UnifiedAIProvider()