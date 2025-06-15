"""
AI Engine Adapter for Python Backend
Bridges FastAPI backend with existing AI/NLP services
"""

import asyncio
import json
import logging
import sys
import os
from typing import Dict, List, Any, Optional
from datetime import datetime
# from .utils.async_utils import _execute_async_command # Commented out
from server.python_nlp.nlp_engine import NLPEngine as FallbackNLPEngine # Renamed for clarity

logger = logging.getLogger(__name__)

class AIAnalysisResult:
    """AI analysis result wrapper"""
    
    def __init__(self, data: Dict[str, Any]):
        self.topic = data.get('topic', 'unknown')
        self.sentiment = data.get('sentiment', 'neutral')
        self.intent = data.get('intent', 'unknown')
        self.urgency = data.get('urgency', 'low')
        self.confidence = data.get('confidence', 0.0)
        self.categories = data.get('categories', [])
        self.keywords = data.get('keywords', [])
        self.reasoning = data.get('reasoning', '')
        self.suggested_labels = data.get('suggested_labels', [])
        self.risk_flags = data.get('risk_flags', [])
        self.category_id = data.get('category_id')
        self.action_items = data.get('action_items', []) # Added action_items
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'topic': self.topic,
            'sentiment': self.sentiment,
            'intent': self.intent,
            'urgency': self.urgency,
            'confidence': self.confidence,
            'categories': self.categories,
            'keywords': self.keywords,
            'reasoning': self.reasoning,
            'suggested_labels': self.suggested_labels,
            'risk_flags': self.risk_flags,
            'category_id': self.category_id,
            'action_items': self.action_items # Added action_items
        }

