"""
Pydantic Models for Gmail AI Email Management
Data validation and serialization models
"""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, validator


# Enums
class EmailPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class SentimentType(str, Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"


class ActivityType(str, Enum):
    LABEL = "label"
    CATEGORIZE = "categorize"
    FILTER = "filter"
    SYNC = "sync"
    ANALYZE = "analyze"


# Base Models
class EmailBase(BaseModel):
    sender: str = Field(..., min_length=1, max_length=255)
    senderEmail: str = Field(..., pattern=r"^[^@]+@[^@]+\.[^@]+$")
    subject: str = Field(..., min_length=1)
    content: str = Field(..., min_length=1)
    time: datetime


class EmailCreate(EmailBase):
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

    @validator("preview", always=True)
    def set_preview(cls, v, values):
        if not v and "content" in values:
            return (
                values["content"][:200] + "..."
                if len(values["content"]) > 200
                else values["content"]
            )
        return v


class EmailUpdate(BaseModel):
    subject: Optional[str] = None
    content: Optional[str] = None
    categoryId: Optional[int] = None
    labels: Optional[List[str]] = None
    isImportant: Optional[bool] = None
    isStarred: Optional[bool] = None
    isUnread: Optional[bool] = None
    isRead: Optional[bool] = None


class EmailResponse(EmailBase):
    id: int
    messageId: Optional[str]
    threadId: Optional[str]
    preview: str
    category: Optional[str]
    categoryId: Optional[int]
    labels: List[str]
    confidence: int = Field(ge=0, le=100)
    isImportant: bool
    isStarred: bool
    isUnread: bool
    hasAttachments: bool
    attachmentCount: int
    sizeEstimate: int
    aiAnalysis: Dict[str, Any] = Field(default_factory=dict)
    filterResults: Dict[str, Any] = Field(default_factory=dict)


# Category Models
class CategoryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    color: str = Field(default="#6366f1", pattern=r"^#[0-9A-Fa-f]{6}$")


class CategoryCreate(CategoryBase):
    pass


class CategoryResponse(CategoryBase):
    id: int
    count: int = 0


# Activity Models
class ActivityBase(BaseModel):
    type: ActivityType
    description: str = Field(..., min_length=1)
    emailId: Optional[int] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ActivityCreate(ActivityBase):
    pass


class ActivityResponse(ActivityBase):
    id: int
    emailSubject: Optional[str] = None
    createdAt: datetime


# AI Analysis Models
class AIAnalysisResponse(BaseModel):
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

    class Config:
        validate_by_name = True


# Models moved from main.py for Action Item Extraction
class ActionExtractionRequest(BaseModel):
    subject: Optional[str] = None
    content: str


class ActionItem(BaseModel):
    action_phrase: str
    verb: Optional[str] = None
    object: Optional[str] = None
    raw_due_date_text: Optional[str] = None
    context: str


# Gmail Sync Models
class GmailSyncRequest(BaseModel):
    maxEmails: int = Field(default=500, ge=1, le=5000)
    queryFilter: str = "newer_than:1d"
    includeAIAnalysis: bool = True
    strategies: List[str] = Field(default_factory=list)
    timeBudgetMinutes: int = Field(default=15, ge=1, le=120)


class GmailSyncResponse(BaseModel):
    success: bool
    processedCount: int
    emailsCreated: int = 0
    errorsCount: int = 0
    batchInfo: Dict[str, Any]
    statistics: Dict[str, Any]
    error: Optional[str] = None


# Smart Retrieval Models
class SmartRetrievalRequest(BaseModel):
    strategies: List[str] = Field(default_factory=list)
    maxApiCalls: int = Field(default=100, ge=1, le=1000)
    timeBudgetMinutes: int = Field(default=30, ge=1, le=180)


class RetrievalStrategy(BaseModel):
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
    fromPatterns: Optional[List[str]] = Field(alias="from_patterns")
    subjectKeywords: Optional[List[str]] = Field(alias="subject_keywords")
    contentKeywords: Optional[List[str]] = Field(alias="content_keywords")
    excludePatterns: Optional[List[str]] = Field(alias="exclude_patterns")
    timeSensitivity: Optional[str] = Field(alias="time_sensitivity")

    class Config:
        validate_by_name = True


class EmailFilterActions(BaseModel):
    addLabel: Optional[str] = Field(alias="add_label")
    markImportant: bool = Field(default=False, alias="mark_important")
    markRead: bool = Field(default=False, alias="mark_read")
    archive: bool = False
    forwardTo: Optional[str] = Field(alias="forward_to")
    autoReply: bool = Field(default=False, alias="auto_reply")

    class Config:
        validate_by_name = True


class FilterRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    criteria: EmailFilterCriteria
    actions: EmailFilterActions
    priority: int = Field(default=5, ge=1, le=10)


class FilterResponse(BaseModel):
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

    class Config:
        validate_by_name = True


# Performance Models
class PerformanceMetric(BaseModel):
    metricType: str = Field(alias="metric_type")
    metricName: str = Field(alias="metric_name")
    metricValue: float = Field(alias="metric_value")
    metadata: Dict[str, Any] = Field(default_factory=dict)
    recordedAt: datetime = Field(alias="recorded_at")

    class Config:
        validate_by_name = True


class QuotaStatus(BaseModel):
    dailyUsage: Dict[str, Any] = Field(alias="daily_usage")
    hourlyUsage: Dict[str, Any] = Field(alias="hourly_usage")
    projectedDailyUsage: int = Field(alias="projected_daily_usage")

    class Config:
        validate_by_name = True


class PerformanceAlert(BaseModel):
    type: str
    strategy: str
    message: str
    severity: str
    timestamp: datetime


class PerformanceRecommendation(BaseModel):
    type: str
    strategy: str
    priority: str
    recommendation: str
    expectedImprovement: str = Field(alias="expected_improvement")
    action: str

    class Config:
        validate_by_name = True


class PerformanceOverview(BaseModel):
    timestamp: datetime
    overallStatus: Dict[str, Any] = Field(alias="overall_status")
    quotaStatus: QuotaStatus = Field(alias="quota_status")
    strategyPerformance: List[Dict[str, Any]] = Field(alias="strategy_performance")
    alerts: List[PerformanceAlert]
    recommendations: List[PerformanceRecommendation]

    class Config:
        validate_by_name = True


# Dashboard Models
class WeeklyGrowth(BaseModel):
    emails: int
    percentage: float


class DashboardStats(BaseModel):
    totalEmails: int = Field(alias="total_emails")
    autoLabeled: int = Field(alias="auto_labeled")
    categories: int
    timeSaved: str = Field(alias="time_saved")
    weeklyGrowth: WeeklyGrowth = Field(alias="weekly_growth")

    class Config:
        validate_by_name = True


# Training Models
class TrainingRequest(BaseModel):
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

    class Config:
        validate_by_name = True


class TrainingResponse(BaseModel):
    success: bool
    modelsTrained: List[str] = Field(alias="models_trained")
    trainingAccuracy: Dict[str, float] = Field(alias="training_accuracy")
    validationAccuracy: Dict[str, float] = Field(alias="validation_accuracy")
    trainingTime: float = Field(alias="training_time")
    emailsProcessed: int = Field(alias="emails_processed")
    error: Optional[str] = None

    class Config:
        validate_by_name = True


# Health Check Models
class ServiceHealth(BaseModel):
    status: str = Field(pattern=r"^(healthy|degraded|unhealthy)$")
    error: Optional[str] = None
    timestamp: datetime
    responseTime: Optional[float] = Field(alias="response_time")

    class Config:
        validate_by_name = True


class SystemHealth(BaseModel):
    status: str
    timestamp: datetime
    version: str = "2.0.0"
    services: Dict[str, ServiceHealth]
    uptime: Optional[float] = None


# Search Models
class SearchRequest(BaseModel):
    query: str = Field(..., min_length=1)
    category: Optional[int] = None
    dateFrom: Optional[datetime] = Field(alias="date_from")
    dateTo: Optional[datetime] = Field(alias="date_to")
    labels: Optional[List[str]] = None
    isImportant: Optional[bool] = Field(alias="is_important")
    isUnread: Optional[bool] = Field(alias="is_unread")
    limit: int = Field(default=50, ge=1, le=200)
    offset: int = Field(default=0, ge=0)

    class Config:
        validate_by_name = True


class SearchResponse(BaseModel):
    emails: List[EmailResponse]
    totalCount: int = Field(alias="total_count")
    hasMore: bool = Field(alias="has_more")
    searchTime: float = Field(alias="search_time")

    class Config:
        validate_by_name = True


# Batch Operations
class BatchEmailUpdate(BaseModel):
    emailIds: List[int] = Field(alias="email_ids", min_items=1)
    updates: EmailUpdate

    class Config:
        validate_by_name = True


class BatchOperationResponse(BaseModel):
    success: bool
    processedCount: int = Field(alias="processed_count")
    successCount: int = Field(alias="success_count")
    errorCount: int = Field(alias="error_count")
    errors: List[Dict[str, Any]] = Field(default_factory=list)

    class Config:
        validate_by_name = True
