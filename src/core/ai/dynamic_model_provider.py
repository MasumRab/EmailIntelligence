"""
Dynamic model provider for Email Intelligence Platform
"""

import asyncio
import logging
import time
from typing import Any, Dict, List, Optional

from .model_provider import BaseModelProvider
from ..dynamic_model_manager import DynamicModelManager
from ..model_registry import ModelType

logger = logging.getLogger(__name__)


class DynamicModelProvider(BaseModelProvider):
    """
    Model provider that integrates with the dynamic model manager.
    
    This provider uses the advanced model management system to load and
    use AI models for analysis tasks.
    """
    
    def __init__(self, model_manager: DynamicModelManager):
        self.model_manager = model_manager
        self._initialized = False
        self._model_info = {
            "name": "Dynamic Model Provider",
            "version": "1.0.0",
            "type": "dynamic",
            "description": "Provider using dynamic model management system"
        }
        logger.info("DynamicModelProvider initialized")
    
    async def initialize(self):
        """
        Initialize the provider by ensuring the model manager is ready.
        """
        if self._initialized:
            return
            
        try:
            await self.model_manager.initialize()
            self._initialized = True
            logger.info("DynamicModelProvider fully initialized")
        except Exception as e:
            logger.error(f"Failed to initialize DynamicModelProvider: {e}")
            raise
    
    async def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """
        Analyze sentiment using the sentiment model from the model manager.
        """
        if not self._initialized:
            raise RuntimeError("Provider not initialized")
            
        start_time = time.time()
        
        try:
            # Get the best sentiment model
            sentiment_model = await self.model_manager.get_sentiment_model()
            
            if sentiment_model:
                # Perform analysis using the model
                result = await sentiment_model.model_object.analyze(text)
                
                # Standardize the result format
                standardized_result = {
                    "sentiment": result.get("label", result.get("sentiment", "neutral")),
                    "confidence": result.get("confidence", 0.5),
                    "processing_time": time.time() - start_time,
                    "method_used": "dynamic_model",
                    "model_id": sentiment_model.metadata.model_id,
                    "model_name": sentiment_model.metadata.name
                }
                
                return standardized_result
            else:
                # Fallback to rule-based analysis if no model available
                logger.warning("No sentiment model available, using rule-based fallback")
                from .rule_based_provider import RuleBasedModelProvider
                fallback = RuleBasedModelProvider()
                return await fallback.analyze_sentiment(text)
                
        except Exception as e:
            logger.error(f"Error in sentiment analysis: {e}")
            # Fallback to rule-based analysis on error
            from .rule_based_provider import RuleBasedModelProvider
            fallback = RuleBasedModelProvider()
            return await fallback.analyze_sentiment(text)
    
    async def analyze_topics(self, text: str) -> Dict[str, Any]:
        """
        Analyze topics using the topic model from the model manager.
        """
        if not self._initialized:
            raise RuntimeError("Provider not initialized")
            
        start_time = time.time()
        
        try:
            # Get the best topic model
            topic_model = await self.model_manager.get_topic_model()
            
            if topic_model:
                # Perform analysis using the model
                result = await topic_model.model_object.analyze(text)
                
                # Standardize the result format
                standardized_result = {
                    "topics": result.get("topics", ["general"]),
                    "topic_confidences": result.get("confidences", {}),
                    "processing_time": time.time() - start_time,
                    "method_used": "dynamic_model",
                    "model_id": topic_model.metadata.model_id,
                    "model_name": topic_model.metadata.name
                }
                
                return standardized_result
            else:
                # Fallback to rule-based analysis if no model available
                logger.warning("No topic model available, using rule-based fallback")
                from .rule_based_provider import RuleBasedModelProvider
                fallback = RuleBasedModelProvider()
                return await fallback.analyze_topics(text)
                
        except Exception as e:
            logger.error(f"Error in topic analysis: {e}")
            # Fallback to rule-based analysis on error
            from .rule_based_provider import RuleBasedModelProvider
            fallback = RuleBasedModelProvider()
            return await fallback.analyze_topics(text)
    
    async def analyze_intent(self, text: str) -> Dict[str, Any]:
        """
        Analyze intent using the intent model from the model manager.
        """
        if not self._initialized:
            raise RuntimeError("Provider not initialized")
            
        start_time = time.time()
        
        try:
            # Get the best intent model
            intent_model = await self.model_manager.get_intent_model()
            
            if intent_model:
                # Perform analysis using the model
                result = await intent_model.model_object.analyze(text)
                
                # Standardize the result format
                standardized_result = {
                    "intent": result.get("intent", "information"),
                    "confidence": result.get("confidence", 0.5),
                    "processing_time": time.time() - start_time,
                    "method_used": "dynamic_model",
                    "model_id": intent_model.metadata.model_id,
                    "model_name": intent_model.metadata.name
                }
                
                return standardized_result
            else:
                # Fallback to rule-based analysis if no model available
                logger.warning("No intent model available, using rule-based fallback")
                from .rule_based_provider import RuleBasedModelProvider
                fallback = RuleBasedModelProvider()
                return await fallback.analyze_intent(text)
                
        except Exception as e:
            logger.error(f"Error in intent analysis: {e}")
            # Fallback to rule-based analysis on error
            from .rule_based_provider import RuleBasedModelProvider
            fallback = RuleBasedModelProvider()
            return await fallback.analyze_intent(text)
    
    async def analyze_urgency(self, text: str) -> Dict[str, Any]:
        """
        Analyze urgency using the urgency model from the model manager.
        """
        if not self._initialized:
            raise RuntimeError("Provider not initialized")
            
        start_time = time.time()
        
        try:
            # Get the best urgency model
            urgency_model = await self.model_manager.get_urgency_model()
            
            if urgency_model:
                # Perform analysis using the model
                result = await urgency_model.model_object.analyze(text)
                
                # Standardize the result format
                standardized_result = {
                    "urgency": result.get("level", "low"),
                    "confidence": result.get("confidence", 0.5),
                    "processing_time": time.time() - start_time,
                    "method_used": "dynamic_model",
                    "model_id": urgency_model.metadata.model_id,
                    "model_name": urgency_model.metadata.name
                }
                
                return standardized_result
            else:
                # Fallback to rule-based analysis if no model available
                logger.warning("No urgency model available, using rule-based fallback")
                from .rule_based_provider import RuleBasedModelProvider
                fallback = RuleBasedModelProvider()
                return await fallback.analyze_urgency(text)
                
        except Exception as e:
            logger.error(f"Error in urgency analysis: {e}")
            # Fallback to rule-based analysis on error
            from .rule_based_provider import RuleBasedModelProvider
            fallback = RuleBasedModelProvider()
            return await fallback.analyze_urgency(text)
    
    async def health_check(self) -> Dict[str, Any]:
        """
        Perform a health check of the dynamic model provider.
        """
        start_time = time.time()
        
        try:
            # Get overall system health
            system_health = self.model_manager.get_health_status()
            
            # Get available models
            available_models = await self.model_manager.get_available_models()
            
            # Test each model type
            test_results = {}
            
            # Test sentiment model
            try:
                sentiment_result = await self.analyze_sentiment("Test message for health check")
                test_results["sentiment"] = sentiment_result["sentiment"]
            except Exception as e:
                test_results["sentiment"] = f"Error: {e}"
            
            # Test topic model
            try:
                topic_result = await self.analyze_topics("Test message for health check")
                test_results["topic"] = topic_result["topics"][0] if topic_result["topics"] else "none"
            except Exception as e:
                test_results["topic"] = f"Error: {e}"
            
            # Test intent model
            try:
                intent_result = await self.analyze_intent("Test message for health check")
                test_results["intent"] = intent_result["intent"]
            except Exception as e:
                test_results["intent"] = f"Error: {e}"
            
            # Test urgency model
            try:
                urgency_result = await self.analyze_urgency("Test message for health check")
                test_results["urgency"] = urgency_result["urgency"]
            except Exception as e:
                test_results["urgency"] = f"Error: {e}"
            
            processing_time = time.time() - start_time
            
            return {
                "status": "healthy" if system_health["status"] == "healthy" else "degraded",
                "provider_info": self._model_info,
                "system_health": system_health,
                "available_models": len(available_models),
                "test_results": test_results,
                "processing_time": processing_time,
                "timestamp": time.time()
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "provider_info": self._model_info,
                "error": str(e),
                "timestamp": time.time()
            }