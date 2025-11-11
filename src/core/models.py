"""
Pydantic Models for the Email Intelligence Platform
Data validation and serialization models for the core application and modules.
"""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field, validator

# A default color for categories, can be moved to a config file later
DEFAULT_CATEGORY_COLOR = "#FFFFFF"


# Enums
class EmailPriority(str, Enum):
    """Enumeration for the priority levels of an email."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class SentimentType(str, Enum):
    """Enumeration for the sentiment types of an email."""

    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"


class ActivityType(str, Enum):
    """Enumeration for different types of activities recorded in the system."""

    LABEL = "label"
    CATEGORIZE = "categorize"
    FILTER = "filter"
    SYNC = "sync"
    ANALYZE = "analyze"


# Base Models
class EmailBase(BaseModel):
    """Base model for an email, containing common core fields."""

    sender: str = Field(..., min_length=1, max_length=255)
    senderEmail: str = Field(..., pattern=r"^[^@]+@[^@]+\.[^@]+$")
    subject: str = Field(..., min_length=1)
    content: str = Field(..., min_length=1)
    time: datetime


class EmailCreate(EmailBase):
    """Model for creating a new email record."""

    messageId: Optional[str] = None
    threadId: Optional[str] = None
    contentHtml: Optional[str] = None
    preview: Optional[str] = None
    labels: List[str] = Field(default_factory=list)
    isImportant: bool = False
    isStarred: bool = False
    isUnread: bool = True
    hasAttachments: bool = False
    attachmentCount: int = 0
    sizeEstimate: int = 0

    @validator("preview", pre=True)
    @classmethod
    def set_preview(cls, v, values):
        """Sets the preview from the content if not provided."""
        if not v and values and "content" in values:
            content = values["content"]
            return content[:200] + "..." if len(content) > 200 else content
        return v


class EmailUpdate(BaseModel):
    """Model for updating an existing email record."""

    subject: Optional[str] = None
    content: Optional[str] = None
    categoryId: Optional[int] = None
    labels: Optional[List[str]] = None
    isImportant: Optional[bool] = None
    isStarred: Optional[bool] = None
    isUnread: Optional[bool] = None
    isRead: Optional[bool] = None


class EmailResponse(BaseModel):
    """Model for the response when an email is retrieved."""

    id: int
    messageId: Optional[str]
    threadId: Optional[str]
    sender: str
    senderEmail: str
    subject: str
    content: str
    time: datetime
    preview: str
    category: Optional[str]
    categoryId: Optional[int]
    labels: List[str]
    confidence: int
    isImportant: bool
    isStarred: bool
    isUnread: bool
    hasAttachments: bool
    attachmentCount: int
    sizeEstimate: int
    aiAnalysis: Dict[str, Any]
    filterResults: Dict[str, Any]


# Category Models
class CategoryBase(BaseModel):
    """Base model for an email category."""

    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    color: str = Field(default=DEFAULT_CATEGORY_COLOR, pattern=r"^#[0-9A-Fa-f]{6}$")


class CategoryCreate(CategoryBase):
    """Model for creating a new category."""

    pass


class CategoryResponse(CategoryBase):
    """Model for the response when a category is retrieved."""

    id: int
    count: int = 0


# Activity Models
class ActivityBase(BaseModel):
    """Base model for a system activity record."""

    type: ActivityType
    description: str = Field(..., min_length=1)
    emailId: Optional[int] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ActivityCreate(ActivityBase):
    """Model for creating a new activity record."""

    pass


class ActivityResponse(ActivityBase):
    """Model for the response when an activity is retrieved."""

    id: int
    emailSubject: Optional[str] = None
    createdAt: datetime


# AI Analysis Models
class AIAnalysisRequest(BaseModel):
    """Model for a request to analyze an email with AI."""
    subject: str
    content: str
    models: Optional[Dict[str, str]] = None


class AIAnalysisResponse(BaseModel):
    """Model representing the detailed output of an AI email analysis."""

    topic: str
    sentiment: SentimentType
    intent: str
    urgency: EmailPriority
    confidence: float = Field(ge=0.0, le=1.0)
    categories: List[str]
    keywords: List[str]
    reasoning: str
    suggestedLabels: List[str] = Field(alias="suggested_labels")
    riskFlags: List[str] = Field(alias="risk_flags")
    categoryId: Optional[int] = None

    model_config = ConfigDict(populate_by_name=True)


class AICategorizeRequest(BaseModel):
    """Model for a request to categorize an email with AI."""
    emailId: int
    autoAnalyze: bool
    categoryId: Optional[int] = None
    confidence: Optional[int] = None


class AICategorizeResponse(BaseModel):
    """Model for the response of an AI categorization request."""
    success: bool
    email: Optional[EmailResponse] = None
    analysis: Optional[AIAnalysisResponse] = None


class AIValidateRequest(BaseModel):
    """Model for a request to validate AI analysis with user feedback."""
    emailId: int
    userFeedback: str
    correctCategory: Optional[str] = None


class AIValidateResponse(BaseModel):
    """Model for the response of an AI validation request."""
    success: bool
    message: str


# Models for Action Item Extraction
class ActionExtractionRequest(BaseModel):
    """Model for a request to extract action items from an email."""

    subject: Optional[str] = None
    content: str


class ActionItem(BaseModel):
    """Model representing a single extracted action item from an email."""

    action_phrase: str
    verb: Optional[str] = None
    object: Optional[str] = None
    raw_due_date_text: Optional[str] = None
    context: str


# Gmail Sync Models
class GmailSyncRequest(BaseModel):
    """Model for a request to synchronize emails from a Gmail account."""

    maxEmails: int = Field(default=500, ge=1, le=5000)
    queryFilter: str = "newer_than:1d"
    includeAIAnalysis: bool = True
    strategies: List[str] = Field(default_factory=list)
    timeBudgetMinutes: int = Field(default=15, ge=1, le=120)


class GmailSyncResponse(BaseModel):
    """Model for the response after a Gmail synchronization task."""

    success: bool
    processedCount: int
    emailsCreated: int = 0
    errorsCount: int = 0
    batchInfo: Dict[str, Any]
    statistics: Dict[str, Any]
    error: Optional[str] = None


# Smart Retrieval Models
class SmartRetrievalRequest(BaseModel):
    """Model for a request to perform a smart retrieval of emails from Gmail."""

    strategies: List[str] = Field(default_factory=list)
    maxApiCalls: int = Field(default=100, ge=1, le=1000)
    timeBudgetMinutes: int = Field(default=30, ge=1, le=180)


class RetrievalStrategy(BaseModel):
    """Model representing a single strategy for smart email retrieval."""

    name: str
    queryFilter: str
    priority: int = Field(ge=1, le=10)
    batchSize: int = Field(ge=1, le=500)
    frequency: str
    maxEmailsPerRun: int = Field(ge=1, le=2000)
    includeFolders: List[str] = Field(default_factory=list)
    excludeFolders: List[str] = Field(default_factory=list)
    dateRangeDays: int = Field(ge=1, le=365)


# Filter Models
class EmailFilterCriteria(BaseModel):
    """Model representing the criteria for an email filter."""

    fromPatterns: Optional[List[str]] = Field(alias="from_patterns")
    subjectKeywords: Optional[List[str]] = Field(alias="subject_keywords")
    contentKeywords: Optional[List[str]] = Field(alias="content_keywords")
    excludePatterns: Optional[List[str]] = Field(alias="exclude_patterns")
    timeSensitivity: Optional[str] = Field(alias="time_sensitivity")

    model_config = ConfigDict(populate_by_name=True)


class EmailFilterActions(BaseModel):
    """Model representing the actions to be taken by an email filter."""

    addLabel: Optional[str] = Field(alias="add_label")
    markImportant: bool = Field(default=False, alias="mark_important")
    markRead: bool = Field(default=False, alias="mark_read")
    archive: bool = False
    forwardTo: Optional[str] = Field(alias="forward_to")
    autoReply: bool = Field(default=False, alias="auto_reply")

    model_config = ConfigDict(populate_by_name=True)


class FilterRequest(BaseModel):
    """Model for a request to create a new email filter."""

    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    criteria: EmailFilterCriteria
    actions: EmailFilterActions
    priority: int = Field(default=5, ge=1, le=10)


class FilterResponse(BaseModel):
    """Model for the response when an email filter is retrieved."""

    filterId: str = Field(alias="filter_id")
    name: str
    description: Optional[str]
    criteria: Dict[str, Any]
    actions: Dict[str, Any]
    priority: int
    effectivenessScore: float = Field(alias="effectiveness_score")
    createdDate: datetime = Field(alias="created_date")
    lastUsed: datetime = Field(alias="last_used")
    usageCount: int = Field(alias="usage_count")
    falsePositiveRate: float = Field(alias="false_positive_rate")
    isActive: bool = Field(alias="is_active")

    model_config = ConfigDict(populate_by_name=True)


# Performance Models
class PerformanceMetric(BaseModel):
    """Model representing a single performance metric record."""

    metricType: str = Field(alias="metric_type")
    metricName: str = Field(alias="metric_name")
    metricValue: float = Field(alias="metric_value")
    metadata: Dict[str, Any] = Field(default_factory=dict)
    recordedAt: datetime = Field(alias="recorded_at")

    model_config = ConfigDict(populate_by_name=True)


class QuotaStatus(BaseModel):
    """Model representing the status of API usage quotas."""

    dailyUsage: Dict[str, Any] = Field(alias="daily_usage")
    hourlyUsage: Dict[str, Any] = Field(alias="hourly_usage")
    projectedDailyUsage: int = Field(alias="projected_daily_usage")

    model_config = ConfigDict(populate_by_name=True)


class PerformanceAlert(BaseModel):
    """Model representing a performance-related alert."""

    type: str
    strategy: str
    message: str
    severity: str
    timestamp: datetime


class PerformanceRecommendation(BaseModel):
    """Model representing a recommendation for improving performance."""

    type: str
    strategy: str
    priority: str
    recommendation: str
    expectedImprovement: str = Field(alias="expected_improvement")
    action: str

    model_config = ConfigDict(populate_by_name=True)


class PerformanceOverview(BaseModel):
    """Model for a comprehensive overview of system performance."""

    timestamp: datetime
    overallStatus: Dict[str, Any] = Field(alias="overall_status")
    quotaStatus: QuotaStatus = Field(alias="quota_status")
    strategyPerformance: List[Dict[str, Any]] = Field(alias="strategy_performance")
    alerts: List[PerformanceAlert]
    recommendations: List[PerformanceRecommendation]

    model_config = ConfigDict(populate_by_name=True)


# Dashboard Models
class WeeklyGrowth(BaseModel):
    """Model representing weekly growth statistics."""

    emails: int
    percentage: float


class DashboardStats(BaseModel):
    """Model for the main statistics displayed on the dashboard."""

    totalEmails: int = Field(alias="total_emails")
    autoLabeled: int = Field(alias="auto_labeled")
    categories: int
    timeSaved: str = Field(alias="time_saved")
    weeklyGrowth: WeeklyGrowth = Field(alias="weekly_growth")

    model_config = ConfigDict(populate_by_name=True)


# Training Models
class TrainingRequest(BaseModel):
    """Model for a request to train the AI models."""

    trainingQuery: str = Field(default="newer_than:30d", alias="training_query")
    maxTrainingEmails: int = Field(
        default=5000, ge=100, le=10000, alias="max_training_emails"
    )
    modelTypes: List[str] = Field(
        default_factory=lambda: ["sentiment", "topic", "intent", "urgency"],
        alias="model_types",
    )
    validationSplit: float = Field(
        default=0.2, ge=0.1, le=0.5, alias="validation_split"
    )

    model_config = ConfigDict(populate_by_name=True)


class TrainingResponse(BaseModel):
    """Model for the response after an AI model training task."""

    success: bool
    modelsTrained: List[str] = Field(alias="models_trained")
    trainingAccuracy: Dict[str, float] = Field(alias="training_accuracy")
    validationAccuracy: Dict[str, float] = Field(alias="validation_accuracy")
    trainingTime: float = Field(alias="training_time")
    emailsProcessed: int = Field(alias="emails_processed")
    error: Optional[str] = None

    model_config = ConfigDict(populate_by_name=True)


# Health Check Models
class ServiceHealth(BaseModel):
    """Model representing the health status of a single service."""

    status: str = Field(pattern=r"^(healthy|degraded|unhealthy)$")
    error: Optional[str] = None
    timestamp: datetime
    responseTime: Optional[float] = Field(alias="response_time")

    model_config = ConfigDict(populate_by_name=True)


class SystemHealth(BaseModel):
    """Model for the overall system health check response."""

    status: str
    timestamp: datetime
    version: str = "2.0.0"
    services: Dict[str, ServiceHealth]
    uptime: Optional[float] = None


# Search Models
class SearchRequest(BaseModel):
    """Model for a request to search for emails."""

    query: str = Field(..., min_length=1)
    category: Optional[int] = None
    dateFrom: Optional[datetime] = Field(alias="date_from")
    dateTo: Optional[datetime] = Field(alias="date_to")
    labels: Optional[List[str]] = None
    isImportant: Optional[bool] = Field(alias="is_important")
    isUnread: Optional[bool] = Field(alias="is_unread")
    limit: int = Field(default=50, ge=1, le=200)
    offset: int = Field(default=0, ge=0)

    model_config = ConfigDict(populate_by_name=True)


class SearchResponse(BaseModel):
    """Model for the response of an email search."""

    emails: List[EmailResponse]
    totalCount: int = Field(alias="total_count")
    hasMore: bool = Field(alias="has_more")
    searchTime: float = Field(alias="search_time")

    model_config = ConfigDict(populate_by_name=True)


# Batch Operations
class BatchEmailUpdate(BaseModel):
    """Model for a request to update a batch of emails."""

    emailIds: List[int] = Field(alias="email_ids")
    updates: EmailUpdate

    @validator("emailIds")
    @classmethod
    def validate_email_ids(cls, v):
        if not v or len(v) < 1:
            raise ValueError("emailIds must contain at least one email ID")
        return v

    model_config = ConfigDict(populate_by_name=True)


class BatchOperationResponse(BaseModel):
    """Model for the response of a batch operation."""

    success: bool
    processedCount: int = Field(alias="processed_count")
    successCount: int = Field(alias="success_count")
    errorCount: int = Field(alias="error_count")
    errors: List[Dict[str, Any]] = Field(default_factory=list)

    model_config = ConfigDict(populate_by_name=True)

# Workflow Models
class WorkflowCreate(BaseModel):
    """Model for creating a new workflow."""
    name: str = Field(..., description="The unique name for the workflow.")
    description: str = ""
    workflow_type: str = Field(
        default="legacy", description="Type of workflow: 'legacy' or 'node_based'"
    )
    models: Dict[str, str] = Field(
        default={},
        description="A dictionary mapping model types to model names for legacy workflows.",
    )
    nodes: List[Dict[str, Any]] = Field(
        default=[], description="List of nodes for node-based workflows."
    )
    connections: List[Dict[str, str]] = Field(
        default=[], description="List of connections for node-based workflows."
    )

# Aliases for backward compatibility
Email = EmailResponse
Category = CategoryResponse
