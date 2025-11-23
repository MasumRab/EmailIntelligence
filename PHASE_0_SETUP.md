# Phase 0: Pre-Integration Setup & Audit

**Duration**: 8 hours  
**Goal**: Verify existing modules work and fix broken imports

---

## Tasks Checklist

- [x] Audit existing `src/resolution/` modules
- [x] Identify missing vs existing files
- [x] Fix broken `__init__.py` imports
- [x] Test module imports
- [x] Fix archived OpenAI client reference in strategies.py
- [ ] Setup OpenAI (if using AI strategies)
- [ ] Create integration test plan

---

## 1. Module Audit Results

### ✅ Files That Exist (5 files)

| File | Size | Status | Purpose |
|------|------|--------|---------|
| `constitutional_engine.py` | 29.6 KB | ✅ Working | Constitutional validation with regex rules |
| `strategies.py` | 25.2 KB | ✅ Working | AI-powered strategy generation (OpenAI) |
| `prompts.py` | 26.1 KB | ✅ Working | Prompt engineering for AI |
| `types.py` | 17.0 KB | ✅ Working | Pydantic models for all data structures |
| `__init__.py` | 1.4 KB | ⚠️ Broken | Imports non-existent modules |

### ❌ Files That Don't Exist (7 files)

These are imported in `__init__.py` but **don't exist**:

1. `engine.py` - ResolutionEngine
2. `generation.py` - CodeChangeGenerator
3. `validation.py` - ValidationFramework
4. `execution.py` - ExecutionEngine
5. `workflows.py` - WorkflowOrchestrator
6. `metrics.py` - QualityMetrics implementation
7. `queue.py` - ResolutionQueue

**Impact**: Any import from `src.resolution` will fail with `ModuleNotFoundError`

---

## 2. Fix Broken `__init__.py`

### Problem

Current file tries to import non-existent modules:
```python
from .engine import ResolutionEngine  # ❌ File doesn't exist
from .generation import CodeChangeGenerator  # ❌ File doesn't exist
# ... 5 more missing imports
```

### Solution

Comment out missing imports, keep only what exists:

```python
"""
Intelligent Conflict Resolution Engine for PR Resolution Automation System

Available modules:
- ConstitutionalEngine: Constitutional validation
- StrategyGenerator: AI-powered strategy generation (requires OpenAI)
- PromptEngine: Prompt engineering for AI
- Data models: MergeConflict, ResolutionStrategy, etc.
"""

# ===== EXISTING MODULES =====
from .strategies import StrategyGenerator
from .prompts import PromptEngine
from .constitutional_engine import ConstitutionalEngine
from .types import (
    # Enums
    ConflictTypeExtended,
    RiskLevel,
    ExecutionStatus,
    ValidationStatus,
    # Models
    CodeChange,
    ResolutionStep,
    ResolutionStrategy,
    ValidationResult,
    QualityMetrics,
    ResolutionPlan,
    # Conflict types (imported from models.graph_entities)
    MergeConflict,
    DependencyConflict,
    ArchitectureViolation,
    SemanticConflict,
    ResourceConflict,
)

# ===== MISSING MODULES (commented out) =====
# TODO: Implement these modules or remove from API
# from .engine import ResolutionEngine
# from .generation import CodeChangeGenerator
# from .validation import ValidationFramework
# from .execution import ExecutionEngine
# from .workflows import WorkflowOrchestrator
# from .metrics import QualityMetrics  # Note: Model exists in types.py
# from .queue import ResolutionQueue

__all__ = [
    # Available classes
    "StrategyGenerator",
    "PromptEngine",
    "ConstitutionalEngine",
    # Enums
    "ConflictTypeExtended",
    "RiskLevel",
    "ExecutionStatus",
    "ValidationStatus",
    # Models
    "CodeChange",
    "ResolutionStep",
    "ResolutionStrategy",
    "ValidationResult",
    "QualityMetrics",
    "ResolutionPlan",
    # Conflict types
    "MergeConflict",
    "DependencyConflict",
    "ArchitectureViolation",
    "SemanticConflict",
    "ResourceConflict",
]
```

---

## 3. Test Module Imports

After fixing, test that imports work:

```bash
cd c:\Users\masum\Documents\EmailIntelligence
python -c "from src.resolution import ConstitutionalEngine; print('✅ ConstitutionalEngine imported')"
python -c "from src.resolution import StrategyGenerator; print('✅ StrategyGenerator imported')"
python -c "from src.resolution import PromptEngine; print('✅ PromptEngine imported')"
python -c "from src.resolution import MergeConflict; print('✅ MergeConflict imported')"
```

**Expected**: All imports succeed  
**If fails**: Check Python path and module structure

---

## 4. OpenAI Setup (Optional - for AI Strategies)

### 4.1. Get OpenAI API Key

1. Go to https://platform.openai.com/api-keys
2. Create new API key
3. Copy the key (starts with `sk-`)

### 4.2. Configure Environment

Create or update `.env` file:

```bash
# c:\Users\masum\Documents\EmailIntelligence\.env

# OpenAI Configuration
OPENAI_API_KEY=sk-your-key-here
OPENAI_MODEL=gpt-4o  # or gpt-4-turbo, gpt-3.5-turbo

# Optional: Rate limiting
OPENAI_MAX_RETRIES=3
OPENAI_TIMEOUT=60
```

### 4.3. Install Dependencies

```bash
pip install openai python-dotenv
```

### 4.4. Test OpenAI Connection

```python
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Test API
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Say 'API working!'"}],
    max_tokens=10
)

print(response.choices[0].message.content)
# Expected: "API working!" or similar
```

