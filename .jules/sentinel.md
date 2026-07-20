## 2026-06-22 - [Insecure Deserialization via joblib.load]

**Vulnerability:** Arbitrary Code Execution via insecure model path loading (joblib.load)
**Learning:** `joblib.load` can execute malicious code during deserialization. Simply blocking paths outside a specific directory is too rigid and breaks custom model loading.
**Prevention:** Use a hybrid approach: verify model paths against an allowlist of known-safe directories (`models`, `artifacts`, `checkpoints`) and fallback to SHA256 signature verification for paths outside the allowlist. This preserves flexibility while preventing arbitrary code execution.
