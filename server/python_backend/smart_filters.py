"""
Smart Filters Adapter for Python Backend
Bridges FastAPI backend with smart filter management
"""

import asyncio
import json
import logging
import sys
import os
from typing import Dict, List, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class EmailFilter:
    """Email filter wrapper"""
    
    def __init__(self, data: Dict[str, Any]):
        self.filter_id = data['filter_id']
        self.name = data['name']
        self.description = data.get('description', '')
        self.criteria = data['criteria']
        self.actions = data['actions']
        self.priority = data.get('priority', 5)
        self.effectiveness_score = data.get('effectiveness_score', 0.0)
        self.created_date = datetime.fromisoformat(data['created_date']) if isinstance(data['created_date'], str) else data['created_date']
        self.last_used = datetime.fromisoformat(data['last_used']) if isinstance(data['last_used'], str) else data['last_used']
        self.usage_count = data.get('usage_count', 0)
        self.false_positive_rate = data.get('false_positive_rate', 0.0)
        self.is_active = data.get('is_active', True)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'filter_id': self.filter_id,
            'name': self.name,
            'description': self.description,
            'criteria': self.criteria,
            'actions': self.actions,
            'priority': self.priority,
            'effectiveness_score': self.effectiveness_score,
            'created_date': self.created_date.isoformat(),
            'last_used': self.last_used.isoformat(),
            'usage_count': self.usage_count,
            'false_positive_rate': self.false_positive_rate,
            'is_active': self.is_active
        }

