
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

logger = logging.getLogger(__name__)

class GmailAIService:
    """Gmail AI service for Python backend"""
    
    def __init__(self):
        self.nlp_path = os.path.join(os.path.dirname(__file__), '..', 'python_nlp')
        self.gmail_script = os.path.join(self.nlp_path, 'gmail_integration.py')
        self.retrieval_script = os.path.join(self.nlp_path, 'smart_retrieval.py')
        
    async def sync_gmail_emails(
        self, 
        max_emails: int = 500,
        query_filter: str = "newer_than:1d",
        include_ai_analysis: bool = True,
        strategies: List[str] = None,
        time_budget_minutes: int = 15
    ) -> Dict[str, Any]:
        """Sync emails from Gmail with AI analysis"""
        try:
            cmd = [
                sys.executable,
                self.gmail_script,
                '--sync-emails',
                '--max-emails', str(max_emails),
                '--query-filter', query_filter,
                '--time-budget', str(time_budget_minutes)
            ]
            
            if include_ai_analysis:
                cmd.append('--include-ai-analysis')
            
            if strategies:
                cmd.extend(['--strategies'] + strategies)
            
            result = await self._execute_async_command(cmd)
            
            return {
                "success": result.get('success', False),
                "processedCount": result.get('processed_count', 0),
                "emailsCreated": result.get('emails_created', 0),
                "errorsCount": result.get('errors_count', 0),
                "batchInfo": {
                    "batchId": result.get('batch_id', f'batch_{int(datetime.now().timestamp())}'),
                    "queryFilter": query_filter,
                    "timestamp": datetime.now().isoformat()
                },
                "statistics": {
                    "totalProcessed": result.get('total_processed', 0),
                    "successfulExtractions": result.get('successful_extractions', 0),
                    "failedExtractions": result.get('failed_extractions', 0),
                    "aiAnalysesCompleted": result.get('ai_analyses_completed', 0),
                    "lastSync": datetime.now().isoformat()
                },
                "error": result.get('error')
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
            
            result = await self._execute_async_command(cmd)
            
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
            
            result = await self._execute_async_command(cmd)
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
            
            result = await self._execute_async_command(cmd)
            
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
    
    async def _execute_async_command(self, cmd: List[str]) -> Dict[str, Any]:
        """Execute command asynchronously"""
        try:
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=self.nlp_path
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode != 0:
                error_msg = stderr.decode() if stderr else "Unknown error"
                logger.error(f"Command failed: {error_msg}")
                return {"success": False, "error": error_msg}
            
            try:
                return json.loads(stdout.decode())
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse response: {e}")
                return {"success": False, "error": f"Invalid JSON response: {e}"}
                
        except Exception as e:
            logger.error(f"Command execution failed: {e}")
            return {"success": False, "error": str(e)}
