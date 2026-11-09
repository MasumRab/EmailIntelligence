1. **Create the documentation file `docs/CI_REVIEW_AUTH_SETUP.md`**
   - It will contain a short, clear explanation of how to configure the required secrets/variables for the `gemini-review.yml` workflow.
   - It will explain that either `GEMINI_API_KEY`, `GOOGLE_API_KEY` (as Secrets), or `GCP_WIF_PROVIDER` (as a Variable) must be set in GitHub repository Settings > Secrets and variables > Actions.
2. **Complete pre-commit steps**
   - Complete pre-commit steps to ensure proper testing, verification, review, and reflection are done.
3. **Submit the changes**
   - Submit the PR with the new file and reply with the PR URL.
