1. **Understand CI failure:** The tests `test_workflow_engine.py`, `test_dashboard.py`, `test_modular_ai_engine.py`, `test_auth.py`, `test_gmail_api.py`, `test_launcher.py`, `test_mfa.py`, `test_password_hashing.py` failed due to missing `networkx`, `argon2`, `googleapiclient`, `pyotp` etc. This occurs because the GitHub Actions CI (`ci.yml` or `test.yml`) installs dependencies from `requirements-dev.txt` (`pip install -r requirements-dev.txt`) for verification. The newly added modules and requirements in PR #571 are missing from `requirements-dev.txt`.
2. **Fix `requirements-dev.txt`:** Added missing dependencies to `requirements-dev.txt`:
   - `networkx>=3.1`
   - `argon2-cffi>=23.1.0`
   - `pyotp>=2.9.0`
   - `qrcode>=7.4.2`
   - `google-api-python-client>=2.172.0`
3. **Commit and Push:** The fix is committed with the message "Update ignoring and requirements-dev.txt for tests". Needs pushing to GitHub.
4. **Fix massive diff:** Because the git branch is bloated with untracked cache and `.jules` directories and `temp_untracked_files/`, I have successfully added them to `.gitignore` and removed cached files.
5. **Verify checks:** Monitor workflow runs in GitHub using `gh run watch` or `gh pr checks`
