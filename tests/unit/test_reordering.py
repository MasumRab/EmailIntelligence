import pytest
from src.git.reordering import CommitReorderer

@pytest.fixture
def reorderer():
    return CommitReorderer()

def test_group_commits_by_module(reorderer):
    commits = [
        {'hash': '1', 'files': ['src/core/models.py'], 'message': 'Core change'},
        {'hash': '2', 'files': ['src/git/repo.py'], 'message': 'Git change'},
        {'hash': '3', 'files': ['src/core/utils.py'], 'message': 'Another core change'},
        {'hash': '4', 'files': ['README.md'], 'message': 'Docs change'}
    ]
    
    groups = reorderer.group_commits_by_module(commits)
    
    assert len(groups['core']) == 2
    assert len(groups['git']) == 1
    assert len(groups['docs']) == 1
    assert groups['core'][0]['hash'] == '1'
    assert groups['core'][1]['hash'] == '3'

def test_suggest_order_priority(reorderer):
    commits = [
        {'hash': '1', 'files': ['src/cli/main.py'], 'message': 'CLI'},
        {'hash': '2', 'files': ['src/core/base.py'], 'message': 'Core'},
        {'hash': '3', 'files': ['src/git/ops.py'], 'message': 'Git'},
    ]
    
    # Expected order based on priority: core -> git -> cli
    ordered = reorderer.suggest_order(commits)
    
    assert ordered[0]['hash'] == '2'  # Core
    assert ordered[1]['hash'] == '3'  # Git
    assert ordered[2]['hash'] == '1'  # CLI

def test_mixed_module_commits(reorderer):
    commits = [
        {'hash': '1', 'files': ['src/core/a.py', 'src/git/b.py'], 'message': 'Mixed'},
    ]
    
    groups = reorderer.group_commits_by_module(commits)
    assert 'cross-cutting' in groups
    assert len(groups['cross-cutting']) == 1
