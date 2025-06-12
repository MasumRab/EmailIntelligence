"""
Comprehensive Gmail Integration Service
Combines metadata extraction, rate limiting, and AI training for complete email processing
"""

import asyncio
import json
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
import logging

from .gmail_integration import GmailDataCollector, EmailBatch, RateLimitConfig
from .gmail_metadata import GmailMetadataExtractor, GmailMessage
from .data_strategy import DataCollectionStrategy, EmailSample
from .ai_training import ModelTrainer, PromptEngineer, ModelConfig

class GmailAIService:
    """Complete Gmail integration with AI processing and metadata extraction"""
    
    def __init__(self, rate_config: Optional[RateLimitConfig] = None):
        self.collector = GmailDataCollector(rate_config)
        self.metadata_extractor = GmailMetadataExtractor()
        self.data_strategy = DataCollectionStrategy()
        self.model_trainer = ModelTrainer()
        self.prompt_engineer = PromptEngineer()
        self.logger = logging.getLogger(__name__)
        
        # Processing statistics
        self.stats = {
            'total_processed': 0,
            'successful_extractions': 0,
            'failed_extractions': 0,
            'ai_analyses_completed': 0,
            'last_sync': None
        }
    
    async def sync_gmail_emails(
        self, 
        query_filter: str = "newer_than:7d",
        max_emails: int = 1000,
        include_ai_analysis: bool = True
    ) -> Dict[str, Any]:
        """
        Comprehensive Gmail sync with metadata extraction and AI analysis
        """
        self.logger.info(f"Starting Gmail sync with filter: {query_filter}")
        
        try:
            # Collect emails with rate limiting
            email_batch = await self.collector.collect_emails_incremental(
                query_filter=query_filter,
                max_emails=max_emails
            )
            
            processed_emails = []
            
            # Process each email for complete metadata extraction
            for gmail_msg in email_batch.messages:
                try:
                    # Extract complete Gmail metadata
                    gmail_metadata = self.metadata_extractor.extract_complete_metadata(gmail_msg)
                    
                    # Convert to training format for AI analysis
                    training_sample = self.metadata_extractor.to_training_format(gmail_metadata)
                    
                    # Perform AI analysis if requested
                    if include_ai_analysis:
                        ai_analysis = await self._perform_ai_analysis(training_sample)
                        training_sample['ai_analysis'] = ai_analysis
                    
                    # Convert to database format
                    db_email = self._convert_to_db_format(gmail_metadata, training_sample)
                    processed_emails.append(db_email)
                    
                    self.stats['successful_extractions'] += 1
                    
                except Exception as e:
                    self.logger.error(f"Failed to process email {gmail_msg.get('id', 'unknown')}: {e}")
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
                'statistics': self.stats
            }
            
        except Exception as e:
            self.logger.error(f"Gmail sync failed: {e}")
            return {
                'success': False,
                'error': str(e),
                'processed_count': 0,
                'emails': [],
                'statistics': self.stats
            }
    
    async def _perform_ai_analysis(self, email_sample: Dict[str, Any]) -> Dict[str, Any]:
        """Perform comprehensive AI analysis on email sample"""
        try:
            # Prepare text for analysis
            text_content = f"{email_sample.get('subject', '')} {email_sample.get('content', '')}"
            
            # Create email sample for data strategy processing
            sample = EmailSample(
                id=email_sample['id'],
                subject=email_sample['subject'],
                content=email_sample['content'],
                sender=email_sample['sender_email'],
                timestamp=email_sample['timestamp'],
                labels={},
                metadata={}
            )
            
            # Preprocess and annotate
            processed_sample = self.data_strategy.preprocess_email(sample)
            annotation = self.data_strategy.annotate_email(processed_sample)
            
            # Extract features for model training
            features = self.model_trainer.feature_extractor.extract_features(text_content)
            
            analysis_result = {
                'topic': annotation.topic,
                'sentiment': annotation.sentiment,
                'intent': annotation.intent,
                'urgency': annotation.urgency,
                'confidence': annotation.confidence,
                'keywords': annotation.keywords,
                'entities': annotation.entities,
                'reasoning': annotation.reasoning,
                'suggested_labels': annotation.suggested_labels,
                'risk_flags': annotation.risk_flags,
                'features': features,
                'processing_timestamp': datetime.now().isoformat()
            }
            
            self.stats['ai_analyses_completed'] += 1
            return analysis_result
            
        except Exception as e:
            self.logger.error(f"AI analysis failed for email {email_sample.get('id', 'unknown')}: {e}")
            return {
                'error': str(e),
                'topic': 'unknown',
                'sentiment': 'neutral',
                'intent': 'information',
                'urgency': 'low',
                'confidence': 0.0
            }
    
    def _convert_to_db_format(self, gmail_metadata: GmailMessage, training_sample: Dict[str, Any]) -> Dict[str, Any]:
        """Convert Gmail metadata and AI analysis to database format"""
        
        # Determine category ID based on AI analysis
        category_id = self._map_topic_to_category_id(
            training_sample.get('ai_analysis', {}).get('topic', 'unknown')
        )
        
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
            'preview': gmail_metadata.snippet[:200] + '...' if len(gmail_metadata.snippet) > 200 else gmail_metadata.snippet,
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
            'categoryId': category_id,
            'confidence': int(training_sample.get('ai_analysis', {}).get('confidence', 0) * 100),
            'analysisMetadata': json.dumps({
                'ai_analysis': training_sample.get('ai_analysis', {}),
                'importance_markers': gmail_metadata.importance_markers,
                'thread_info': gmail_metadata.thread_info,
                'custom_headers': gmail_metadata.custom_headers,
                'attachments': gmail_metadata.attachments
            }),
            
            # Legacy compatibility
            'isRead': not gmail_metadata.is_unread
        }
        
        return db_email
    
    def _map_topic_to_category_id(self, topic: str) -> Optional[int]:
        """Map AI-detected topic to database category ID"""
        topic_mappings = {
            'work_business': 1,
            'personal_family': 2, 
            'finance_banking': 3,
            'promotions': 4,
            'travel': 5,
            'healthcare': 6
        }
        return topic_mappings.get(topic)
    
    async def train_models_from_gmail_data(
        self, 
        training_query: str = "newer_than:30d",
        max_training_emails: int = 5000
    ) -> Dict[str, Any]:
        """Train AI models using Gmail data"""
        
        self.logger.info("Starting model training from Gmail data")
        
        try:
            # Collect training data
            training_batch = await self.collector.collect_emails_incremental(
                query_filter=training_query,
                max_emails=max_training_emails
            )
            
            # Extract and preprocess training samples
            training_samples = []
            for gmail_msg in training_batch.messages:
                try:
                    metadata = self.metadata_extractor.extract_complete_metadata(gmail_msg)
                    training_format = self.metadata_extractor.to_training_format(metadata)
                    
                    # Create structured training sample
                    sample_dict = {
                        'subject': training_format['subject'],
                        'content': training_format['content'],
                        'sender': training_format['sender_email'],
                        'labels': {
                            'topic': self._infer_topic_from_metadata(metadata),
                            'sentiment': self._infer_sentiment_from_metadata(metadata),
                            'intent': self._infer_intent_from_metadata(metadata),
                            'urgency': self._infer_urgency_from_metadata(metadata)
                        }
                    }
                    training_samples.append(sample_dict)
                    
                except Exception as e:
                    self.logger.warning(f"Failed to process training sample: {e}")
                    continue
            
            # Train models for different tasks
            training_results = {}
            
            # Topic modeling
            topic_config = ModelConfig(
                model_type='topic_modeling',
                algorithm='naive_bayes',
                hyperparameters={'smoothing': 1.0},
                feature_set=['word_count', 'sentiment_score', 'urgency_score', 'business_terms'],
                training_data_version='gmail_v1.0'
            )
            
            features, labels = self.model_trainer.prepare_training_data(training_samples, 'topic')
            topic_result = self.model_trainer.train_naive_bayes(features, labels, topic_config)
            training_results['topic_model'] = {
                'model_id': topic_result.model_id,
                'accuracy': topic_result.accuracy,
                'f1_score': topic_result.f1_score
            }
            
            # Sentiment analysis
            sentiment_config = ModelConfig(
                model_type='sentiment_analysis',
                algorithm='logistic_regression',
                hyperparameters={'learning_rate': 0.01, 'epochs': 100},
                feature_set=['sentiment_score', 'positive_word_count', 'negative_word_count'],
                training_data_version='gmail_v1.0'
            )
            
            features, labels = self.model_trainer.prepare_training_data(training_samples, 'sentiment')
            sentiment_result = self.model_trainer.train_logistic_regression(features, labels, sentiment_config)
            training_results['sentiment_model'] = {
                'model_id': sentiment_result.model_id,
                'accuracy': sentiment_result.accuracy,
                'f1_score': sentiment_result.f1_score
            }
            
            # Generate optimized prompts
            prompt_templates = self.prompt_engineer.generate_email_classification_prompts()
            training_results['prompt_templates'] = list(prompt_templates.keys())
            
            return {
                'success': True,
                'training_samples_count': len(training_samples),
                'models_trained': training_results,
                'training_timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Model training failed: {e}")
            return {
                'success': False,
                'error': str(e),
                'training_samples_count': 0
            }
    
    def _infer_topic_from_metadata(self, metadata: GmailMessage) -> str:
        """Infer topic from Gmail metadata and labels"""
        # Use Gmail categories as topic indicators
        if metadata.category == 'primary':
            # Look at labels and content for more specific classification
            if any(label in ['CATEGORY_PERSONAL'] for label in metadata.label_ids):
                return 'personal_family'
            elif metadata.mailing_list or any(word in metadata.subject.lower() for word in ['newsletter', 'promotion', 'offer']):
                return 'promotions'
            else:
                return 'work_business'
        elif metadata.category == 'social':
            return 'personal_family'
        elif metadata.category == 'promotions':
            return 'promotions'
        elif metadata.category == 'updates':
            # Could be financial or business updates
            if any(word in metadata.subject.lower() for word in ['bank', 'payment', 'invoice', 'statement']):
                return 'finance_banking'
            else:
                return 'work_business'
        else:
            return 'work_business'  # Default
    
    def _infer_sentiment_from_metadata(self, metadata: GmailMessage) -> str:
        """Infer sentiment from Gmail metadata"""
        # Check importance and star status
        if metadata.is_important and metadata.is_starred:
            return 'positive'
        elif metadata.is_spam or metadata.is_trash:
            return 'negative'
        else:
            return 'neutral'
    
    def _infer_intent_from_metadata(self, metadata: GmailMessage) -> str:
        """Infer intent from Gmail metadata"""
        subject_lower = metadata.subject.lower()
        
        if any(word in subject_lower for word in ['?', 'question', 'help', 'how']):
            return 'question'
        elif any(word in subject_lower for word in ['confirmation', 'confirm', 'booking', 'receipt']):
            return 'confirmation'
        elif any(word in subject_lower for word in ['request', 'please', 'need']):
            return 'request'
        elif metadata.mailing_list or 'newsletter' in subject_lower:
            return 'information'
        else:
            return 'information'  # Default
    
    def _infer_urgency_from_metadata(self, metadata: GmailMessage) -> str:
        """Infer urgency from Gmail metadata"""
        subject_lower = metadata.subject.lower()
        
        if metadata.is_important or any(word in subject_lower for word in ['urgent', 'asap', 'emergency', 'critical']):
            return 'high'
        elif any(word in subject_lower for word in ['today', 'tomorrow', 'deadline']):
            return 'medium'
        else:
            return 'low'
    
    def get_processing_statistics(self) -> Dict[str, Any]:
        """Get comprehensive processing statistics"""
        return {
            'processing_stats': self.stats,
            'rate_limiter_stats': {
                'tokens_available': getattr(self.collector.rate_limiter, 'tokens', 0),
                'requests_in_window': len(getattr(self.collector.rate_limiter, 'request_times', []))
            },
            'cache_stats': {
                # Could add cache hit/miss ratios here
                'cache_enabled': True
            }
        }

async def main():
    """Example usage of Gmail AI Service"""
    service = GmailAIService()
    
    # Sync recent emails with AI analysis
    result = await service.sync_gmail_emails(
        query_filter="newer_than:1d",
        max_emails=50,
        include_ai_analysis=True
    )
    
    print(f"Sync result: {result['success']}")
    print(f"Processed emails: {result['processed_count']}")
    
    # Train models
    training_result = await service.train_models_from_gmail_data(
        training_query="newer_than:7d",
        max_training_emails=500
    )
    
    print(f"Training result: {training_result['success']}")
    if training_result['success']:
        print(f"Models trained: {list(training_result['models_trained'].keys())}")
    
    # Get statistics
    stats = service.get_processing_statistics()
    print(f"Processing statistics: {stats}")

if __name__ == "__main__":
    asyncio.run(main())