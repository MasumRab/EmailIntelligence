"""
Conflict Analyzer - Consolidated
"""

from base_controller import BaseAIController
from response_parser import AIResponseParser


class ConflictAnalyzer(BaseAIController):
    def __init__(self):
        super().__init__()
        self.client = None
    
    async def _perform(self, context):
        pr_data = context.get("pr_data", {})
        conflict_data = context.get("conflict_data", {})
        
        if not self.client:
            from openai import AsyncOpenAI
            self.client = AsyncOpenAI(api_key="key")
        
        prompt = [
            {"role": "system", "content": "Analyze Git conflicts and suggest resolution strategies"},
            {"role": "user", "content": f"PR: {pr_data}\nConflict: {conflict_data}"}
        ]
        
        response = await self.client.chat.completions.create(
            model="gpt-4", messages=prompt, max_tokens=800
        )
        
        return AIResponseParser.conflict(
            {"choices": [{"message": response.choices[0].message}]},
            pr_data,
            conflict_data,
            f"conflict_{pr_data.get('id', 'unknown')}"
        )