class AdvancedAIEngine:
    """Advanced AI engine with async support"""
    
    def __init__(self):
        self.python_nlp_path = os.path.join(os.path.dirname(__file__), '..', 'python_nlp')
        self.ai_training_script = os.path.join(self.python_nlp_path, 'ai_training.py')
        self.nlp_service_script = os.path.join(self.python_nlp_path, 'nlp_engine.py')
        # Instantiate the NLP engine for fallback analysis
        self.fallback_nlp_engine = FallbackNLPEngine()
        
    async def initialize(self):
        """Initialize AI engine"""
        try:
            # Test connection to NLP services
            await self.health_check()
            logger.info("AI Engine initialized successfully")
        except Exception as e:
            logger.error(f"AI Engine initialization failed: {e}")
    
    async def analyze_email(self, subject: str, content: str) -> AIAnalysisResult:
        """Analyze email content with AI by calling the NLPEngine script."""
        logger.info(f"Initiating AI analysis for email with subject: '{subject[:50]}...'")
        try:
            cmd = [
                sys.executable,
                self.nlp_service_script,
                '--analyze-email',
                '--subject', subject,
                '--content', content,
                '--output-format', 'json'
            ]
            
            logger.debug(f"Executing NLPEngine script with command: {' '.join(cmd)}")
            # result_json_str = await _execute_async_command(cmd, cwd=self.python_nlp_path) # Commented out
            logger.warning("_execute_async_command is commented out. Using fallback for analyze_email.")
            return self._get_fallback_analysis(subject, content, "_execute_async_command not available")
            
            # This part below will be skipped due to the direct return above
            if not result_json_str: # type: ignore
                logger.error("NLPEngine script returned empty output.")
                return self._get_fallback_analysis(subject, content, "empty script output")

            try:
                result = json.loads(result_json_str)
            except json.JSONDecodeError as je:
                logger.error(f"Failed to parse JSON output from NLPEngine: {je}. Output: {result_json_str[:200]}")
                return self._get_fallback_analysis(subject, content, "invalid JSON output")

            if 'error' in result or result.get('status') == 'error': # Assuming nlp_engine might return a status field
                error_message = result.get('error', 'Unknown error from NLPEngine script')
                logger.error(f"NLPEngine script returned an error: {error_message}")
                # Fallback to basic analysis, passing the error message for context
                return self._get_fallback_analysis(subject, content, error_message)
            
            logger.info(f"Successfully received analysis from NLPEngine. Method used: {result.get('validation', {}).get('method', 'unknown')}")
            return AIAnalysisResult(result)
            
        except FileNotFoundError:
            logger.critical(f"NLPEngine script not found at {self.nlp_service_script}. Ensure the path is correct.")
            return self._get_fallback_analysis(subject, content, "NLP script not found")
        except asyncio.TimeoutError:
            logger.error("NLPEngine script execution timed out.")
            return self._get_fallback_analysis(subject, content, "script execution timeout")
        except Exception as e:
            logger.error(f"An unexpected error occurred during AI analysis: {e}", exc_info=True)
            return self._get_fallback_analysis(subject, content, str(e))
    
    async def train_models(self, training_emails: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Train AI models with email data"""
        try:
            # Save training data to temporary file
            training_file = os.path.join(self.python_nlp_path, 'temp_training_data.json')
            with open(training_file, 'w') as f:
                json.dump(training_emails, f)
            
            cmd = [
                sys.executable,
                self.ai_training_script,
                '--train-models',
                '--training-data', training_file,
                '--output-format', 'json'
            ]
            
            # result = await _execute_async_command(cmd, cwd=self.python_nlp_path) # Commented out
            logger.warning("_execute_async_command is commented out. Returning error for train_models.")
            result = {"error": "_execute_async_command not available"} # Mock result
            
            # Cleanup temporary file
            try:
                os.remove(training_file)
            except:
                pass
            
            return {
                "success": True,
                "modelsTrained": result.get('models_trained', []),
                "trainingAccuracy": result.get('training_accuracy', {}),
                "validationAccuracy": result.get('validation_accuracy', {}),
                "trainingTime": result.get('training_time', 0),
                "emailsProcessed": len(training_emails),
                "error": result.get('error')
            }
            
        except Exception as e:
            logger.error(f"Model training failed: {e}")
            return {
                "success": False,
                "modelsTrained": [],
                "trainingAccuracy": {},
                "validationAccuracy": {},
                "trainingTime": 0,
                "emailsProcessed": 0,
                "error": str(e)
            }
    
    async def health_check(self) -> Dict[str, Any]:
        """Check AI engine health"""
        try:
            cmd = [
                sys.executable,
                self.nlp_service_script,
                '--health-check',
                '--output-format', 'json'
            ]
            
            # result = await _execute_async_command(cmd, cwd=self.python_nlp_path) # Commented out
            logger.warning("_execute_async_command is commented out. Returning unhealthy for health_check.")
            result = {"status": "error", "error": "_execute_async_command not available"} # Mock result
            
            return {
                "status": "unhealthy", # Changed to unhealthy due to missing command
                "models_available": result.get('models_available', []),
                "performance": result.get('performance', {}),
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"AI health check failed: {e}")
            return {
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    async def cleanup(self):
        """Cleanup AI engine resources"""
        try:
            # Cleanup any temporary files or resources
            temp_files = [
                os.path.join(self.python_nlp_path, 'temp_training_data.json')
            ]
            for temp_file in temp_files:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
            logger.info("AI Engine cleanup completed")
        except Exception as e:
            logger.error(f"AI Engine cleanup failed: {e}")
    
    def _get_fallback_analysis(self, subject: str, content: str, error_context: Optional[str] = None) -> AIAnalysisResult:
        """
        Provides a basic fallback analysis if the primary NLPEngine script fails or returns an error.
        This uses the in-memory FallbackNLPEngine instance.
        """
        reason = "Fallback analysis due to AI service error"
        if error_context:
            reason += f": {error_context}"
        
        logger.warning(f"{reason}. Subject: {subject[:50]}...")

        try:
            # Use the _get_simple_fallback_analysis from the FallbackNLPEngine instance
            # This method provides: topic, sentiment, intent (default), urgency,
            # confidence (default), categories, keywords (empty), reasoning.
            fallback_data = self.fallback_nlp_engine._get_simple_fallback_analysis(subject, content)

            # Override reasoning if a specific error context was provided
            if error_context:
                fallback_data['reasoning'] = reason

            # Adapt the result to AIAnalysisResult structure.
            # Most fields should align or have sensible defaults from _get_simple_fallback_analysis.
            return AIAnalysisResult({
                'topic': fallback_data.get('topic', 'general_communication'),
                'sentiment': fallback_data.get('sentiment', 'neutral'),
                'intent': fallback_data.get('intent', 'informational'),
                'urgency': fallback_data.get('urgency', 'low'),
                'confidence': fallback_data.get('confidence', 0.3),
                'categories': fallback_data.get('categories', ['general']),
                'keywords': fallback_data.get('keywords', []),
                'reasoning': fallback_data.get('reasoning', 'Fallback analysis - AI service unavailable'),
                'suggested_labels': fallback_data.get('suggested_labels', ['general']),
                'risk_flags': fallback_data.get('risk_flags', ['ai_analysis_failed']),
                'category_id': None,
                'action_items': [] # Ensure action_items is in the fallback
            })
        except Exception as e:
            logger.error(f"Error generating fallback analysis itself: {e}", exc_info=True)
            # If even the fallback engine fails, return a very minimal structure
            return AIAnalysisResult({
                'topic': 'unknown',
                'sentiment': 'neutral',
                'intent': 'unknown',
                'urgency': 'low',
                'confidence': 0.1,
                'categories': ['general'],
                'keywords': [],
                'reasoning': f'Critical failure in AI analysis and fallback: {e}',
                'suggested_labels': ['general'],
                'risk_flags': ['ai_analysis_critically_failed'],
                'category_id': None,
                'action_items': [] # Ensure action_items is in the critical fallback
            })