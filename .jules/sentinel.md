## 2026-04-12 - [MEDIUM] Enforce secure timezone-aware datetimes
**Vulnerability:** Deprecated and timezone-naive `datetime.utcnow()` usage across authentication and context models.
**Learning:** The codebase previously relied on `datetime.utcnow()`, which in Python 3.12+ is deprecated and yields timezone-naive objects. When passed around or used in token claims, naive datetimes can introduce subtle validation bugs.
**Prevention:** Replace all occurrences of `datetime.utcnow()` with timezone-aware `datetime.now(timezone.utc)`. For Pydantic models, use a module-level `utc_now` helper function as the `default_factory`.
