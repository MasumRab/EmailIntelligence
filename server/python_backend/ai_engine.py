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
        self.nlp_service_script = os.path.join(self.python_nlp_path, 'nlp_service.py')
        
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
            
            result = await self._execute_async_command(cmd)
            
            if 'error' in result:
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
            
            result = await self._execute_async_command(cmd)
            
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
            
            result = await self._execute_async_command(cmd)
            
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
        """Fallback analysis when AI service is unavailable"""
        # Basic keyword-based analysis
        text = f"{subject} {content}".lower()
        
        # Basic sentiment
        positive_words = ['good', 'great', 'excellent', 'thank', 'please', 'welcome']
        negative_words = ['bad', 'terrible', 'problem', 'issue', 'error', 'failed']
        
        positive_count = sum(1 for word in positive_words if word in text)
        negative_count = sum(1 for word in negative_words if word in text)
        
        if positive_count > negative_count:
            sentiment = 'positive'
        elif negative_count > positive_count:
            sentiment = 'negative'
        else:
            sentiment = 'neutral'
        
        # Basic urgency
        urgent_words = ['urgent', 'asap', 'immediately', 'critical', 'emergency']
        urgency = 'high' if any(word in text for word in urgent_words) else 'low'
        
        # Basic keywords
        keywords = []
        common_keywords = ['meeting', 'project', 'report', 'deadline', 'update', 'review']
        for keyword in common_keywords:
            if keyword in text:
                keywords.append(keyword)
        
        return AIAnalysisResult({
            'topic': 'general_communication',
            'sentiment': sentiment,
            'intent': 'information_sharing',
            'urgency': urgency,
            'confidence': 0.3,  # Low confidence for fallback
            'categories': ['general'],
            'keywords': keywords,
            'reasoning': 'Fallback analysis - AI service unavailable',
            'suggested_labels': ['general'],
            'risk_flags': [],
            'category_id': None
        })
    
    async def _execute_async_command(self, cmd: List[str]) -> Dict[str, Any]:
        """Execute command asynchronously"""
        try:
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=self.python_nlp_path
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode != 0:
                error_msg = stderr.decode() if stderr else "Unknown error"
                logger.error(f"AI command failed: {error_msg}")
                return {"error": error_msg}
            
            # Parse JSON output
            try:
                return json.loads(stdout.decode())
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse AI response: {e}")
                return {"error": f"Invalid JSON response: {e}"}
                
        except Exception as e:
            logger.error(f"AI command execution failed: {e}")
            return {"error": str(e)}