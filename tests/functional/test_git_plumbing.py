import pytest
from src.core.git.plumbing import GitPlumbing
from src.core.git.detector import ConflictDetector

def test_merge_tree_conflict(git_repo):
    """Verify merge-tree detects conflicts in a real repo."""
    repo_path = git_repo.working_tree_dir
    plumbing = GitPlumbing(repo_path)
    
    # Create conflict
    main = git_repo.head.reference
    
    # Branch A
    branch_a = git_repo.create_head("branch_a")
    git_repo.head.reference = branch_a
    (Path(repo_path) / "conflict.txt").write_text("Change A")
    git_repo.index.add(["conflict.txt"])
    git_repo.index.commit("Commit A")
    
    # Branch B
    git_repo.head.reference = main
    branch_b = git_repo.create_head("branch_b")
    git_repo.head.reference = branch_b
    (Path(repo_path) / "conflict.txt").write_text("Change B")
    git_repo.index.add(["conflict.txt"])
    git_repo.index.commit("Commit B")
    
    # Run merge-tree
    output = plumbing.merge_tree("branch_a", "branch_b")
    
    assert "conflict.txt" in output
    assert "CONFLICT" in output

from pathlib import Path
