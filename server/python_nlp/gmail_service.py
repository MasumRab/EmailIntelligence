"""
Comprehensive Gmail Integration Service
Combines metadata extraction, rate limiting, and AI training for complete email processing
"""

import asyncio
import json
import logging
import os  # Added
import sys  # Added
from datetime import datetime
from typing import Any, Dict, List, Optional

# Import AdvancedAIEngine (assuming it's now the primary way to get AI analysis)
# Adjust the import path as necessary based on your project structure.
# This assumes AdvancedAIEngine is in a module that can be imported.
# If it's in python_backend, the path needs to be correct.
# For now, let's assume a placeholder for where AdvancedAIEngine would be imported from.
from server.python_backend.ai_engine import \
    AdvancedAIEngine  # Assuming this import works
from server.python_backend.database import \
    DatabaseManager  # Assuming this import works

from .data_strategy import DataCollectionStrategy
from .gmail_integration import EmailBatch, GmailDataCollector, RateLimitConfig
from .gmail_metadata import GmailMessage, GmailMetadataExtractor

# AI Training and PromptEngineer might not be directly used by GmailAIService after refactoring
# if all AI analysis is delegated to AdvancedAIEngine.
from .ai_training import ModelConfig



class GmailAIService:
    """Complete Gmail integration with AI processing and metadata extraction"""

    def __init__(
        self,
        rate_config: Optional[RateLimitConfig] = None,
        advanced_ai_engine: Optional[AdvancedAIEngine] = None,  # Typed hint
        db_manager: Optional[DatabaseManager] = None,
    ):  # Added db_manager
        self.collector = GmailDataCollector(rate_config)
        self.metadata_extractor = GmailMetadataExtractor()
        self.data_strategy = DataCollectionStrategy()
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")

        if advanced_ai_engine:
            self.advanced_ai_engine = advanced_ai_engine
        else:
            self.logger.info(
                "No AdvancedAIEngine provided, instantiating a new one for GmailAIService."
            )
            self.advanced_ai_engine = AdvancedAIEngine()
            # Consider if AIEngine needs initialization here, e.g., self.advanced_ai_engine.initialize()

        self.db_manager = db_manager
        if not self.db_manager:
            self.logger.info(
                "No DatabaseManager provided to GmailAIService, instantiating a new one."
            )
            # This might be problematic if DB URL isn't available easily here or for testing.
            # Ideally, db_manager should be a required dependency if category matching is always on.
            self.db_manager = DatabaseManager()

        # Path definitions for scripts (like smart_retrieval.py) might still be relevant
        self.nlp_path = os.path.dirname(__file__)
        self.retrieval_script = os.path.join(self.nlp_path, "smart_retrieval.py")

        # Processing statistics
        self.stats = {
            "total_processed": 0,
            "successful_extractions": 0,
            "failed_extractions": 0,
            "ai_analyses_completed": 0,
            "last_sync": None,
        }

    # Added _execute_async_command method
    async def _execute_async_command(
        self, cmd: List[str], cwd: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Execute command asynchronously.
        Returns a dictionary with 'success': True/False and other command output.
        """
        try:
            self.logger.debug(
                f"Executing async command: {' '.join(cmd)} in {cwd or '.'}"
            )
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=cwd,
            )

            stdout, stderr = await process.communicate()
            stdout_decoded = stdout.decode().strip() if stdout else ""
            stderr_decoded = stderr.decode().strip() if stderr else ""

            if process.returncode != 0:
                error_msg = (
                    stderr_decoded
                    or stdout_decoded
                    or "Unknown error during command execution."
                )
                self.logger.error(
                    f"Async command failed (return code {process.returncode}): {cmd}. Error: {error_msg}"
                )
                return {
                    "success": False,
                    "error": error_msg,
                    "return_code": process.returncode,
                }

            if stdout_decoded:
                try:
                    parsed_output = json.loads(stdout_decoded)
                    if (
                        isinstance(parsed_output, dict)
                        and "success" not in parsed_output
                    ):
                        # If script provides JSON dict but no 'success' field, assume true as command didn't fail
                        parsed_output["success"] = True
                    elif not isinstance(
                        parsed_output, dict
                    ):  # Handle cases where script returns non-dict JSON (e.g. list, string)
                        return {"success": True, "data": parsed_output}
                    return parsed_output
                except json.JSONDecodeError as e:
                    self.logger.warning(
                        f"Command {cmd} output was not valid JSON, but command succeeded. Output: {stdout_decoded[:200]}..."
                    )
                    return {
                        "success": True,
                        "output": stdout_decoded,
                        "error": f"Non-JSON output: {str(e)}",
                    }  # Script success, but output not JSON
            else:
                self.logger.info(f"Command {cmd} executed successfully with no stdout.")
                return {"success": True, "output": ""}  # Script success, no output

        except FileNotFoundError as e:
            self.logger.error(
                f"Async command failed: Executable not found for {cmd}. Error: {e}"
            )
            return {
                "success": False,
                "error": f"Executable not found: {cmd[0]}. {str(e)}",
            }
        except PermissionError as e:
            self.logger.error(
                f"Async command failed: Permission denied for {cmd}. Error: {e}"
            )
            return {
                "success": False,
                "error": f"Permission denied for {cmd[0]}. {str(e)}",
            }
        except Exception as e:
            self.logger.error(
                f"Generic async command execution failed for {cmd}: {e}", exc_info=True
            )
            return {"success": False, "error": str(e)}

    async def sync_gmail_emails(
        self,
        query_filter: str = "newer_than:7d",
        max_emails: int = 1000,
        include_ai_analysis: bool = True,
    ) -> Dict[str, Any]:
        """
        Comprehensive Gmail sync with metadata extraction and AI analysis
        """
        self.logger.info(
            f"Starting Gmail sync with filter: {query_filter}, max_emails: {max_emails}"
        )
        try:
            # 1. Fetch emails
            email_batch = await self._fetch_emails_from_gmail(query_filter, max_emails)
            if not email_batch:
                # _fetch_emails_from_gmail would have logged the error
                return {
                    "success": False,
                    "error": "Failed to fetch emails.",
                    "processed_count": 0,
                    "emails": [],
                    "statistics": self.stats.copy(),
                }

            # 2. Process and Analyze emails
            processed_db_emails = await self._process_and_analyze_batch(
                email_batch, include_ai_analysis
            )

            # 3. Store/Return results (Storing is not explicitly handled here, focus on processing)
            self.stats["total_processed"] += len(
                processed_db_emails
            )  # Assuming all processed emails are successfully converted
            self.stats["last_sync"] = datetime.now().isoformat()

            return {
                "success": True,
                "processed_count": len(processed_db_emails),
                "emails": processed_db_emails,  # These are now in DB format
                "batch_info": {
                    "batch_id": email_batch.batch_id,
                    "query_filter": email_batch.query_filter,
                    "timestamp": email_batch.timestamp.isoformat(),
                },
                "statistics": self.stats.copy(),
            }

        except Exception as e:
            self.logger.error(f"Gmail sync failed: {e}", exc_info=True)
            return {
                "success": False,
                "error": str(e),
                "processed_count": 0,
                "emails": [],
                "statistics": self.stats.copy(),
            }

    async def _fetch_emails_from_gmail(
        self, query_filter: str, max_emails: int
    ) -> Optional[EmailBatch]:
        """Helper to fetch emails using GmailDataCollector."""
        self.logger.info(
            f"Fetching emails with query: {query_filter}, max: {max_emails}"
        )
        try:
            email_batch = await self.collector.collect_emails_incremental(
                query_filter=query_filter, max_emails=max_emails
            )
            self.logger.info(
                f"Fetched {len(email_batch.messages)} emails in batch {email_batch.batch_id}"
            )
            return email_batch
        except Exception as e:
            self.logger.error(f"Failed to fetch email batch: {e}", exc_info=True)
            return None

    async def _process_and_analyze_batch(
        self, email_batch: EmailBatch, include_ai_analysis: bool
    ) -> List[Dict[str, Any]]:
        """Helper to process metadata, perform AI analysis, and convert to DB format for a batch of emails."""
        processed_db_emails = []
        self.logger.info(
            f"Processing {len(email_batch.messages)} emails from batch {email_batch.batch_id}"
        )
        for gmail_msg in email_batch.messages:
            try:
                gmail_metadata = self.metadata_extractor.extract_complete_metadata(
                    gmail_msg
                )

                # The 'training_sample' here is a bit of a misnomer if it's just for AI analysis input
                # It's essentially the data structure expected by _perform_ai_analysis or _convert_to_db_format
                email_data_for_analysis = {
                    "id": gmail_metadata.message_id,  # Ensure an ID is present
                    "subject": gmail_metadata.subject,
                    "content": gmail_metadata.body_plain
                    or gmail_metadata.snippet
                    or "",  # Ensure content is not None
                    "sender_email": gmail_metadata.from_address,  # Ensure this field matches what _perform_ai_analysis expects
                    "timestamp": gmail_metadata.date,  # Ensure timestamp is present
                }

                ai_analysis_result = None
                if include_ai_analysis:
                    ai_analysis_result = await self._perform_ai_analysis(
                        email_data_for_analysis
                    )

                db_email = self._convert_to_db_format(
                    gmail_metadata, ai_analysis_result
                )  # Pass ai_analysis_result directly
                processed_db_emails.append(db_email)
                self.stats["successful_extractions"] += 1

            except Exception as e:
                self.logger.error(
                    f"Failed to process email {gmail_msg.get('id', 'unknown')}: {e}",
                    exc_info=True,
                )
                self.stats["failed_extractions"] += 1
                continue
        return processed_db_emails

    async def _perform_ai_analysis(
        self, email_data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Perform AI analysis on email data using AdvancedAIEngine.
        `email_data` should contain 'subject' and 'content'.
        """
        if not self.advanced_ai_engine:
            self.logger.error("AdvancedAIEngine not available for AI analysis.")
            return self._get_basic_fallback_analysis_structure(
                "AdvancedAIEngine not configured"
            )

        if not self.db_manager:
            self.logger.warning(
                "DatabaseManager not available in GmailAIService, category ID matching will be skipped for AI analysis."
            )
            # Fallback to analysis without DB-based category matching
            db_for_analysis = None
        else:
            db_for_analysis = self.db_manager

        self.logger.debug(
            f"Performing AI analysis for email ID: {email_data.get('id', 'unknown')}"
        )
        try:
            # AdvancedAIEngine is expected to have an `analyze_email` method
            # that takes subject and content, and returns an object or dict with analysis.
            analysis_result_obj = await self.advanced_ai_engine.analyze_email(
                subject=email_data.get("subject", ""),
                content=email_data.get("content", ""),
                db=db_for_analysis,  # Pass the db_manager instance
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
                return self._get_basic_fallback_analysis_structure(
                    "Unexpected AI result type"
                )

            self.stats["ai_analyses_completed"] += 1
            self.logger.info(
                f"AI analysis successful for email ID: {email_data.get('id', 'unknown')}. Topic: {analysis_dict.get('topic')}"
            )
            return analysis_dict

        except Exception as e:
            self.logger.error(
                f"AI analysis failed for email {email_data.get('id', 'unknown')}: {e}",
                exc_info=True,
            )
            return self._get_basic_fallback_analysis_structure(str(e))

    def _get_basic_fallback_analysis_structure(
        self, error_message: str
    ) -> Dict[str, Any]:
        """Returns a minimal AI analysis structure in case of errors during _perform_ai_analysis."""
        return {
            "error": error_message,
            "topic": "unknown",
            "sentiment": "neutral",
            "intent": "unknown",
            "urgency": "low",
            "confidence": 0.0,
            "keywords": [],
            "categories": ["unknown"],
            "reasoning": f"Fallback due to error: {error_message}",
            "suggested_labels": ["unknown"],
            "risk_flags": ["analysis_failed"],
            "action_items": [],  # Added missing action_items
        }

    def _convert_to_db_format(
        self, gmail_metadata: GmailMessage, ai_analysis_result: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Convert Gmail metadata and AI analysis (if available) to database format."""

        ai_topic = "unknown"
        ai_confidence = 0.0
        analysis_metadata_payload = {}

        if ai_analysis_result:
            ai_topic = ai_analysis_result.get("topic", "unknown")
            ai_confidence = ai_analysis_result.get("confidence", 0.0)
            # Ensure all expected keys from ai_analysis_result are included for analysisMetadata
            analysis_metadata_payload["ai_analysis"] = {
                "topic": ai_topic,  # This is the raw topic string from AI
                "sentiment": ai_analysis_result.get("sentiment", "neutral"),
                "intent": ai_analysis_result.get("intent", "unknown"),
                "urgency": ai_analysis_result.get("urgency", "low"),
                "confidence": ai_confidence,
                "categories": ai_analysis_result.get(
                    "categories", []
                ),  # Raw AI category suggestions
                "keywords": ai_analysis_result.get("keywords", []),
                "reasoning": ai_analysis_result.get("reasoning", ""),
                "suggested_labels": ai_analysis_result.get("suggested_labels", []),
                "risk_flags": ai_analysis_result.get("risk_flags", []),
                "action_items": ai_analysis_result.get("action_items", []),
                "category_id": ai_analysis_result.get(
                    "category_id"
                ),  # This is the matched DB category ID
            }
        else:
            # Handle case where AI analysis was skipped or failed
            analysis_metadata_payload["ai_analysis"] = (
                self._get_basic_fallback_analysis_structure(
                    "AI analysis not performed or failed"
                )
            )
            ai_topic = analysis_metadata_payload["ai_analysis"][
                "topic"
            ]  # Fallback topic
            ai_confidence = analysis_metadata_payload["ai_analysis"][
                "confidence"
            ]  # Fallback confidence

        # category_id now comes directly from ai_analysis_result if matching was successful
        category_id = analysis_metadata_payload["ai_analysis"].get("category_id")

        # Common metadata to include regardless of AI analysis success/failure
        analysis_metadata_payload.update(
            {
                "importance_markers": gmail_metadata.importance_markers,
                "thread_info": gmail_metadata.thread_info,
                "custom_headers": gmail_metadata.custom_headers,
                "attachments_summary": [
                    {"filename": att.get("filename"), "size": att.get("size")}
                    for att in gmail_metadata.attachments
                ],
            }
        )

        db_email = {
            # Core identifiers
            "messageId": gmail_metadata.message_id,
            "threadId": gmail_metadata.thread_id,
            "historyId": gmail_metadata.history_id,
            # Basic properties (maintain backward compatibility)
            "sender": gmail_metadata.from_address.split("<")[0].strip(' "'),
            "senderEmail": gmail_metadata.from_address,
            "subject": gmail_metadata.subject,
            "content": gmail_metadata.body_plain or gmail_metadata.snippet,
            "contentHtml": gmail_metadata.body_html,
            "preview": (
                (gmail_metadata.snippet[:200] + "...")
                if gmail_metadata.snippet and len(gmail_metadata.snippet) > 200
                else gmail_metadata.snippet
            ),
            "snippet": gmail_metadata.snippet,
            "time": gmail_metadata.date or datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "internalDate": gmail_metadata.internal_date,
            # Recipients
            "toAddresses": gmail_metadata.to_addresses,
            "ccAddresses": gmail_metadata.cc_addresses,
            "bccAddresses": gmail_metadata.bcc_addresses,
            "replyTo": gmail_metadata.reply_to,
            # Gmail-specific properties
            "labelIds": gmail_metadata.label_ids,
            "labels": gmail_metadata.labels,
            "category": gmail_metadata.category,
            # Message state
            "isUnread": gmail_metadata.is_unread,
            "isStarred": gmail_metadata.is_starred,
            "isImportant": gmail_metadata.is_important,
            "isDraft": gmail_metadata.is_draft,
            "isSent": gmail_metadata.is_sent,
            "isSpam": gmail_metadata.is_spam,
            "isTrash": gmail_metadata.is_trash,
            "isChat": gmail_metadata.is_chat,
            # Content properties
            "hasAttachments": gmail_metadata.has_attachments,
            "attachmentCount": len(gmail_metadata.attachments),
            "sizeEstimate": gmail_metadata.size_estimate,
            # Security and authentication
            "spfStatus": gmail_metadata.spf_status,
            "dkimStatus": gmail_metadata.dkim_status,
            "dmarcStatus": gmail_metadata.dmarc_status,
            "isEncrypted": gmail_metadata.encryption_info.get("tls_encrypted", False)
            or gmail_metadata.encryption_info.get("end_to_end_encrypted", False),
            "isSigned": gmail_metadata.encryption_info.get("signed", False),
            # Priority and handling
            "priority": gmail_metadata.priority,
            "isAutoReply": gmail_metadata.auto_reply,
            "mailingList": gmail_metadata.mailing_list,
            # Thread and conversation
            "inReplyTo": gmail_metadata.in_reply_to,
            "references": gmail_metadata.references,
            "isFirstInThread": gmail_metadata.thread_info.get("is_first_message", True),
            # AI analysis results
            "category_id": category_id,  # Use the resolved category_id from AI analysis
            "confidence": int(ai_confidence * 100),  # Use confidence from AI analysis
            "analysisMetadata": json.dumps(analysis_metadata_payload),
            "isRead": not gmail_metadata.is_unread,
        }

        return db_email

    async def train_models_from_gmail_data(
        self, training_query: str = "newer_than:30d", max_training_emails: int = 5000
    ) -> Dict[str, Any]:
        self.logger.info(
            f"Starting model training from Gmail data. Query: {training_query}, Max emails: {max_training_emails}"
        )
        try:
            training_batch = await self.collector.collect_emails_incremental(
                query_filter=training_query, max_emails=max_training_emails
            )

            # Extract and preprocess training samples
            training_samples = []
            for gmail_msg in training_batch.messages:
                try:
                    metadata = self.metadata_extractor.extract_complete_metadata(
                        gmail_msg
                    )
                    training_format = self.metadata_extractor.to_training_format(
                        metadata
                    )

                    sample_dict = {
                        "subject": training_format["subject"],
                        "content": training_format["content"],
                        "sender": training_format["sender_email"],
                        "labels": {
                            "topic": self._infer_topic_from_metadata(metadata),
                            "sentiment": self._infer_sentiment_from_metadata(metadata),
                            "intent": self._infer_intent_from_metadata(metadata),
                            "urgency": self._infer_urgency_from_metadata(metadata),
                        },
                    }
                    training_samples.append(sample_dict)
                except Exception as e:
                    self.logger.warning(
                        f"Skipping training sample due to processing error: {e}",
                        exc_info=True,
                    )
                    continue

            if not training_samples:
                self.logger.warning(
                    "No training samples collected, aborting model training."
                )
                return {
                    "success": False,
                    "error": "No training samples collected.",
                    "training_samples_count": 0,
                }

            training_results = {}
            topic_config = ModelConfig(
                model_type="topic_modeling",
                algorithm="naive_bayes",
                hyperparameters={"smoothing": 1.0},
                feature_set=[
                    "word_count",
                    "sentiment_score",
                    "urgency_score",
                    "business_terms",
                ],
                training_data_version="gmail_v1.0",
            )

            features, labels = self.model_trainer.prepare_training_data(
                training_samples, "topic"
            )
            if features and labels:
                topic_result = self.model_trainer.train_naive_bayes(
                    features, labels, topic_config
                )
                training_results["topic_model"] = {
                    "model_id": topic_result.model_id,
                    "accuracy": topic_result.accuracy,
                    "f1_score": topic_result.f1_score,
                }

            sentiment_config = ModelConfig(
                model_type="sentiment_analysis",
                algorithm="logistic_regression",
                hyperparameters={"learning_rate": 0.01, "epochs": 100},
                feature_set=[
                    "sentiment_score",
                    "positive_word_count",
                    "negative_word_count",
                ],
                training_data_version="gmail_v1.0",
            )

            features, labels = self.model_trainer.prepare_training_data(
                training_samples, "sentiment"
            )
            if features and labels:
                sentiment_result = self.model_trainer.train_logistic_regression(
                    features, labels, sentiment_config
                )
                training_results["sentiment_model"] = {
                    "model_id": sentiment_result.model_id,
                    "accuracy": sentiment_result.accuracy,
                    "f1_score": sentiment_result.f1_score,
                }

            prompt_templates = (
                self.prompt_engineer.generate_email_classification_prompts()
            )
            training_results["prompt_templates"] = list(prompt_templates.keys())

            return {
                "success": True,
                "training_samples_count": len(training_samples),
                "models_trained": training_results,
                "training_timestamp": datetime.now().isoformat(),
            }
        except Exception as e:
            self.logger.error(f"Model training failed: {e}", exc_info=True)
            return {"success": False, "error": str(e), "training_samples_count": 0}

    def _infer_topic_from_metadata(self, metadata: GmailMessage) -> str:
        """Infer topic from Gmail metadata and labels"""
        # Use Gmail categories as topic indicators
        if metadata.category == "primary":
            # Look at labels and content for more specific classification
            if any(label in ["CATEGORY_PERSONAL"] for label in metadata.label_ids):
                return "personal_family"
            elif metadata.mailing_list or any(
                word in metadata.subject.lower()
                for word in ["newsletter", "promotion", "offer"]
            ):
                return "promotions"
            else:
                return "work_business"
        elif metadata.category == "social":
            return "personal_family"
        elif metadata.category == "promotions":
            return "promotions"
        elif metadata.category == "updates":
            # Could be financial or business updates
            if any(
                word in metadata.subject.lower()
                for word in ["bank", "payment", "invoice", "statement"]
            ):
                return "finance_banking"
            else:
                return "work_business"
        else:
            return "work_business"  # Default

    def _infer_sentiment_from_metadata(self, metadata: GmailMessage) -> str:
        """Infer sentiment from Gmail metadata"""
        # Check importance and star status
        if metadata.is_important and metadata.is_starred:
            return "positive"
        elif metadata.is_spam or metadata.is_trash:
            return "negative"
        else:
            return "neutral"

    def _infer_intent_from_metadata(self, metadata: GmailMessage) -> str:
        """Infer intent from Gmail metadata"""
        subject_lower = metadata.subject.lower()

        if any(word in subject_lower for word in ["?", "question", "help", "how"]):
            return "question"
        elif any(
            word in subject_lower
            for word in ["confirmation", "confirm", "booking", "receipt"]
        ):
            return "confirmation"
        elif any(word in subject_lower for word in ["request", "please", "need"]):
            return "request"
        elif metadata.mailing_list or "newsletter" in subject_lower:
            return "information"
        else:
            return "information"  # Default

    def _infer_urgency_from_metadata(self, metadata: GmailMessage) -> str:
        """Infer urgency from Gmail metadata"""
        subject_lower = metadata.subject.lower()

        if metadata.is_important or any(
            word in subject_lower
            for word in ["urgent", "asap", "emergency", "critical"]
        ):
            return "high"
        elif any(word in subject_lower for word in ["today", "tomorrow", "deadline"]):
            return "medium"
        else:
            return "low"

    def get_processing_statistics(self) -> Dict[str, Any]:
        """Get comprehensive processing statistics"""
        return {
            "processing_stats": self.stats,
            "rate_limiter_stats": {
                "tokens_available": getattr(self.collector.rate_limiter, "tokens", 0),
                "requests_in_window": len(
                    getattr(self.collector.rate_limiter, "request_times", [])
                ),
            },
            "cache_stats": {"cache_enabled": True},
        }

    # --- Methods moved from backend GmailAIService ---
    async def execute_smart_retrieval(
        self,
        strategies: List[str] = None,
        max_api_calls: int = 100,
        time_budget_minutes: int = 30,
    ) -> Dict[str, Any]:
        """Execute smart Gmail retrieval with multiple strategies using smart_retrieval.py script."""
        self.logger.info(
            f"Executing smart retrieval. Strategies: {strategies}, Max API calls: {max_api_calls}, Budget: {time_budget_minutes}min"
        )
        try:
            cmd = [
                sys.executable,
                self.retrieval_script,
                "--execute-strategies",
                "--max-api-calls",
                str(max_api_calls),
                "--time-budget",
                str(time_budget_minutes),
            ]
            if strategies:
                cmd.extend(["--strategies"] + strategies)

            result = await self._execute_async_command(cmd, cwd=self.nlp_path)

            if not result.get(
                "success"
            ):  # Check success from _execute_async_command's perspective
                self.logger.error(
                    f"Smart retrieval script execution failed or reported an error. Result: {result}"
                )
                return {
                    "success": False,
                    "strategiesExecuted": result.get("strategies_executed", []),
                    "totalEmails": result.get("total_emails", 0),
                    "performance": result.get("performance", {}),
                    "error": result.get(
                        "error", "Smart retrieval script execution failed."
                    ),
                }

            # If _execute_async_command was successful, 'result' contains the script's output.
            # The script itself should ideally also have a 'success' field in its JSON output.
            return {
                "success": result.get(
                    "success", True
                ),  # Prioritize script's success flag if present, else True
                "strategiesExecuted": result.get("strategies_executed", []),
                "totalEmails": result.get("total_emails", 0),
                "performance": result.get("performance", {}),
                "error": result.get(
                    "error"
                ),  # Pass along any error reported by the script
                "data": result,  # Include full script result for more details
            }
        except Exception as e:
            self.logger.error(
                f"Smart retrieval task failed unexpectedly: {e}", exc_info=True
            )
            return {
                "success": False,
                "strategiesExecuted": [],
                "totalEmails": 0,
                "performance": {},
                "error": str(e),
            }

    async def get_retrieval_strategies(self) -> List[Dict[str, Any]]:
        """Get available retrieval strategies from smart_retrieval.py script."""
        self.logger.info("Fetching retrieval strategies.")
        try:
            cmd = [sys.executable, self.retrieval_script, "--list-strategies"]
            result = await self._execute_async_command(cmd, cwd=self.nlp_path)

            if result.get("success") and "strategies" in result.get(
                "data", result
            ):  # Check success and if 'strategies' is in result or result.data
                # _execute_async_command might return {'success':True, 'data': [...] } for non-dict JSON
                return (
                    result.get("data", result).get("strategies", [])
                    if isinstance(result.get("data", result), dict)
                    else result.get("data", [])
                )

            error_msg = result.get(
                "error",
                "Failed to get strategies: No 'strategies' key in script response or script error.",
            )
            self.logger.error(error_msg)
            return []
        except Exception as e:
            self.logger.error(
                f"Failed to get retrieval strategies unexpectedly: {e}", exc_info=True
            )
            return []

    async def get_performance_metrics(self) -> Optional[Dict[str, Any]]:
        """Get Gmail API performance metrics from smart_retrieval.py script."""
        self.logger.info("Fetching performance metrics.")
        try:
            cmd = [sys.executable, self.retrieval_script, "--get-performance"]
            result = await self._execute_async_command(cmd, cwd=self.nlp_path)

            if result.get("success"):  # Script command execution was successful
                # Adapt script output (which is in 'result' dict) to the expected structure
                # If script's JSON output has 'success':false, it will be caught by result.get('success', True)
                # in the calling function, but here we assume the structure based on a successful script run.
                return {
                    "overallStatus": {
                        "status": result.get("status", "healthy"),
                        "avgEfficiency": result.get("avg_efficiency", 0.0),
                        "activeStrategies": result.get("active_strategies", 0),
                    },
                    "quotaStatus": {
                        "dailyUsage": {
                            "percentage": result.get("quota_used_percent", 0)
                        }
                    },
                    "alerts": result.get("alerts", []),
                    "recommendations": result.get("recommendations", []),
                    "raw_data": result,  # Include full script output for debugging or richer info
                }
            else:
                error_msg = result.get(
                    "error",
                    "Failed to get performance metrics: Script error or no data.",
                )
                self.logger.error(error_msg)
                return None
        except Exception as e:
            self.logger.error(
                f"Failed to get performance metrics unexpectedly: {e}", exc_info=True
            )
            return None


async def main():
    # Setup basic logging for the main example
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    # Get a logger for the main function
    main_logger = logging.getLogger(
        __name__
    )  # This will use the root logger if not further specified

    # For testing, if AdvancedAIEngine is required, you'd mock it or instantiate it:
    # from server.python_backend.ai_engine import AdvancedAIEngine
    # from server.python_backend.database import DatabaseManager
    # advanced_ai_engine_instance = AdvancedAIEngine()
    # db_manager_instance = DatabaseManager() # Needs DATABASE_URL
    # service = GmailAIService(advanced_ai_engine=advanced_ai_engine_instance, db_manager=db_manager_instance)

    # Simplified instantiation for example, may not fully work if DB_URL is not set
    service = GmailAIService()
    main_logger.info("Starting example usage of GmailAIService...")
    # Sync recent emails with AI analysis
    # Reduced max_emails for quicker testing, set include_ai_analysis to False if NLP models aren't set up
    sync_result = await service.sync_gmail_emails(
        query_filter="newer_than:1d",
        max_emails=2,  # Very few for testing
        include_ai_analysis=True,  # Set to True to test the new _perform_ai_analysis flow
    )
    main_logger.info(
        f"Sync result success: {sync_result.get('success')}, Processed: {sync_result.get('processed_count')}"
    )
    if not sync_result.get("success"):
        main_logger.error(f"Sync error: {sync_result.get('error')}")

    # --- Test moved methods ---
    # These require smart_retrieval.py to be present and executable in the same directory.
    # For a unit test, you'd mock _execute_async_command.
    # For an integration test, you need the script.

    # Example: Create a dummy smart_retrieval.py for testing
    # File: server/python_nlp/smart_retrieval.py
    # #!/usr/bin/env python
    # import json
    # import sys
    # if __name__ == "__main__":
    #     if '--list-strategies' in sys.argv:
    #         print(json.dumps({"success": True, "strategies": [{"name": "test_strat", "description": "A test strategy"}]}))
    #     elif '--execute-strategies' in sys.argv:
    #         print(json.dumps({"success": True, "strategies_executed": ["test_exec"], "total_emails": 5, "performance": {"avg_time": 0.1}}))
    #     elif '--get-performance' in sys.argv:
    #         print(json.dumps({"success": True, "avg_efficiency": 0.95, "active_strategies": 1, "quota_used_percent": 10}))
    #     else:
    #         print(json.dumps({"success": False, "error": "Unknown command"}))

    main_logger.info("Testing get_retrieval_strategies...")
    strategies = await service.get_retrieval_strategies()
    main_logger.info(f"Retrieved strategies: {strategies}")

    main_logger.info("Testing execute_smart_retrieval...")
    retrieval_result = await service.execute_smart_retrieval(
        strategies=["test_strat"], max_api_calls=10, time_budget_minutes=5
    )
    main_logger.info(f"Smart retrieval result: {retrieval_result}")

    main_logger.info("Testing get_performance_metrics...")
    performance = await service.get_performance_metrics()
    main_logger.info(f"Performance metrics: {performance}")

    stats = service.get_processing_statistics()
    main_logger.info(f"Final processing statistics: {stats}")


if __name__ == "__main__":
    asyncio.run(main())
