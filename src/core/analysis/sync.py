import hashlib
from typing import List
from pathlib import Path
from src.core.utils.files import get_hash
from src.core.models.orchestration import SyncReport
from src.core.git.plumbing import GitPlumbing

class SyncService:
    """Detects divergence between local scripts and canonical source (git ref)."""
    
    def __init__(self, plumbing: GitPlumbing, canonical_ref: str = "origin/orchestration-tools"):
        self.plumbing = plumbing
        self.canonical_ref = canonical_ref

    def check_sync(self, paths: List[str]) -> SyncReport:
        diverged = []
        for p in paths:
            local_path = Path(self.plumbing.repo_root) / p
            
            # Get remote content
            try:
                remote_content = self.plumbing.cat_file(self.canonical_ref, p)
                remote_hash = hashlib.sha256(remote_content.encode('utf-8')).hexdigest()
            except Exception:
                # If remote file doesn't exist but local does, it's a divergence (or just extra local file)
                # For sync, we focus on things that SHOULD match.
                continue

            if not local_path.exists():
                diverged.append(p) # Missing locally
                continue
                
            local_hash = get_hash(local_path)
            
            if local_hash != remote_hash:
                diverged.append(p)
                
        return SyncReport(
            diverged_files=diverged,
            up_to_date=len(diverged) == 0
        )