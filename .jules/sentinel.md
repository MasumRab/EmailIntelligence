## 2025-06-15 - Defense in Depth: CORS and Path validation

**Vulnerability:** Overly permissive CORS settings and lack of input validation on branch names derived from git stash messages.
**Learning:** Found an overly permissive CORS configuration (`allow_methods=["*"]`, `allow_headers=["*"]`) in `src/main.py`. Additionally, the git stash resolution script (`src/cli/commands/git/stash_resolve.py`) extracted branch names directly from stash messages using regex and passed them to `git checkout` without validation, making it theoretically possible for a malicious branch/stash name to inject command flags or traverse paths.
**Prevention:** Hardcode specific, safe allowed HTTP methods and headers for CORS when possible. For CLI tools, always validate and sanitize identifiers (like branch names) parsed from external or untrusted sources before passing them to subprocesses or the filesystem.