### 4.5. Alternative: Use Non-AI Strategy Generator

If you don't want OpenAI costs, use `MultiPhaseStrategyGenerator` instead:

```python
# No OpenAI needed!
from src.strategy.multi_phase_generator import MultiPhaseStrategyGenerator

generator = MultiPhaseStrategyGenerator()
strategies = generator.generate_multi_phase_strategies(...)
```

**Pros**: Free, no external API, deterministic  
**Cons**: Less intelligent than AI

---

## 5. Database Setup (Neo4j)

### 5.1. Check if Neo4j is Installed

Your code uses Neo4j. Check if it's configured:

```python
# Test database connection
from src.database.connection import connection_manager
import asyncio

async def test_db():
    await connection_manager.connect()
    health = await connection_manager.health_check()
    print(f"Neo4j health: {health}")
    await connection_manager.disconnect()

asyncio.run(test_db())
```

### 5.2. Configure Neo4j (if needed)

Create or update configuration:

```bash
# .env

# Neo4j Configuration
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your-password-here
```

### 5.3. Initialize Database Schema

```python
from src.database.connection import initialize_database_schema
import asyncio

asyncio.run(initialize_database_schema())
```

---

## 6. Create Integration Test Plan

### 6.1. Test Constitutional Engine

```python
import asyncio
from src.resolution import ConstitutionalEngine

async def test_constitutional():
    engine = ConstitutionalEngine(constitutions_dir="constitutions")
    await engine.initialize()
    
    # Test validation
    result = await engine.validate_specification_template(
        template_content='{"test": "content"}',
        template_type="test",
        context={"pr_number": 123}
    )
    
    print(f"Score: {result.overall_score}")
    print(f"Violations: {len(result.violations)}")
    
asyncio.run(test_constitutional())
```

### 6.2. Test Strategy Generator (Non-AI)

```python
from src.strategy.multi_phase_generator import MultiPhaseStrategyGenerator
from src.resolution import MergeConflict

generator = MultiPhaseStrategyGenerator()

conflict = MergeConflict(
    id="test_1",
    file_path="test.py",
    conflict_type="MERGE_CONFLICT",
    pr1_id="PR-1",
    pr2_id="PR-2",
    content1="version 1",
    content2="version 2",
    base_content="original",
    complexity_score=5
)

strategies = generator.generate_multi_phase_strategies(
    conflict_data=conflict,
    context={"complexity_score": 5},
    risk_tolerance="medium"
)

print(f"Generated {len(strategies)} strategies")
print(f"Best: {strategies[0].name}")
```

### 6.3. Test Validator

```python
import asyncio
from src.validation.comprehensive_validator import ComprehensiveValidator

async def test_validator():
    validator = ComprehensiveValidator()
    
    # Create test strategy
    from src.resolution import ResolutionStrategy, ResolutionStep
    
    strategy = ResolutionStrategy(
        id="test_strat",
        name="Test Strategy",
        description="Test",
        approach="Test approach",
        steps=[],
        pros=["Pro 1"],
        cons=["Con 1"],
        confidence=0.8,
        estimated_time=60,
        risk_level="LOW",
        requires_approval=False,
        success_criteria=["Pass"],
        rollback_strategy="Git revert",
        validation_approach="Testing",
        ai_generated=False,
        model_used="none"
    )
    
    result = await validator.validate_comprehensive_resolution(
        conflict_data=conflict,
        resolution_strategy=strategy
    )
    
    print(f"Validation score: {result.overall_score}")
    print(f"Execution ready: {result.execution_readiness}")

asyncio.run(test_validator())
```

---

## 7. Verification Checklist

After completing Phase 0, verify:

- [ ] `__init__.py` imports work without errors
- [ ] ConstitutionalEngine can be imported and initialized
- [ ] StrategyGenerator can be imported (even if not configured)
- [ ] PromptEngine can be imported
- [ ] All data models (MergeConflict, etc.) can be imported
- [ ] OpenAI API key configured (if using AI)
- [ ] Neo4j connection works (if using database)
- [ ] Test scripts run successfully

---

## 8. Next Steps

After Phase 0 is complete:

### Option A: Quick Win (Weeks 1-2)
- Week 1: Integrate ConstitutionalEngine into CLI
- Week 2: Integrate MultiPhaseStrategyGenerator into CLI

### Option B: Full Integration (Weeks 1-5)
- Week 1: Constitutional analysis
- Week 2: Strategy generation (AI)
- Week 3: Validation
- Weeks 4-5: Testing + polish

---

## Common Issues & Solutions

### Issue: `ModuleNotFoundError: No module named 'src'`

**Solution**: Add project root to Python path:
```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
```

### Issue: `ImportError: cannot import name 'ResolutionEngine'`

**Solution**: Update imports to only use existing modules (see section 2)

### Issue: OpenAI API errors

**Solution**: 
1. Check API key is valid
2. Check you have credits
3. Use non-AI alternative (`MultiPhaseStrategyGenerator`)

### Issue: Neo4j connection fails

**Solution**:
1. Install Neo4j Desktop or Docker container
2. Check URI, username, password in `.env`
3. Alternative: Use file-based storage instead

---

## Status

- [x] Module audit complete
- [x] `__init__.py` fix documented
- [x] `__init__.py` fix applied
- [x] Imports tested successfully
- [x] Archived OpenAI client reference fixed
- [ ] OpenAI configured (optional)
- [ ] Neo4j tested (optional)
- [ ] Integration tests run

**Next**: Optional - Configure OpenAI for AI-powered strategies, or proceed to Phase 1 foundation work
