
"""
Gmail Service Adapter for Python Backend
Bridges Python FastAPI backend with existing Gmail NLP services
"""

import asyncio
import subprocess
import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
import os
import sys
from .utils.async_utils import _execute_async_command
# Import the NLP version of GmailAIService
from server.python_nlp.gmail_service import GmailAIService as NLPGmailAIService
from server.python_nlp.gmail_integration import RateLimitConfig # For NLPGS constructor if needed

logger = logging.getLogger(__name__)

class GmailAIService:
    """Gmail AI service for Python backend"""
    
    def __init__(self):
        self.nlp_path = os.path.join(os.path.dirname(__file__), '..', 'python_nlp')
        # self.gmail_script = os.path.join(self.nlp_path, 'gmail_integration.py') # No longer directly calling script for sync
        self.retrieval_script = os.path.join(self.nlp_path, 'smart_retrieval.py')
        
        # Instantiate the NLP Gmail Service
        # TODO: Determine if RateLimitConfig needs to be passed or if NLPGS default is fine.
        # For now, using default.
        self.nlp_gmail_service = NLPGmailAIService()

    async def sync_gmail_emails(
        self, 
        max_emails: int = 500,
        query_filter: str = "newer_than:1d",
        include_ai_analysis: bool = True,
        strategies: List[str] = None, # This parameter is not used by NLPGS.sync_gmail_emails
        time_budget_minutes: int = 15 # This parameter is not used by NLPGS.sync_gmail_emails
    ) -> Dict[str, Any]:
        """Sync emails from Gmail with AI analysis by calling NLP GmailAIService directly."""
        try:
            # Call the NLP service's sync_gmail_emails method
            # Note: NLPGS.sync_gmail_emails returns a slightly different structure.
            # We need to adapt it to match the expected output of BackendGS.sync_gmail_emails.
            nlp_result = await self.nlp_gmail_service.sync_gmail_emails(
                query_filter=query_filter,
                max_emails=max_emails,
                include_ai_analysis=include_ai_analysis
            )

            # Adapt NLP result to BackendGS expected format
            if nlp_result.get('success'):
                # emailsCreated might not be directly available; NLPGS focuses on processed_count.
                # Assuming processed_count is the closest equivalent to what emailsCreated might have implied.
                # NLPGS statistics are cumulative for the instance, BackendGS implies per-call.
                # For simplicity, we'll pass NLPGS cumulative stats.
                return {
                    "success": True,
                    "processedCount": nlp_result.get('processed_count', 0),
                    "emailsCreated": nlp_result.get('processed_count', 0), # Approximation
                    "errorsCount": 0, # NLPGS sync_gmail_emails doesn't explicitly return errors count in success case
                    "batchInfo": {
                        "batchId": nlp_result.get('batch_info', {}).get('batch_id', f'batch_{int(datetime.now().timestamp())}'),
                        "queryFilter": query_filter, # Use the input query_filter
                        "timestamp": nlp_result.get('batch_info', {}).get('timestamp', datetime.now().isoformat())
                    },
                    "statistics": nlp_result.get('statistics', {}), # Pass through NLPGS stats
                    "error": None
                }
            else:
                return {
                    "success": False,
                    "processedCount": 0,
                    "emailsCreated": 0,
                    "errorsCount": 1, # General error
                    "batchInfo": {
                        "batchId": f'error_batch_{int(datetime.now().timestamp())}',
                        "queryFilter": query_filter,
                        "timestamp": datetime.now().isoformat()
                    },
                    "statistics": nlp_result.get('statistics', {}), # Pass through any partial stats
                    "error": nlp_result.get('error', 'Unknown error from NLP service')
                }
            
        except Exception as e:
            logger.error(f"Gmail sync failed: {e}")
            return {
                "success": False,
                "processedCount": 0,
                "emailsCreated": 0,
                "errorsCount": 1,
                "batchInfo": {
                    "batchId": f'error_{int(datetime.now().timestamp())}',
                    "queryFilter": query_filter,
                    "timestamp": datetime.now().isoformat()
                },
                "statistics": {
                    "totalProcessed": 0,
                    "successfulExtractions": 0,
                    "failedExtractions": 1,
                    "aiAnalysesCompleted": 0,
                    "lastSync": datetime.now().isoformat()
                },
                "error": str(e)
            }
    
    async def execute_smart_retrieval(
        self,
        strategies: List[str] = None,
        max_api_calls: int = 100,
        time_budget_minutes: int = 30
    ) -> Dict[str, Any]:
        """Execute smart Gmail retrieval with multiple strategies"""
        try:
            cmd = [
                sys.executable,
                self.retrieval_script,
                '--execute-strategies',
                '--max-api-calls', str(max_api_calls),
                '--time-budget', str(time_budget_minutes)
            ]
            
            if strategies:
                cmd.extend(['--strategies'] + strategies)
            
            result = await _execute_async_command(cmd, cwd=self.nlp_path)
            
            return {
                "success": result.get('success', False),
                "strategiesExecuted": result.get('strategies_executed', []),
                "totalEmails": result.get('total_emails', 0),
                "performance": result.get('performance', {}),
                "error": result.get('error')
            }
            
        except Exception as e:
            logger.error(f"Smart retrieval failed: {e}")
            return {
                "success": False,
                "strategiesExecuted": [],
                "totalEmails": 0,
                "performance": {},
                "error": str(e)
            }
    
    async def get_retrieval_strategies(self) -> List[Dict[str, Any]]:
        """Get available retrieval strategies"""
        try:
            cmd = [
                sys.executable,
                self.retrieval_script,
                '--list-strategies'
            ]
            
            result = await _execute_async_command(cmd, cwd=self.nlp_path)
            return result.get('strategies', [])
            
        except Exception as e:
            logger.error(f"Failed to get strategies: {e}")
            return []
    
    async def get_performance_metrics(self) -> Optional[Dict[str, Any]]:
        """Get Gmail API performance metrics"""
        try:
            cmd = [
                sys.executable,
                self.retrieval_script,
                '--get-performance'
            ]
            
            result = await _execute_async_command(cmd, cwd=self.nlp_path)
            
            if result.get('success'):
                return {
                    "overallStatus": {
                        "status": "healthy",
                        "avgEfficiency": result.get('avg_efficiency', 0.85),
                        "activeStrategies": result.get('active_strategies', 0)
                    },
                    "quotaStatus": {
                        "dailyUsage": {
                            "percentage": result.get('quota_used_percent', 25)
                        }
                    },
                    "alerts": result.get('alerts', []),
                    "recommendations": result.get('recommendations', [])
                }
            return None
            
        except Exception as e:
            logger.error(f"Failed to get performance metrics: {e}")
            return None
