import yaml
import os
from typing import Dict, Any, Optional
from ..models.profile import VerificationProfile


class ConfigService:
    """
    Configuration service for loading and managing orchestration tool configurations
    """
    
    def __init__(self, config_dir: str = "config"):
        self.config_dir = config_dir
        self.verification_profiles = {}
        self._load_verification_profiles()
    
    def _load_verification_profiles(self):
        """Load verification profiles from configuration file"""
        profiles_path = os.path.join(self.config_dir, "verification_profiles.yaml")
        
        if os.path.exists(profiles_path):
            with open(profiles_path, 'r') as file:
                profiles_data = yaml.safe_load(file)
                
                for profile_name, profile_data in profiles_data.items():
                    profile = VerificationProfile(
                        name=profile_name,
                        description=profile_data.get("description", ""),
                        required_checks=profile_data.get("required_checks", []),
                        optional_checks=profile_data.get("optional_checks", []),
                        context_requirements=profile_data.get("context_requirements", []),
                        branch_specific_rules=profile_data.get("branch_specific_rules", []),
                        notification_config=profile_data.get("notification_config")
                    )
                    self.verification_profiles[profile_name] = profile
    
    def get_verification_profile(self, profile_name: str) -> Optional[VerificationProfile]:
        """
        Get a verification profile by name
        
        Args:
            profile_name: Name of the profile to retrieve
            
        Returns:
            VerificationProfile if found, None otherwise
        """
        return self.verification_profiles.get(profile_name)
    
    def get_all_profiles(self) -> Dict[str, VerificationProfile]:
        """
        Get all verification profiles
        
        Returns:
            Dictionary of all verification profiles
        """
        return self.verification_profiles
    
    def get_profile_for_branch_type(self, branch_type: str) -> Optional[VerificationProfile]:
        """
        Get the appropriate verification profile for a branch type
        
        Args:
            branch_type: Type of branch (feature, scientific, main, release)
            
        Returns:
            VerificationProfile if found, None otherwise
        """
        # Map branch types to profile names
        branch_to_profile = {
            "main": "main-branch",
            "scientific": "scientific-branch",
            "feature": "feature-branch"
        }
        
        profile_name = branch_to_profile.get(branch_type)
        if profile_name:
            return self.get_verification_profile(profile_name)
        
        return None