class SmartFilterManager:
    """Smart filter management with async support"""
    
    def __init__(self):
        self.python_nlp_path = os.path.join(os.path.dirname(__file__), '..', 'python_nlp')
        self.smart_filters_script = os.path.join(self.python_nlp_path, 'smart_filters.py')
    
    async def get_all_filters(self) -> List[EmailFilter]:
        """Get all active filters"""
        try:
            cmd = [
                sys.executable,
                self.smart_filters_script,
                '--list-filters',
                '--active-only',
                '--output-format', 'json'
            ]
            
            result = await self._execute_async_command(cmd)
            
            if 'error' in result:
                logger.error(f"Failed to get filters: {result['error']}")
                return []
            
            filters_data = result.get('filters', [])
            return [EmailFilter(filter_data) for filter_data in filters_data]
            
        except Exception as e:
            logger.error(f"Failed to get filters: {e}")
            return []
    
    async def create_filter(
        self,
        name: str,
        criteria: Dict[str, Any],
        actions: Dict[str, Any],
        priority: int = 5
    ) -> EmailFilter:
        """Create new email filter"""
        try:
            filter_data = {
                'name': name,
                'criteria': criteria,
                'actions': actions,
                'priority': priority
            }
            
            # Save filter data to temporary file
            temp_file = os.path.join(self.python_nlp_path, 'temp_filter_data.json')
            with open(temp_file, 'w') as f:
                json.dump(filter_data, f)
            
            cmd = [
                sys.executable,
                self.smart_filters_script,
                '--create-filter',
                '--filter-data', temp_file,
                '--output-format', 'json'
            ]
            
            result = await self._execute_async_command(cmd)
            
            # Cleanup temporary file
            try:
                os.remove(temp_file)
            except:
                pass
            
            if 'error' in result:
                raise Exception(result['error'])
            
            return EmailFilter(result['filter'])
            
        except Exception as e:
            logger.error(f"Failed to create filter: {e}")
            raise
    
    async def create_intelligent_filters(self, email_samples: List[Dict[str, Any]]) -> List[EmailFilter]:
        """Create intelligent filters based on email patterns"""
        try:
            # Save email samples to temporary file
            temp_file = os.path.join(self.python_nlp_path, 'temp_email_samples.json')
            with open(temp_file, 'w') as f:
                json.dump(email_samples, f)
            
            cmd = [
                sys.executable,
                self.smart_filters_script,
                '--generate-intelligent-filters',
                '--email-samples', temp_file,
                '--output-format', 'json'
            ]
            
            result = await self._execute_async_command(cmd)
            
            # Cleanup temporary file
            try:
                os.remove(temp_file)
            except:
                pass
            
            if 'error' in result:
                logger.error(f"Failed to generate intelligent filters: {result['error']}")
                return []
            
            filters_data = result.get('created_filters', [])
            return [EmailFilter(filter_data) for filter_data in filters_data]
            
        except Exception as e:
            logger.error(f"Failed to generate intelligent filters: {e}")
            return []
    
    async def prune_ineffective_filters(self) -> Dict[str, Any]:
        """Prune ineffective filters"""
        try:
            cmd = [
                sys.executable,
                self.smart_filters_script,
                '--prune-filters',
                '--output-format', 'json'
            ]
            
            result = await self._execute_async_command(cmd)
            
            if 'error' in result:
                logger.error(f"Failed to prune filters: {result['error']}")
                return {
                    "pruned_filters": [],
                    "disabled_filters": [],
                    "updated_filters": [],
                    "total_analyzed": 0,
                    "error": result['error']
                }
            
            return result.get('pruning_results', {})
            
        except Exception as e:
            logger.error(f"Failed to prune filters: {e}")
            return {
                "pruned_filters": [],
                "disabled_filters": [],
                "updated_filters": [],
                "total_analyzed": 0,
                "error": str(e)
            }
    
    async def apply_filters_to_email(self, email_data: Dict[str, Any]) -> Dict[str, Any]:
        """Apply filters to email"""
        try:
            # Save email data to temporary file
            temp_file = os.path.join(self.python_nlp_path, 'temp_email_filter.json')
            with open(temp_file, 'w') as f:
                json.dump(email_data, f)
            
            cmd = [
                sys.executable,
                self.smart_filters_script,
                '--apply-filters',
                '--email-data', temp_file,
                '--output-format', 'json'
            ]
            
            result = await self._execute_async_command(cmd)
            
            # Cleanup temporary file
            try:
                os.remove(temp_file)
            except:
                pass
            
            if 'error' in result:
                logger.error(f"Failed to apply filters: {result['error']}")
                return {}
            
            return result.get('filter_results', {})
            
        except Exception as e:
            logger.error(f"Failed to apply filters: {e}")
            return {}
    
    async def get_filter_performance(self, filter_id: str) -> Optional[Dict[str, Any]]:
        """Get filter performance metrics"""
        try:
            cmd = [
                sys.executable,
                self.smart_filters_script,
                '--get-performance',
                '--filter-id', filter_id,
                '--output-format', 'json'
            ]
            
            result = await self._execute_async_command(cmd)
            
            if 'error' in result:
                logger.error(f"Failed to get filter performance: {result['error']}")
                return None
            
            return result.get('performance')
            
        except Exception as e:
            logger.error(f"Failed to get filter performance: {e}")
            return None
    
    async def optimize_all_filters(self) -> Dict[str, Any]:
        """Optimize all filters for better performance"""
        try:
            cmd = [
                sys.executable,
                self.smart_filters_script,
                '--optimize-filters',
                '--output-format', 'json'
            ]
            
            result = await self._execute_async_command(cmd)
            
            if 'error' in result:
                logger.error(f"Failed to optimize filters: {result['error']}")
                return {
                    "success": False,
                    "optimized_count": 0,
                    "error": result['error']
                }
            
            return {
                "success": True,
                "optimized_count": result.get('optimized_count', 0),
                "optimization_results": result.get('optimization_results', [])
            }
            
        except Exception as e:
            logger.error(f"Failed to optimize filters: {e}")
            return {
                "success": False,
                "optimized_count": 0,
                "error": str(e)
            }
    
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
                logger.error(f"Filter command failed: {error_msg}")
                return {"error": error_msg}
            
            # Parse JSON output
            try:
                return json.loads(stdout.decode())
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse filter response: {e}")
                return {"error": f"Invalid JSON response: {e}"}
                
        except Exception as e:
            logger.error(f"Filter command execution failed: {e}")
            return {"error": str(e)}