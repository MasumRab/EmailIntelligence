"""
Configuration management module for EmailIntelligence CLI
Separated from main CLI to follow Single Responsibility Principle
"""
import json
from pathlib import Path
from typing import Dict, Any, Optional
import yaml


class ConfigurationManager:
    """Handles configuration loading, validation, and management"""
    
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.config_file = self.repo_root / ".emailintelligence" / "config.yaml"
        self.default_config = {
            'constitutional_framework': {
                'default_constitutions': [],
                'compliance_threshold': 0.8
            },
            'worktree_settings': {
                'cleanup_on_completion': True,
                'max_worktrees': 10
            },
            'analysis_settings': {
                'enable_ai_analysis': False,
                'detailed_reporting': True
            }
        }
        self.config = self._load_config()

    def _ensure_config_directory(self):
        """Ensure configuration directory exists"""
        self.config_file.parent.mkdir(parents=True, exist_ok=True)

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file or create default"""
        self._ensure_config_directory()
        
        if not self.config_file.exists():
            self._create_default_config()
            return self.default_config.copy()

        with open(self.config_file, 'r', encoding='utf-8') as f:
            if self.config_file.suffix.lower() in ['.yaml', '.yml'] and yaml:
                return yaml.safe_load(f) or self.default_config
            else:
                return json.load(f)

    def _create_default_config(self):
        """Create default configuration file"""
        self._ensure_config_directory()
        with open(self.config_file, 'w', encoding='utf-8') as f:
            if yaml:
                yaml.dump(self.default_config, f, default_flow_style=False)
            else:
                json.dump(self.default_config, f, indent=2)
                
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by dot notation key (e.g., 'constitutional_framework.compliance_threshold')"""
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
                
        return value

    def update(self, key: str, value: Any):
        """Update configuration value by dot notation key"""
        keys = key.split('.')
        config_ref = self.config
        
        for k in keys[:-1]:
            if k not in config_ref:
                config_ref[k] = {}
            config_ref = config_ref[k]
            
        config_ref[keys[-1]] = value

    def save(self):
        """Save current configuration to file"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            if self.config_file.suffix.lower() in ['.yaml', '.yml'] and yaml:
                yaml.dump(self.config, f, default_flow_style=False)
            else:
                json.dump(self.config, f, indent=2)