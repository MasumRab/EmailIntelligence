# Scientific Branch Repair Runbook: Maintenance & Alignment

This runbook provides a structured approach for repairing, maintaining, and aligning the `scientific` branch. It clarifies the relationship between the branch and its subtrees, and covers specialized scientific components.

---

## 1. Branch Architecture & Subtrees

The `scientific` branch is a **separate, long-lived branch** dedicated to data science, machine learning, and exploratory UI (Gradio).

### The `setup/` Subtree
While `scientific` is a separate branch, it manages its `setup/` directory as a **Git Subtree** pulled from the central `launch-setup-fixes` (or equivalent) branch.
*   **Purpose:** Ensures the scientific branch benefits from global launcher improvements without manual file copying.
*   **Command Prefix:** Always use `--prefix=setup` for subtree operations.

### remote Tracking
Verify the `origin` remote is correctly configured to point to the main repository to enable subtree pulls.

---

## 2. Subtree Recovery & Sync

### Pulling Global Improvements
To sync the `setup/` directory with the latest global launcher fixes:
```bash
git subtree pull --prefix=setup origin launch-setup-fixes --squash
```

### Resolving "No Common Ancestor" Errors
If the subtree relationship is broken, you must re-initialize it:
1.  **Backup:** `cp -r setup/ ../setup_backup`
2.  **Remove & Commit:** `git rm -r setup && git commit -m "chore: remove broken setup subtree"`
3.  **Re-add:**
    ```bash
    git subtree add --prefix=setup origin launch-setup-fixes --squash
    ```
4.  **Restore:** Manually re-integrate any scientific-specific tweaks from `../setup_backup`.

---

## 3. Scientific-Specific Components

### Gradio UI Troubleshooting
The scientific branch includes a Gradio-based interface.
*   **Startup Failure:** If `python3 setup/launch.py --share` fails, verify that `gradio` is installed in the virtual environment.
*   **Port Conflicts:** Gradio defaults to port `7860`. Use `lsof -i :7860` to check for hanging processes.

### Specialized Dependencies
The `scientific` branch requires `pandas`, `scipy`, `scikit-learn`, and often `torch`.
*   **Missing Libs:** If a pull from the `setup` subtree overwrites `requirements.txt`, you must ensure scientific dependencies are restored.
*   **Best Practice:** Maintain a `requirements-scientific.txt` and ensure the launcher or setup scripts reference it during environment creation.

---

## 4. Alignment & Validation

### Aligning with Feature Branches
As per the `SCIENTIFIC_BRANCH_ALIGNMENT_PLAN.md`, regular merges from feature branches are required.
1.  **Merge Strategy:** Favor the `scientific` branch implementation for core infrastructure files.
2.  **Conflict Resolution:** Use `git merge scientific` within feature branches to bring them up to date before they are merged back into `scientific`.

### Validation Shield
After any repair or alignment:
1.  **Syntax Check:** `python3 -m py_compile setup/*.py`
2.  **System Info:** `python3 setup/launch.py --system-info`
3.  **Scientific Test:** Verify the Gradio UI starts by running the launcher with the `--share` or `--debug` flags.

### Post-Repair Checklist
- [ ] `setup/` directory is correctly synchronized with global fixes.
- [ ] Gradio UI launches and is accessible.
- [ ] Scientific-specific dependencies are present in the virtual environment.
- [ ] No regression in specialized ML/NLP processing capabilities.
