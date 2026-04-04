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

# AI Training and PromptEngineer might not be directly used by GmailAIService after refactoring
# if all AI analysis is delegated to AdvancedAIEngine.
from .ai_training import ModelConfig
from .data_strategy import DataCollectionStrategy
from .gmail_integration import EmailBatch, GmailDataCollector, RateLimitConfig
from .gmail_metadata import GmailMessage, GmailMetadataExtractor


class GmailAIService:
    """
    Provides a complete service for Gmail integration, including AI processing.

    This class combines functionalities for fetching emails, extracting metadata,
    performing AI analysis, and training models, offering a unified interface
    for advanced email management.

    Attributes:
        collector: An instance of `GmailDataCollector` for fetching emails.
        metadata_extractor: An instance of `GmailMetadataExtractor`.
        data_strategy: An instance of `DataCollectionStrategy`.
        logger: A logger for this class.
        advanced_ai_engine: An instance of the AI engine for analysis.
        db_manager: An instance of the database manager.
        stats: A dictionary to hold processing statistics.
    """

    def __init__(
        self,
        rate_config: Optional[RateLimitConfig] = None,
        advanced_ai_engine=None,
        db_manager=None,
    ):
        self.collector = GmailDataCollector(rate_config)
        self.metadata_extractor = GmailMetadataExtractor()
        self.data_strategy = DataCollectionStrategy()
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")

        if advanced_ai_engine:
            self.advanced_ai_engine = advanced_ai_engine
        else:
            self.logger.warning(
                "No AI engine provided to GmailAIService. AI analysis will be disabled."
            )
            self.advanced_ai_engine = None

        self.db_manager = db_manager
        if not self.db_manager:
            self.logger.warning(
                "No Database manager provided to GmailAIService. Category matching will be disabled."
            )
            self.db_manager = None

        # Path definitions for scripts (like smart_retrieval.py) might still be relevant
        self.nlp_path = os.path.dirname(__file__)
        self.retrieval_script = os.path.join(self.nlp_path, "smart_retrieval.py")
        self.stats = {
            "total_processed": 0,
            "successful_extractions": 0,
            "failed_extractions": 0,
            "ai_analyses_completed": 0,
            "last_sync": None,
        }

    async def _execute_async_command(
        self, cmd: List[str], cwd: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Executes a shell command asynchronously.

        Args:
            cmd: The command and its arguments as a list of strings.
            cwd: The working directory for the command.

        Returns:
            A dictionary with the execution status and output.
        """
        try:
            process = await asyncio.create_subprocess_exec(
                *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE, cwd=cwd
            )
            stdout, stderr = await process.communicate()
            if process.returncode != 0:
                error_msg = (stderr.decode().strip() if stderr else "") or "Unknown error"
                self.logger.error(f"Async command failed: {cmd}, Error: {error_msg}")
                return {"success": False, "error": error_msg}
            if stdout:
                try:
                    return json.loads(stdout.decode())
                except json.JSONDecodeError:
                    return {"success": True, "output": stdout.decode()}
            return {"success": True, "output": ""}
        except (FileNotFoundError, PermissionError, Exception) as e:
            self.logger.error(f"Async command execution failed for {cmd}: {e}", exc_info=True)
            return {"success": False, "error": str(e)}

    async def sync_gmail_emails(
        self,
        query_filter: str = "newer_than:7d",
        max_emails: int = 1000,
        include_ai_analysis: bool = True,
    ) -> Dict[str, Any]:
        """
        Performs a comprehensive sync of Gmail emails.

        This method fetches emails, extracts metadata, performs AI analysis,
        and prepares the data for database insertion.

        Args:
            query_filter: The Gmail query to filter which emails to sync.
            max_emails: The maximum number of emails to sync.
            include_ai_analysis: Whether to perform AI analysis on the emails.

        Returns:
            A dictionary with the results of the synchronization, including
            the number of processed emails and any errors.
        """
        self.logger.info(
            f"Starting Gmail sync with filter: {query_filter}, max_emails: {max_emails}"
        )
        try:
            email_batch = await self._fetch_emails_from_gmail(query_filter, max_emails)
            if not email_batch:
                return {"success": False, "error": "Failed to fetch emails.", "processed_count": 0}
            processed_db_emails = await self._process_and_analyze_batch(
                email_batch, include_ai_analysis
            )
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

    async def _fetch_emails_from_gmail(
        self, query_filter: str, max_emails: int
    ) -> Optional[EmailBatch]:
        """Fetches a batch of emails from Gmail using the data collector."""
        try:
            return await self.collector.collect_emails_incremental(
                query_filter=query_filter, max_emails=max_emails
            )
        except Exception as e:
            self.logger.error(f"Failed to fetch email batch: {e}", exc_info=True)
            return None

    async def _process_and_analyze_batch(
        self, email_batch: EmailBatch, include_ai_analysis: bool
    ) -> List[Dict[str, Any]]:
        """Processes a batch of emails, including metadata extraction and AI analysis."""
        processed_emails = []
        for gmail_msg in email_batch.messages:
            try:
                gmail_metadata = self.metadata_extractor.extract_complete_metadata(gmail_msg)
                email_data = {
                    "subject": gmail_metadata.subject,
                    "content": gmail_metadata.body_plain or gmail_metadata.snippet,
                }
                ai_analysis_result = (
                    await self._perform_ai_analysis(email_data) if include_ai_analysis else None
                )
                db_email = self._convert_to_db_format(gmail_metadata, ai_analysis_result)
                processed_emails.append(db_email)
                self.stats["successful_extractions"] += 1
            except Exception as e:
                self.logger.error(
                    f"Failed to process email {gmail_msg.get('id', 'unknown')}: {e}", exc_info=True
                )
                self.stats["failed_extractions"] += 1
        return processed_emails

    async def _perform_ai_analysis(self, email_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Performs AI analysis on a single email."""
        if not self.advanced_ai_engine:
            self.logger.error("AI engine not available for AI analysis.")
            return self._get_basic_fallback_analysis_structure("AI engine not configured")

        # Pass the db manager (which could be None) to the AI engine
        db_for_analysis = self.db_manager

        self.logger.debug(f"Performing AI analysis for email ID: {email_data.get('id', 'unknown')}")
        try:
            # AdvancedAIEngine is expected to have an `analyze_email` method
            # that takes subject and content, and returns an object or dict with analysis.
            analysis_result_obj = await self.advanced_ai_engine.analyze_email(
                subject=email_data.get("subject", ""),
                content=email_data.get("content", ""),
                db=db_for_analysis,  # Pass the db manager (could be None)
            )

            # Assuming analyze_email returns an object with a to_dict() method or is a dict
            if hasattr(analysis_result_obj, "to_dict"):
                analysis_dict = analysis_result_obj.to_dict()
            elif isinstance(analysis_result_obj, dict):
                analysis_dict = analysis_result_obj
            else:
                self.logger.error(
                    f"Unexpected AI analysis result type for email {email_data.get('id', 'unknown')}"
                )
                return self._get_basic_fallback_analysis_structure("Unexpected AI result type")

            self.stats["ai_analyses_completed"] += 1
            return analysis_dict
        except Exception as e:
            self.logger.error(f"AI analysis failed for email: {e}", exc_info=True)
            return None

    def _get_basic_fallback_analysis_structure(self, error_message: str) -> Dict[str, Any]:
        """Provides a fallback structure for AI analysis results in case of an error."""
        return {
            "error": error_message,
            "topic": "unknown",
            "sentiment": "neutral",
            "intent": "unknown",
            "urgency": "low",
            "confidence": 0.0,
        }

    def _convert_to_db_format(
        self, gmail_metadata: GmailMessage, ai_analysis_result: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
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

    async def train_models_from_gmail_data(
        self, training_query: str = "newer_than:30d", max_training_emails: int = 5000
    ) -> Dict[str, Any]:
        """
        Trains AI models using data fetched directly from Gmail.

        Args:
            training_query: The Gmail query to select emails for training.
            max_training_emails: The maximum number of emails to use for training.

        Returns:
            A dictionary with the results of the training process.
        """
        self.logger.info(f"Starting model training from Gmail data with query: {training_query}")
        try:
            batch = await self.collector.collect_emails_incremental(
                query_filter=training_query, max_emails=max_training_emails
            )
            samples = [
                self.metadata_extractor.to_training_format(
                    self.metadata_extractor.extract_complete_metadata(msg)
                )
                for msg in batch.messages
            ]
            if not samples:
                return {"success": False, "error": "No training samples collected."}
            # Placeholder for actual model training logic
            return {
                "success": True,
                "training_samples_count": len(samples),
                "message": "Training logic not implemented.",
            }
        except Exception as e:
            self.logger.error(f"Model training failed: {e}", exc_info=True)
            return {"success": False, "error": str(e)}

    def _infer_topic_from_metadata(self, metadata: GmailMessage) -> str:
        """Infers a topic label from email metadata."""
        return metadata.category or "work_business"

    def _infer_sentiment_from_metadata(self, metadata: GmailMessage) -> str:
        """Infers a sentiment label from email metadata."""
        return "positive" if metadata.is_important and metadata.is_starred else "neutral"

    def _infer_intent_from_metadata(self, metadata: GmailMessage) -> str:
        """Infers an intent label from email metadata."""
        return "question" if "?" in metadata.subject else "information"

    def _infer_urgency_from_metadata(self, metadata: GmailMessage) -> str:
        """Infers an urgency label from email metadata."""
        return "high" if metadata.is_important else "low"

    def get_processing_statistics(self) -> Dict[str, Any]:
        """Returns a dictionary of processing statistics."""
        return {"processing_stats": self.stats}

    async def execute_smart_retrieval(
        self, strategies: List[str] = None, max_api_calls: int = 100, time_budget_minutes: int = 30
    ) -> Dict[str, Any]:
        """
        Execute smart retrieval with the given strategies.
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


async def main():
    """Demonstrates the usage of the GmailAIService."""
    logging.basicConfig(
        level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    service = GmailAIService()
    sync_result = await service.sync_gmail_emails(max_emails=2)
    logging.info(f"Sync result: {sync_result}")


if __name__ == "__main__":
    asyncio.run(main())
