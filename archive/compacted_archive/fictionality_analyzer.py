"""
Fictionality Analyzer - Consolidated
"""

from base_controller import BaseAIController
from response_parser import AIResponseParser


class FictionalityAnalyzer(BaseAIController):
    def __init__(self):
        super().__init__()
        self.client = None
    
    async def _perform(self, context):
        if not self.client:
            # Initialize client
            from openai import AsyncOpenAI
            self.client = AsyncOpenAI(api_key="key")
        
        # Create prompt
        prompt = [
            {"role": "system", "content": "Analyze fictionality score 0-1 for content"},
            {"role": "user", "content": f"Content: {context.get('content', '')}"}
        ]
        
        # Make request
        response = await self.client.chat.completions.create(
            model="gpt-4", messages=prompt, max_tokens=500
        )
        
        # Parse result
        return AIResponseParser.fictionality(
            {"choices": [{"message": response.choices[0].message}]},
            context,
            context.get("hash", "default")
        )
    
    async def batch_analyze(self, requests):
        batch = BatchProcessor()
        return await batch.process_batch(requests, self.analyze)