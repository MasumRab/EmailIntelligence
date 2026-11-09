# Sentinel Learnings

## 2025-01-26 - Insecure Model Loading via joblib.load
**Vulnerability:** In `src/backend/python_nlp/nlp_engine.py` and `src/core/model_registry.py`, machine learning models are loaded directly with `joblib.load(model_path)` without verifying if the path is safe. This can lead to insecure deserialization attacks if a malicious model is loaded.
**Learning:** Found that strict path validation breaks legitimate custom model loading. The `src.core.security.verify_model_safety` function exists to provide a hybrid approach (allowlist directories + SHA256 signature verification).
**Prevention:** Always use `verify_model_safety` before loading deserialized objects via `joblib` or `pickle`.
