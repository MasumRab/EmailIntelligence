#!/usr/bin/env python3
"""
AI Tools Configurations Syncing and Consolidation Script
Consolidates AI tool configs from .aiglobal to EmailIntelligence dirs.
"""

import os
import json
import shutil
import argparse
import requests
from pathlib import Path

# Paths
SOURCE_DIR = Path.home() / ".aiglobal"
TARGET_DIRS = [
    Path.home() / "github" / "EmailIntelligence",
    Path.home() / "github" / "EmailIntelligenceAuto",
    Path.home() / "github" / "EmailIntelligenceGem",
    Path.home() / "github" / "EmailIntelligenceQwen",
]
CONSOLIDATION_DIR = Path.home() / "github" / "ai_consolidation"
ARCHIVED_DIR = CONSOLIDATION_DIR / "archived"
LOG_FILE = CONSOLIDATION_DIR / "ai_consolidation.log"

# AI tool dirs to look for
AI_DIRS = [".claude", ".cursor", ".copilot", ".codex", ".gemini", ".qwen", ".iflow"]
AI_FILES = ["AGENTS.md", "CLAUDE.md", "opencode.json", ".mcp.json"]

def setup_dirs():
    """Create necessary directories."""
    CONSOLIDATION_DIR.mkdir(exist_ok=True)
    ARCHIVED_DIR.mkdir(exist_ok=True)

def log(message):
    """Log message to file and print."""
    with open(LOG_FILE, 'a') as f:
        f.write(message + '\n')
    print(message)

def find_ai_files():
    """Find AI files in source and targets."""
    ai_files = {}
    for dir_name in AI_DIRS + AI_FILES:
        for target in TARGET_DIRS + [SOURCE_DIR]:
            path = target / dir_name
            if path.exists():
                if dir_name not in ai_files:
                    ai_files[dir_name] = []
                ai_files[dir_name].append(path)
    return ai_files

def consolidate_files(ai_files):
    """Consolidate same-named files."""
    for name, paths in ai_files.items():
        if len(paths) > 1:
            consolidated_path = CONSOLIDATION_DIR / f"consolidated_{name}"
            with open(consolidated_path, 'w') as outfile:
                for i, path in enumerate(paths):
                    outfile.write(f"--- SOURCE {i+1}: {path} ---\n")
                    if path.is_file():
                        try:
                            with open(path, 'r') as infile:
                                outfile.write(infile.read())
                        except UnicodeDecodeError:
                            outfile.write("(binary file)\n")
                    else:
                        outfile.write("(directory)\n")
                    outfile.write("\n")
            log(f"Consolidated {name} from {len(paths)} sources")
        else:
            # Single file or dir, copy directly
            if paths[0].is_file():
                shutil.copy2(paths[0], CONSOLIDATION_DIR / name)
            else:
                shutil.copytree(paths[0], CONSOLIDATION_DIR / name, dirs_exist_ok=True)
            log(f"Copied single {name}")

def validate_and_archive():
    """Validate files and archive invalid ones."""
    for file_path in CONSOLIDATION_DIR.glob("*"):
        if file_path.is_file():
            if file_path.name.startswith("consolidated_"):
                # Check if JSON
                try:
                    with open(file_path, 'r') as f:
                        content = f.read()
                        if content.strip().startswith("{"):
                            json.loads(content.split("---", 1)[0])  # Test first part
                        log(f"Validated {file_path.name}")
                except (json.JSONDecodeError, UnicodeDecodeError):
                    shutil.move(file_path, ARCHIVED_DIR / file_path.name)
                    log(f"Archived invalid: {file_path.name}")
            # Placeholder for outdated tool check
            try:
                if "outdated_tool" in file_path.read_text().lower():
                    shutil.move(file_path, ARCHIVED_DIR / file_path.name)
                    log(f"Archived outdated: {file_path.name}")
            except UnicodeDecodeError:
                pass  # Skip binary files

def regenerate_via_ai():
    """Regenerate consolidated files using Gemini AI."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        log("GEMINI_API_KEY not set. Skipping AI regeneration.")
        return

    regenerated_dir = CONSOLIDATION_DIR / "regenerated"
    regenerated_dir.mkdir(exist_ok=True)

    for file_path in CONSOLIDATION_DIR.glob("consolidated_*"):
        if file_path.is_file():
            with open(file_path, 'r') as f:
                content = f.read()

            prompt = f"Consolidate and clean up the following AI tool configurations from multiple sources. Resolve conflicts, ensure validity, and make it functional. Output only the consolidated content without explanations. Input:\n{content}"

            try:
                response = requests.post(
                    "https://api.gemini.ai/openai/v1/chat/completions",  # Assuming Gemini compatible endpoint
                    headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
                    json={"model": "gemini-1.5-flash", "messages": [{"role": "user", "content": prompt}], "max_tokens": 2000}
                )
                if response.status_code == 200:
                    result = response.json()["choices"][0]["message"]["content"]
                    regenerated_path = regenerated_dir / f"regenerated_{file_path.name.replace('consolidated_', '')}"
                    with open(regenerated_path, 'w') as f:
                        f.write(result)
                    log(f"Regenerated {file_path.name} using Gemini")
                else:
                    log(f"Failed to regenerate {file_path.name}: {response.text}")
            except Exception as e:
                log(f"Error regenerating {file_path.name}: {str(e)}")

def sync_to_dirs():
    """Sync consolidated files to target dirs."""
    for target in TARGET_DIRS:
        for file_path in CONSOLIDATION_DIR.glob("*"):
            if not file_path.name.startswith("consolidated_") and not file_path.is_dir():
                shutil.copy2(file_path, target)
                log(f"Synced {file_path.name} to {target}")

def dry_run(ai_files):
    """Perform dry run to show files with potential new info."""
    log("DRY RUN: Demonstrating files with potential new information")
    for name, paths in ai_files.items():
        log(f"File/Dir: {name}")
        for path in paths:
            log(f"  Source: {path}")
            # Placeholder: Check if content differs from rulesync
            rulesync_path = path.parent / ".rulesync" / "rules" / "overview.md"
            if rulesync_path.exists():
                with open(rulesync_path, 'r') as f:
                    rules = f.read()
                if path.is_file():
                    with open(path, 'r') as f:
                        content = f.read()
                    if content not in rules:
                        log(f"    Contains new info not in rulesync")
                    else:
                        log(f"    Info already in rulesync")
                else:
                    log(f"    Directory - check subfiles manually")
            else:
                log(f"    No rulesync rules found for comparison")
        log("")

def main():
    parser = argparse.ArgumentParser(description="AI Tools Consolidation Script")
    parser.add_argument("--dry-run", action="store_true", help="Perform dry run to show files with new info")
    parser.add_argument("--sync-only", action="store_true", help="Only sync existing consolidated files without re-consolidating")
    args = parser.parse_args()

    setup_dirs()
    log("Starting AI consolidation")
    if args.sync_only:
        sync_to_dirs()
        log("Sync complete")
        return
    ai_files = find_ai_files()
    if args.dry_run:
        dry_run(ai_files)
        log("Dry run complete")
        return
    consolidate_files(ai_files)
    validate_and_archive()
    regenerate_via_ai()
    sync_to_dirs()
    log("AI consolidation complete")

if __name__ == "__main__":
    main()