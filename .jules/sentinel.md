## 2024-05-18: Timezone-Aware Datetimes in Pydantic Models

* **Vulnerability Discover:** The Pydantic models in `src/context_control/models.py` and the FastAPI app in `src/main.py` were using `datetime.utcnow()` without timezone information. This can lead to timezone confusion vulnerabilities (CWE-116), especially when dates are serialized/deserialized across different systems or when comparing timestamps.
* **Learning:** Use `datetime.now(timezone.utc)` to ensure that all datetimes are timezone-aware. In Pydantic models with a `default_factory`, use a lambda function `lambda: datetime.now(timezone.utc)` to evaluate the current time when the model is instantiated.
* **Prevention Note:** Ensure that all newly added datetimes are timezone-aware using `datetime.now(timezone.utc)` instead of `datetime.utcnow()`.
