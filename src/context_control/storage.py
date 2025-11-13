"""Storage layer for context profile persistence following SOLID principles."""

import json
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, List, Optional

from .config import get_current_config
from .exceptions import StorageError
from .logging import get_context_logger
from .models import ContextProfile

logger = get_context_logger(__name__)


class IProfileStorage(ABC):
    """Interface for profile storage operations."""
    
    @abstractmethod
    def save_profile(self, profile: ContextProfile) -> bool:
        """Save a context profile."""
        pass
    
    @abstractmethod
    def load_profile(self, profile_id: str) -> Optional[ContextProfile]:
        """Load a context profile by ID."""
        pass
    
    @abstractmethod
    def load_all_profiles(self) -> List[ContextProfile]:
        """Load all available context profiles."""
        pass
    
    @abstractmethod
    def delete_profile(self, profile_id: str) -> bool:
        """Delete a context profile."""
        pass
    
    @abstractmethod
    def clear_cache(self) -> None:
        """Clear cached profiles."""
        pass


class ProfileStorage(IProfileStorage):
    """Manages storage and retrieval of context profiles following SOLID principles."""
    
    def __init__(self, config=None):
        """Initialize the profile storage.

        Args:
            config: Configuration instance
        """
        self.config = config or get_current_config()
        self._profiles_cache: Dict[str, ContextProfile] = {}
        self._ensure_directories()
    
    def _ensure_directories(self):
        """Ensure required directories exist."""
        try:
            self.config.config_dir.mkdir(parents=True, exist_ok=True)
            self.config.profiles_dir.mkdir(parents=True, exist_ok=True)
        except (IOError, OSError) as e:
            raise StorageError(f"Could not create directories: {e}", "init")
    
    def _get_profile_file_path(self, profile_id: str) -> Path:
        """Get the file path for a profile.

        Args:
            profile_id: Profile identifier

        Returns:
            Path to the profile file
        """
        return self.config.profiles_dir / f"{profile_id}.json"
    
    def _serialize_profile(self, profile: ContextProfile) -> Dict[str, Any]:
        """Serialize a profile to dictionary format.

        Args:
            profile: Profile to serialize

        Returns:
            Serialized profile data
        """
        profile_data = profile.dict()
        # Convert datetime objects to ISO format
        for key in ["created_at", "updated_at"]:
            if key in profile_data and profile_data[key]:
                profile_data[key] = profile_data[key].isoformat()
        return profile_data
    
    def _deserialize_profile(self, data: Dict[str, Any]) -> ContextProfile:
        """Deserialize profile data to ContextProfile instance.

        Args:
            data: Serialized profile data

        Returns:
            ContextProfile instance
        """
        # Convert ISO strings back to datetime objects
        for key in ["created_at", "updated_at"]:
            if key in data and data[key]:
                from datetime import datetime
                data[key] = datetime.fromisoformat(data[key])
        
        return ContextProfile(**data)
    
    def save_profile(self, profile: ContextProfile) -> bool:
        """Save a context profile.

        Args:
            profile: Profile to save

        Returns:
            True if successful, False otherwise
        """
        try:
            file_path = self._get_profile_file_path(profile.id)
            profile_data = self._serialize_profile(profile)
            
            # Save to file
            with open(file_path, "w") as f:
                json.dump(profile_data, f, indent=2)
            
            # Update cache
            self._profiles_cache[profile.id] = profile
            
            logger.info(f"Saved profile: {profile.id}")
            return True
            
        except (IOError, OSError) as e:
            logger.error(f"Failed to save profile {profile.id}: {e}")
            return False
    
    def load_profile(self, profile_id: str) -> Optional[ContextProfile]:
        """Load a context profile by ID.

        Args:
            profile_id: Profile identifier

        Returns:
            ContextProfile instance or None if not found
        """
        # Check cache first
        if profile_id in self._profiles_cache:
            return self._profiles_cache[profile_id]
        
        file_path = self._get_profile_file_path(profile_id)
        if not file_path.exists():
            return None
        
        try:
            with open(file_path, "r") as f:
                data = json.load(f)
            
            # Deserialize and cache
            profile = self._deserialize_profile(data)
            self._profiles_cache[profile_id] = profile
            
            logger.debug(f"Loaded profile: {profile_id}")
            return profile
            
        except (json.JSONDecodeError, IOError, OSError) as e:
            logger.error(f"Failed to load profile {profile_id}: {e}")
            return None
    
    def load_all_profiles(self) -> List[ContextProfile]:
        """Load all available context profiles.

        Returns:
            List of all ContextProfile instances
        """
        profiles = []
        
        if not self.config.profiles_dir.exists():
            return profiles
        
        try:
            for file_path in self.config.profiles_dir.glob("*.json"):
                profile_id = file_path.stem
                profile = self.load_profile(profile_id)
                if profile:
                    profiles.append(profile)
        
        except Exception as e:
            logger.error(f"Failed to load all profiles: {e}")
        
        return profiles
    
    def delete_profile(self, profile_id: str) -> bool:
        """Delete a context profile.

        Args:
            profile_id: Profile identifier

        Returns:
            True if successful, False otherwise
        """
        file_path = self._get_profile_file_path(profile_id)
        
        try:
            if file_path.exists():
                file_path.unlink()
            
            # Remove from cache
            if profile_id in self._profiles_cache:
                del self._profiles_cache[profile_id]
            
            logger.info(f"Deleted profile: {profile_id}")
            return True
            
        except (IOError, OSError) as e:
            logger.error(f"Failed to delete profile {profile_id}: {e}")
            return False
    
    def clear_cache(self):
        """Clear all cached profiles."""
        self._profiles_cache.clear()
        logger.debug("Cleared profile cache")


