"""Storage layer for context profile persistence."""

from pathlib import Path
from typing import List, Optional, Dict, Any
import json

from .models import ContextProfile
from .logging import get_context_logger
from .config import get_current_config


logger = get_context_logger()


class ProfileStorage:
    """Handles loading and saving of context profiles."""

    def __init__(self, config=None):
        """Initialize the profile storage.

        Args:
            config: Optional configuration override
        """
        self.config = config or get_current_config()
        self._cache: Dict[str, ContextProfile] = {}

    def load_all_profiles(self) -> List[ContextProfile]:
        """Load all available context profiles.

        Returns:
            List of ContextProfile instances
        """
        profiles_dir = self.config.profiles_dir
        profiles = []

        if not profiles_dir.exists():
            logger.warning(f"Profiles directory does not exist: {profiles_dir}")
            return profiles

        for profile_file in profiles_dir.glob("*.json"):
            try:
                profile = self.load_profile_from_file(profile_file)
                if profile:
                    profiles.append(profile)
            except Exception as e:
                logger.error(f"Failed to load profile from {profile_file}: {e}")

        logger.debug(f"Loaded {len(profiles)} context profiles")
        return profiles

    def load_profile_from_file(self, profile_file: Path) -> Optional[ContextProfile]:
        """Load a context profile from a JSON file.

        Args:
            profile_file: Path to the profile JSON file

        Returns:
            ContextProfile instance or None if loading fails
        """
        cache_key = str(profile_file)

        if cache_key in self._cache:
            return self._cache[cache_key]

        try:
            with open(profile_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            profile = ContextProfile(**data)
            self._cache[cache_key] = profile

            logger.debug(f"Loaded profile '{profile.name}' from {profile_file}")
            return profile

        except (json.JSONDecodeError, KeyError, ValueError) as e:
            logger.error(f"Invalid profile file {profile_file}: {e}")
            return None

    def save_profile_to_file(
        self, profile: ContextProfile, profile_file: Optional[Path] = None
    ) -> bool:
        """Save a context profile to a JSON file.

        Args:
            profile: The profile to save
            profile_file: Optional file path. If None, uses default location.

        Returns:
            True if saved successfully, False otherwise
        """
        if profile_file is None:
            profile_file = self.config.profiles_dir / f"{profile.id}.json"

        assert profile_file is not None, "profile_file should not be None"

        try:
            profile_file.parent.mkdir(parents=True, exist_ok=True)

            with open(profile_file, "w", encoding="utf-8") as f:
                json.dump(profile.dict(), f, indent=2, ensure_ascii=False)

            # Update cache
            self._cache[str(profile_file)] = profile

            logger.info(f"Saved profile '{profile.name}' to {profile_file}")
            return True

        except Exception as e:
            logger.error(f"Failed to save profile to {profile_file}: {e}")
            return False

    def find_profile_by_id(self, profile_id: str) -> Optional[ContextProfile]:
        """Find a profile by its ID.

        Args:
            profile_id: The profile ID to search for

        Returns:
            ContextProfile if found, None otherwise
        """
        profiles = self.load_all_profiles()
        for profile in profiles:
            if profile.id == profile_id:
                return profile
        return None

    def clear_cache(self):
        """Clear the profile cache."""
        self._cache.clear()
        logger.debug("Profile cache cleared")

    def get_cache_info(self) -> Dict[str, Any]:
        """Get information about the current cache state.

        Returns:
            Dictionary with cache statistics
        """
        return {
            "cached_profiles": len(self._cache),
            "cache_keys": list(self._cache.keys()),
        }
