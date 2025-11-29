
import pytest
import asyncio
from pathlib import Path
from src.git.conflict_detector import GitConflictDetector
from src.core.models import ConflictTypeExtended
from src.git.repository import RepositoryOperations

@pytest.fixture
async def git_repo_with_conflict(temp_dir):
    """
    Sets up a real git repository with a conflict between 'main' and 'feature'.
    """
    repo_path = temp_dir / "conflict_repo"
    repo_path.mkdir()
    
    repo = RepositoryOperations(repo_path)
    
    # helper to run git commands
    async def git(*args):
        return await repo.run_git(list(args))

    await git("init")
    await git("branch", "-M", "main")
    await git("config", "user.email", "test@example.com")
    await git("config", "user.name", "Test User")
    
    # Create base commit
    file_path = repo_path / "conflict_file.txt"
    file_path.write_text("Base content\nLine 2\nLine 3\n")
    await git("add", "conflict_file.txt")
    await git("commit", "-m", "Initial commit")
    
    # Create feature branch
    await git("checkout", "-b", "feature")
    file_path.write_text("Feature content\nLine 2\nLine 3\n")
    await git("add", "conflict_file.txt")
    await git("commit", "-m", "Feature change")
    
    # Create conflict in main
    await git("checkout", "main")
    file_path.write_text("Main content\nLine 2\nLine 3\n")
    await git("add", "conflict_file.txt")
    await git("commit", "-m", "Main change")
    
    return repo_path

@pytest.mark.asyncio
async def test_detect_conflicts_between_branches(git_repo_with_conflict):
    repo_path = git_repo_with_conflict
    detector = GitConflictDetector(repo_path)
    
    conflicts = await detector.detect_conflicts_between_branches("feature", "main")
    
    assert len(conflicts) == 1
    conflict = conflicts[0]
    assert conflict.file_paths == ["conflict_file.txt"]
    assert conflict.type == ConflictTypeExtended.MERGE_CONFLICT
    
    # This is expected to fail until we implement block extraction
    assert len(conflict.blocks) > 0
    assert conflict.blocks[0].start_line > 0
    assert "Feature content" in conflict.blocks[0].content
    assert "Main content" in conflict.blocks[0].content
