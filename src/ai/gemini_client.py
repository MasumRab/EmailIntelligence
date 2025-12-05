"""
Gemini API Client for AI-powered conflict resolution.
"""
import os
import google.generativeai as genai
from typing import Optional
import structlog

from ..config.settings import settings

logger = structlog.get_logger()

class GeminiClient:
    """Client for interacting with Google's Gemini API."""
    
    def __init__(self):
        self.api_key = settings.gemini_api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            logger.warning("GEMINI_API_KEY not found. AI features will be disabled.")
            self.model = None
        else:
            try:
                genai.configure(api_key=self.api_key)
                self.model_name = settings.gemini_model or "gemini-pro"
                self.model = genai.GenerativeModel(self.model_name)
                logger.info(f"Gemini client initialized with model: {self.model_name}")
            except Exception as e:
                logger.error("Failed to initialize Gemini client", error=str(e))
                self.model = None

    async def generate_content(self, prompt: str) -> Optional[str]:
        """
        Generate content using Gemini.
        
        Args:
            prompt: The prompt to send to the model.
            
        Returns:
            The generated text response, or None if failed.
        """
        if not self.model:
            logger.error("Gemini model not initialized. Check API key.")
            return None

        try:
            # Gemini's async API
            response = await self.model.generate_content_async(prompt)
            return response.text
        except Exception as e:
            logger.error("Gemini generation failed", error=str(e))
            return None
