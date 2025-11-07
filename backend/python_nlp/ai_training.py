"""
AI Model Training Configuration.

This module defines the data structures and configurations required for
training the various AI models used in the Email Intelligence application.
It provides a standardized way to specify model parameters and data paths.
It also includes the PromptEngineer class for LLM interaction capabilities.
"""

import json
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class ModelConfig:
    """Configuration for AI models used in training."""

    model_name: str = "default"
    model_type: str = "classification"
    parameters: Dict[str, Any] = field(default_factory=dict)
    training_data_path: Optional[str] = None


class PromptEngineer:
    """
    Class for engineering and managing prompts for LLM interaction.

    This class provides capabilities for generating, templating, and managing
    prompts that could be used with external LLMs if the system is enhanced
    to use them in addition to the existing local models.
    """

    def __init__(self, template: str = None):
        self.template = template
        self.templates = {}
        self.defaults = {
            "system_prompt": "You are an AI assistant specialized in email analysis and management. You help users categorize emails, identify important information, and suggest actions.",
            "email_analysis_template": "Analyze the following email:\nSubject: {subject}\nContent: {content}\n\nProvide: 1) Topic, 2) Sentiment, 3) Intent, 4) Urgency level, 5) Key action items.",
        }

    def register_template(self, name: str, template: str):
        """Register a new prompt template."""
        self.templates[name] = template

    def generate_prompt(self, template_name: str, **kwargs) -> str:
        """
        Generate a prompt using a named template and provided variables.

        Args:
            template_name: Name of the template to use
            **kwargs: Variables to substitute in the template

        Returns:
            str: The generated prompt
        """
        if template_name in self.templates:
            template = self.templates[template_name]
        elif template_name in self.defaults:
            template = self.defaults[template_name]
        else:
            raise ValueError(f"Template '{template_name}' not found")

        try:
            return template.format(**kwargs)
        except KeyError as e:
            raise ValueError(f"Missing required variable {e} for template '{template_name}'")

    def fill(self, **kwargs) -> str:
        """
        Fill the template with provided variables (backward compatibility method).
        """
        if self.template:
            return self.template.format(**kwargs)
        else:
            raise ValueError("No template provided to PromptEngineer")

    def execute(self, **kwargs) -> str:
        """
        Execute the prompt by filling template and adding execution prefix (backward compatibility method).
        """
        filled = self.fill(**kwargs)
        return f"Executing prompt: {filled}"

    def create_email_categorization_prompt(
        self, subject: str, content: str, categories: List[str]
    ) -> str:
        """
        Create a prompt for email categorization based on available categories.

        Args:
            subject: Subject of the email
            content: Content of the email
            categories: List of available category names

        Returns:
            str: A prompt for categorizing the email
        """
        categories_str = ", ".join(categories)
        prompt = (
            f"Classify the following email into one of these categories: {categories_str}.\n\n"
            f"Subject: {subject}\n"
            f"Content: {content}\n\n"
            f"Respond with only the category name that best fits this email."
        )
        return prompt

    def create_action_item_extraction_prompt(self, subject: str, content: str) -> str:
        """
        Create a prompt for extracting action items from an email.

        Args:
            subject: Subject of the email
            content: Content of the email

        Returns:
            str: A prompt for extracting action items
        """
        prompt = (
            f"Extract action items from the following email:\n\n"
            f"Subject: {subject}\n"
            f"Content: {content}\n\n"
            f"Return a JSON list of action items, where each item has 'description', 'priority' (high/medium/low), and 'due_date' (if mentioned or can be inferred)."
        )
        return prompt

    def create_summary_prompt(self, subject: str, content: str, max_length: int = 100) -> str:
        """
        Create a prompt for summarizing an email.

        Args:
            subject: Subject of the email
            content: Content of the email
            max_length: Maximum length of the summary in words

        Returns:
            str: A prompt for summarizing the email
        """
        prompt = (
            f"Summarize the following email in no more than {max_length} words:\n\n"
            f"Subject: {subject}\n\n"
            f"Content: {content}\n\n"
            f"Provide a concise summary that captures the key points and any important details."
        )
        return prompt
