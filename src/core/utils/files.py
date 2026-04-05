import shutil
import hashlib
from pathlib import Path

def get_hash(path: Path) -> str:
    """Calculate SHA-256 hash of a file."""
    sha256 = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            data = f.read(65536)
            if not data:
                break
            sha256.update(data)
    return sha256.hexdigest()

def backup_and_overwrite(src: Path, dest: Path):
    """Safely overwrite a file with a backup of the original."""
    if dest.exists():
        backup_path = dest.with_suffix(dest.suffix + ".bak")
        shutil.move(dest, backup_path)
    
    # Ensure directory exists
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(src, dest)
