"""
Smart Merge Command Module

Implements semantic-aware 3-way merging for individual files.
Ported from orchestration-tools:scripts/intelligent_merger.py.
"""

import subprocess
from argparse import Namespace
from pathlib import Path
from typing import Any, Dict, List, Tuple

from ..interface import Command


class MergeSmartCommand(Command):
    """
    Command for intelligently merging two versions of a file using a common ancestor.
    
    This tool identifies changes from both local and remote refs and applies them
    where they don't overlap, inserting conflict markers for intersecting changes.
    """

    def __init__(self):
        self._security_validator = None

    @property
    def name(self) -> str:
        return "merge-smart"

    @property
    def description(self) -> str:
        return "Intelligently merge two versions of a file using a common ancestor"

    def add_arguments(self, parser: Any) -> None:
        """Add command-specific arguments."""
        parser.add_argument("file", help="Path to the file to merge")
        parser.add_argument("--local", default="HEAD", help="Local git ref (default: HEAD)")
        parser.add_argument("--remote", required=True, help="Remote git ref to merge from")
        parser.add_argument("--output", help="Custom output path for merged file")

    def get_dependencies(self) -> Dict[str, Any]:
        """Get required dependencies."""
        return {
            "security_validator": "SecurityValidator"
        }

    def set_dependencies(self, dependencies: Dict[str, Any]) -> None:
        """Set command dependencies."""
        self._security_validator = dependencies.get("security_validator")

    async def execute(self, args: Namespace) -> int:
        """Execute the smart merge command."""
        file_path = Path(args.file)
        local_ref = args.local
        remote_ref = args.remote

        # Security validation
        if self._security_validator:
            is_safe, error = self._security_validator.validate_path_security(str(file_path.absolute()))
            if not is_safe:
                print(f"Error: Security violation for file '{file_path}': {error}")
                return 1

        if not file_path.exists():
            print(f"Error: File '{file_path}' not found.")
            return 1

        print(f"🧬 Starting smart merge for '{file_path}'...")
        print(f"   Refs: {local_ref} <-> {remote_ref}")

        try:
            # 1. Get merge base
            base_ref = self._run_git(["merge-base", local_ref, remote_ref]).strip()
            if not base_ref:
                print("Error: Could not find common ancestor (merge-base).")
                return 1

            # 2. Get content versions
            base_content = self._get_git_content(file_path, base_ref)
            local_content = self._get_git_content(file_path, local_ref)
            remote_content = self._get_git_content(file_path, remote_ref)

            # 3. Get changed lines
            local_changes = self._get_changed_lines(file_path, base_ref, local_ref)
            remote_changes = self._get_changed_lines(file_path, base_ref, remote_ref)

            # 4. Perform 3-way merge
            merged_content, conflicts = self._do_3way_merge(
                base_content, local_content, remote_content, 
                local_changes, remote_changes,
                local_ref, remote_ref
            )

            # 5. Write output
            output_path = Path(args.output) if args.output else file_path.with_suffix(".merged")
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(merged_content)

            print(f"\n✅ Merged content written to: {output_path}")
            if conflicts == 0:
                print("✨ No conflicts detected!")
            else:
                print(f"⚠️  Detected {conflicts} conflicts. Manual resolution required.")

            return 0 if conflicts == 0 else 2
        except Exception as e:
            print(f"Error during smart merge: {e}")
            return 1

    def _run_git(self, args: List[str]) -> str:
        """Execute a git command and return output."""
        result = subprocess.run(["git"] + args, capture_output=True, text=True, check=True)
        return result.stdout

    def _get_git_content(self, path: Path, ref: str) -> str:
        """Get file content at specific git ref."""
        return self._run_git(["show", f"{ref}:{path}"])

    def _get_changed_lines(self, path: Path, base: str, target: str) -> set:
        """Identify which lines changed in target relative to base."""
        diff = self._run_git(["diff", f"{base}..{target}", "--", str(path)])
        changed = set()
        for line in diff.split("\n"):
            if line.startswith("@@"):
                parts = line.split("+")
                if len(parts) > 1:
                    info = parts[1].split(" ")[0]
                    start = int(info.split(",")[0]) if "," in info else int(info)
                    count = int(info.split(",")[1]) if "," in info else 1
                    for i in range(start, start + count):
                        changed.add(i)
        return changed

    def _do_3way_merge(self, base, local, remote, local_chg, remote_chg, l_ref, r_ref):
        """Core 3-way merge logic with conflict markers."""
        base_lines = base.splitlines()
        local_lines = local.splitlines()
        remote_lines = remote.splitlines()
        
        merged = []
        conflicts = 0
        max_ln = max(len(base_lines), len(local_lines), len(remote_lines))

        for i in range(max_ln):
            ln = i + 1
            b = base_lines[i] if i < len(base_lines) else ""
            l = local_lines[i] if i < len(local_lines) else b
            r = remote_lines[i] if i < len(remote_lines) else b

            l_mod = ln in local_chg
            r_mod = ln in remote_chg

            if l_mod and r_mod and l != r:
                merged.append(f"<<<<<<< LOCAL ({l_ref})")
                merged.append(l)
                merged.append("=======")
                merged.append(r)
                merged.append(f">>>>>>> REMOTE ({r_ref})")
                conflicts += 1
            elif l_mod:
                merged.append(l)
            elif r_mod:
                merged.append(r)
            else:
                merged.append(b)

        return "\n".join(merged), conflicts
