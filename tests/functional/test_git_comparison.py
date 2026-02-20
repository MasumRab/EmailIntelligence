import pytest
from pathlib import Path
from src.core.git.plumbing import GitPlumbing
from src.core.git.comparison import BranchComparator

def test_comparison(git_repo):
    """Verify branch similarity calculation."""
    repo_path = Path(git_repo.working_tree_dir)
    plumbing = GitPlumbing(str(repo_path))
    
    # Commit A
    (repo_path / "a.txt").write_text("A")
    git_repo.index.add(["a.txt"])
    git_repo.index.commit("A")
    
    # Branch Feature
    feature = git_repo.create_head("feature")
    git_repo.head.reference = feature
    (repo_path / "b.txt").write_text("B")
    git_repo.index.add(["b.txt"])
    git_repo.index.commit("B")
    
    # Branch Main
    main = git_repo.heads.master # fixture uses master
    git_repo.head.reference = main
    (repo_path / "c.txt").write_text("C")
    git_repo.index.add(["c.txt"])
    git_repo.index.commit("C")
    
    # Structure:
    # A -> B (Feature)
    # A -> C (Main)
    
    # Common: A (1 commit)
    # Base (Main): A, C (2 commits)
    # Head (Feature): A, B (2 commits)
    # Union: A, B, C (3 unique commits)
    # Similarity: 1 / 3 = 0.33
    
    comparator = BranchComparator(plumbing)
    score = comparator.calculate_similarity("master", "feature")
    
    # Note: 'initial commit' from fixture is also shared.
    # So A is child of Initial.
    # Initial -> A -> B
    #              -> C
    # Common: Initial, A (2)
    # Base: Initial, A, C (3)
    # Head: Initial, A, B (3)
    # Union: 4 commits
    # Sim: 2/4 = 0.5
    
    assert 0.49 < score < 0.51
    
    base_only, head_only = comparator.get_unique_commits("master", "feature")
    assert len(base_only) == 1 # C
    assert len(head_only) == 1 # B
