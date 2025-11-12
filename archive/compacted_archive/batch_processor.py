"""
Batch Processor - Minimal batch handling
"""

import asyncio
import time


class BatchProcessor:
    def __init__(self, max_concurrent=3):
        self.max = max_concurrent
        self.semaphore = asyncio.Semaphore(max_concurrent)
    
    async def process_batch(self, ops, func):
        async def process(op):
            async with self.semaphore:
                return await func(op)
        
        results = await asyncio.gather(*[process(op) for op in ops], return_exceptions=True)
        
        successful = [r for r in results if isinstance(r, dict) and "error" not in r]
        failed = [r for r in results if isinstance(r, Exception)]
        
        return {
            "total": len(ops),
            "successful": len(successful),
            "failed": len(failed),
            "results": successful,
            "errors": [str(f) for f in failed]
        }