class IProfileManager(ABC):
    """Interface for high-level profile management."""
    
    @abstractmethod
    def create_default_profiles(self) -> bool:
        """Create default context profiles."""
        pass
    
    @abstractmethod
    def get_profile_statistics(self) -> Dict[str, Any]:
        """Get statistics about stored profiles."""
        pass


class ProfileManager(IProfileManager):
    """High-level manager for profile operations following SOLID principles."""
    
    def __init__(self, storage: IProfileStorage, config=None):
        """Initialize the profile manager.

        Args:
            storage: Profile storage instance
            config: Configuration instance
        """
        self.storage = storage
        self.config = config or get_current_config()
    
    def create_default_profiles(self) -> bool:
        """Create default context profiles.

        Returns:
            True if successful, False otherwise
        """
        # Development profile
        dev_profile = ContextProfile(
            id="development",
            name="Development",
            description="Development environment profile",
            branch_patterns=["develop", "dev", "feature/*", "bugfix/*"],
            allowed_files=[
                "src/**/*",
                "tests/**/*",
                "docs/**/*",
                "*.md",
                "*.json",
                "*.yml",
                "*.yaml"
            ],
            blocked_files=[
                "**/node_modules/**",
                "**/.git/**",
                "**/venv/**",
                "**/env/**",
                "**/.env*",
                "**/build/**",
                "**/dist/**"
            ]
        )
        
        # Staging profile
        staging_profile = ContextProfile(
            id="staging",
            name="Staging",
            description="Staging environment profile",
            branch_patterns=["staging", "stage", "release/*"],
            allowed_files=[
                "src/**/*",
                "docs/**/*",
                "*.md",
                "*.json",
                "*.yml",
                "*.yaml"
            ],
            blocked_files=[
                "**/tests/**",
                "**/test/**",
                "**/node_modules/**",
                "**/.git/**",
                "**/venv/**",
                "**/env/**",
                "**/.env*",
                "**/build/**",
                "**/dist/**"
            ]
        )
        
        # Production profile
        prod_profile = ContextProfile(
            id="production",
            name="Production",
            description="Production environment profile",
            branch_patterns=["main", "master"],
            allowed_files=[
                "src/**/*",
                "docs/**/*",
                "*.md",
                "*.json",
                "*.yml",
                "*.yaml"
            ],
            blocked_files=[
                "**/tests/**",
                "**/test/**",
                "**/node_modules/**",
                "**/.git/**",
                "**/venv/**",
                "**/env/**",
                "**/.env*",
                "**/build/**",
                "**/dist/**",
                "**/dev/**"
            ]
        )
        
        # Save profiles
        success = True
        for profile in [dev_profile, staging_profile, prod_profile]:
            if not self.storage.save_profile(profile):
                success = False
        
        if success:
            logger.info("Created default context profiles")
        
        return success
    
    def get_profile_statistics(self) -> Dict[str, Any]:
        """Get statistics about stored profiles.

        Returns:
            Dictionary with profile statistics
        """
        profiles = self.storage.load_all_profiles()
        
        stats = {
            "total_profiles": len(profiles),
            "profiles_by_type": {},
            "branch_patterns": {},
            "file_patterns": {
                "allowed_files": set(),
                "blocked_files": set()
            }
        }
        
        for profile in profiles:
            # Count by type
            profile_type = "custom"
            if profile.branch_patterns:
                if any("feature" in p for p in profile.branch_patterns):
                    profile_type = "feature"
                elif any("develop" in p for p in profile.branch_patterns):
                    profile_type = "development"
                elif any("release" in p for p in profile.branch_patterns):
                    profile_type = "release"
                elif any("main" in p for p in profile.branch_patterns):
                    profile_type = "production"
            
            stats["profiles_by_type"][profile_type] = stats["profiles_by_type"].get(profile_type, 0) + 1
            
            # Count branch patterns
            for pattern in profile.branch_patterns:
                stats["branch_patterns"][pattern] = stats["branch_patterns"].get(pattern, 0) + 1
            
            # Collect file patterns
            stats["file_patterns"]["allowed_files"].update(profile.allowed_files)
            stats["file_patterns"]["blocked_files"].update(profile.blocked_files)
        
        # Convert sets to lists
        stats["file_patterns"]["allowed_files"] = list(stats["file_patterns"]["allowed_files"])
        stats["file_patterns"]["blocked_files"] = list(stats["file_patterns"]["blocked_files"])
        
        return stats


# Legacy class for backward compatibility
class ProfileStorageLegacy(ProfileStorage):
    """Legacy profile storage for backward compatibility."""
    pass
