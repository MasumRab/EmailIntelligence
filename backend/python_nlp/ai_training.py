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
    """
    Holds the configuration for an AI model.

    Attributes:
        model_name: The name of the model.
        model_type: The type of model (e.g., 'classification', 'ner').
        parameters: A dictionary of hyperparameters for the model.
        training_data_path: The file path to the training data.
    """
    model_name: str = "default"
    model_type: str = "classification"
    parameters: Dict[str, Any] = field(default_factory=dict)
    training_data_path: Optional[str] = None