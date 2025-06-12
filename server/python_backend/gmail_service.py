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
    """Async adapter for Gmail AI services"""
    
    def __init__(self):
        self.python_nlp_path = os.path.join(os.path.dirname(__file__), '..', 'python_nlp')
        
    async def sync_gmail_emails(
        self,
        max_emails: int = 500,
        query_filter: str = "newer_than:1d",
        include_ai_analysis: bool = True,
        strategies: List[str] = None,
        time_budget_minutes: int = 15
    ) -> Dict[str, Any]:
        """Sync Gmail emails with AI analysis"""
        try:
            cmd = [
                sys.executable,
                os.path.join(self.python_nlp_path, 'gmail_integration.py'),
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
                "success": True,
                "processedCount": result.get('emails_processed', 0),
                "emailsCreated": result.get('emails_created', 0),
                "errorsCount": result.get('errors_count', 0),
                "batchInfo": result.get('batch_info', {}),
                "statistics": result.get('statistics', {}),
                "error": result.get('error')
            }
            
        except Exception as e:
            logger.error(f"Gmail sync failed: {e}")
            return {
                "success": False,
                "processedCount": 0,
                "emailsCreated": 0,
                "errorsCount": 1,
                "error": str(e),
                "batchInfo": {},
                "statistics": {}
            }
    
    async def execute_smart_retrieval(
        self,
        strategies: List[str] = None,
        max_api_calls: int = 100,
        time_budget_minutes: int = 30
    ) -> Dict[str, Any]:
        """Execute smart Gmail retrieval"""
        try:
            cmd = [
                sys.executable,
                os.path.join(self.python_nlp_path, 'smart_retrieval.py'),
                '--execute-retrieval',
                '--max-api-calls', str(max_api_calls),
                '--time-budget', str(time_budget_minutes)
            ]
            
            if strategies:
                cmd.extend(['--strategies'] + strategies)
            
            result = await self._execute_async_command(cmd)
            
            return {
                "success": True,
                "strategiesExecuted": result.get('strategies_executed', []),
                "emailsRetrieved": result.get('emails_retrieved', 0),
                "apiCallsUsed": result.get('api_calls_used', 0),
                "performance": result.get('performance', {}),
                "error": result.get('error')
            }
            
        except Exception as e:
            logger.error(f"Smart retrieval failed: {e}")
            return {
                "success": False,
                "strategiesExecuted": [],
                "emailsRetrieved": 0,
                "apiCallsUsed": 0,
                "error": str(e)
            }
    
    async def get_retrieval_strategies(self) -> List[Dict[str, Any]]:
        """Get available retrieval strategies"""
        try:
            cmd = [
                sys.executable,
                os.path.join(self.python_nlp_path, 'smart_retrieval.py'),
                '--list-strategies'
            ]
            
            result = await self._execute_async_command(cmd)
            return result.get('strategies', [])
            
        except Exception as e:
            logger.error(f"Failed to get strategies: {e}")
            return []
    
    async def get_performance_metrics(self) -> Optional[Dict[str, Any]]:
        """Get Gmail performance metrics"""
        try:
            cmd = [
                sys.executable,
                os.path.join(self.python_nlp_path, 'retrieval_monitor.py'),
                '--get-metrics'
            ]
            
            result = await self._execute_async_command(cmd)
            return result.get('metrics')
            
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
                cwd=self.python_nlp_path
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode != 0:
                error_msg = stderr.decode() if stderr else "Unknown error"
                logger.error(f"Command failed: {error_msg}")
                return {"error": error_msg}
            
            # Parse JSON output
            try:
                return json.loads(stdout.decode())
            except json.JSONDecodeError:
                # If not JSON, return raw output
                return {"output": stdout.decode(), "stderr": stderr.decode()}
                
        except Exception as e:
            logger.error(f"Command execution failed: {e}")
            return {"error": str(e)}