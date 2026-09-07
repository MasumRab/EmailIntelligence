## 2026-04-02

### Fix arbitrary shell input injection formatting bugs

**Vulnerability Discovered:** Bash scripts used `echo -e` which can cause command/escape sequence injection vulnerabilities based on user input, and triggers a SonarCloud security hotspot.

**Learning:** When printing variables into bash scripts, especially within loops or strings with format modifiers, use `printf "%b\n"` instead of `echo -e` for dynamic input safety.

**Prevention Note:** Lint bash scripts and replace `echo -e` with `printf "%b\n"` in codebase updates.
