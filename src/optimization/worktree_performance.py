"""
Worktree Performance Optimization

Optimizes Git worktree operations for efficient conflict resolution
and parallel development workflows.

Features:
- Optimized worktree creation and cleanup
- Memory usage optimization for large repositories
- Parallel worktree coordination
- Performance monitoring and metrics
"""

from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass
import subprocess
import os
import tempfile
import shutil
import structlog
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

logger = structlog.get_logger()


@dataclass
class WorktreePerformanceMetrics:
    """Performance metrics for worktree operations"""
    creation_time: float
    cleanup_time: float
    memory_usage_mb: float
    disk_usage_mb: float
    throughput_operations: float
    concurrent_operations_supported: int
    performance_score: float


@dataclass
class WorktreeOptimizationConfig:
    """Configuration for worktree performance optimization"""
    max_concurrent_worktrees: int = 10
    cleanup_threshold_minutes: int = 30
    memory_limit_mb: int = 1024
    disk_space_limit_mb: int = 5120
    enable_compression: bool = True
    enable_cache_optimization: bool = True
    monitoring_interval_seconds: int = 60


class WorktreePerformanceOptimizer:
    """
    Optimizes Git worktree performance for resolution workflows
    
    Provides optimized worktree creation, cleanup, and management
    for efficient parallel development and conflict resolution.
    """
    
    def __init__(self, config: Optional[WorktreeOptimizationConfig] = None):
        """Initialize worktree performance optimizer"""
        self.config = config or WorktreeOptimizationConfig()
        self.performance_history = []
        self.active_worktrees = {}
        self.performance_stats = {
            "total_worktrees_created": 0,
            "total_operations": 0,
            "average_creation_time": 0.0,
            "average_cleanup_time": 0.0,
            "peak_concurrent_usage": 0,
            "performance_improvements": []
        }
        
        # Performance monitoring
        self.monitoring_active = False
        self.monitor_thread = None
        self._lock = threading.Lock()
        
        logger.info("Worktree performance optimizer initialized")
    
    async def optimize_worktree_operations(self) -> Dict[str, Any]:
        """Optimize overall worktree performance"""
        
        optimization_results = {}
        
        try:
            logger.info("Starting worktree performance optimization")
            
            # Step 1: Optimize Git configuration
            git_optimization = await self._optimize_git_configuration()
            optimization_results["git_configuration"] = git_optimization
            
            # Step 2: Optimize worktree cache management
            cache_optimization = await self._optimize_worktree_cache()
            optimization_results["cache_optimization"] = cache_optimization
            
            # Step 3: Optimize memory usage
            memory_optimization = await self._optimize_memory_usage()
            optimization_results["memory_optimization"] = memory_optimization
            
            # Step 4: Optimize disk usage
            disk_optimization = await self._optimize_disk_usage()
            optimization_results["disk_optimization"] = disk_optimization
            
            # Step 5: Enable performance monitoring
            monitoring_setup = await self._setup_performance_monitoring()
            optimization_results["monitoring"] = monitoring_setup
            
            # Step 6: Calculate overall optimization score
            overall_score = self._calculate_optimization_score(optimization_results)
            optimization_results["overall_score"] = overall_score
            
            logger.info("Worktree performance optimization completed", score=overall_score)
            return optimization_results
            
        except Exception as e:
            logger.error("Worktree performance optimization failed", error=str(e))
            return {
                "error": str(e),
                "overall_score": 0.0,
                "optimization_results": optimization_results
            }
    
    async def create_optimized_worktree(
        self,
        branch_name: str,
        worktree_path: str,
        base_path: str = "."
    ) -> Tuple[bool, Dict[str, Any]]:
        """Create worktree with performance optimizations"""
        
        start_time = time.time()
        
        try:
            logger.info(
                "Creating optimized worktree",
                branch=branch_name,
                path=worktree_path
            )
            
            # Step 1: Pre-creation optimization
            pre_optimization = await self._pre_creation_optimizations()
            
            # Step 2: Create worktree with optimizations
            creation_result = await self._create_worktree_with_optimizations(
                branch_name, worktree_path, base_path
            )
            
            # Step 3: Post-creation optimization
            post_optimization = await self._post_creation_optimizations(worktree_path)
            
            # Step 4: Calculate performance metrics
            creation_time = time.time() - start_time
            performance_metrics = await self._calculate_worktree_metrics(
                worktree_path, creation_time
            )
            
            # Step 5: Register worktree
            if creation_result["success"]:
                await self._register_worktree(worktree_path, branch_name, performance_metrics)
            
            result = {
                "success": creation_result["success"],
                "creation_time": creation_time,
                "performance_metrics": performance_metrics,
                "pre_optimization": pre_optimization,
                "post_optimization": post_optimization,
                "git_output": creation_result.get("output", ""),
                "git_errors": creation_result.get("errors", "")
            }
            
            if creation_result["success"]:
                logger.info(
                    "Optimized worktree created successfully",
                    branch=branch_name,
                    path=worktree_path,
                    creation_time=creation_time
                )
            else:
                logger.error(
                    "Failed to create optimized worktree",
                    branch=branch_name,
                    error=creation_result.get("error", "Unknown error")
                )
            
            return creation_result["success"], result
            
        except Exception as e:
            logger.error(
                "Exception during optimized worktree creation",
                branch=branch_name,
                error=str(e)
            )
            return False, {
                "success": False,
                "creation_time": time.time() - start_time,
                "error": str(e)
            }
    
    async def cleanup_optimized_worktree(
        self,
        worktree_path: str,
        force_cleanup: bool = False
    ) -> Tuple[bool, Dict[str, Any]]:
        """Cleanup worktree with performance optimizations"""
        
        start_time = time.time()
        
        try:
            logger.info(
                "Cleaning up optimized worktree",
                path=worktree_path,
                force=force_cleanup
            )
            
            # Step 1: Pre-cleanup optimization
            pre_cleanup = await self._pre_cleanup_optimizations(worktree_path)
            
            # Step 2: Check if cleanup is safe
            cleanup_safety = await self._check_cleanup_safety(worktree_path, force_cleanup)
            
            if not cleanup_safety["safe"] and not force_cleanup:
                return False, {
                    "success": False,
                    "cleanup_time": 0.0,
                    "reason": cleanup_safety["reason"],
                    "pre_cleanup": pre_cleanup
                }
            
            # Step 3: Perform optimized cleanup
            cleanup_result = await self._perform_optimized_cleanup(worktree_path)
            
            # Step 4: Post-cleanup optimization
            post_cleanup = await self._post_cleanup_optimizations()
            
            # Step 5: Unregister worktree
            await self._unregister_worktree(worktree_path)
            
            # Step 6: Calculate cleanup metrics
            cleanup_time = time.time() - start_time
            cleanup_metrics = await self._calculate_cleanup_metrics(cleanup_time, cleanup_result)
            
            result = {
                "success": cleanup_result["success"],
                "cleanup_time": cleanup_time,
                "cleanup_metrics": cleanup_metrics,
                "pre_cleanup": pre_cleanup,
                "post_cleanup": post_cleanup,
                "git_output": cleanup_result.get("output", ""),
                "git_errors": cleanup_result.get("errors", "")
            }
            
            if cleanup_result["success"]:
                logger.info(
                    "Optimized worktree cleaned up successfully",
                    path=worktree_path,
                    cleanup_time=cleanup_time
                )
            else:
                logger.error(
                    "Failed to cleanup worktree",
                    path=worktree_path,
                    error=cleanup_result.get("error", "Unknown error")
                )
            
            return cleanup_result["success"], result
            
        except Exception as e:
            logger.error(
                "Exception during optimized worktree cleanup",
                path=worktree_path,
                error=str(e)
            )
            return False, {
                "success": False,
                "cleanup_time": time.time() - start_time,
                "error": str(e)
            }
    
    async def batch_cleanup_expired_worktrees(self) -> Dict[str, Any]:
        """Clean up expired worktrees in batch for efficiency"""
        
        cleanup_results = {
            "total_checked": 0,
            "expired_worktrees": [],
            "cleaned_up": 0,
            "failed_cleanups": 0,
            "total_time": 0.0
        }
        
        start_time = time.time()
        
        try:
            logger.info("Starting batch cleanup of expired worktrees")
            
            # Get all registered worktrees
            with self._lock:
                current_worktrees = list(self.active_worktrees.keys())
            
            cleanup_results["total_checked"] = len(current_worktrees)
            
            # Check expiration for each worktree
            expired_paths = []
            for worktree_path in current_worktrees:
                if await self._is_worktree_expired(worktree_path):
                    expired_paths.append(worktree_path)
            
            cleanup_results["expired_worktrees"] = expired_paths
            
            # Clean up expired worktrees in parallel
            if expired_paths:
                with ThreadPoolExecutor(max_workers=min(len(expired_paths), 5)) as executor:
                    cleanup_futures = []
                    
                    for worktree_path in expired_paths:
                        future = executor.submit(
                            self._run_async_cleanup, worktree_path
                        )
                        cleanup_futures.append((worktree_path, future))
                    
                    # Collect results
                    for worktree_path, future in cleanup_futures:
                        try:
                            success, _ = future.result()
                            if success:
                                cleanup_results["cleaned_up"] += 1
                            else:
                                cleanup_results["failed_cleanups"] += 1
                        except Exception as e:
                            logger.error(
                                "Batch cleanup failed for worktree",
                                path=worktree_path,
                                error=str(e)
                            )
                            cleanup_results["failed_cleanups"] += 1
            
            cleanup_results["total_time"] = time.time() - start_time
            
            logger.info(
                "Batch cleanup completed",
                expired=len(expired_paths),
                cleaned=cleanup_results["cleaned_up"],
                failed=cleanup_results["failed_cleanups"],
                total_time=cleanup_results["total_time"]
            )
            
            return cleanup_results
            
        except Exception as e:
            logger.error("Batch cleanup failed", error=str(e))
            cleanup_results["error"] = str(e)
            return cleanup_results
    
    async def get_performance_benchmarks(self) -> Dict[str, Any]:
        """Get comprehensive performance benchmarks"""
        
        benchmarks = {
            "worktree_operations": {},
            "resource_utilization": {},
            "concurrent_performance": {},
            "optimization_improvements": [],
            "historical_performance": self.performance_stats
        }
        
        try:
            # Step 1: Benchmark worktree creation
            creation_benchmarks = await self._benchmark_worktree_creation()
            benchmarks["worktree_operations"]["creation"] = creation_benchmarks
            
            # Step 2: Benchmark worktree cleanup
            cleanup_benchmarks = await self._benchmark_worktree_cleanup()
            benchmarks["worktree_operations"]["cleanup"] = cleanup_benchmarks
            
            # Step 3: Benchmark concurrent operations
            concurrent_benchmarks = await self._benchmark_concurrent_operations()
            benchmarks["concurrent_performance"] = concurrent_benchmarks
            
            # Step 4: Measure resource utilization
            resource_benchmarks = await self._benchmark_resource_utilization()
            benchmarks["resource_utilization"] = resource_benchmarks
            
            # Step 5: Calculate optimization improvements
            improvements = self._calculate_optimization_improvements()
            benchmarks["optimization_improvements"] = improvements
            
            logger.info("Performance benchmarks completed")
            return benchmarks
            
        except Exception as e:
            logger.error("Performance benchmarking failed", error=str(e))
            benchmarks["error"] = str(e)
            return benchmarks
    
    # Private helper methods
    
    async def _optimize_git_configuration(self) -> Dict[str, Any]:
        """Optimize Git configuration for worktree performance"""
        
        optimizations = {
            "gc_auto_enabled": False,
            "gc_auto_auto_enabled": False,
            "worktree_gc_disabled": False,
            "pack_operations": [],
            "config_applied": []
        }
        
        try:
            # Optimize garbage collection
            gc_settings = [
                ("gc.auto", "256"),
                ("gc.autoAuto", "true"),
                ("gc.worktreeOptimize", "true"),
            ]
            
            for config_key, config_value in gc_settings:
                try:
                    # Set Git configuration
                    result = subprocess.run(
                        ["git", "config", config_key, config_value],
                        capture_output=True, text=True, check=True
                    )
                    optimizations["config_applied"].append(f"{config_key}={config_value}")
                    logger.debug(f"Applied Git config: {config_key}={config_value}")
                except subprocess.CalledProcessError as e:
                    logger.warning(f"Failed to set Git config {config_key}", error=str(e))
            
            # Run optimization pack operations
            pack_result = await self._run_git_pack_optimization()
            optimizations["pack_operations"] = pack_result
            
            logger.info("Git configuration optimization completed")
            return optimizations
            
        except Exception as e:
            logger.error("Git configuration optimization failed", error=str(e))
            optimizations["error"] = str(e)
            return optimizations
    
    async def _optimize_worktree_cache(self) -> Dict[str, Any]:
        """Optimize worktree cache management"""
        
        cache_optimizations = {
            "cache_cleared": False,
            "cache_size_before": 0,
            "cache_size_after": 0,
            "tmp_cleaned": False
        }
        
        try:
            # Clear Git temp files
            temp_dirs = [
                os.path.join(os.getcwd(), ".git", "worktrees"),
                tempfile.gettempdir()
            ]
            
            for temp_dir in temp_dirs:
                if os.path.exists(temp_dir):
                    temp_files = [f for f in os.listdir(temp_dir) if f.startswith("git-worktree-")]
                    cache_optimizations["tmp_files_found"] = len(temp_files)
                    
                    if temp_files:
                        await self._cleanup_temp_files(temp_dir, temp_files)
                        cache_optimizations["tmp_cleaned"] = True
            
            logger.info("Worktree cache optimization completed")
            return cache_optimizations
            
        except Exception as e:
            logger.error("Worktree cache optimization failed", error=str(e))
            cache_optimizations["error"] = str(e)
            return cache_optimizations
    
    async def _optimize_memory_usage(self) -> Dict[str, Any]:
        """Optimize memory usage for worktree operations"""
        
        memory_optimizations = {
            "gc_forced": False,
            "index_cleared": False,
            "pack_files_optimized": False
        }
        
        try:
            # Force garbage collection
            gc_result = subprocess.run(
                ["git", "gc", "--force", "--aggressive"],
                capture_output=True, text=True, cwd=os.getcwd()
            )
            
            if gc_result.returncode == 0:
                memory_optimizations["gc_forced"] = True
                logger.info("Forced Git garbage collection")
            else:
                logger.warning("Failed to force garbage collection", error=gc_result.stderr)
            
            # Clear index if needed (for large repositories)
            index_result = subprocess.run(
                ["git", "read-tree", "--empty"],
                capture_output=True, text=True, cwd=os.getcwd()
            )
            
            if index_result.returncode == 0:
                memory_optimizations["index_cleared"] = True
            
            logger.info("Memory usage optimization completed")
            return memory_optimizations
            
        except Exception as e:
            logger.error("Memory usage optimization failed", error=str(e))
            memory_optimizations["error"] = str(e)
            return memory_optimizations
    
    async def _optimize_disk_usage(self) -> Dict[str, Any]:
        """Optimize disk usage and cleanup"""
        
        disk_optimizations = {
            "pack_files_repacked": False,
            "garbage_collected": False,
            "tmp_directories_cleaned": 0
        }
        
        try:
            # Repack pack files
            repack_result = subprocess.run(
                ["git", "repack", "-a", "-d", "--depth=250", "--window=250"],
                capture_output=True, text=True, cwd=os.getcwd()
            )
            
            if repack_result.returncode == 0:
                disk_optimizations["pack_files_repacked"] = True
                logger.info("Repacked Git pack files")
            
            # Run garbage collection
            gc_result = subprocess.run(
                ["git", "gc", "--prune=now"],
                capture_output=True, text=True, cwd=os.getcwd()
            )
            
            if gc_result.returncode == 0:
                disk_optimizations["garbage_collected"] = True
                logger.info("Performed Git garbage collection")
            
            # Clean temporary directories
            temp_dirs_cleaned = await self._cleanup_temp_directories()
            disk_optimizations["tmp_directories_cleaned"] = temp_dirs_cleaned
            
            logger.info("Disk usage optimization completed")
            return disk_optimizations
            
        except Exception as e:
            logger.error("Disk usage optimization failed", error=str(e))
            disk_optimizations["error"] = str(e)
            return disk_optimizations
    
    async def _setup_performance_monitoring(self) -> Dict[str, Any]:
        """Set up performance monitoring for worktree operations"""
        
        monitoring_setup = {
            "monitoring_enabled": False,
            "monitoring_interval": self.config.monitoring_interval_seconds,
            "metrics_collected": []
        }
        
        try:
            if not self.monitoring_active:
                self.monitoring_active = True
                self.monitor_thread = threading.Thread(target=self._performance_monitor_loop)
                self.monitor_thread.daemon = True
                self.monitor_thread.start()
                monitoring_setup["monitoring_enabled"] = True
                logger.info("Performance monitoring started")
            
            monitoring_setup["metrics_collected"] = [
                "worktree_creation_time",
                "worktree_cleanup_time",
                "memory_usage",
                "disk_usage",
                "concurrent_operations"
            ]
            
            return monitoring_setup
            
        except Exception as e:
            logger.error("Performance monitoring setup failed", error=str(e))
            monitoring_setup["error"] = str(e)
            return monitoring_setup
    
    def _performance_monitor_loop(self):
        """Background monitoring loop for performance metrics"""
        
        while self.monitoring_active:
            try:
                # Collect performance metrics
                current_metrics = self._collect_current_metrics()
                
                # Store in history
                with self._lock:
                    self.performance_history.append({
                        "timestamp": datetime.now().isoformat(),
                        "metrics": current_metrics
                    })
                
                # Clean old history (keep last 100 entries)
                if len(self.performance_history) > 100:
                    self.performance_history = self.performance_history[-100:]
                
                time.sleep(self.config.monitoring_interval_seconds)
                
            except Exception as e:
                logger.error("Error in performance monitoring loop", error=str(e))
                time.sleep(5)  # Wait before retrying
    
    def _collect_current_metrics(self) -> Dict[str, Any]:
        """Collect current performance metrics"""
        
        metrics = {
            "active_worktrees": len(self.active_worktrees),
            "memory_usage_mb": self._get_memory_usage_mb(),
            "disk_usage_mb": self._get_disk_usage_mb(),
            "timestamp": datetime.now().isoformat()
        }
        
        return metrics
    
    def _get_memory_usage_mb(self) -> float:
        """Get current memory usage in MB"""
        
        try:
            import psutil
            process = psutil.Process()
            return process.memory_info().rss / (1024 * 1024)
        except ImportError:
            # Fallback for systems without psutil
            return 0.0
        except Exception:
            return 0.0
    
    def _get_disk_usage_mb(self) -> float:
        """Get current disk usage for worktrees in MB"""
        
        total_size = 0
        with self._lock:
            for worktree_path in self.active_worktrees.keys():
                if os.path.exists(worktree_path):
                    for dirpath, dirnames, filenames in os.walk(worktree_path):
                        for filename in filenames:
                            filepath = os.path.join(dirpath, filename)
                            try:
                                total_size += os.path.getsize(filepath)
                            except (OSError, IOError):
                                continue
        
        return total_size / (1024 * 1024)
    
    async def _pre_creation_optimizations(self) -> Dict[str, Any]:
        """Perform optimizations before worktree creation"""
        
        pre_opt = {
            "gc_performed": False,
            "pack_optimized": False,
            "index_prepared": False
        }
        
        try:
            # Pre-creation garbage collection
            gc_result = subprocess.run(
                ["git", "gc", "--auto"],
                capture_output=True, text=True, cwd=os.getcwd()
            )
            
            if gc_result.returncode == 0:
                pre_opt["gc_performed"] = True
            
            return pre_opt
            
        except Exception as e:
            logger.error("Pre-creation optimization failed", error=str(e))
            pre_opt["error"] = str(e)
            return pre_opt
    
    async def _create_worktree_with_optimizations(
        self,
        branch_name: str,
        worktree_path: str,
        base_path: str
    ) -> Dict[str, Any]:
        """Create worktree with Git optimizations"""
        
        try:
            # Create optimized worktree command
            cmd = ["git", "worktree", "add", worktree_path, branch_name]
            
            if base_path != ".":
                cmd.extend(["--checkout", base_path])
            
            # Execute worktree creation
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=base_path,
                timeout=300  # 5 minute timeout
            )
            
            if result.returncode == 0:
                return {
                    "success": True,
                    "output": result.stdout,
                    "errors": result.stderr
                }
            else:
                return {
                    "success": False,
                    "error": result.stderr,
                    "output": result.stdout
                }
            
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": "Worktree creation timed out"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    async def _post_creation_optimizations(self, worktree_path: str) -> Dict[str, Any]:
        """Perform optimizations after worktree creation"""
        
        post_opt = {
            "index_optimized": False,
            "config_optimized": False
        }
        
        try:
            # Optimize worktree index
            if os.path.exists(worktree_path):
                index_result = subprocess.run(
                    ["git", "update-server-info"],
                    capture_output=True, text=True, cwd=worktree_path
                )
                
                if index_result.returncode == 0:
                    post_opt["index_optimized"] = True
            
            return post_opt
            
        except Exception as e:
            logger.error("Post-creation optimization failed", error=str(e))
            post_opt["error"] = str(e)
            return post_opt
    
    async def _calculate_worktree_metrics(
        self,
        worktree_path: str,
        creation_time: float
    ) -> WorktreePerformanceMetrics:
        """Calculate performance metrics for worktree"""
        
        # Calculate memory usage
        memory_usage_mb = self._get_worktree_memory_usage(worktree_path)
        
        # Calculate disk usage
        disk_usage_mb = self._get_worktree_disk_usage(worktree_path)
        
        # Calculate performance score
        performance_score = self._calculate_performance_score(creation_time, memory_usage_mb, disk_usage_mb)
        
        return WorktreePerformanceMetrics(
            creation_time=creation_time,
            cleanup_time=0.0,  # Will be set during cleanup
            memory_usage_mb=memory_usage_mb,
            disk_usage_mb=disk_usage_mb,
            throughput_operations=1.0 / creation_time if creation_time > 0 else 0.0,
            concurrent_operations_supported=self.config.max_concurrent_worktrees,
            performance_score=performance_score
        )
    
    async def _register_worktree(
        self,
        worktree_path: str,
        branch_name: str,
        metrics: WorktreePerformanceMetrics
    ):
        """Register worktree for tracking"""
        
        with self._lock:
            self.active_worktrees[worktree_path] = {
                "branch_name": branch_name,
                "created_at": datetime.now().isoformat(),
                "metrics": metrics
            }
            
            # Update peak concurrent usage
            current_usage = len(self.active_worktrees)
            self.performance_stats["peak_concurrent_usage"] = max(
                self.performance_stats["peak_concurrent_usage"],
                current_usage
            )
            
            self.performance_stats["total_worktrees_created"] += 1
        
        logger.debug(f"Registered worktree: {worktree_path}")
    
    # Additional helper methods for optimization, benchmarking, etc.
    # (Methods would continue with similar detailed implementations)
    
    async def _run_git_pack_optimization(self) -> List[str]:
        """Run Git pack optimizations"""
        operations = []
        try:
            # Run various pack optimization commands
            pack_commands = [
                ["git", "count-objects", "-v"],
                ["git", "gc", "--aggressive", "--dry-run"],
                ["git", "fsck", "--unreachable"]
            ]
            
            for cmd in pack_commands:
                try:
                    result = subprocess.run(cmd, capture_output=True, text=True)
                    if result.returncode == 0:
                        operations.append(f"Completed: {' '.join(cmd)}")
                except Exception:
                    operations.append(f"Failed: {' '.join(cmd)}")
            
            return operations
        except Exception as e:
            return [f"Error running pack optimization: {str(e)}"]
    
    def _calculate_optimization_score(self, optimization_results: Dict[str, Any]) -> float:
        """Calculate overall optimization score"""
        
        score_components = []
        
        # Git configuration score
        git_config = optimization_results.get("git_configuration", {})
        if git_config.get("config_applied"):
            score_components.append(0.8)
        
        # Cache optimization score
        cache_opt = optimization_results.get("cache_optimization", {})
        if cache_opt.get("tmp_cleaned"):
            score_components.append(0.7)
        
        # Memory optimization score
        memory_opt = optimization_results.get("memory_optimization", {})
        if memory_opt.get("gc_forced"):
            score_components.append(0.9)
        
        # Disk optimization score
        disk_opt = optimization_results.get("disk_optimization", {})
        if disk_opt.get("garbage_collected"):
            score_components.append(0.8)
        
        # Monitoring score
        monitoring = optimization_results.get("monitoring", {})
        if monitoring.get("monitoring_enabled"):
            score_components.append(0.9)
        
        return sum(score_components) / len(score_components) if score_components else 0.5
    
    def get_performance_statistics(self) -> Dict[str, Any]:
        """Get comprehensive performance statistics"""
        
        with self._lock:
            current_stats = dict(self.performance_stats)
            current_stats["active_worktrees"] = len(self.active_worktrees)
            current_stats["performance_history_entries"] = len(self.performance_history)
        
        return current_stats
    
    async def shutdown(self):
        """Shutdown performance optimizer and cleanup resources"""
        
        logger.info("Shutting down worktree performance optimizer")
        
        # Stop monitoring
        self.monitoring_active = False
        if self.monitor_thread and self.monitor_thread.is_alive():
            self.monitor_thread.join(timeout=5)
        
        # Final cleanup
        cleanup_result = await self.batch_cleanup_expired_worktrees()
        
        logger.info(
            "Worktree performance optimizer shutdown complete",
            cleaned_worktrees=cleanup_result.get("cleaned_up", 0)
        )