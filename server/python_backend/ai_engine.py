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
# Removed: from .utils.async_utils import _execute_async_command
from server.python_nlp.nlp_engine import NLPEngine as FallbackNLPEngine # Renamed for clarity

logger = logging.getLogger(__name__)


# Copied and adapted from GmailAIService as a temporary solution
async def _execute_async_command_helper(cmd: List[str], cwd: Optional[str] = None, logger_instance: Optional[logging.Logger] = None) -> Dict[str, Any]:
    """
    Execute command asynchronously.
    Returns a dictionary with 'success': True/False and other command output.
    """
    current_logger = logger_instance if logger_instance else logger
    try:
        # Logging is now handled by the caller
        # current_logger.debug(f"Executing async command: {' '.join(cmd)} in {cwd or '.'}")
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=cwd
        )

        stdout, stderr = await process.communicate()
        stdout_decoded = stdout.decode().strip() if stdout else ""
        stderr_decoded = stderr.decode().strip() if stderr else ""

        if process.returncode != 0:
            error_msg = stderr_decoded or stdout_decoded or "Unknown error during command execution."
            current_logger.error(f"Async command failed (return code {process.returncode}): {cmd}. Error: {error_msg}")
            return {"success": False, "error": error_msg, "return_code": process.returncode}

        if stdout_decoded:
            try:
                parsed_output = json.loads(stdout_decoded)
                if isinstance(parsed_output, dict) and 'success' not in parsed_output:
                    parsed_output['success'] = True
                elif not isinstance(parsed_output, dict):
                     return {"success": True, "data": parsed_output}
                return parsed_output
            except json.JSONDecodeError as e:
                current_logger.warning(f"Command {cmd} output was not valid JSON, but command succeeded. Output: {stdout_decoded[:200]}...")
                return {"success": True, "output": stdout_decoded, "error": f"Non-JSON output: {str(e)}"}
        else:
            current_logger.info(f"Command {cmd} executed successfully with no stdout.")
            return {"success": True, "output": ""}

    except FileNotFoundError as e:
        current_logger.error(f"Async command failed: Executable not found for {cmd}. Error: {e}")
        return {"success": False, "error": f"Executable not found: {cmd[0]}. {str(e)}"}
    except PermissionError as e:
        current_logger.error(f"Async command failed: Permission denied for {cmd}. Error: {e}")
        return {"success": False, "error": f"Permission denied for {cmd[0]}. {str(e)}"}
    except Exception as e:
        current_logger.error(f"Generic async command execution failed for {cmd}: {e}", exc_info=True)
        return {"success": False, "error": str(e)}


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
            'category_id': self.category_id
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
        """Analyze email content with AI"""
        try:
            cmd = [
                sys.executable,
                self.nlp_service_script,
                '--analyze-email',
                '--subject', subject,
                '--content', content,
                '--output-format', 'json'
            ]
            
            # Redaction logic for logging
            redacted_cmd_for_logging = []
            skip_next = False
            for i, arg in enumerate(cmd):
                if skip_next:
                    skip_next = False
                    continue
                if arg == '--subject' or arg == '--content':
                    redacted_cmd_for_logging.append(arg)
                    if (i + 1) < len(cmd):
                        redacted_cmd_for_logging.append("<REDACTED>")
                        skip_next = True
                else:
                    redacted_cmd_for_logging.append(arg)
            logger.debug(f"Executing NLPEngine script for email analysis with command: {' '.join(redacted_cmd_for_logging)}")

            result = await _execute_async_command_helper(cmd, cwd=self.python_nlp_path, logger_instance=logger)
            
            if 'error' in result or not result.get("success"): # Check result from helper too
                # Fallback to basic analysis
                return self._get_fallback_analysis(subject, content)
            
            return AIAnalysisResult(result)
            
        except Exception as e:
            logger.error(f"AI analysis failed: {e}")
            return self._get_fallback_analysis(subject, content)
    
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
            
            # For train_models, cmd itself is not directly sensitive with subject/content.
            # The sensitive data is in training_file, which is already temp.
            logger.debug(f"Executing AI training script with command: {' '.join(cmd)}")
            result = await _execute_async_command_helper(cmd, cwd=self.python_nlp_path, logger_instance=logger)
            
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
            
            logger.debug(f"Executing AI health check script with command: {' '.join(cmd)}")
            result = await _execute_async_command_helper(cmd, cwd=self.python_nlp_path, logger_instance=logger)
            
            return {
                "status": "healthy" if result.get('status') == 'ok' else "degraded",
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
    
    def _get_fallback_analysis(self, subject: str, content: str) -> AIAnalysisResult:
        """Fallback analysis when AI service is unavailable, using NLPEngine's simple fallback."""
        
        # Use the _get_simple_fallback_analysis from the NLPEngine instance
        # This method already provides: topic, sentiment, intent (default), urgency,
        # confidence (default), categories, keywords (empty), reasoning.
        fallback_data = self.fallback_nlp_engine._get_simple_fallback_analysis(subject, content)

        # Adapt the result to AIAnalysisResult structure.
        # Most fields should align or have sensible defaults from _get_simple_fallback_analysis.
        return AIAnalysisResult({
            'topic': fallback_data.get('topic', 'general_communication'),
            'sentiment': fallback_data.get('sentiment', 'neutral'),
            'intent': fallback_data.get('intent', 'information_sharing'), # NLPEngine fallback gives 'informational'
            'urgency': fallback_data.get('urgency', 'low'),
            'confidence': fallback_data.get('confidence', 0.3), # NLPEngine fallback gives 0.6, we can override if needed
            'categories': fallback_data.get('categories', ['general']),
            'keywords': fallback_data.get('keywords', []), # NLPEngine fallback gives empty list
            'reasoning': fallback_data.get('reasoning', 'Fallback analysis - AI service unavailable'),
            'suggested_labels': fallback_data.get('suggested_labels', ['general']),
            'risk_flags': fallback_data.get('risk_flags', []),
            'category_id': None # Not provided by this simple fallback
        })