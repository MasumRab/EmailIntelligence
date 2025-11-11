import git
from typing import List, Optional, Dict
from ..models.branch import Branch, BranchType

class GitService:
    """
    Service for Git operations and repository interactions
    """
    
    def __init__(self, repo_path: str = "."):
        self.repo_path = repo_path
        self.repo = git.Repo(repo_path)
    
    def get_current_branch(self) -> str:
        """
        Get the name of the current branch
        
        Returns:
            Name of the current branch
        """
        return self.repo.active_branch.name
    
    def get_all_branches(self) -> List[str]:
        """
        Get names of all branches in the repository
        
        Returns:
            List of branch names
        """
        return [branch.name for branch in self.repo.branches]
    
    def get_branch_info(self, branch_name: str) -> Optional[Branch]:
        """
        Get information about a specific branch
        
        Args:
            branch_name: Name of the branch to get info for
            
        Returns:
            Branch object if found, None otherwise
        """
        try:
            # Check if branch exists
            if branch_name in [b.name for b in self.repo.branches]:
                # Determine branch type based on naming convention
                branch_type = BranchType.FEATURE  # default
                if branch_name in ["main", "master"]:
                    branch_type = BranchType.MAIN
                elif "scientific" in branch_name:
                    branch_type = BranchType.SCIENTIFIC
                elif branch_name.startswith("release"):
                    branch_type = BranchType.RELEASE
                
                # Get branch object
                branch = self.repo.heads[branch_name]
                
                return Branch(
                    name=branch_name,
                    type=branch_type,
                    created_at=branch.commit.committed_datetime,
                    last_updated=branch.commit.committed_datetime
                )
        except Exception:
            # If branch doesn't exist or error occurs
            pass
        
        return None
    
    def get_branch_type(self, branch_name: str) -> BranchType:
        """
        Determine the type of a branch based on naming conventions
        
        Args:
            branch_name: Name of the branch
            
        Returns:
            BranchType for the given branch
        """
        if branch_name in ["main", "master"]:
            return BranchType.MAIN
        elif "scientific" in branch_name:
            return BranchType.SCIENTIFIC
        elif branch_name.startswith("release"):
            return BranchType.RELEASE
        else:
            return BranchType.FEATURE
    
    def checkout_branch(self, branch_name: str) -> bool:
        """
        Checkout a specific branch
        
        Args:
            branch_name: Name of the branch to checkout
            
        Returns:
            True if checkout successful, False otherwise
        """
        try:
            self.repo.git.checkout(branch_name)
            return True
        except Exception:
            return False
    
    def get_diff_between_branches(self, source_branch: str, target_branch: str) -> str:
        """
        Get the diff between two branches
        
        Args:
            source_branch: Source branch name
            target_branch: Target branch name
            
        Returns:
            String representation of the diff
        """
        try:
            source_ref = self.repo.heads[source_branch]
            target_ref = self.repo.heads[target_branch]
            
            diff = source_ref.commit.diff(target_ref.commit)
            return "\n".join([str(d) for d in diff])
        except Exception as e:
            return f"Error getting diff: {str(e)}"
    
    def get_recent_commits(self, branch_name: str, count: int = 10) -> List[Dict]:
        """
        Get recent commits for a branch
        
        Args:
            branch_name: Name of the branch
            count: Number of commits to retrieve
            
        Returns:
            List of commit information dictionaries
        """
        try:
            branch = self.repo.heads[branch_name]
            commits = list(branch.commit.traverse(max_count=count))
            
            commit_list = []
            for commit in commits:
                commit_list.append({
                    "hexsha": commit.hexsha,
                    "message": commit.message,
                    "author": commit.author.name,
                    "committed_datetime": commit.committed_datetime
                })
            
            return commit_list
        except Exception:
            return []
    
    def is_branch_up_to_date(self, branch_name: str, target_branch: str) -> bool:
        """
        Check if a branch is up to date with respect to a target branch
        
        Args:
            branch_name: Name of the branch to check
            target_branch: Name of the target branch
            
        Returns:
            True if branch is up to date, False otherwise
        """
        try:
            source_ref = self.repo.heads[branch_name]
            target_ref = self.repo.heads[target_branch]
            
            # Check if target branch is an ancestor of source branch
            return self.repo.is_ancestor(target_ref.commit, source_ref.commit)
        except Exception:
            return False
