import pytest
from unittest.mock import Mock, patch
from src.lib.git_wrapper import GitWrapper
import git

# Mock a GitPython Repo object and its methods
@pytest.fixture
def mock_repo():
    mock_repo_obj = Mock(spec=git.Repo)
    
    # Mock iter_commits
    mock_commit1 = Mock(spec=git.Commit)
    mock_commit1.hexsha = "commit1_sha"
    mock_commit1.author.name = "Author 1"
    mock_commit1.authored_date = 1678886400 # March 15, 2023 00:00:00 UTC
    mock_commit1.message = "Commit 1 message"
    mock_commit1.parents = [] # First commit
    mock_commit1.tree.diff.return_value = "diff for commit 1"

    mock_commit2 = Mock(spec=git.Commit)
    mock_commit2.hexsha = "commit2_sha"
    mock_commit2.author.name = "Author 2"
    mock_commit2.authored_date = 1678972800 # March 16, 2023 00:00:00 UTC
    mock_commit2.message = "Commit 2 message"
    mock_commit2.parents = [mock_commit1]
    mock_commit2.diff.return_value = "diff for commit 2"

    mock_repo_obj.iter_commits.return_value = [mock_commit2, mock_commit1]

    # Mock head.ref.log()
    mock_reflog_entry1 = Mock(spec=git.RefLogEntry)
    mock_reflog_entry1.message = "commit: initial commit"
    mock_reflog_entry2 = Mock(spec=git.RefLogEntry)
    mock_reflog_entry2.message = "rebase (start): checkout main"
    mock_reflog_entry3 = Mock(spec=git.RefLogEntry)
    mock_reflog_entry3.message = "rebase (finish): refs/heads/feature"
    
    mock_repo_obj.head.ref.log.return_value = [mock_reflog_entry3, mock_reflog_entry2, mock_reflog_entry1]

    # Mock active_branch
    mock_branch_head = Mock(spec=git.Head)
    mock_branch_head.name = "main"
    mock_repo_obj.active_branch = mock_branch_head

    # Mock heads
    mock_head1 = Mock(spec=git.Head)
    mock_head1.name = "main"
    mock_head2 = Mock(spec=git.Head)
    mock_head2.name = "feature"
    mock_repo_obj.heads = [mock_head1, mock_head2]

    # Mock commit by hexsha
    mock_repo_obj.commit.side_effect = lambda x: {
        "commit1_sha": mock_commit1,
        "commit2_sha": mock_commit2,
        "main": mock_commit2, # Assuming main points to commit2
        "feature": mock_commit1 # Assuming feature points to commit1
    }.get(x)

    return mock_repo_obj

# Patch git.Repo to return our mock_repo_obj
@patch('git.Repo')
def test_git_wrapper_init(mock_git_repo, mock_repo):
    mock_git_repo.return_value = mock_repo
    wrapper = GitWrapper("/fake/path")
    mock_git_repo.assert_called_once_with("/fake/path")
    assert wrapper.repo == mock_repo

@patch('git.Repo')
def test_get_commits_all(mock_git_repo, mock_repo):
    mock_git_repo.return_value = mock_repo
    wrapper = GitWrapper("/fake/path")
    commits = list(wrapper.get_commits())
    assert len(commits) == 2
    assert commits[0].hexsha == "commit2_sha"
    assert commits[1].hexsha == "commit1_sha"
    mock_repo.iter_commits.assert_called_once_with()

@patch('git.Repo')
def test_get_commits_range(mock_git_repo, mock_repo):
    mock_git_repo.return_value = mock_repo
    wrapper = GitWrapper("/fake/path")
    commits = list(wrapper.get_commits("HEAD~1..HEAD"))
    assert len(commits) == 2 # Mock returns all commits regardless of range for simplicity
    mock_repo.iter_commits.assert_called_once_with("HEAD~1..HEAD")

@patch('git.Repo')
def test_get_reflog(mock_git_repo, mock_repo):
    mock_git_repo.return_value = mock_repo
    wrapper = GitWrapper("/fake/path")
    reflog = wrapper.get_reflog()
    assert len(reflog) == 3
    assert "rebase (finish)" in reflog[0].message

@patch('git.Repo')
def test_get_commit_diff_initial_commit(mock_git_repo, mock_repo):
    mock_git_repo.return_value = mock_repo
    wrapper = GitWrapper("/fake/path")
    
    mock_commit1 = mock_repo.commit.side_effect("commit1_sha")
    diff = wrapper.get_commit_diff(mock_commit1)
    assert diff == "diff for commit 1"
    mock_commit1.tree.diff.assert_called_once_with(mock_repo.tree('4b825dc642cb6eb9a060e54bf8d69288fbee4904'))

@patch('git.Repo')
def test_get_commit_diff_non_initial_commit(mock_git_repo, mock_repo):
    mock_git_repo.return_value = mock_repo
    wrapper = GitWrapper("/fake/path")
    
    mock_commit2 = mock_repo.commit.side_effect("commit2_sha")
    diff = wrapper.get_commit_diff(mock_commit2)
    assert diff == "diff for commit 2"
    mock_commit2.diff.assert_called_once_with(mock_commit2.parents[0])

@patch('git.Repo')
def test_get_branch_head_commit(mock_git_repo, mock_repo):
    mock_git_repo.return_value = mock_repo
    wrapper = GitWrapper("/fake/path")
    commit = wrapper.get_branch_head_commit("main")
    assert commit.hexsha == "commit2_sha"
    mock_repo.commit.assert_called_once_with("main")

@patch('git.Repo')
def test_get_all_branches(mock_git_repo, mock_repo):
    mock_git_repo.return_value = mock_repo
    wrapper = GitWrapper("/fake/path")
    branches = wrapper.get_all_branches()
    assert len(branches) == 2
    assert branches[0].name == "main"
    assert branches[1].name == "feature"

@patch('git.Repo')
def test_get_current_branch(mock_git_repo, mock_repo):
    mock_git_repo.return_value = mock_repo
    wrapper = GitWrapper("/fake/path")
    branch = wrapper.get_current_branch()
    assert branch.name == "main"
    assert wrapper.repo.active_branch.name == "main"

@patch('git.Repo')
def test_get_commit_by_hexsha(mock_git_repo, mock_repo):
    mock_git_repo.return_value = mock_repo
    wrapper = GitWrapper("/fake/path")
    commit = wrapper.get_commit_by_hexsha("commit1_sha")
    assert commit.hexsha == "commit1_sha"
    mock_repo.commit.assert_called_once_with("commit1_sha")
