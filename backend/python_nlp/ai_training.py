"""
AI Model Training Configuration.

This module defines the data structures and configurations required for
training the various AI models used in the Email Intelligence application.
It provides a standardized way to specify model parameters and data paths.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class ModelConfig:

    model_name: str = "default"
    model_type: str = "classification"
    parameters: Dict[str, Any] = field(default_factory=dict)
    training_data_path: Optional[str] = None
