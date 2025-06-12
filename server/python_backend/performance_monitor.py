"""
Performance Monitor for Python Backend
Real-time performance tracking and optimization recommendations
"""

import asyncio
import json
import logging
import sys
import os
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import time
from collections import defaultdict, deque

logger = logging.getLogger(__name__)

class PerformanceMonitor:
    """Real-time performance monitoring with optimization recommendations"""
    
    def __init__(self):
        self.python_nlp_path = os.path.join(os.path.dirname(__file__), '..', 'python_nlp')
        self.performance_script = os.path.join(self.python_nlp_path, 'retrieval_monitor.py')
        
        # In-memory metrics storage
        self.metrics_buffer = deque(maxlen=1000)
        self.email_processing_times = deque(maxlen=100)
        self.ai_analysis_times = deque(maxlen=100)
        self.filter_performance = defaultdict(list)
        
    async def initialize(self):
        """Initialize performance monitoring"""
        try:
            logger.info("Performance Monitor initialized successfully")
        except Exception as e:
            logger.error(f"Performance Monitor initialization failed: {e}")
    
    async def get_real_time_dashboard(self) -> Dict[str, Any]:
        """Get real-time performance dashboard data"""
        try:
            # Get performance metrics from Python NLP services
            cmd = [
                sys.executable,
                self.performance_script,
                '--get-dashboard',
                '--output-format', 'json'
            ]
            
            result = await self._execute_async_command(cmd)
            
            if 'error' in result:
                # Return fallback dashboard data
                return self._get_fallback_dashboard()
            
            # Enhance with local metrics
            dashboard_data = result.get('dashboard', {})
            dashboard_data.update(self._get_local_metrics())
            
            return dashboard_data
            
        except Exception as e:
            logger.error(f"Failed to get real-time dashboard: {e}")
            return self._get_fallback_dashboard()
    
    async def get_comprehensive_metrics(self) -> Dict[str, Any]:
        """Get comprehensive performance metrics"""
        try:
            cmd = [
                sys.executable,
                self.performance_script,
                '--get-comprehensive-metrics',
                '--output-format', 'json'
            ]
            
            result = await self._execute_async_command(cmd)
            
            if 'error' in result:
                return {"error": result['error']}
            
            return result.get('metrics', {})
            
        except Exception as e:
            logger.error(f"Failed to get comprehensive metrics: {e}")
            return {"error": str(e)}
    
    async def get_active_alerts(self) -> List[Dict[str, Any]]:
        """Get active performance alerts"""
        try:
            cmd = [
                sys.executable,
                self.performance_script,
                '--get-alerts',
                '--output-format', 'json'
            ]
            
            result = await self._execute_async_command(cmd)
            
            if 'error' in result:
                return []
            
            return result.get('alerts', [])
            
        except Exception as e:
            logger.error(f"Failed to get alerts: {e}")
            return []
    
    async def get_optimization_recommendations(self) -> List[Dict[str, Any]]:
        """Get optimization recommendations"""
        try:
            cmd = [
                sys.executable,
                self.performance_script,
                '--get-recommendations',
                '--output-format', 'json'
            ]
            
            result = await self._execute_async_command(cmd)
            
            if 'error' in result:
                return []
            
            return result.get('recommendations', [])
            
        except Exception as e:
            logger.error(f"Failed to get recommendations: {e}")
            return []
    
    async def record_email_processing(
        self,
        email_id: int,
        ai_analysis: Any,
        filter_results: Dict[str, Any]
    ):
        """Record email processing performance"""
        try:
            processing_time = time.time()
            
            # Record processing metrics
            self.metrics_buffer.append({
                'type': 'email_processing',
                'email_id': email_id,
                'timestamp': processing_time,
                'ai_confidence': getattr(ai_analysis, 'confidence', 0),
                'filters_applied': len(filter_results.get('applied_filters', [])),
                'processing_duration': 0.1  # Placeholder - would be actual timing
            })
            
        except Exception as e:
            logger.error(f"Failed to record email processing: {e}")
    
    async def record_sync_performance(self, sync_result: Dict[str, Any]):
        """Record Gmail sync performance"""
        try:
            self.metrics_buffer.append({
                'type': 'gmail_sync',
                'timestamp': time.time(),
                'emails_processed': sync_result.get('processedCount', 0),
                'emails_created': sync_result.get('emailsCreated', 0),
                'errors_count': sync_result.get('errorsCount', 0),
                'success': sync_result.get('success', False)
            })
            
        except Exception as e:
            logger.error(f"Failed to record sync performance: {e}")
    
    async def record_ai_analysis(self, analysis: Any):
        """Record AI analysis performance"""
        try:
            analysis_time = time.time()
            
            self.ai_analysis_times.append({
                'timestamp': analysis_time,
                'confidence': getattr(analysis, 'confidence', 0),
                'processing_time': 0.05  # Placeholder - would be actual timing
            })
            
        except Exception as e:
            logger.error(f"Failed to record AI analysis: {e}")
    
    async def cleanup(self):
        """Cleanup performance monitor resources"""
        try:
            # Clear in-memory buffers
            self.metrics_buffer.clear()
            self.email_processing_times.clear()
            self.ai_analysis_times.clear()
            self.filter_performance.clear()
            
            logger.info("Performance Monitor cleanup completed")
        except Exception as e:
            logger.error(f"Performance Monitor cleanup failed: {e}")
    
    def _get_local_metrics(self) -> Dict[str, Any]:
        """Get local performance metrics"""
        try:
            # Calculate averages from recent data
            recent_emails = [m for m in self.metrics_buffer if m['type'] == 'email_processing']
            recent_syncs = [m for m in self.metrics_buffer if m['type'] == 'gmail_sync']
            
            avg_processing_time = 0
            if recent_emails:
                avg_processing_time = sum(m.get('processing_duration', 0) for m in recent_emails) / len(recent_emails)
            
            avg_ai_confidence = 0
            if self.ai_analysis_times:
                avg_ai_confidence = sum(a['confidence'] for a in self.ai_analysis_times) / len(self.ai_analysis_times)
            
            sync_success_rate = 1.0
            if recent_syncs:
                successful_syncs = sum(1 for s in recent_syncs if s.get('success', False))
                sync_success_rate = successful_syncs / len(recent_syncs)
            
            return {
                'local_metrics': {
                    'avg_processing_time_ms': avg_processing_time * 1000,
                    'avg_ai_confidence': avg_ai_confidence,
                    'sync_success_rate': sync_success_rate,
                    'emails_processed_today': len(recent_emails),
                    'active_filters': len(self.filter_performance),
                    'last_updated': datetime.now().isoformat()
                }
            }
            
        except Exception as e:
            logger.error(f"Failed to get local metrics: {e}")
            return {}
    
    def _get_fallback_dashboard(self) -> Dict[str, Any]:
        """Fallback dashboard when monitoring service is unavailable"""
        return {
            'status': 'monitoring_degraded',
            'timestamp': datetime.now().isoformat(),
            'overview': {
                'overall_status': 'unknown',
                'service_availability': 'degraded',
                'performance_score': 0.5,
                'alerts_count': 0,
                'recommendations_count': 0
            },
            'metrics': {
                'emails_processed': len([m for m in self.metrics_buffer if m['type'] == 'email_processing']),
                'ai_analyses_completed': len(self.ai_analysis_times),
                'average_confidence': sum(a['confidence'] for a in self.ai_analysis_times) / max(len(self.ai_analysis_times), 1),
                'uptime_percentage': 95.0  # Estimated
            },
            'local_metrics': self._get_local_metrics().get('local_metrics', {}),
            'message': 'Performance monitoring running in fallback mode'
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
                logger.error(f"Performance command failed: {error_msg}")
                return {"error": error_msg}
            
            # Parse JSON output
            try:
                return json.loads(stdout.decode())
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse performance response: {e}")
                return {"error": f"Invalid JSON response: {e}"}
                
        except Exception as e:
            logger.error(f"Performance command execution failed: {e}")
            return {"error": str(e)}