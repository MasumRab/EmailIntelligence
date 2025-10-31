Branch-specific config folder

Naming convention:
- `llm_guidelines.<branch>.json` — branch-specific LLM guideline file tracked in Git.
- `llm_guidelines.local.json` — local-only overrides; add this pattern to `.gitignore` if not already ignored.

Usage:
- Tools and scripts can read `config/llm_guidelines.<branch>.json` to tailor model parameters per branch.
- Keep the `llm_guidelines.<branch>.json` committed on branches where persistent behavior is desired.

Presets included:
- `llm_guidelines.opencode.json` — prepared for code-first workflows (gpt-4o-code preset).
- `llm_guidelines.qwen.json` — research/concise responses (qwen-7b preset).

Local overrides:
- A sample `llm_guidelines.local.json.sample` is provided. Copy it to `config/llm_guidelines.local.json` to create a local, untracked override (this filename is in `.gitignore`).

Best practices:
- Store sensitive keys or credentials in `jsons/` or in environment variables, not in these files.
- If you need ephemeral overrides, use `llm_guidelines.local.json` and add it to `.gitignore`.
- When switching branches, Git will show changes only if the branch has a different `llm_guidelines.<branch>.json` file; this is intentional.

Loading behavior summary:
- Load order: `llm_guidelines.json` (base) <- `llm_guidelines.<branch>.json` (branch) <- `llm_guidelines.local.json` (local, highest precedence).
