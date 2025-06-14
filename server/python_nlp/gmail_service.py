"""
Comprehensive Gmail Integration Service
Combines metadata extraction, rate limiting, and AI training for complete email processing
"""

import asyncio
import json
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
import logging
import os # Added
import subprocess # Added
import sys # Added

from server.python_backend.ai_engine import AdvancedAIEngine, AIAnalysisResult # Added
from .gmail_integration import GmailDataCollector, EmailBatch, RateLimitConfig
from .gmail_metadata import GmailMetadataExtractor, GmailMessage
# from .data_strategy import DataCollectionStrategy, EmailSample # Removed as it's no longer used
# Removed ModelTrainer, PromptEngineer, ModelConfig imports as they are replaced by AdvancedAIEngine
# from .ai_training import ModelTrainer, PromptEngineer, ModelConfig


class GmailAIService:
    """Complete Gmail integration with AI processing and metadata extraction"""
    
    def __init__(self, advanced_ai_engine: AdvancedAIEngine, rate_config: Optional[RateLimitConfig] = None): # Modified
        self.collector = GmailDataCollector(rate_config)
        self.metadata_extractor = GmailMetadataExtractor()
        # self.data_strategy = DataCollectionStrategy() # Removed
        self.advanced_ai_engine = advanced_ai_engine # Ensure it's assigned
        # self.model_trainer = ModelTrainer() # Removed
        # self.prompt_engineer = PromptEngineer() # Removed
        # Changed for more specific logger name
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")

        # Added path definitions for scripts
        self.nlp_path = os.path.dirname(__file__)
        self.retrieval_script = os.path.join(self.nlp_path, 'smart_retrieval.py')
        
        # Processing statistics
        self.stats = {
            'total_processed': 0,
            'successful_extractions': 0,
            'failed_extractions': 0,
            'ai_analyses_completed': 0,
            'last_sync': None
        }

    # Added _execute_async_command method
    async def _execute_async_command(self, cmd: List[str], cwd: Optional[str] = None) -> Dict[str, Any]:
        """
        Execute command asynchronously.
        Returns a dictionary with 'success': True/False and other command output.
        """
        try:
            self.logger.debug(f"Executing async command: {' '.join(cmd)} in {cwd or '.'}")
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=cwd
            )

            stdout, stderr = await process.communicate()
            stdout_decoded = stdout.decode().strip() if stdout else ""
            stderr_decoded = stderr.decode().strip() if stderr else ""

            if process.returncode != 0:
                error_msg = stderr_decoded or stdout_decoded or "Unknown error during command execution."
                self.logger.error(f"Async command failed (return code {process.returncode}): {cmd}. Error: {error_msg}")
                return {"success": False, "error": error_msg, "return_code": process.returncode}

            if stdout_decoded:
                try:
                    parsed_output = json.loads(stdout_decoded)
                    if isinstance(parsed_output, dict) and 'success' not in parsed_output:
                        # If script provides JSON dict but no 'success' field, assume true as command didn't fail
                        parsed_output['success'] = True
                    elif not isinstance(parsed_output, dict): # Handle cases where script returns non-dict JSON (e.g. list, string)
                         return {"success": True, "data": parsed_output}
                    return parsed_output
                except json.JSONDecodeError as e:
                    self.logger.warning(f"Command {cmd} output was not valid JSON, but command succeeded. Output: {stdout_decoded[:200]}...")
                    return {"success": True, "output": stdout_decoded, "error": f"Non-JSON output: {str(e)}"} # Script success, but output not JSON
            else:
                self.logger.info(f"Command {cmd} executed successfully with no stdout.")
                return {"success": True, "output": ""} # Script success, no output

        except FileNotFoundError as e:
            self.logger.error(f"Async command failed: Executable not found for {cmd}. Error: {e}")
            return {"success": False, "error": f"Executable not found: {cmd[0]}. {str(e)}"}
        except PermissionError as e:
            self.logger.error(f"Async command failed: Permission denied for {cmd}. Error: {e}")
            return {"success": False, "error": f"Permission denied for {cmd[0]}. {str(e)}"}
        except Exception as e:
            self.logger.error(f"Generic async command execution failed for {cmd}: {e}", exc_info=True)
            return {"success": False, "error": str(e)}
    
    async def sync_gmail_emails(
        self, 
        query_filter: str = "newer_than:7d",
        max_emails: int = 1000,
        include_ai_analysis: bool = True
    ) -> Dict[str, Any]:
        """
        Comprehensive Gmail sync with metadata extraction and AI analysis
        """
        self.logger.info(f"Starting Gmail sync with filter: {query_filter}, max_emails: {max_emails}")
        
        try:
            email_batch = await self.collector.collect_emails_incremental(
                query_filter=query_filter,
                max_emails=max_emails
            )
            
            processed_emails = []
            
            # Process each email for complete metadata extraction
            for gmail_msg in email_batch.messages:
                try:
                    gmail_metadata = self.metadata_extractor.extract_complete_metadata(gmail_msg)
                    training_sample = self.metadata_extractor.to_training_format(gmail_metadata)
                    
                    if include_ai_analysis:
                        ai_analysis = await self._perform_ai_analysis(training_sample)
                        training_sample['ai_analysis'] = ai_analysis
                    
                    db_email = self._convert_to_db_format(gmail_metadata, training_sample)
                    processed_emails.append(db_email)
                    self.stats['successful_extractions'] += 1
                    
                except Exception as e:
                    self.logger.error(f"Failed to process email {gmail_msg.get('id', 'unknown')}: {e}", exc_info=True)
                    self.stats['failed_extractions'] += 1
                    continue
            
            self.stats['total_processed'] += len(processed_emails)
            self.stats['last_sync'] = datetime.now().isoformat()
            
            return {
                'success': True,
                'processed_count': len(processed_emails),
                'emails': processed_emails,
                'batch_info': {
                    'batch_id': email_batch.batch_id,
                    'query_filter': email_batch.query_filter,
                    'timestamp': email_batch.timestamp.isoformat()
                },
                'statistics': self.stats.copy()
            }
            
        except Exception as e:
            self.logger.error(f"Gmail sync failed: {e}", exc_info=True)
            return {
                'success': False,
                'error': str(e),
                'processed_count': 0,
                'emails': [],
                'statistics': self.stats.copy()
            }
    
    async def _perform_ai_analysis(self, email_sample: Dict[str, Any]) -> Dict[str, Any]:
        """Perform comprehensive AI analysis on email sample using AdvancedAIEngine"""
        try:
            if not self.advanced_ai_engine:
                self.logger.error("AdvancedAIEngine not initialized for AI analysis.")
                return { 'error': 'AdvancedAIEngine not available', 'topic': 'unknown', 'sentiment': 'neutral', 'intent': 'information', 'urgency': 'low', 'confidence': 0.0 }

            subject = email_sample.get('subject', '')
            content = email_sample.get('content', '')
            
            # Call AdvancedAIEngine
            ai_result_obj: AIAnalysisResult = await self.advanced_ai_engine.analyze_email(subject=subject, content=content)
            analysis_result = ai_result_obj.to_dict() # Convert AIAnalysisResult to dictionary
            
            # Ensure processing_timestamp is part of the successful analysis result
            analysis_result['processing_timestamp'] = datetime.now().isoformat()
            
            self.stats['ai_analyses_completed'] += 1
            return analysis_result
            
        except Exception as e:
            self.logger.error(f"AI analysis failed for email {email_sample.get('id', 'unknown')}: {e}", exc_info=True)
            # Return a default error structure that matches AIAnalysisResult.to_dict() or is acceptable downstream
            return {
                'error': str(e),
                'topic': 'unknown', 'sentiment': 'neutral', 'intent': 'information', 'urgency': 'low',
                'confidence': 0.0, 'keywords': [], 'entities': [], 'reasoning': '',
                'suggested_labels': [], 'risk_flags': [], 'category_id': None,
                'processing_timestamp': datetime.now().isoformat()
            }
    
    def _convert_to_db_format(self, gmail_metadata: GmailMessage, training_sample: Dict[str, Any]) -> Dict[str, Any]: # training_sample contains ai_analysis result
        """Convert Gmail metadata and AI analysis to database format"""
        
        ai_analysis_data = training_sample.get('ai_analysis', {})

        # Determine category ID based on AI analysis
        # The category_id might now be directly available from ai_analysis_data if AdvancedAIEngine provides it
        category_id = ai_analysis_data.get('category_id')
        if category_id is None: # Fallback to mapping if not directly provided
            category_id = self._map_topic_to_category_id(ai_analysis_data.get('topic', 'unknown'))
        
        # Create comprehensive database record
        db_email = {
            # Core identifiers
            'messageId': gmail_metadata.message_id,
            'threadId': gmail_metadata.thread_id,
            'historyId': gmail_metadata.history_id,
            
            # Basic properties (maintain backward compatibility)
            'sender': gmail_metadata.from_address.split('<')[0].strip(' "'),
            'senderEmail': gmail_metadata.from_address,
            'subject': gmail_metadata.subject,
            'content': gmail_metadata.body_plain or gmail_metadata.snippet,
            'contentHtml': gmail_metadata.body_html,
            'preview': (gmail_metadata.snippet[:200] + '...') if gmail_metadata.snippet and len(gmail_metadata.snippet) > 200 else gmail_metadata.snippet,
            'snippet': gmail_metadata.snippet,
            'time': gmail_metadata.date or datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'internalDate': gmail_metadata.internal_date,
            
            # Recipients
            'toAddresses': gmail_metadata.to_addresses,
            'ccAddresses': gmail_metadata.cc_addresses,
            'bccAddresses': gmail_metadata.bcc_addresses,
            'replyTo': gmail_metadata.reply_to,
            
            # Gmail-specific properties
            'labelIds': gmail_metadata.label_ids,
            'labels': gmail_metadata.labels,
            'category': gmail_metadata.category,
            
            # Message state
            'isUnread': gmail_metadata.is_unread,
            'isStarred': gmail_metadata.is_starred,
            'isImportant': gmail_metadata.is_important,
            'isDraft': gmail_metadata.is_draft,
            'isSent': gmail_metadata.is_sent,
            'isSpam': gmail_metadata.is_spam,
            'isTrash': gmail_metadata.is_trash,
            'isChat': gmail_metadata.is_chat,
            
            # Content properties
            'hasAttachments': gmail_metadata.has_attachments,
            'attachmentCount': len(gmail_metadata.attachments),
            'sizeEstimate': gmail_metadata.size_estimate,
            
            # Security and authentication
            'spfStatus': gmail_metadata.spf_status,
            'dkimStatus': gmail_metadata.dkim_status,
            'dmarcStatus': gmail_metadata.dmarc_status,
            'isEncrypted': gmail_metadata.encryption_info.get('tls_encrypted', False) or gmail_metadata.encryption_info.get('end_to_end_encrypted', False),
            'isSigned': gmail_metadata.encryption_info.get('signed', False),
            
            # Priority and handling
            'priority': gmail_metadata.priority,
            'isAutoReply': gmail_metadata.auto_reply,
            'mailingList': gmail_metadata.mailing_list,
            
            # Thread and conversation
            'inReplyTo': gmail_metadata.in_reply_to,
            'references': gmail_metadata.references,
            'isFirstInThread': gmail_metadata.thread_info.get('is_first_message', True),
            
            # AI analysis results
            'categoryId': category_id, # Updated to use category_id from ai_analysis_data or mapping
            'confidence': int(ai_analysis_data.get('confidence', 0) * 100), # Use ai_analysis_data
            'analysisMetadata': json.dumps({ # Ensure all relevant ai_analysis_data is included
                'ai_analysis': ai_analysis_data,
                'importance_markers': gmail_metadata.importance_markers,
                'thread_info': gmail_metadata.thread_info,
                'custom_headers': gmail_metadata.custom_headers,
                'attachments': gmail_metadata.attachments
            }),
            
            'isRead': not gmail_metadata.is_unread
        }
        
        return db_email
    
    def _map_topic_to_category_id(self, topic: str) -> Optional[int]:
        """Map AI-detected topic to database category ID"""
        topic_mappings = {
            'work_business': 1, 'personal_family': 2, 'finance_banking': 3,
            'promotions': 4, 'travel': 5, 'healthcare': 6
        }
        return topic_mappings.get(topic.lower())
    
    async def train_models_from_gmail_data(
        self, training_query: str = "newer_than:30d", max_training_emails: int = 5000
    ) -> Dict[str, Any]:
        self.logger.info(f"Starting model training from Gmail data. Query: {training_query}, Max emails: {max_training_emails}")
        try:
            training_batch = await self.collector.collect_emails_incremental(
                query_filter=training_query,
                max_emails=max_training_emails
            )
            
            training_samples = []
            for gmail_msg in training_batch.messages:
                try:
                    metadata = self.metadata_extractor.extract_complete_metadata(gmail_msg)
                    # Convert metadata to a simpler format suitable for training,
                    # AdvancedAIEngine.train_models will handle the detailed preparation.
                    sample_dict = {
                        'id': metadata.message_id, # Include an ID
                        'subject': metadata.subject,
                        'content': metadata.body_plain or metadata.snippet, # Prefer plain text
                        'sender_email': metadata.from_address,
                        'timestamp': metadata.date, # Or internal_date
                        'label_ids': metadata.label_ids, # Pass existing labels, training script might use them
                        'category': metadata.category # Pass existing category
                    }
                    # Add any other relevant raw fields that the training process might find useful
                    if metadata.to_addresses:
                        sample_dict['to_addresses'] = metadata.to_addresses
                    if metadata.cc_addresses:
                        sample_dict['cc_addresses'] = metadata.cc_addresses

                    training_samples.append(sample_dict)
                except Exception as e:
                    self.logger.warning(f"Skipping training sample for email ID {gmail_msg.get('id', 'unknown')} due to processing error: {e}", exc_info=True)
                    continue
            
            if not training_samples:
                 self.logger.warning("No training samples collected, aborting model training.")
                 return {'success': False, 'error': 'No training samples collected.', 'training_samples_count': 0}

            # Call AdvancedAIEngine to train models
            # Ensure self.advanced_ai_engine is available
            if not self.advanced_ai_engine:
                self.logger.error("AdvancedAIEngine not initialized in GmailAIService for training.")
                return {'success': False, 'error': 'AdvancedAIEngine not initialized.'}

            training_results = await self.advanced_ai_engine.train_models(training_emails=training_samples)
            
            # The return structure from AdvancedAIEngine.train_models is:
            # { "success": True/False, "modelsTrained": [], "trainingAccuracy": {}, ..., "error": str(e) }
            # Adapt this to the existing return structure of train_models_from_gmail_data or decide on a new one.
            # For now, largely pass through, ensuring 'success' key is present.
            return {
                'success': training_results.get('success', False),
                'training_samples_count': len(training_samples),
                'models_trained_details': training_results, # Pass through the detailed results
                'error': training_results.get('error'),
                'training_timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            self.logger.error(f"Model training failed: {e}", exc_info=True)
            return {'success': False, 'error': str(e), 'training_samples_count': 0}

    # Obsolete helper methods _infer_topic_from_metadata, _infer_sentiment_from_metadata,
    # _infer_intent_from_metadata, _infer_urgency_from_metadata, and _infer_labels_for_training
    # have been removed as this logic is now centralized in AdvancedAIEngine or its underlying scripts.

    def get_processing_statistics(self) -> Dict[str, Any]:
        """Get comprehensive processing statistics"""
        return {
            'processing_stats': self.stats,
            'rate_limiter_stats': {
                'tokens_available': getattr(self.collector.rate_limiter, 'tokens', 0),
                'requests_in_window': len(getattr(self.collector.rate_limiter, 'request_times', []))
            },
            'cache_stats': {'cache_enabled': True }
        }

    # --- Methods moved from backend GmailAIService ---
    async def execute_smart_retrieval(
        self, strategies: List[str] = None, max_api_calls: int = 100, time_budget_minutes: int = 30
    ) -> Dict[str, Any]:
        """Execute smart Gmail retrieval with multiple strategies using smart_retrieval.py script."""
        self.logger.info(f"Executing smart retrieval. Strategies: {strategies}, Max API calls: {max_api_calls}, Budget: {time_budget_minutes}min")
        try:
            cmd = [sys.executable, self.retrieval_script, '--execute-strategies',
                   '--max-api-calls', str(max_api_calls), '--time-budget', str(time_budget_minutes)]
            if strategies:
                cmd.extend(['--strategies'] + strategies)

            result = await self._execute_async_command(cmd, cwd=self.nlp_path)

            if not result.get("success"): # Check success from _execute_async_command's perspective
                self.logger.error(f"Smart retrieval script execution failed or reported an error. Result: {result}")
                return {
                    "success": False,
                    "strategiesExecuted": result.get('strategies_executed', []),
                    "totalEmails": result.get('total_emails', 0),
                    "performance": result.get('performance', {}),
                    "error": result.get('error', "Smart retrieval script execution failed.")
                }

            # If _execute_async_command was successful, 'result' contains the script's output.
            # The script itself should ideally also have a 'success' field in its JSON output.
            return {
                "success": result.get('success', True), # Prioritize script's success flag if present, else True
                "strategiesExecuted": result.get('strategies_executed', []),
                "totalEmails": result.get('total_emails', 0),
                "performance": result.get('performance', {}),
                "error": result.get("error"), # Pass along any error reported by the script
                "data": result # Include full script result for more details
            }
        except Exception as e:
            self.logger.error(f"Smart retrieval task failed unexpectedly: {e}", exc_info=True)
            return {"success": False, "strategiesExecuted": [], "totalEmails": 0, "performance": {}, "error": str(e)}

    async def get_retrieval_strategies(self) -> List[Dict[str, Any]]:
        """Get available retrieval strategies from smart_retrieval.py script."""
        self.logger.info("Fetching retrieval strategies.")
        try:
            cmd = [sys.executable, self.retrieval_script, '--list-strategies']
            result = await self._execute_async_command(cmd, cwd=self.nlp_path)

            if result.get("success") and 'strategies' in result.get('data', result): # Check success and if 'strategies' is in result or result.data
                # _execute_async_command might return {'success':True, 'data': [...] } for non-dict JSON
                return result.get('data', result).get('strategies', []) if isinstance(result.get('data', result), dict) else result.get('data', [])

            error_msg = result.get('error', "Failed to get strategies: No 'strategies' key in script response or script error.")
            self.logger.error(error_msg)
            return []
        except Exception as e:
            self.logger.error(f"Failed to get retrieval strategies unexpectedly: {e}", exc_info=True)
            return []

    async def get_performance_metrics(self) -> Optional[Dict[str, Any]]:
        """Get Gmail API performance metrics from smart_retrieval.py script."""
        self.logger.info("Fetching performance metrics.")
        try:
            cmd = [sys.executable, self.retrieval_script, '--get-performance']
            result = await self._execute_async_command(cmd, cwd=self.nlp_path)

            if result.get("success"): # Script command execution was successful
                # Adapt script output (which is in 'result' dict) to the expected structure
                # If script's JSON output has 'success':false, it will be caught by result.get('success', True)
                # in the calling function, but here we assume the structure based on a successful script run.
                return {
                    "overallStatus": {
                        "status": result.get('status', "healthy"),
                        "avgEfficiency": result.get('avg_efficiency', 0.0),
                        "activeStrategies": result.get('active_strategies', 0)
                    },
                    "quotaStatus": {
                        "dailyUsage": {"percentage": result.get('quota_used_percent', 0)}
                    },
                    "alerts": result.get('alerts', []),
                    "recommendations": result.get('recommendations', []),
                    "raw_data": result # Include full script output for debugging or richer info
                }
            else:
                error_msg = result.get('error', "Failed to get performance metrics: Script error or no data.")
                self.logger.error(error_msg)
                return None
        except Exception as e:
            self.logger.error(f"Failed to get performance metrics unexpectedly: {e}", exc_info=True)
            return None

async def main():
    # Setup basic logging for the main example
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # Get a logger for the main function
    main_logger = logging.getLogger(__name__) # This will use the root logger if not further specified

    # --- Updated main function for AdvancedAIEngine ---
    # Ensure AdvancedAIEngine is imported if it's not already at the top
    # from server.python_backend.ai_engine import AdvancedAIEngine

    ai_engine = AdvancedAIEngine()
    # It's important that ai_engine is initialized if it has an async setup method.
    # Assuming AdvancedAIEngine() instantiation is synchronous and
    # its methods handle internal initialization if needed, or it has an explicit init method.
    # If AdvancedAIEngine has an async initialize() method:
    # await ai_engine.initialize() # This needs to be called within an async context.

    # Pass the AdvancedAIEngine instance to GmailAIService
    # service = GmailAIService(advanced_ai_engine=ai_engine) # This line will be inside main()
    
    main_logger.info("Starting example usage of GmailAIService...")
    # Sync recent emails with AI analysis
    # include_ai_analysis should now leverage the AdvancedAIEngine
    # Set include_ai_analysis to True to test the new integration.
    # Ensure AdvancedAIEngine is configured and its models are available if analysis is to succeed.
    # sync_result = await service.sync_gmail_emails( # This line will be inside main()
    #     query_filter="newer_than:1d",
    #     max_emails=2,
    #     include_ai_analysis=True
    # )
    # main_logger.info(f"Sync result success: {sync_result.get('success')}, Processed: {sync_result.get('processed_count')}")
    # if not sync_result.get('success'): # This line will be inside main()
    #     main_logger.error(f"Sync error: {sync_result.get('error')}")

    # --- Test moved methods ---
    # These require smart_retrieval.py to be present and executable in the same directory.
    
    # main_logger.info("Testing get_retrieval_strategies...") # This line will be inside main()
    # strategies = await service.get_retrieval_strategies() # This line will be inside main()
    # main_logger.info(f"Retrieved strategies: {strategies}") # This line will be inside main()

    # main_logger.info("Testing execute_smart_retrieval...") # This line will be inside main()
    # retrieval_result = await service.execute_smart_retrieval(strategies=["test_strat"], max_api_calls=10, time_budget_minutes=5) # This line will be inside main()
    # main_logger.info(f"Smart retrieval result: {retrieval_result}") # This line will be inside main()

    # main_logger.info("Testing get_performance_metrics...") # This line will be inside main()
    # performance = await service.get_performance_metrics() # This line will be inside main()
    # main_logger.info(f"Performance metrics: {performance}") # This line will be inside main()
    
    # stats = service.get_processing_statistics() # This line will be inside main()
    # main_logger.info(f"Final processing statistics: {stats}") # This line will be inside main()

if __name__ == "__main__":
    # Wrap main execution in an async function to use await for ai_engine.initialize()
    async def run_main():
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        main_logger_local = logging.getLogger(__name__) # Use a local logger for main

        main_logger_local.info("Initializing AdvancedAIEngine...")
        ai_engine_instance = AdvancedAIEngine()
        try:
            await ai_engine_instance.initialize() # Initialize the AI engine
            main_logger_local.info("AdvancedAIEngine initialized successfully.")
        except Exception as e:
            main_logger_local.error(f"Failed to initialize AdvancedAIEngine: {e}", exc_info=True)
            return # Exit if AI engine fails to initialize

        service_instance = GmailAIService(advanced_ai_engine=ai_engine_instance)
        main_logger_local.info("GmailAIService instantiated with AdvancedAIEngine.")

        main_logger_local.info("Starting example usage of GmailAIService...")

        sync_result = await service_instance.sync_gmail_emails(
            query_filter="newer_than:1d",
            max_emails=2,
            include_ai_analysis=True # Test with AI analysis enabled
        )
        main_logger_local.info(f"Sync result success: {sync_result.get('success')}, Processed: {sync_result.get('processed_count')}")
        if not sync_result.get('success'):
            main_logger_local.error(f"Sync error: {sync_result.get('error')}")

        # You can uncomment these other test calls if smart_retrieval.py is set up
        # main_logger_local.info("Testing get_retrieval_strategies...")
        # strategies = await service_instance.get_retrieval_strategies()
        # main_logger_local.info(f"Retrieved strategies: {strategies}")

        # main_logger_local.info("Testing execute_smart_retrieval...")
        # retrieval_result = await service_instance.execute_smart_retrieval(strategies=["test_strat"], max_api_calls=10, time_budget_minutes=5)
        # main_logger_local.info(f"Smart retrieval result: {retrieval_result}")

        # main_logger_local.info("Testing get_performance_metrics...")
        # performance = await service_instance.get_performance_metrics()
        # main_logger_local.info(f"Performance metrics: {performance}")

        stats = service_instance.get_processing_statistics()
        main_logger_local.info(f"Final processing statistics: {stats}")

    asyncio.run(run_main())