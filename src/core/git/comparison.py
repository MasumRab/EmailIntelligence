from typing import List, Tuple
from src.core.git.plumbing import GitPlumbing

class BranchComparator:
    """Advanced comparison between branches."""
    
    def __init__(self, plumbing: GitPlumbing):
        self.plumbing = plumbing

    def get_unique_commits(self, base: str, head: str) -> Tuple[List[str], List[str]]:
        """
        Return lists of unique commit OIDs for (base_only, head_only).
        """
        # Commits in base but not head
        base_only_res = self.plumbing._run(["rev-list", f"{head}..{base}"])
        base_only = base_only_res.stdout.splitlines()
        
        # Commits in head but not base
        head_only_res = self.plumbing._run(["rev-list", f"{base}..{head}"])
        head_only = head_only_res.stdout.splitlines()
        
        return base_only, head_only

    def calculate_similarity(self, base: str, head: str) -> float:
        """
        Calculate Jaccard-like similarity index based on commit history.
        Similarity = Intersection / Union
        """
        # Get merge base (common ancestor)
        merge_base_res = self.plumbing._run(["merge-base", base, head])
        if merge_base_res.returncode != 0:
            return 0.0 # No common history
            
        merge_base = merge_base_res.stdout.strip()
        
        # Count commits from base to HEADs
        count_base_res = self.plumbing._run(["rev-list", "--count", base])
        count_head_res = self.plumbing._run(["rev-list", "--count", head])
        count_common_res = self.plumbing._run(["rev-list", "--count", merge_base])
        
        count_base = int(count_base_res.stdout.strip())
        count_head = int(count_head_res.stdout.strip())
        count_common = int(count_common_res.stdout.strip())
        
        # Intersection = Common
        # Union = Base + Head - Common
        union = count_base + count_head - count_common
        
        if union == 0:
            return 1.0 # Both empty (or same initial empty state)
            
        return count_common / union
