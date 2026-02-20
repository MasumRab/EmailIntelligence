import pytest
import subprocess
from pathlib import Path
from src.core.git.plumbing import GitPlumbing
from src.core.git.history import DAGBuilder, HistoryService

def run_git(repo_path, args):
    subprocess.run(["git"] + args, cwd=repo_path, check=True)

def test_dag_builder(git_repo):
    """Verify DAG construction from real git history."""
    repo_path = Path(git_repo.working_tree_dir)
    plumbing = GitPlumbing(str(repo_path))
    
    # Setup history using CLI for certainty
    # Initial commit is already done by fixture
    
    # Commit A
    (repo_path / "a.txt").write_text("A")
    run_git(repo_path, ["add", "a.txt"])
    run_git(repo_path, ["commit", "-m", "Commit A"])
    
    # Branch Feature
    run_git(repo_path, ["checkout", "-b", "feature"])
    (repo_path / "b.txt").write_text("B")
    run_git(repo_path, ["add", "b.txt"])
    run_git(repo_path, ["commit", "-m", "Commit B"])
    
    # Branch Main
    run_git(repo_path, ["checkout", "master"]) # fixture uses master usually, or main?
    # Check what branch we are on
    
    # Let's verify branch name
    # git_repo.active_branch.name might be master
    current = git_repo.active_branch.name
    
    (repo_path / "c.txt").write_text("C")
    run_git(repo_path, ["add", "c.txt"])
    run_git(repo_path, ["commit", "-m", "Commit C"])
    
    # Analyze Feature vs Main (current)
    builder = DAGBuilder(plumbing)
    dag = builder.build("feature", current)
    
    # Should contain C
    assert len(dag) >= 1
    found_c = False
    for node in dag.values():
        if node.message == "Commit C":
            found_c = True
            
    assert found_c

def test_rebase_plan(git_repo):
    """Verify topological sort."""
    repo_path = Path(git_repo.working_tree_dir)
    plumbing = GitPlumbing(str(repo_path))
    service = HistoryService(DAGBuilder(plumbing))
    
    # Linear history: Initial -> A -> B -> C
    (repo_path / "a.txt").write_text("A")
    run_git(repo_path, ["add", "a.txt"])
    run_git(repo_path, ["commit", "-m", "A"])
    
    (repo_path / "b.txt").write_text("B")
    run_git(repo_path, ["add", "b.txt"])
    run_git(repo_path, ["commit", "-m", "B"])
    
    (repo_path / "c.txt").write_text("C")
    run_git(repo_path, ["add", "c.txt"])
    run_git(repo_path, ["commit", "-m", "C"])
    
    head_sha = git_repo.head.commit.hexsha
    # Initial -> A -> B -> C
    # Parents: C->B->A->Initial
    initial = git_repo.head.commit.parents[0].parents[0].parents[0]
    base_sha = initial.hexsha
    
    plan = service.plan_rebase(base_sha, head_sha)
    
    assert len(plan.commits) == 3
    assert plan.commits[0].message == "A"
    assert plan.commits[1].message == "B"
    assert plan.commits[2].message == "C"
