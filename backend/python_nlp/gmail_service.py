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
    from .protocols import AIEngineProtocol, DatabaseProtocol

from ..python_backend.ai_engine import AdvancedAIEngine
from ..python_backend.database import DatabaseManager
from .ai_training import ModelConfig
from .data_strategy import DataCollectionStrategy
from .gmail_integration import EmailBatch, GmailDataCollector, RateLimitConfig
from .gmail_metadata import GmailMessage, GmailMetadataExtractor


class GmailAIService:
    """
    Provides a complete service for Gmail integration, including AI processing.
    """

    def __init__(
        self,
        rate_config: Optional[RateLimitConfig] = None,
        advanced_ai_engine: Optional["AIEngineProtocol"] = None,
        db_manager: Optional["DatabaseProtocol"] = None,
    ):
        """Initializes the GmailAIService."""
        self.collector = GmailDataCollector(rate_config)
        self.metadata_extractor = GmailMetadataExtractor()
        self.data_strategy = DataCollectionStrategy()
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")

        self.advanced_ai_engine = advanced_ai_engine
        if not self.advanced_ai_engine:
            self.logger.warning("No AI engine provided. AI analysis will be disabled.")

        self.db_manager = db_manager
        if not self.db_manager:
            self.logger.warning("No Database manager provided. Category matching will be disabled.")

        self.nlp_path = os.path.dirname(__file__)
        self.retrieval_script = os.path.join(self.nlp_path, "smart_retrieval.py")
        self.stats = {
            "total_processed": 0,
            "successful_extractions": 0,
            "failed_extractions": 0,
            "ai_analyses_completed": 0,
            "last_sync": None,
        }

    async def _execute_async_command(self, cmd: List[str], cwd: Optional[str] = None) -> Dict[str, Any]:
        """Executes a shell command asynchronously."""
        try:
            process = await asyncio.create_subprocess_exec(
                *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE, cwd=cwd
            )
            stdout, stderr = await process.communicate()
            if process.returncode != 0:
                error_msg = (stderr.decode().strip() if stderr else "Unknown error")
                self.logger.error(f"Async command failed: {cmd}, Error: {error_msg}")
                return {"success": False, "error": error_msg}
            if stdout:
                try:
                    return json.loads(stdout.decode())
                except json.JSONDecodeError:
                    return {"success": True, "output": stdout.decode()}
            return {"success": True, "output": ""}
        except Exception as e:
            self.logger.error(f"Async command execution failed for {cmd}: {e}", exc_info=True)
            return {"success": False, "error": str(e)}

    async def sync_gmail_emails(
        self, query_filter: str = "newer_than:7d", max_emails: int = 1000, include_ai_analysis: bool = True
    ) -> Dict[str, Any]:
        """Performs a comprehensive sync of Gmail emails."""
        self.logger.info(f"Starting Gmail sync with filter: {query_filter}, max_emails: {max_emails}")
        try:
            email_batch = await self._fetch_emails_from_gmail(query_filter, max_emails)
            if not email_batch:
                return {"success": False, "error": "Failed to fetch emails.", "processed_count": 0}
            processed_db_emails = await self._process_and_analyze_batch(email_batch, include_ai_analysis)
            self.stats["total_processed"] += len(processed_db_emails)
            self.stats["last_sync"] = datetime.now().isoformat()
            return {
                "success": True,
                "processed_count": len(processed_db_emails),
                "emails": processed_db_emails,
                "statistics": self.stats.copy(),
            }
        except Exception as e:
            self.logger.error(f"Gmail sync failed: {e}", exc_info=True)
            return {"success": False, "error": str(e), "processed_count": 0}

    async def _fetch_emails_from_gmail(self, query_filter: str, max_emails: int) -> Optional[EmailBatch]:
        """Fetches a batch of emails from Gmail."""
        try:
            return await self.collector.collect_emails_incremental(query_filter=query_filter, max_emails=max_emails)
        except Exception as e:
            self.logger.error(f"Failed to fetch email batch: {e}", exc_info=True)
            return None

    async def _process_and_analyze_batch(self, email_batch: EmailBatch, include_ai_analysis: bool) -> List[Dict[str, Any]]:
        """Processes a batch of emails, including metadata extraction and AI analysis."""
        tasks = []
        for gmail_msg in email_batch.messages:
            tasks.append(self._process_single_email(gmail_msg, include_ai_analysis))

        results = await asyncio.gather(*tasks)
        return [res for res in results if res is not None]

    async def _process_single_email(self, gmail_msg: Dict[str, Any], include_ai_analysis: bool) -> Optional[Dict[str, Any]]:
        """Helper to process one email, allowing for concurrent processing."""
        try:
            gmail_metadata = self.metadata_extractor.extract_complete_metadata(gmail_msg)
            email_data = {"subject": gmail_metadata.subject, "content": gmail_metadata.body_plain or gmail_metadata.snippet}

            ai_analysis_result = None
            if include_ai_analysis:
                ai_analysis_result = await self._perform_ai_analysis(email_data)

            db_email = self._convert_to_db_format(gmail_metadata, ai_analysis_result)
            self.stats["successful_extractions"] += 1
            return db_email
        except Exception as e:
            self.logger.error(f"Failed to process email {gmail_msg.get('id', 'unknown')}: {e}", exc_info=True)
            self.stats["failed_extractions"] += 1
            return None

    async def _perform_ai_analysis(self, email_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Performs AI analysis on a single email."""
        if not self.advanced_ai_engine:
            self.logger.error("AI engine not available for AI analysis.")
            return self._get_basic_fallback_analysis_structure("AI engine not configured")

        try:
            analysis_result_obj = await self.advanced_ai_engine.analyze_email(
                subject=email_data.get("subject", ""),
                content=email_data.get("content", ""),
                db=self.db_manager,
            )
            if hasattr(analysis_result_obj, "to_dict"):
                analysis_dict = analysis_result_obj.to_dict()
            elif isinstance(analysis_result_obj, dict):
                analysis_dict = analysis_result_obj
            else:
                self.logger.error("Unexpected AI analysis result type.")
                return self._get_basic_fallback_analysis_structure("Unexpected AI result type")

            self.stats["ai_analyses_completed"] += 1
            return analysis_dict
        except Exception as e:
            self.logger.error(f"AI analysis failed for email: {e}", exc_info=True)
            return self._get_basic_fallback_analysis_structure(str(e))

    def _get_basic_fallback_analysis_structure(self, error_message: str) -> Dict[str, Any]:
        """Provides a fallback structure for AI analysis results in case of an error."""
        return {"error": error_message, "topic": "unknown", "sentiment": "neutral", "intent": "unknown", "urgency": "low", "confidence": 0.0}

    def _convert_to_db_format(self, gmail_metadata: GmailMessage, ai_analysis_result: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Converts extracted metadata and AI results into the database schema format."""
        analysis_payload = ai_analysis_result or {}
        return {
            "messageId": gmail_metadata.message_id,
            "threadId": gmail_metadata.thread_id,
            "sender": gmail_metadata.from_address,
            "subject": gmail_metadata.subject,
            "content": gmail_metadata.body_plain or gmail_metadata.snippet,
            "time": gmail_metadata.date,
            "isUnread": gmail_metadata.is_unread,
            "categoryId": analysis_payload.get("category_id"),
            "analysisMetadata": json.dumps(analysis_payload),
        }

    async def execute_smart_retrieval(self, strategies: List[str] = None, max_api_calls: int = 100, time_budget_minutes: int = 30) -> Dict[str, Any]:
        """Execute smart Gmail retrieval with multiple strategies."""
        self.logger.info(f"Executing smart retrieval. Strategies: {strategies}, Max API calls: {max_api_calls}, Budget: {time_budget_minutes}min")
        cmd = [sys.executable, self.retrieval_script, "execute-strategies", "--max-api-calls", str(max_api_calls), "--time-budget", str(time_budget_minutes)]
        if strategies:
            cmd.extend(["--strategies"] + strategies)
        return await self._execute_async_command(cmd, cwd=self.nlp_path)

    async def get_retrieval_strategies(self) -> List[Dict[str, Any]]:
        """Get available retrieval strategies."""
        self.logger.info("Fetching retrieval strategies.")
        cmd = [sys.executable, self.retrieval_script, "list-strategies"]
        result = await self._execute_async_command(cmd, cwd=self.nlp_path)
        if result.get("success") and "strategies" in result:
            return result["strategies"]
        self.logger.error(f"Failed to get strategies: {result.get('error', 'Unknown error')}")
        return []

    async def get_performance_metrics(self) -> Optional[Dict[str, Any]]:
        """Get Gmail API performance metrics."""
        self.logger.info("Fetching performance metrics.")
        cmd = [sys.executable, self.retrieval_script, "get-retrieval-analytics"]
        result = await self._execute_async_command(cmd, cwd=self.nlp_path)
        if result.get("success"):
            return result
        self.logger.error(f"Failed to get performance metrics: {result.get('error', 'Unknown error')}")
        return None
