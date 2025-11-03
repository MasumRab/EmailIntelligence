#!/usr/bin/env python3
"""
Script to automatically synchronize documentation between worktrees.
This script is called by the post-commit hook when documentation changes are detected.
"""

import os
import sys
import shutil
import subprocess
import argparse
from pathlib import Path


def is_git_repo(path):
    """Check if a directory is a git repository."""
    return (path / '.git').exists()


def get_git_root():
    """Get the root directory of the current git repository."""
    try:
        result = subprocess.run(
            ['git', 'rev-parse', '--show-toplevel'],
            capture_output=True,
            text=True,
            check=True
        )
        return Path(result.stdout.strip())
    except subprocess.CalledProcessError:
        print("Error: Not in a git repository")
        sys.exit(1)


def sync_docs_between_worktrees(run_once=False, verbose=False):
    """
    Synchronize documentation between worktrees.
    
    Args:
        run_once (bool): Whether to run once and exit
        verbose (bool): Whether to show verbose output
    """
    git_root = get_git_root()
    worktrees_dir = git_root / 'worktrees'
    
    if not worktrees_dir.exists():
        if verbose:
            print(f"Warning: {worktrees_dir} does not exist")
        return
    
    # Define source and target worktrees for documentation
    source_worktrees = [
        worktrees_dir / 'docs-main',
        worktrees_dir / 'docs-scientific'
    ]
    
    # Documentation directories to sync
    doc_dirs = ['docs', 'backlog']
    
    for source_worktree in source_worktrees:
        if not source_worktree.exists():
            if verbose:
                print(f"Warning: Source worktree {source_worktree} does not exist")
            continue
            
        # Determine the target worktree based on the source
        if source_worktree.name == 'docs-main':
            target_worktree = worktrees_dir / 'docs-scientific'
        elif source_worktree.name == 'docs-scientific':
            target_worktree = worktrees_dir / 'docs-main'
        else:
            continue  # Skip if not a recognized documentation worktree
            
        if not target_worktree.exists():
            if verbose:
                print(f"Warning: Target worktree {target_worktree} does not exist")
            continue
            
        # Sync documentation directories
        for doc_dir in doc_dirs:
            source_doc_dir = source_worktree / doc_dir
            target_doc_dir = target_worktree / doc_dir
            
            if source_doc_dir.exists():
                if verbose:
                    print(f"Syncing {source_doc_dir} to {target_doc_dir}")
                    
                # Create target directory if it doesn't exist
                target_doc_dir.mkdir(parents=True, exist_ok=True)
                
                # Use rsync to copy files (preserving metadata and using efficient transfer)
                try:
                    subprocess.run([
                        'rsync', '-av', '--delete',
                        str(source_doc_dir) + '/',
                        str(target_doc_dir)
                    ], check=True, capture_output=not verbose)
                    
                    if verbose:
                        print(f"Successfully synced {doc_dir} from {source_worktree.name} to {target_worktree.name}")
                except subprocess.CalledProcessError as e:
                    print(f"Error syncing {source_doc_dir} to {target_doc_dir}: {e}")
                    continue
    
    if verbose or run_once:
        print("Documentation synchronization completed")


def main():
    parser = argparse.ArgumentParser(description='Synchronize documentation between worktrees')
    parser.add_argument('--run-once', action='store_true', 
                       help='Run synchronization once and exit')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Enable verbose output')
    
    args = parser.parse_args()
    
    sync_docs_between_worktrees(run_once=args.run_once, verbose=args.verbose)


if __name__ == '__main__':
    main()