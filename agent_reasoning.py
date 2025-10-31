"""
Agent reasoning module for formatting prompts with tags.

This module provides utilities for formatting reasoning prompts
with tagged prefixes for better organization and categorization.
"""


def generate_reasoning_prompt(prompt: str, tag: str) -> str:
    """
    Generate a reasoning prompt with a tagged prefix.
    
    Args:
        prompt: The main prompt text to be tagged
        tag: The tag to prefix the prompt with
        
    Returns:
        A formatted string in the format "[tag] prompt"
        
    Examples:
        >>> generate_reasoning_prompt("Analyze this code", "review")
        '[review] Analyze this code'
        
        >>> generate_reasoning_prompt("", "empty")
        '[empty] '
    """
    return f"[{tag}] {prompt}"