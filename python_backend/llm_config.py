from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict


def load_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def get_git_branch() -> str:
    """Return the current git branch name if available, otherwise 'unknown'.

    This function reads the HEAD ref from the .git directory if present. It avoids
    calling out to `git` so it's safe in constrained environments.
    """
    repo_root = Path(__file__).resolve().parents[1]
    git_head = repo_root / ".git" / "HEAD"
    try:
        text = git_head.read_text(encoding="utf-8").strip()
    except Exception:
        return "unknown"
    if text.startswith("ref: "):
        return text.split("refs/heads/")[-1]
    return text


def load_llm_guidelines() -> Dict[str, Any]:
    """Load LLM guidelines by merging, in order of precedence:
      1. config/llm_guidelines.local.json (UNTRACKED, highest precedence)
      2. config/llm_guidelines.<branch>.json (tracked per-branch)
      3. config/llm_guidelines.json (tracked base defaults)

    Returns the merged dict.
    """
    repo_root = Path(__file__).resolve().parents[1]
    cfg_dir = repo_root / "config"

    base = load_json(cfg_dir / "llm_guidelines.json")

    branch = get_git_branch()
    branch_cfg = load_json(cfg_dir / f"llm_guidelines.{branch}.json")

    local = load_json(cfg_dir / "llm_guidelines.local.json")

    # Merge: base <- branch_cfg <- local (later keys override earlier)
    merged = {**base, **branch_cfg, **local}
    return merged


if __name__ == "__main__":
    import pprint

    cfg = load_llm_guidelines()
    pprint.pprint(cfg)
