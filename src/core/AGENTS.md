# src/core/ AGENTS.md

**High-complexity domain module** — core business logic layer

## OVERVIEW
Task Master AI core domain: security validation, git operations, conflict detection/resolution. Pure Python with async patterns.

## FILES
| File | Purpose |
|------|---------|
| `security.py` | SecurityValidator: path safety, PR number validation |
| `interfaces.py` | ABC contracts: IConflictDetector, IConflictResolver, IAnalyzer |
| `git_operations.py` | Git CLI operations, branch/PR management |
| `conflict_models.py` | Conflict, AnalysisResult, ResolutionStrategy, ValidationResult, ResolutionPlan |
| `exceptions.py` | Custom exceptions for domain errors |
| `config.py` | Configuration management |

## WHERE TO LOOK
| Task | Location |
|------|----------|
| Add new detector | `interfaces.py` → implement IConflictDetector |
| Add new model | `conflict_models.py` |
| Security checks | `security.py` → SecurityValidator |
| Git logic | `git_operations.py` |

## CONVENTIONS
- All interfaces use `abc.ABC` + `@abstractmethod`
- Async methods return `List[T]` or `Optional[T]`
- Models use dataclasses/Enums from `conflict_models.py`
- Security: paths MUST be validated via `SecurityValidator.is_safe_path()`

## ANTI-PATTERNS
- DO NOT call git directly — use `git_operations.py` wrapper
- DO NOT skip path validation in security.py
- DO NOT add sync methods where async is used

## NOTES
- Interfaces defined in `interfaces.py` MUST be implemented by detectors/resolvers
- Models in `conflict_models.py` are shared across modules
