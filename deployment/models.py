#!/usr/bin/env python3
"""
Models Manager for EmailIntelligence

This module provides functions for managing machine learning models,
including downloading, loading, and updating models.
"""

import os
import sys
import subprocess
import logging
import json
import hashlib
import requests
import zipfile
import tarfile
import shutil
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple, Union

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("models")

# Project root directory
ROOT_DIR = Path(__file__).resolve().parent.parent

class ModelsManager:
    """Manages machine learning models for EmailIntelligence."""
    
    def __init__(self, root_dir: Path = ROOT_DIR):
        """Initialize the models manager."""
        self.root_dir = root_dir
        self.models_dir = root_dir / "models"
        
        # Create the models directory if it doesn't exist
        if not self.models_dir.exists():
            self.models_dir.mkdir(parents=True)
    
    def download_model(self, url: str, model_name: str, force: bool = False) -> bool:
        """Download a model from a URL."""
        model_dir = self.models_dir / model_name
        
        # Check if the model is already downloaded
        if model_dir.exists() and not force:
            logger.info(f"Model {model_name} is already downloaded")
            return True
        
        # Create the model directory if it doesn't exist
        if not model_dir.exists():
            model_dir.mkdir(parents=True)
        
        # Download the model
        logger.info(f"Downloading model {model_name} from {url}")
        try:
            # Download the file
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            # Determine the file extension
            content_disposition = response.headers.get("Content-Disposition", "")
            if "filename=" in content_disposition:
                filename = content_disposition.split("filename=")[1].strip('"')
            else:
                filename = url.split("/")[-1]
            
            file_path = model_dir / filename
            
            # Save the file
            with open(file_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            # Extract the file if it's an archive
            if filename.endswith(".zip"):
                with zipfile.ZipFile(file_path, "r") as zip_ref:
                    zip_ref.extractall(model_dir)
                os.remove(file_path)
            elif filename.endswith((".tar.gz", ".tgz")):
                with tarfile.open(file_path, "r:gz") as tar_ref:
                    tar_ref.extractall(model_dir)
                os.remove(file_path)
            
            logger.info(f"Downloaded model {model_name}")
            return True
        except Exception as e:
            logger.error(f"Failed to download model {model_name}: {e}")
            return False
    
    def list_models(self) -> List[str]:
        """List all available models."""
        if not self.models_dir.exists():
            return []
        
        return [d.name for d in self.models_dir.iterdir() if d.is_dir()]
    
    def get_model_path(self, model_name: str) -> Optional[Path]:
        """Get the path to a model."""
        model_dir = self.models_dir / model_name
        if not model_dir.exists():
            logger.error(f"Model {model_name} not found")
            return None
        
        return model_dir
    
    def delete_model(self, model_name: str) -> bool:
        """Delete a model."""
        model_dir = self.models_dir / model_name
        if not model_dir.exists():
            logger.error(f"Model {model_name} not found")
            return False
        
        try:
            shutil.rmtree(model_dir)
            logger.info(f"Deleted model {model_name}")
            return True
        except Exception as e:
            logger.error(f"Failed to delete model {model_name}: {e}")
            return False
    
    def verify_model(self, model_name: str, expected_hash: str) -> bool:
        """Verify a model's integrity using a hash."""
        model_dir = self.models_dir / model_name
        if not model_dir.exists():
            logger.error(f"Model {model_name} not found")
            return False
        
        # Find the model file
        model_files = list(model_dir.glob("*.bin")) + list(model_dir.glob("*.pt")) + list(model_dir.glob("*.pth"))
        if not model_files:
            logger.error(f"No model files found for {model_name}")
            return False
        
        model_file = model_files[0]
        
        # Calculate the hash
        try:
            with open(model_file, "rb") as f:
                file_hash = hashlib.sha256(f.read()).hexdigest()
            
            # Compare the hash
            if file_hash == expected_hash:
                logger.info(f"Model {model_name} verified successfully")
                return True
            else:
                logger.error(f"Model {model_name} verification failed: hash mismatch")
                return False
        except Exception as e:
            logger.error(f"Failed to verify model {model_name}: {e}")
            return False
    
    def download_default_models(self) -> bool:
        """Download the default models."""
        # Define the default models
        default_models = {
            "sentiment": "https://example.com/models/sentiment.zip",
            "topic": "https://example.com/models/topic.zip",
            "intent": "https://example.com/models/intent.zip",
            "urgency": "https://example.com/models/urgency.zip"
        }
        
        # Download each model
        success = True
        for model_name, url in default_models.items():
            if not self.download_model(url, model_name):
                success = False
        
        return success

    def create_placeholder_nlp_models(self) -> bool:
        """Create empty placeholder .pkl files for default NLP models if they don't exist."""
        placeholder_dir = self.root_dir / "server" / "python_nlp"
        placeholder_model_files = [
            "sentiment_model.pkl",
            "topic_model.pkl",
            "intent_model.pkl",
            "urgency_model.pkl"
        ]
        all_created_or_exist = True

        if not placeholder_dir.exists():
            logger.info(f"Placeholder directory {placeholder_dir} does not exist. Creating it.")
            try:
                placeholder_dir.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                logger.error(f"Failed to create placeholder directory {placeholder_dir}: {e}")
                return False # Cannot proceed if directory cannot be created

        logger.info(f"Checking for placeholder NLP models in {placeholder_dir}...")
        for model_file in placeholder_model_files:
            file_path = placeholder_dir / model_file
            if not file_path.exists():
                logger.info(f"Creating placeholder model file: {file_path}")
                try:
                    file_path.touch() # Create an empty file
                except Exception as e:
                    logger.error(f"Failed to create placeholder file {file_path}: {e}")
                    all_created_or_exist = False
            else:
                logger.info(f"Placeholder model file already exists: {file_path}")

        if all_created_or_exist:
            logger.info("Placeholder NLP model file check/creation complete.")
        else:
            logger.warning("Failed to create one or more placeholder NLP model files.")
        return all_created_or_exist
    
    def create_model_config(self, model_name: str, config: Dict[str, Any]) -> bool:
        """Create a configuration file for a model."""
        model_dir = self.models_dir / model_name
        if not model_dir.exists():
            logger.error(f"Model {model_name} not found")
            return False
        
        config_file = model_dir / "config.json"
        
        try:
            with open(config_file, "w") as f:
                json.dump(config, f, indent=4)
            
            logger.info(f"Created configuration for model {model_name}")
            return True
        except Exception as e:
            logger.error(f"Failed to create configuration for model {model_name}: {e}")
            return False
    
    def get_model_config(self, model_name: str) -> Optional[Dict[str, Any]]:
        """Get the configuration for a model."""
        model_dir = self.models_dir / model_name
        if not model_dir.exists():
            logger.error(f"Model {model_name} not found")
            return None
        
        config_file = model_dir / "config.json"
        if not config_file.exists():
            logger.error(f"Configuration file not found for model {model_name}")
            return None
        
        try:
            with open(config_file, "r") as f:
                config = json.load(f)
            
            return config
        except Exception as e:
            logger.error(f"Failed to load configuration for model {model_name}: {e}")
            return None
    
    def update_model_config(self, model_name: str, config: Dict[str, Any]) -> bool:
        """Update the configuration for a model."""
        model_dir = self.models_dir / model_name
        if not model_dir.exists():
            logger.error(f"Model {model_name} not found")
            return False
        
        config_file = model_dir / "config.json"
        
        try:
            # Load the existing configuration if it exists
            if config_file.exists():
                with open(config_file, "r") as f:
                    existing_config = json.load(f)
                
                # Update the configuration
                existing_config.update(config)
                config = existing_config
            
            # Save the configuration
            with open(config_file, "w") as f:
                json.dump(config, f, indent=4)
            
            logger.info(f"Updated configuration for model {model_name}")
            return True
        except Exception as e:
            logger.error(f"Failed to update configuration for model {model_name}: {e}")
            return False

# Create a singleton instance
models_manager = ModelsManager()

if __name__ == "__main__":
    # If run directly, list all models
    models = models_manager.list_models()
    
    print(f"Found {len(models)} models:")
    for model in models:
        print(f"  {model}")
        
        # Print the model configuration if available
        config = models_manager.get_model_config(model)
        if config:
            print(f"    Configuration:")
            for key, value in config.items():
                print(f"      {key}: {value}")
        
        print()