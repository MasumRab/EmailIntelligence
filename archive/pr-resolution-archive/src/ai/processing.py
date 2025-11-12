"""
Background processing pipeline for AI operations
"""

import asyncio
import uuid
import json
import structlog
from typing import Dict, List, Any, Optional, Callable
from datetime import datetime, timedelta
from enum import Enum
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor

from .client import get_openai_client
from .analysis import get_conflict_analyzer
from .interfaces import AIProvider
from ..utils.caching import cache_manager

logger = structlog.get_logger()


class TaskStatus(Enum):
    """Status of background tasks"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    RETRYING = "retrying"


class TaskPriority(Enum):
    """Task priority levels"""
    LOW = 1
    NORMAL = 2
    HIGH = 3
    CRITICAL = 4


@dataclass
class AITask:
    """AI task representation"""
    id: str
    task_type: str  # 'analyze_conflict', 'generate_suggestions', 'validate_solution'
    payload: Dict[str, Any]
    status: TaskStatus
    priority: TaskPriority
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error: Optional[str] = None
    result: Optional[Dict[str, Any]] = None
    retry_count: int = 0
    max_retries: int = 3
    callback: Optional[Callable] = None


class AIProcessor:
    """
    Background AI processing pipeline
    """
    
    def __init__(self, max_workers: int = 5):
        self.max_workers = max_workers
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.task_queue: asyncio.Queue = asyncio.Queue()
        self.active_tasks: Dict[str, AITask] = {}
        self.completed_tasks: Dict[str, AITask] = {}
        self.running = False
        self.processors: Dict[str, Callable] = {}
        
        # Register default processors
        self._register_default_processors()
    
    def _register_default_processors(self):
        """Register default task processors"""
        self.processors = {
            "analyze_conflict": self._process_conflict_analysis,
            "generate_suggestions": self._process_resolution_suggestions,
            "validate_solution": self._process_solution_validation,
            "assess_complexity": self._process_complexity_assessment
        }
    
    async def start(self):
        """Start the processing pipeline"""
        if self.running:
            logger.warning("AI processor already running")
            return
        
        self.running = True
        logger.info("Starting AI processing pipeline", max_workers=self.max_workers)
        
        # Start worker tasks
        tasks = []
        for i in range(self.max_workers):
            task = asyncio.create_task(self._worker(f"worker-{i}"))
            tasks.append(task)
        
        # Start task cleanup task
        cleanup_task = asyncio.create_task(self._cleanup_completed_tasks())
        tasks.append(cleanup_task)
        
        return tasks
    
    async def stop(self):
        """Stop the processing pipeline"""
        if not self.running:
            return
        
        self.running = False
        logger.info("Stopping AI processing pipeline")
        
        # Cancel all active tasks
        for task_id, task in self.active_tasks.items():
            task.status = TaskStatus.CANCELLED
            logger.info("Cancelling active task", task_id=task_id)
        
        # Wait for tasks to complete
        await asyncio.sleep(2)
        
        # Shutdown executor
        self.executor.shutdown(wait=True)
        logger.info("AI processing pipeline stopped")
    
    async def submit_task(
        self,
        task_type: str,
        payload: Dict[str, Any],
        priority: TaskPriority = TaskPriority.NORMAL,
        callback: Optional[Callable] = None,
        max_retries: int = 3
    ) -> str:
        """
        Submit a task for processing
        """
        task_id = str(uuid.uuid4())
        task = AITask(
            id=task_id,
            task_type=task_type,
            payload=payload,
            status=TaskStatus.PENDING,
            priority=priority,
            created_at=datetime.utcnow(),
            max_retries=max_retries,
            callback=callback
        )
        
        await self.task_queue.put((priority.value, task))
        logger.info("Task submitted", task_id=task_id, task_type=task_type, priority=priority.name)
        
        return task_id
    
    async def get_task_status(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get status of a specific task"""
        # Check active tasks
        if task_id in self.active_tasks:
            task = self.active_tasks[task_id]
            return self._task_to_dict(task)
        
        # Check completed tasks
        if task_id in self.completed_tasks:
            task = self.completed_tasks[task_id]
            return self._task_to_dict(task)
        
        return None
    
    async def cancel_task(self, task_id: str) -> bool:
        """Cancel a pending task"""
        # Find task in queue
        queue_tasks = []
        found = False
        
        while not self.task_queue.empty():
            try:
                priority, task = await asyncio.wait_for(self.task_queue.get(), timeout=0.1)
                if task.id != task_id:
                    queue_tasks.append((priority, task))
                else:
                    found = True
                    task.status = TaskStatus.CANCELLED
                    logger.info("Task cancelled from queue", task_id=task_id)
            except asyncio.TimeoutError:
                break
        
        # Put back remaining tasks
        for priority, task in queue_tasks:
            await self.task_queue.put((priority, task))
        
        # Check active tasks
        if task_id in self.active_tasks:
            self.active_tasks[task_id].status = TaskStatus.CANCELLED
            found = True
            logger.info("Task cancelled from active tasks", task_id=task_id)
        
        return found
    
    async def _worker(self, worker_id: str):
        """Worker task that processes tasks from queue"""
        logger.info("AI worker started", worker_id=worker_id)
        
        while self.running:
            try:
                # Get next task with timeout
                priority, task = await asyncio.wait_for(
                    self.task_queue.get(), 
                    timeout=1.0
                )
                
                # Check if task was cancelled before processing
                if task.status == TaskStatus.CANCELLED:
                    logger.info("Skipping cancelled task", task_id=task.id)
                    continue
                
                # Process task
                await self._process_task(task, worker_id)
                
            except asyncio.TimeoutError:
                # No tasks available, continue
                continue
            except Exception as e:
                logger.error("Worker error", worker_id=worker_id, error=str(e))
                await asyncio.sleep(1)
        
        logger.info("AI worker stopped", worker_id=worker_id)
    
    async def _process_task(self, task: AITask, worker_id: str):
        """Process a single task"""
        task.status = TaskStatus.RUNNING
        task.started_at = datetime.utcnow()
        self.active_tasks[task.id] = task
        
        logger.info("Processing task",
                   task_id=task.id,
                   task_type=task.task_type,
                   worker_id=worker_id)
        
        try:
            # Get processor for task type
            processor = self.processors.get(task.task_type)
            if not processor:
                raise Exception(f"No processor found for task type: {task.task_type}")
            
            # Process task
            result = await processor(task)
            
            # Update task
            task.status = TaskStatus.COMPLETED
            task.completed_at = datetime.utcnow()
            task.result = result
            
            # Move to completed tasks
            self.completed_tasks[task.id] = task
            del self.active_tasks[task.id]
            
            # Execute callback if provided
            if task.callback:
                try:
                    await task.callback(task)
                except Exception as e:
                    logger.error("Task callback failed", task_id=task.id, error=str(e))
            
            logger.info("Task completed successfully",
                       task_id=task.id,
                       processing_time=(task.completed_at - task.started_at).total_seconds())
            
        except Exception as e:
            error_msg = str(e)
            task.error = error_msg
            
            # Check if we should retry
            if task.retry_count < task.max_retries:
                task.retry_count += 1
                task.status = TaskStatus.RETRYING
                
                # Exponential backoff
                delay = 2 ** task.retry_count
                logger.warning("Task failed, retrying",
                             task_id=task.id,
                             retry_count=task.retry_count,
                             delay=delay,
                             error=error_msg)
                
                # Re-queue with delay
                await asyncio.sleep(delay)
                task.status = TaskStatus.PENDING
                await self.task_queue.put((task.priority.value, task))
            else:
                task.status = TaskStatus.FAILED
                task.completed_at = datetime.utcnow()
                self.completed_tasks[task.id] = task
                del self.active_tasks[task.id]
                
                logger.error("Task failed after all retries",
                           task_id=task.id,
                           retry_count=task.retry_count,
                           error=error_msg)
    
    async def _process_conflict_analysis(self, task: AITask) -> Dict[str, Any]:
        """Process conflict analysis task"""
        pr_data = task.payload.get("pr_data")
        conflict_data = task.payload.get("conflict_data")
        
        analyzer = await get_conflict_analyzer()
        return await analyzer.analyze_conflict(pr_data, conflict_data)
    
    async def _process_resolution_suggestions(self, task: AITask) -> Dict[str, Any]:
        """Process resolution suggestions task"""
        analysis = task.payload.get("analysis")
        
        analyzer = await get_conflict_analyzer()
        suggestions = await analyzer.generate_resolution_suggestions(analysis)
        
        return {
            "suggestions": suggestions,
            "analysis_id": analysis.get("id"),
            "generated_at": datetime.utcnow().isoformat()
        }
    
    async def _process_solution_validation(self, task: AITask) -> Dict[str, Any]:
        """Process solution validation task"""
        solution = task.payload.get("solution")
        context = task.payload.get("context")
        
        analyzer = await get_conflict_analyzer()
        return await analyzer.validate_solution(solution, context)
    
    async def _process_complexity_assessment(self, task: AITask) -> Dict[str, Any]:
        """Process complexity assessment task"""
        pr_data = task.payload.get("pr_data")
        
        analyzer = await get_conflict_analyzer()
        complexity = await analyzer.assess_complexity(pr_data)
        
        return {
            "complexity_score": complexity,
            "pr_id": pr_data.get("id"),
            "assessed_at": datetime.utcnow().isoformat()
        }
    
    async def _cleanup_completed_tasks(self):
        """Cleanup old completed tasks"""
        while self.running:
            try:
                # Remove tasks older than 24 hours
                cutoff_time = datetime.utcnow() - timedelta(hours=24)
                
                tasks_to_remove = []
                for task_id, task in self.completed_tasks.items():
                    if task.completed_at and task.completed_at < cutoff_time:
                        tasks_to_remove.append(task_id)
                
                for task_id in tasks_to_remove:
                    del self.completed_tasks[task_id]
                    logger.debug("Cleaned up old task", task_id=task_id)
                
                # Sleep for 1 hour
                await asyncio.sleep(3600)
                
            except Exception as e:
                logger.error("Task cleanup error", error=str(e))
                await asyncio.sleep(300)  # Retry after 5 minutes
    
    def _task_to_dict(self, task: AITask) -> Dict[str, Any]:
        """Convert task to dictionary"""
        return {
            "id": task.id,
            "task_type": task.task_type,
            "status": task.status.value,
            "priority": task.priority.name,
            "created_at": task.created_at.isoformat(),
            "started_at": task.started_at.isoformat() if task.started_at else None,
            "completed_at": task.completed_at.isoformat() if task.completed_at else None,
            "error": task.error,
            "result": task.result,
            "retry_count": task.retry_count,
            "max_retries": task.max_retries
        }
    
    def get_stats(self) -> Dict[str, Any]:
        """Get processor statistics"""
        active_count = len(self.active_tasks)
        completed_count = len(self.completed_tasks)
        
        # Count by status
        status_counts = {}
        for task in self.completed_tasks.values():
            status = task.status.value
            status_counts[status] = status_counts.get(status, 0) + 1
        
        # Calculate success rate
        total_completed = sum(status_counts.values())
        successful = status_counts.get("completed", 0)
        success_rate = successful / total_completed if total_completed > 0 else 0
        
        return {
            "running": self.running,
            "active_tasks": active_count,
            "completed_tasks": completed_count,
            "status_breakdown": status_counts,
            "success_rate": success_rate,
            "queue_size": self.task_queue.qsize(),
            "max_workers": self.max_workers
        }


# Global AI processor instance
ai_processor = AIProcessor()


async def get_ai_processor() -> AIProcessor:
    """Get initialized AI processor"""
    if not ai_processor.running:
        await ai_processor.start()
    return ai_processor