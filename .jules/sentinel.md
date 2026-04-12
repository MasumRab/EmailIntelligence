
## 2026-04-12 - Fix Command Injection in Deployment Scripts
**Vulnerability:** Found multiple `subprocess.run(..., shell=True)` usages inside generic `run_command` wrappers within `deployment/migrate.py` and `deployment/setup_env.py`. These took direct string input, exposing a risk if those inputs were ever user-controlled.
**Learning:** Shell scripts inside python scripts (`setup_env.py`, `migrate.py`) tend to heavily rely on `shell=True` to quickly replicate bash functionality (like `createdb ... || true`). It introduces latent risk that can spread when people copy the `run_command` wrapper format.
**Prevention:** Always refactor generic `run_command` wrappers to expect list arguments, set `shell=False`, and explicitly handle failures using Python (`check=False` or `try/except`) instead of relying on shell operators.
