"""
A high-level service for comprehensive Gmail integration.

This module orchestrates various components like data collection, metadata
extraction, and AI analysis to provide a complete email processing pipeline.
It serves as the primary interface for all Gmail-related operations.
"""

import asyncio
import json
import logging
import os
import sys
from datetime import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Optional

# To avoid circular imports with type hints
if TYPE_CHECKING:
    from ..python_backend.ai_engine import AdvancedAIEngine
    from ..python_backend.database import DatabaseManager

from backend.node_engine.workflow_engine import workflow_engine
from backend.python_nlp.gmail_integration import GmailDataCollector
from backend.python_nlp.nlp_engine import NLPEngine
from backend.python_nlp.smart_retrieval import SmartRetrieval
from src.core.data_source import DataSource
from src.core.security import PathValidator


class GmailAIService:
    """
    A service class to handle comprehensive Gmail integration tasks.

    This class coordinates email synchronization, metadata extraction,
    AI analysis, and database operations for Gmail accounts.
    """

    def __init__(
        self,
        ai_engine: Optional["AdvancedAIEngine"] = None,
        db_manager: Optional["DatabaseManager"] = None,
    ):
        self.logger = logging.getLogger(f"{self.__class__.__module__}.{self.__class__.__name__}")
        self.ai_engine = ai_engine
        self.db_manager = db_manager
        # Initialize the data collector for Gmail API interactions
        self.data_collector = GmailDataCollector()
        # Initialize the NLP engine for email analysis
        self.nlp_engine = NLPEngine()
        # Initialize smart retrieval system
        self.smart_retrieval = SmartRetrieval()
        # Statistics tracking
        self.stats = {
            "total_sync_operations": 0,
            "successful_sync_operations": 0,
            "failed_sync_operations": 0,
            "total_emails_processed": 0,
            "last_sync_timestamp": None,
            "service_active": True,
        }
        # Path for the smart_retrieval.py script
        self.nlp_path = PathValidator.sanitize_path(os.path.join(os.getcwd(), "backend", "python_nlp"))
        self.retrieval_script = os.path.join(self.nlp_path, "smart_retrieval.py")

    async def sync_gmail_emails(
        self,
        query: str = "",
        max_emails: Optional[int] = None,
        use_smart_retrieval: bool = False,
    ) -> Dict[str, Any]:
        """
        Synchronize emails from Gmail with local storage and perform AI analysis.

        Args:
            query: Gmail search query to filter emails (e.g., 'from:me after:2023-01-01')
            max_emails: Maximum number of emails to sync (None for no limit)
            use_smart_retrieval: Whether to use smart retrieval strategies

        Returns:
            A dictionary with sync results including counts and any errors.
        """
        self.logger.info(f"Starting Gmail sync with query: '{query}', max: {max_emails}")
        sync_start_time = datetime.now()

        try:
            # Update stats
            self.stats["total_sync_operations"] += 1

            # Collect emails from Gmail
            if use_smart_retrieval:
                retrieval_result = await self.execute_smart_retrieval()
                emails = retrieval_result.get("emails", [])
            else:
                email_batch = await self.data_collector.collect_emails_incremental(
                    query_filter=query, max_emails=max_emails
                )
                emails = email_batch.messages

            # Process each email
            processed_count = 0
            errors = []

            for email_data in emails:
                try:
                    # Perform AI analysis on the email
                    analysis_result = await self._analyze_email_with_ai(email_data)

                    # Store the email and analysis in the database
                    await self._store_email_with_analysis(email_data, analysis_result)

                    processed_count += 1
                    self.stats["total_emails_processed"] += 1

                except Exception as e:
                    self.logger.error(f"Error processing email {email_data.get('message_id', 'unknown')}: {e}")
                    errors.append(
                        {
                            "email_id": email_data.get("message_id", "unknown"),
                            "error": str(e),
                        }
                    )

            # Update sync stats
            sync_duration = (datetime.now() - sync_start_time).total_seconds()
            self.stats["last_sync_timestamp"] = sync_start_time.isoformat()
            self.stats["successful_sync_operations"] += 1
            self.stats["total_sync_time_seconds"] = self.stats.get("total_sync_time_seconds", 0) + sync_duration

            result = {
                "status": "success",
                "total_found": len(emails),
                "processed": processed_count,
                "errors": errors,
                "sync_duration_seconds": sync_duration,
                "timestamp": sync_start_time.isoformat(),
            }

            self.logger.info(
                f"Gmail sync completed: {processed_count}/{len(emails)} emails processed in {sync_duration:.2f}s"
            )

            return result

        except Exception as e:
            self.logger.error(f"Gmail sync failed: {e}")
            self.stats["failed_sync_operations"] += 1
            self.stats["last_error_timestamp"] = datetime.now().isoformat()
            self.stats["error_types"] = self.stats.get("error_types", {})
            error_type = type(e).__name__
            self.stats["error_types"][error_type] = self.stats["error_types"].get(error_type, 0) + 1

            return {
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
            }

    async def _analyze_email_with_ai(self, email_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform comprehensive AI analysis on a single email.

        Args:
            email_data: Dictionary containing email information

        Returns:
            A dictionary with AI analysis results.
        """
        if not self.ai_engine:
            # Fallback to NLP engine if AI engine not available
            return await self.nlp_engine.analyze_email(
                subject=email_data.get("subject", ""),
                content=email_data.get("content", ""),
            )

        # Use the AI engine for analysis
        return await self.ai_engine.analyze_email(
            subject=email_data.get("subject", ""),
            content=email_data.get("content", ""),
        )

    async def _store_email_with_analysis(
        self, email_data: Dict[str, Any], analysis_result: Dict[str, Any]
    ) -> None:
        """
        Store the email and its AI analysis in the database.

        Args:
            email_data: Dictionary containing email information
            analysis_result: Dictionary containing AI analysis results
        """
        if not self.db_manager:
            self.logger.warning("No database manager provided, skipping storage")
            return

        # Combine email data with analysis
        email_record = {**email_data, **analysis_result}

        # Store in database
        await self.db_manager.insert_email(email_record)

    async def get_performance_metrics(self) -> Dict[str, Any]:
        """
        Get detailed performance metrics for Gmail operations.

        Returns comprehensive performance data including sync times, success rates,
        error rates, and resource usage tracking.
        """
        try:
            # Get current timestamp for metrics
            current_time = datetime.now()

            # Calculate performance metrics from stats
            total_operations = self.stats.get("total_sync_operations", 0)
            successful_operations = self.stats.get("successful_sync_operations", 0)
            failed_operations = self.stats.get("failed_sync_operations", 0)

            # Calculate success rate
            success_rate = (
                (successful_operations / total_operations * 100) if total_operations > 0 else 0
            )

            # Calculate average sync time
            total_sync_time = self.stats.get("total_sync_time_seconds", 0)
            avg_sync_time = total_sync_time / total_operations if total_operations > 0 else 0

            # Get API usage metrics
            api_calls_made = self.stats.get("api_calls_made", 0)
            rate_limit_hits = self.stats.get("rate_limit_hits", 0)

            # Get resource usage
            emails_processed = self.stats.get("emails_processed", 0)
            data_processed_mb = self.stats.get("data_processed_bytes", 0) / (
                1024 * 1024
            )  # Convert to MB

            # Build comprehensive performance metrics
            performance_metrics = {
                "summary": {
                    "total_sync_operations": total_operations,
                    "successful_operations": successful_operations,
                    "failed_operations": failed_operations,
                    "success_rate_percent": round(success_rate, 2),
                    "average_sync_time_seconds": round(avg_sync_time, 2),
                    "total_emails_processed": emails_processed,
                    "total_data_processed_mb": round(data_processed_mb, 2),
                },
                "api_usage": {
                    "total_api_calls": api_calls_made,
                    "rate_limit_hits": rate_limit_hits,
                    "api_call_efficiency": round(api_calls_made / max(emails_processed, 1), 2),
                },
                "performance_trends": {
                    "last_sync_time": self.stats.get("last_sync_timestamp"),
                    "average_response_time_ms": self.stats.get("avg_response_time_ms", 0),
                    "peak_sync_duration_seconds": self.stats.get("peak_sync_duration", 0),
                },
                "error_analysis": {
                    "error_rate_percent": round(
                        (failed_operations / max(total_operations, 1)) * 100, 2
                    ),
                    "common_error_types": self.stats.get("error_types", {}),
                    "last_error_timestamp": self.stats.get("last_error_timestamp"),
                },
                "resource_usage": {
                    "bandwidth_used_mb": round(data_processed_mb, 2),
                    "processing_efficiency": round(
                        emails_processed / max(total_sync_time, 1), 2
                    ),  # emails/second
                    "memory_peak_usage_mb": self.stats.get("memory_peak_mb", 0),
                },
                "timestamp": current_time.isoformat(),
                "status": "active" if self.stats.get("service_active", True) else "inactive",
            }

            return performance_metrics

        except Exception as e:
            self.logger.error(f"Error retrieving performance metrics: {e}")
            return {
                "error": f"Failed to retrieve performance metrics: {str(e)}",
                "timestamp": datetime.now().isoformat(),
                "status": "error",
            }

    async def execute_smart_retrieval(
        self, strategies: List[str] = None, max_api_calls: int = 100, time_budget_minutes: int = 30
    ) -> Dict[str, Any]:
        """
        Args:
            strategies: A list of retrieval strategies to execute.
            max_api_calls: The maximum number of API calls allowed.
            time_budget_minutes: The time budget in minutes for the process.

        Returns:
            A dictionary with the results of the retrieval process.
        """
        cmd = [
            sys.executable,
            self.retrieval_script,
            "execute-strategies",
            "--max-api-calls",
            str(max_api_calls),
            "--time-budget",
            str(time_budget_minutes),
        ]
        if strategies:
            cmd.extend(["--strategies"] + strategies)
        return await self._execute_async_command(cmd, cwd=self.nlp_path)

    async def get_retrieval_strategies(self) -> List[Dict[str, Any]]:
        """
        Retrieves available email retrieval strategies.

        Returns:
            A list of dictionaries representing available retrieval strategies.
        """
        # Implementation would go here
        return []

    async def _execute_async_command(self, cmd, cwd=None) -> Dict[str, Any]:
        """Execute a command asynchronously and return the result."""
        try:
            process = await asyncio.create_subprocess_exec(
                *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE, cwd=cwd
            )
            stdout, stderr = await process.communicate()

            result = {
                "returncode": process.returncode,
                "stdout": stdout.decode() if stdout else "",
                "stderr": stderr.decode() if stderr else "",
            }

            if process.returncode != 0:
                self.logger.error(f"Command failed: {result}")
            else:
                self.logger.info(f"Command succeeded: {result}")

            return result
        except Exception as e:
            self.logger.error(f"Error executing command: {e}")
            return {"error": str(e), "returncode": -1}


async def main():
    """
    Demonstrates the usage of the GmailAIService.
    """
    logging.basicConfig(
        level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    service = GmailAIService()
    sync_result = await service.sync_gmail_emails(max_emails=2)
    logging.info(f"Sync result: {sync_result}")


if __name__ == "__main__":
    asyncio.run(main())