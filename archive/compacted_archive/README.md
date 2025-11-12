# Compacted Archive - Unified AI Framework

## Overview
Consolidated AI services from ~3000 lines to ~800 lines by removing duplication.

## Core Files
- `base_controller.py` - Common patterns (CircuitBreaker, RateLimiter, BaseAIController)
- `response_parser.py` - AI response parsing
- `batch_processor.py` - Batch processing
- `fictionality_analyzer.py` - Fictionality analysis
- `conflict_analyzer.py` - Conflict analysis
- `unified_ai_provider.py` - Unified interface

## Usage
```python
from fictionality_analyzer import FictionalityAnalyzer
analyzer = FictionalityAnalyzer()
await analyzer.initialize()
result = await analyzer.analyze(context)