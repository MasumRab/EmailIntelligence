# Phase 2: Repository Feature Analysis

**Generated:** November 22, 2025  
**Status:** IN PROGRESS

---

## Repository Structure Overview

### EmailIntelligence (Main)
**Purpose:** Core Email Intelligence platform
**Key Directories:**
- `src/` - Main application code
- `python_backend/` - Backend services (LLM config, etc.)
- `worktree_system/` - Task decomposer system
- `setup/` - Configuration and setup utilities
- Test files at root level

**Notable Files:** task_decomposer.py, llm_config.py, main.py

---

### EmailIntelligenceAider
**Purpose:** Aider-specific variant
**Key Directories:**
- `setup/` - Contains routing.py, container.py, environment.py
- Root level test files (test_bug5_targeted.py)

**Key Difference from Main:** Includes `routing.py` (not in EmailIntelligence)
**Similarity:** Same structure as EmailIntelligenceGem and EmailIntelligenceQwen

---

### EmailIntelligenceAuto
**Purpose:** Automation features and orchestration
**Key Directories:**
- `src/` - Application code
- `setup/` - Orchestration control, container, launch, settings
- `tests/` - Dedicated test directory with multiple test files

**Unique Features:** 
- `orchestration_control.py` (automation-specific)
- `tests/` directory (separate from root)
- `test_commands.py`, `test_hooks.py`, `test_sync.py`

**Notable:** More comprehensive test structure than variants

---

### EmailIntelligenceGem
**Purpose:** Gemini API variant
**Key Directories:**
- `setup/` - Same structure as Aider and Qwen
- Root level test files

**Similarity:** Nearly identical to Aider and Qwen (cloned variant)

---

### EmailIntelligenceQwen
**Purpose:** Qwen model variant
**Key Directories:**
- `setup/` - Same structure as Aider and Gem
- Root level test files

**Similarity:** Nearly identical to Aider and Gem (cloned variant)

---

### PR/EmailIntelligence
**Purpose:** Pull request tracking branch
**Status:** Need to investigate separately

---

## Code Duplication Analysis

### High Duplication (3 Repos): EmailIntelligenceAider, EmailIntelligenceGem, EmailIntelligenceQwen

These three repos appear to be **cloned variants** with identical structure:
- Same setup files: routing.py, project_config.py, test_stages.py, test_launch.py, utils.py, args.py, test_config.py, container.py, environment.py
- Same test file: test_bug5_targeted.py
- Only difference: likely in configuration or model selection

**Recommendation:** High consolidation candidate

---

### Medium Duplication: EmailIntelligenceAuto vs Main

EmailIntelligenceAuto appears to be:
- An enhanced version with orchestration features
- Better organized tests (`tests/` directory)
- Additional configuration (settings.py, orchestration_control.py)
- Could be merged into main with features under `src/`

---

### Structure Differences

| Aspect | Main | Aider | Auto | Gem | Qwen |
|--------|------|-------|------|-----|------|
| src/ dir | ✓ | - | ✓ | - | - |
| tests/ dir | - | - | ✓ | - | - |
| python_backend/ | ✓ | - | - | - | - |
| worktree_system/ | ✓ | - | - | - | - |
| setup/ | ✓ | ✓ | ✓ | ✓ | ✓ |
| routing.py | - | ✓ | - | ✓ | ✓ |
| orchestration_control.py | - | - | ✓ | - | - |
| python_backend/ | ✓ | - | - | - | - |

---

## Recommendations for Further Analysis

### Next Steps:

1. **Compare setup/ files** across all repos - identify what's truly different
2. **Check requirements.txt/pyproject.toml** - dependency differences
3. **Examine main.py/entry points** - how are variants invoked
4. **Look at git history** - understand how variants were created
5. **Test coverage analysis** - which repos have better tests

### Quick File Count:
```bash
# Count Python files per repo
for repo in EmailIntelligence EmailIntelligenceAider EmailIntelligenceAuto EmailIntelligenceGem EmailIntelligenceQwen; do
  count=$(find /home/masum/github/$repo -name "*.py" | wc -l)
  echo "$repo: $count files"
done
```

---

## Preliminary Consolidation Recommendation

Based on structure analysis:

**Option D (Hybrid)** appears most suitable:
1. **Core library** = EmailIntelligence (main)
2. **Shared utilities** = setup/ modules consolidated
3. **Variant configs** = In separate configuration files or submodule
4. **Automation** = EmailIntelligenceAuto's features merge into core

**Rationale:**
- Aider/Gem/Qwen are clearly cloned variants (easy to consolidate)
- Auto has valuable orchestration features (should be in core)
- Main repository becomes the consolidation point
- Maintain variant-specific configs without code duplication

---

## Action Items for Phase 2

- [ ] Generate file count report
- [ ] Compare dependency files (requirements.txt)
- [ ] Analyze git history of cloned variants
- [ ] Check what makes variants different (configs vs code)
- [ ] Finalize consolidation decision
- [ ] Create migration plan

