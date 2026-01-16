# Strategic Refactoring & Redesign Guide

**EmailIntelligence Project**  
**Date:** December 14, 2025  
**Version:** 1.0  
**Status:** Ready for Implementation

---

## Document Purpose

This guide consolidates insights from documentation analysis, outstanding todos, and codebase structure to provide **strategic inline TODOs** that will inform code refactoring and redesign decisions. Each TODO includes context, impact, and implementation strategy.

---

## 1. Architecture & Dependency Management

### 1.1 Eliminate Global State & Singleton Patterns
**Location:** Backend core modules, database managers, AI engines  
**Status:** BLOCKING multiple feature implementations  
**Impact:** High - blocks modularization, testing, and scaling

```python
# TODO: ARCHITECTURE - Refactor global state management
# Current Issue: Database, AI engine, and cache managers use global/singleton patterns
# Impact: Prevents parallel testing, complicates dependency injection, limits scaling
# Implementation: 
#   1. Convert all singleton patterns to dependency injection
#   2. Move initialization to application startup (e.g., FastAPI lifespan)
#   3. Pass dependencies through function parameters, not globals
#   4. Update all factory functions to accept dependency instances
# Priority: P0 (blocks: testing, modularity, CI/CD)
# Affected Files: src/core/database.py, src/core/ai_engine.py, backend/python_backend/database.py
# Related Tasks: task-database-refactoring-1, task-architecture-improvement-1
```

**Why This Matters:**
- Blocks unit testing (can't isolate components)
- Prevents running tests in parallel
- Makes dependency injection inconsistent
- Complicates feature development and debugging

**Implementation Order:**
1. Database manager (affects all data operations)
2. AI engine (affects analysis pipeline)
3. Cache manager (affects performance)
4. Config manager (affects initialization)

---

### 1.2 Standardize Factory Pattern Implementation
**Location:** All factory functions across codebase  
**Status:** Inconsistently implemented  
**Impact:** Medium - creates confusion, harder to maintain

```python
# TODO: ARCHITECTURE - Standardize factory function patterns
# Current Issue: Different factory implementations in different modules
#   - EmailRepository uses factory, database uses singleton, AI uses global initialization
# Goal: Consistent factory implementation across all modules
# Implementation:
#   1. Define base factory interface/protocol
#   2. Implement factory for: EmailRepository, DataSource, AIEngine, DatabaseManager, CacheManager
#   3. Add factory registry for dependency discovery
#   4. Document factory usage in ARCHITECTURE.md
# Priority: P1 (cleanup, maintainability)
# Dependencies: Must complete 1.1 first
# Acceptance Criteria:
#   - All data source creation uses factory
#   - All service initialization uses factory
#   - Factory registry in place
#   - 100% test coverage for factory functions
```

**Benefits:**
- Consistent dependency creation across codebase
- Easier to add new implementations
- Simpler testing and mocking
- Clear dependency contracts

---

### 1.3 Implement Dependency Injection Container
**Location:** Application initialization, setup scripts  
**Status:** Partially implemented, inconsistent  
**Impact:** Medium-High - simplifies everything downstream

```python
# TODO: ARCHITECTURE - Create DI container for dependency management
# Current State: Manual dependency passing in some places, globals in others
# Goal: Central DI container for all service initialization
# Implementation:
#   1. Create DIContainer class with service registration and resolution
#   2. Register all factories and singletons
#   3. Add configuration-driven service selection (e.g., Notmuch vs SQLite)
#   4. Integrate with FastAPI dependency system
#   5. Add context managers for lifecycle management
# Priority: P1 (enables: testability, configuration, modularity)
# Example Structure:
#   container = DIContainer()
#   container.register('database', DatabaseFactory)
#   container.register('datasource', NotmuchDataSourceFactory)
#   db = container.resolve('database')
# Related: setup/container.py (already exists but incomplete)
# Acceptance Criteria:
#   - All services registered and resolvable
#   - Circular dependency detection
#   - Lazy initialization support
#   - Full test coverage
```

---

## 2. Data Management & Repository Pattern

### 2.1 Complete EmailRepository Integration
**Location:** All data access code  
**Status:** Partial - some modules still bypass repository  
**Impact:** High - affects data consistency, caching, testing

```python
# TODO: DATA - Audit all data access to use EmailRepository
# Current Issue: Some components access database/datasource directly, bypassing repository
# Goal: 100% of data access goes through EmailRepository abstraction
# Implementation:
#   1. Grep for direct database calls (db.query, execute, etc.)
#   2. Create repository methods for each pattern found
#   3. Replace direct calls with repository methods
#   4. Remove any direct datasource instantiation outside factory
#   5. Add audit tests to verify repository usage
# Priority: P0 (data consistency, caching)
# Related Tasks: task-70 (repository pattern integration)
# Files to Audit:
#   - backend/python_backend/routes.py
#   - backend/python_backend/workflow_engine.py
#   - src/core/ai_engine.py
#   - Any dashboard statistics code
# Acceptance Criteria:
#   - No direct database access outside repository
#   - Caching layer working for all queries
#   - Consistent error handling through repository
#   - All tests use mock repository
```

**Why This Matters:**
- Enables query caching (performance)
- Simplifies testing (single mock point)
- Enables data source switching (Notmuch ↔ SQLite)
- Enforces consistent error handling

---

### 2.2 Implement Caching Strategy with Invalidation
**Location:** EmailRepository, DataSource implementations  
**Status:** Partially implemented, no invalidation strategy  
**Impact:** High - affects performance and correctness

```python
# TODO: PERFORMANCE - Implement cache invalidation strategy
# Current State: Caching exists but invalidation is ad-hoc
# Issue: Stale data in cache after writes, no cache coherence strategy
# Goal: Automatic intelligent cache invalidation
# Implementation:
#   1. Define cache key naming convention (resource-id-filter-hash)
#   2. Create cache invalidation registry (tracks which keys depend on which writes)
#   3. Implement write-through cache for mutations
#   4. Add cache warming for common queries
#   5. Add cache metrics (hit rate, eviction rate, staleness)
# Priority: P1 (performance, correctness)
# Strategy Options:
#   A. Time-based: TTL invalidation (simple, may have stale data)
#   B. Event-based: Invalidate on write operations (correct, more complex)
#   C. Hybrid: TTL + event-based with invalidation hints (recommended)
# Pattern:
#   cache.invalidate('email:*:filters')  # Invalidate all emails
#   cache.invalidate_related('email:123', ['thread', 'labels'])
# Acceptance Criteria:
#   - No stale data observed in tests
#   - Cache hit rate > 70% for normal workloads
#   - Cache coherence test suite
#   - Performance metrics dashboard
```

---

### 2.3 Implement Data Source Adapter Pattern
**Location:** Backend datasources, repository  
**Status:** Notmuch and SQLite not fully interchangeable  
**Impact:** Medium - enables flexibility, testing, migration

```python
# TODO: ARCHITECTURE - Create DataSource adapter pattern for true interchangeability
# Current State: Notmuch and SQLite have different capabilities/quirks
# Goal: Transparent datasource switching with adapter pattern
# Implementation:
#   1. Define DataSourceAdapter interface with all required methods
#   2. Create adapters for Notmuch (primary) and SQLite (fallback)
#   3. Add adapter registry for dynamic selection
#   4. Implement feature compatibility checking
#   5. Add performance profiling per adapter
# Priority: P2 (flexibility, testing)
# Adapter Methods to Standardize:
#   - search(query, filters) -> List[Email]
#   - aggregate(group_by, filters) -> Dict
#   - update_labels(email_id, labels)
#   - get_metadata(email_id)
# Configuration:
#   datasource:
#     primary: notmuch    # Try Notmuch first
#     fallback: sqlite    # Fall back to SQLite
#     adaptive: true      # Switch based on availability
# Benefits:
#   - Can test with SQLite (faster, no system deps)
#   - Can migrate from SQLite to Notmuch
#   - Can provide fallback for offline mode
# Acceptance Criteria:
#   - Same test suite passes for both adapters
#   - Performance tests for both adapters
#   - Feature capability matrix
#   - Automatic fallback on error
```

---

## 3. AI & Machine Learning Pipeline

### 3.1 Modularize AI Engine Components
**Location:** src/core/ai_engine.py, backend/python_backend/ai_engine.py  
**Status:** Monolithic, hard to test individual components  
**Impact:** High - blocks AI improvements, testing, customization

```python
# TODO: ML - Break AI engine into pluggable components
# Current Issue: AI engine is monolithic, hard to:
#   - Test individual components
#   - Swap analysis models
#   - Add new analysis types
#   - Monitor component performance
# Goal: Modular AI pipeline with pluggable components
# Architecture:
#   AIEngine (orchestrator)
#     ├── IntentAnalyzer (pluggable)
#     ├── UrgencyAnalyzer (pluggable)
#     ├── SentimentAnalyzer (pluggable)
#     ├── ImportanceAnalyzer (pluggable)
#     └── AnalysisAggregator (combines results)
# Implementation:
#   1. Define AnalysisComponent protocol/interface
#   2. Extract each analysis type into separate component
#   3. Create component registry for discovery
#   4. Add component lifecycle (init, analyze, cleanup)
#   5. Implement error handling per component
#   6. Add component metrics (latency, accuracy, errors)
# Priority: P1 (testability, AI improvements)
# Component Interface:
#   class AnalysisComponent(Protocol):
#     def analyze(email: Email) -> AnalysisResult
#     def supports(feature: str) -> bool
#     def get_metrics() -> Dict[str, float]
# Benefits:
#   - Each component can be tested independently
#   - Can use different models for different components
#   - Can add A/B testing (old vs new analyzer)
#   - Can disable components for performance
# Related Tasks: AI & Machine Learning category (20 tasks)
# Acceptance Criteria:
#   - Each component tested independently
#   - Component registry working
#   - 95%+ test coverage per component
#   - Performance profile per component
#   - Ability to disable components via config
```

---

### 3.2 Implement Model Selection Strategy
**Location:** AI model initialization, training  
**Status:** Hardcoded models, no strategy for selection  
**Impact:** Medium - limits model improvements, A/B testing

```python
# TODO: ML - Create model selection and versioning strategy
# Current State: Models are hardcoded, no versioning or selection strategy
# Goal: Support multiple models, versions, and selection logic
# Implementation:
#   1. Create ModelRegistry with version management
#   2. Implement model selection logic (performance-based, user-preference, A/B)
#   3. Add model compatibility checking
#   4. Create model evaluation framework
#   5. Document model performance profiles
# Priority: P2 (flexibility, optimization)
# Model Registry Structure:
#   ModelRegistry:
#     - register_model(name, version, provider, config)
#     - select_model(criteria) -> Model
#     - evaluate_model(model, test_data) -> Metrics
#     - deprecate_model(name, version)
# Selection Strategies:
#   1. Performance-based: Select highest accuracy model
#   2. Speed-based: Select fastest model meeting quality threshold
#   3. Cost-based: Select cheapest model for accuracy/latency
#   4. A/B-based: Randomly select between models for experimentation
# Configuration:
#   models:
#     intent:
#       primary: "intent-classifier-v2"
#       versions:
#         v1: {accuracy: 0.92, latency_ms: 15}
#         v2: {accuracy: 0.95, latency_ms: 20}
#     urgency:
#       primary: "urgency-classifier-v1"
#       selection_strategy: "performance"  # or "speed", "cost"
# Acceptance Criteria:
#   - Model registry operational
#   - Multiple models loadable and selectable
#   - Evaluation framework working
#   - Performance comparison dashboard
```

---

## 4. Testing & Quality Assurance

### 4.1 Establish Comprehensive Test Strategy
**Location:** tests/, pytest.ini, test configuration  
**Status:** Partial coverage, inconsistent test structure  
**Impact:** High - blocks confidence in changes, refactoring

```python
# TODO: TESTING - Define and implement comprehensive test strategy
# Current State: Tests exist but coverage is uneven, test structure inconsistent
# Goal: Structured test strategy covering all layers
# Test Pyramid:
#   Level 1: Unit Tests (70% of tests)
#     - Test individual functions/components in isolation
#     - Mock all external dependencies
#     - Fast execution (< 5ms per test)
#     - Location: tests/unit/
#   Level 2: Integration Tests (20% of tests)
#     - Test component interactions
#     - Use real or in-memory databases
#     - Test API endpoints with real handlers
#     - Location: tests/integration/
#   Level 3: E2E Tests (10% of tests)
#     - Test complete workflows
#     - May use real external services
#     - Slow but comprehensive
#     - Location: tests/e2e/
# Implementation:
#   1. Create test structure directory (unit, integration, e2e)
#   2. Establish fixtures and mocks library
#   3. Define test naming conventions
#   4. Set up test data builders
#   5. Configure pytest with proper settings
#   6. Add CI/CD integration
# Priority: P0 (foundation for other work)
# Test Coverage Requirements:
#   - Core modules: 95%+
#   - Data layer: 100%
#   - API routes: 90%+
#   - Utilities: 80%+
# Tools/Configuration:
#   - pytest for test runner
#   - pytest-cov for coverage
#   - pytest-mock for mocking
#   - pytest-asyncio for async tests
#   - testfixtures for fixtures
# Acceptance Criteria:
#   - Test structure established
#   - Coverage reports in CI/CD
#   - All new code requires tests
#   - Coverage threshold enforced (85%)
#   - Test duration < 5 minutes
```

---

### 4.2 Create Mocking & Fixture Framework
**Location:** tests/conftest.py, tests/fixtures/  
**Status:** Minimal, ad-hoc mocking  
**Impact:** High - needed for 4.1 (test strategy)

```python
# TODO: TESTING - Build comprehensive mocking and fixture framework
# Current Issue: Each test creates its own mocks, inconsistent setup
# Goal: Centralized, reusable fixtures and mock builders
# Implementation:
#   1. Create fixture library for common objects:
#     - Mock email objects (complete, minimal variants)
#     - Mock datasource with configurable responses
#     - Mock AI engines with preset results
#     - Mock cache implementations
#     - Mock repository implementations
#   2. Create mock builders for complex objects
#   3. Create pytest fixtures for automatic injection
#   4. Create context managers for resource management
#   5. Add factory methods for test data
# Priority: P1 (enables 4.1)
# Fixture Examples:
#   @pytest.fixture
#   def mock_email():
#     return EmailFactory.minimal()  # Fast, minimal email
#   
#   @pytest.fixture
#   def mock_datasource():
#     return MockDataSource(preset_results={...})
#   
#   @pytest.fixture
#   def mock_ai_engine():
#     return MockAIEngine(results={'intent': 'meeting', ...})
# Benefits:
#   - Consistent test setup
#   - Reduces test code duplication
#   - Easier to add new test scenarios
#   - Better readability
# Acceptance Criteria:
#   - Fixtures for all major components
#   - Mock builders for complex objects
#   - Test data factories
#   - Documentation with examples
```

---

### 4.3 Implement Regression Test Suite
**Location:** tests/regression/  
**Status:** Non-existent  
**Impact:** High - prevents bugs from reoccurring

```python
# TODO: TESTING - Create regression test suite for known bugs
# Goal: Prevent previously-fixed bugs from reoccurring
# Implementation:
#   1. Create regression test directory structure
#   2. For each bug fixed, add a test that would catch it
#   3. Automate regression test execution in CI/CD
#   4. Maintain regression test inventory with bug references
# Priority: P1 (prevents regressions)
# Regression Test Template:
#   def test_regression_bug_XXX():
#     \"\"\"
#     Regression test for: [bug description]
#     Bug ID: [issue/PR number]
#     Date Fixed: [date]
#     Root Cause: [brief explanation]
#     \"\"\"
#     # Test that demonstrates the bug is fixed
#     ...
# Examples to Create Tests For:
#   - Global state initialization issues
#   - Cache invalidation problems
#   - Data inconsistency bugs
#   - AI analysis edge cases
#   - Database error handling
# Acceptance Criteria:
#   - Regression test for every fixed bug
#   - All regression tests pass
#   - Regression tests prevent regressions
```

---

## 5. Performance & Optimization

### 5.1 Implement Query Optimization Strategy
**Location:** Data access layer, repository  
**Status:** Ad-hoc, no systematic optimization  
**Impact:** High - affects user experience, scalability

```python
# TODO: PERFORMANCE - Establish query optimization strategy
# Current Issue: No systematic approach to query optimization
# Goal: Identify slow queries and optimize systematically
# Implementation:
#   1. Add query profiling with execution time tracking
#   2. Create slow query log (queries > 100ms)
#   3. Identify N+1 query problems
#   4. Add query result caching with intelligent invalidation
#   5. Implement batch query operations where needed
#   6. Add database indexes for common queries
#   7. Create query performance dashboard
# Priority: P1 (user experience)
# Profiling Setup:
#   - Log all queries with execution time
#   - Group by type/pattern
#   - Alert on slow queries
#   - Track optimization impact
# Common Optimizations:
#   1. Eager loading (load related data together)
#   2. Batch operations (bulk insert, update, delete)
#   3. Proper indexing (on filter fields)
#   4. Query result caching
#   5. Materialized views for complex aggregations
# Acceptance Criteria:
#   - Query profiling in place
#   - Slow query log maintained
#   - 95th percentile query time < 100ms
#   - N+1 query tests passing
#   - Performance dashboard
```

---

### 5.2 Implement Background Job Processing
**Location:** Batch operations, background tasks  
**Status:** Non-existent, all processing synchronous  
**Impact:** Medium-High - enables scalability, responsiveness

```python
# TODO: PERFORMANCE - Implement background job queue for long operations
# Current State: All processing is synchronous, blocks API responses
# Goal: Async job processing for long-running operations
# Implementation:
#   1. Choose job queue system (RQ, Celery, APScheduler)
#   2. Identify operations that should be async:
#     - Email analysis/processing
#     - Batch label updates
#     - Data exports
#     - Cache warming
#     - Report generation
#   3. Create job definitions with retries
#   4. Implement job monitoring and failure handling
#   5. Add job status API for clients
#   6. Create job result storage (Redis, database)
# Priority: P1 (responsiveness, scalability)
# Job Queue Architecture:
#   Client -> API -> JobQueue
#          -> returns job_id
#   Background Worker processes job
#   Client polls /api/jobs/{job_id} for status/results
# Job Types to Implement:
#   - AnalyzeEmailJob (run AI analysis)
#   - BatchLabelJob (update multiple emails)
#   - ExportDataJob (export as CSV/JSON)
#   - WarmCacheJob (preload common queries)
#   - GenerateReportJob (statistics report)
# Configuration:
#   job_queue:
#     type: redis  # or rq, celery
#     workers: 4
#     timeout: 300  # 5 minute timeout
#     retries: 3
# Acceptance Criteria:
#   - Job system operational
#   - At least 5 job types
#   - Job monitoring dashboard
#   - Failure recovery working
#   - No synchronous operations > 5 seconds
```

---

## 6. Security & Compliance

### 6.1 Audit Secrets & Environment Configuration
**Location:** config management, .env files  
**Status:** Using environment variables but inconsistent  
**Impact:** High - security critical

```python
# TODO: SECURITY - Audit and harden secrets management
# Current State: Environment variables used but no vault, no rotation
# Goal: Secure secrets management with rotation and audit
# Implementation:
#   1. Audit all hardcoded secrets/credentials
#   2. Implement secrets vault (AWS Secrets Manager, HashiCorp Vault)
#   3. Create secret rotation policy
#   4. Add audit logging for secret access
#   5. Implement secret expiration and renewal
#   6. Create secrets documentation
# Priority: P0 (security critical)
# Secret Categories:
#   1. API Keys (Gmail, AI models, external services)
#   2. Database Credentials
#   3. Encryption Keys
#   4. Auth Tokens/Secrets
#   5. Service URLs (sensitive if auth required)
# Implementation Steps:
#   1. Inventory all secrets
#   2. Move to vault/secure storage
#   3. Set up secret rotation schedule
#   4. Add audit trail for access
#   5. Document secret management process
# Configuration:
#   secrets:
#     vault: aws_secrets_manager  # or hashicorp_vault
#     region: us-east-1
#     rotation_days: 90  # Rotate every 90 days
#     audit_logging: true
# Acceptance Criteria:
#   - No hardcoded secrets found
#   - Vault integration working
#   - Rotation schedule implemented
#   - Audit logging enabled
#   - Team trained on secrets management
```

---

### 6.2 Implement Security Testing
**Location:** tests/security/  
**Status:** Non-existent, security tests ad-hoc  
**Impact:** High - prevents security regressions

```python
# TODO: SECURITY - Create security test suite
# Goal: Prevent security vulnerabilities through automated testing
# Implementation:
#   1. Create security test framework
#   2. Implement OWASP top 10 tests:
#     - SQL Injection
#     - Cross-Site Scripting (XSS)
#     - Cross-Site Request Forgery (CSRF)
#     - Insecure Deserialization
#     - Broken Access Control
#     - Sensitive Data Exposure
#     - XML External Entity (XXE)
#     - Broken Authentication
#     - Using Components with Known Vulnerabilities
#     - Insufficient Logging & Monitoring
#   3. Add dependency vulnerability scanning
#   4. Implement secure code pattern checks
#   5. Create security checklist for code review
# Priority: P0 (security critical)
# Security Tests to Implement:
#   - SQL injection via all input vectors
#   - Path traversal attacks
#   - Command injection
#   - Authentication bypass
#   - Authorization bypass
#   - Rate limiting evasion
#   - Sensitive data in logs/responses
# Tooling:
#   - Bandit (Python security linter)
#   - Safety (dependency vulnerability)
#   - OWASP ZAP (web security scanning)
#   - Semgrep (pattern-based scanning)
# Acceptance Criteria:
#   - Security test suite in CI/CD
#   - Zero critical vulnerabilities
#   - Dependency scan passing
#   - Security checklist for PRs
```

---

## 7. Documentation & Knowledge Management

### 7.1 Create Architecture Decision Records (ADRs)
**Location:** docs/adr/  
**Status:** Non-existent  
**Impact:** Medium - improves knowledge transfer, decision tracking

```python
# TODO: DOCUMENTATION - Create ADR process for major decisions
# Goal: Document architectural decisions for future reference
# Implementation:
#   1. Create ADR template
#   2. Establish ADR process for major decisions
#   3. Maintain ADR index
#   4. Reference ADRs in code/docs
#   5. Periodic ADR review
# Priority: P2 (knowledge management)
# ADR Template:
#   # ADR-001: [Decision Title]
#   
#   ## Status: [Proposed|Accepted|Deprecated|Superseded]
#   
#   ## Context: [What's the situation?]
#   
#   ## Decision: [What did we decide?]
#   
#   ## Rationale: [Why this decision?]
#   
#   ## Consequences: [What are the implications?]
#   
#   ## Alternatives Considered: [What else could we do?]
# Example ADRs to Create:
#   - ADR-001: Use dependency injection for service management
#   - ADR-002: Repository pattern for data access
#   - ADR-003: Background job queue for async processing
#   - ADR-004: Notmuch as primary data source with SQLite fallback
# Acceptance Criteria:
#   - ADR process established
#   - At least 5 ADRs created
#   - ADRs referenced in code comments
#   - ADR index maintained
```

---

### 7.2 Maintain Runbook & Operations Guide
**Location:** docs/operations/  
**Status:** Partial, scattered across multiple documents  
**Impact:** Medium - improves operational readiness

```python
# TODO: DOCUMENTATION - Create comprehensive operations runbook
# Goal: Single source of truth for operational procedures
# Implementation:
#   1. Document deployment procedure
#   2. Document troubleshooting guide
#   3. Document monitoring setup
#   4. Document scaling procedures
#   5. Document backup/recovery procedures
#   6. Document incident response procedures
# Priority: P2 (operational readiness)
# Runbook Sections:
#   1. Prerequisites: Software, services, access required
#   2. Deployment: Step-by-step deployment procedure
#   3. Configuration: Configuration parameters and what they do
#   4. Monitoring: What to monitor and expected values
#   5. Troubleshooting: Common issues and solutions
#   6. Scaling: How to scale up/down
#   7. Backup: Backup procedure and testing
#   8. Recovery: Disaster recovery procedures
#   9. Incidents: Common incidents and responses
# Acceptance Criteria:
#   - Runbook covers all operations
#   - Procedures tested and verified
#   - Team trained on procedures
#   - Runbook kept up to date
```

---

## 8. Feature Development & Integration

### 8.1 Implement Notmuch Integration Completely
**Location:** src/backend/notmuch integration  
**Status:** Partial, some functionality missing  
**Impact:** High - core feature for email management

```python
# TODO: FEATURE - Complete Notmuch integration and testing
# Current State: Notmuch datasource exists but not fully tested/integrated
# Goal: Production-ready Notmuch integration with full feature set
# Implementation:
#   1. Complete Notmuch tag management
#   2. Implement Notmuch search with filters
#   3. Implement Notmuch query optimization
#   4. Add Notmuch fallback/error handling
#   5. Create comprehensive Notmuch tests
#   6. Add Notmuch performance profiling
#   7. Document Notmuch dependencies and setup
# Priority: P0 (core feature)
# Features to Implement:
#   - Tag management (add, remove, list)
#   - Advanced search (complex query support)
#   - Thread support (group related emails)
#   - Incremental sync (only new/changed emails)
#   - Performance optimization (caching, batching)
# Testing:
#   - Unit tests for Notmuch operations
#   - Integration tests with real Notmuch database
#   - Performance tests
#   - Fallback/error scenario tests
# Documentation:
#   - Notmuch setup guide
#   - Query syntax guide
#   - Troubleshooting guide
# Acceptance Criteria:
#   - All Notmuch operations working
#   - 95%+ test coverage
#   - Performance meets SLA (queries < 100ms)
#   - Fallback works when Notmuch unavailable
```

---

### 8.2 Implement Dashboard Real-Time Updates
**Location:** Backend dashboard, WebSocket support  
**Status:** Non-existent, polling-based only  
**Impact:** Medium-High - improves UX, reduces server load

```python
# TODO: FEATURE - Implement real-time dashboard updates with WebSocket
# Current State: Dashboard polls API for updates (inefficient, stale data)
# Goal: Real-time updates using WebSocket
# Implementation:
#   1. Add WebSocket support to FastAPI
#   2. Implement connection management
#   3. Create real-time event system
#   4. Broadcast events to connected clients
#   5. Implement reconnection logic
#   6. Add real-time tests
# Priority: P2 (UX improvement)
# Real-Time Events to Emit:
#   - Email received
#   - Email analyzed (AI results)
#   - Labels updated
#   - Status changes
#   - Statistics updates
# Architecture:
#   Client (WebSocket) <-> Server (EventBus) <-> Data Layer
#   
#   EventBus publishes events from data operations
#   Server broadcasts to relevant clients
#   Client updates UI in real-time
# Implementation:
#   class RealtimeEventBus:
#     async def subscribe(user_id) -> AsyncIterator
#     async def emit_event(event: Event)
#     def broadcast(event: Event, recipients: List[str])
# Acceptance Criteria:
#   - WebSocket connections stable
#   - Real-time event delivery < 100ms
#   - Graceful reconnection handling
#   - No memory leaks from connections
#   - Load tests for many concurrent clients
```

---

## 9. Monitoring & Observability

### 9.1 Implement Comprehensive Logging Strategy
**Location:** All modules, logging setup  
**Status:** Basic logging, inconsistent levels  
**Impact:** High - critical for debugging and monitoring

```python
# TODO: MONITORING - Establish structured logging strategy
# Current State: Basic logging with varying verbosity
# Goal: Structured, queryable logs with appropriate detail levels
# Implementation:
#   1. Define logging levels and usage guidelines
#   2. Implement structured logging (JSON format)
#   3. Add context tracking (request ID, user ID, etc.)
#   4. Implement log aggregation
#   5. Create log analysis dashboards
#   6. Define log retention policy
# Priority: P1 (debugging, monitoring)
# Logging Levels:
#   DEBUG: Detailed info for development (variable values, call traces)
#   INFO: Key events (request received, email analyzed, operation completed)
#   WARNING: Unexpected situations (retries, fallbacks, degraded mode)
#   ERROR: Failures that don't stop operation (failed analysis, timeout)
#   CRITICAL: System failures (cannot continue, data loss risk)
# Structured Log Format:
#   {
#     "timestamp": "2025-12-14T12:34:56Z",
#     "level": "INFO",
#     "logger": "backend.email_analysis",
#     "message": "Email analyzed successfully",
#     "request_id": "abc-123",
#     "user_id": "user-456",
#     "email_id": "email-789",
#     "duration_ms": 245,
#     "result": {intent: "meeting", urgency: "high"}
#   }
# Tooling:
#   - structlog for structured logging
#   - ELK (Elasticsearch, Logstash, Kibana) for aggregation
#   - CloudWatch/DataDog for hosted option
# Acceptance Criteria:
#   - All logs in JSON format
#   - Unique request IDs for tracking
#   - Log levels appropriate
#   - Log aggregation working
#   - Searchable logs
```

---

### 9.2 Implement Application Metrics & Monitoring
**Location:** Metrics collection, monitoring setup  
**Status:** Non-existent  
**Impact:** High - critical for production observability

```python
# TODO: MONITORING - Create comprehensive metrics collection and dashboards
# Goal: Monitor application health, performance, and business metrics
# Implementation:
#   1. Implement metrics collection framework
#   2. Define key metrics for different layers
#   3. Set up metrics storage (Prometheus, CloudWatch)
#   4. Create monitoring dashboards
#   5. Set up alerting rules
#   6. Implement health checks
# Priority: P1 (production operations)
# Metrics to Collect:
#   System Metrics:
#     - CPU usage, memory, disk I/O
#     - Request latency (p50, p95, p99)
#     - Error rates
#     - Throughput (requests/sec)
#   Application Metrics:
#     - Emails processed
#     - Analysis success rate
#     - Cache hit rate
#     - Database query times
#     - Background job queue depth
#   Business Metrics:
#     - Active users
#     - Emails per user (average)
#     - Analysis accuracy (human review)
#     - User satisfaction
# Tooling Options:
#   - Prometheus + Grafana (self-hosted)
#   - CloudWatch + CloudDashboards (AWS)
#   - Datadog (SaaS)
# Alert Examples:
#   - Error rate > 5% -> page on-call
#   - P99 latency > 1s -> warn
#   - Queue depth > 1000 -> scale workers
#   - Disk usage > 90% -> alert
# Acceptance Criteria:
#   - Metrics being collected
#   - Dashboards operational
#   - Alerting working
#   - Historical data retention >= 30 days
```

---

## 10. Implementation Roadmap

### Phase 1: Foundation (Weeks 1-2)
**Focus:** Enable better development and testing

1. ✅ Eliminate global state (1.1) - Blocking other improvements
2. ✅ Complete DI container (1.3) - Enables testing
3. ✅ Establish test strategy (4.1) - Foundation for other work

**Definition of Done:**
- All tests passing
- No global state in data access layer
- DI container in use for all services

---

### Phase 2: Data & Caching (Weeks 3-4)
**Focus:** Improve data consistency and performance

1. ✅ Complete repository pattern (2.1) - All data access through repository
2. ✅ Implement cache invalidation (2.2) - Data correctness
3. ✅ Query optimization strategy (5.1) - Performance

**Definition of Done:**
- All data access through repository
- Cache invalidation working
- Query performance improved

---

### Phase 3: Testing & Quality (Weeks 5-6)
**Focus:** Improve confidence in changes

1. ✅ Mocking framework (4.2) - Support testing
2. ✅ Regression tests (4.3) - Prevent regressions
3. ✅ Security testing (6.2) - Prevent vulnerabilities

**Definition of Done:**
- Test coverage > 85%
- All critical bugs have regression tests
- Security tests passing

---

### Phase 4: Performance & Scalability (Weeks 7-8)
**Focus:** Prepare for production scale

1. ✅ Background job processing (5.2) - Handle async work
2. ✅ Notmuch integration (8.1) - Complete core feature
3. ✅ Monitoring setup (9.1, 9.2) - Observe production

**Definition of Done:**
- Job queue operational
- Notmuch integration complete
- Monitoring dashboards live

---

### Phase 5: Polish & Hardening (Weeks 9-10)
**Focus:** Production readiness

1. ✅ Security audit (6.1) - No hardcoded secrets
2. ✅ Operations guide (7.2) - Team ready
3. ✅ Architecture documentation (7.1) - Knowledge preserved

**Definition of Done:**
- Security audit passed
- Team trained on operations
- Documentation complete

---

## Inline TODO Format

When adding these TODOs to code, use this format for consistency:

```python
# TODO: [CATEGORY] - [Brief title]
# Priority: [P0|P1|P2]
# Related: [Other TODOs, tasks, issues]
# Context: [Why is this needed?]
# Implementation:
#   1. Step 1
#   2. Step 2
# Files: [Affected files/modules]
# Acceptance Criteria:
#   - Criterion 1
#   - Criterion 2
```

---

## Using This Guide

### For Code Refactoring:
1. Read section for your area (e.g., "Data Management")
2. Find related TODOs
3. Check priority and dependencies
4. Follow implementation steps
5. Verify against acceptance criteria

### For Code Review:
1. Use TODOs to identify areas needing refactoring
2. Reference TODOs in PR comments
3. Track progress toward completion
4. Update implementation notes as work progresses

### For Planning:
1. Use Phase roadmap to schedule work
2. Consider dependencies between TODOs
3. Allocate time based on priority
4. Track completion in project management tool

---

## Success Metrics

- [ ] All Phase 1 TODOs complete
- [ ] Test coverage > 85%
- [ ] Zero critical security vulnerabilities
- [ ] P99 request latency < 1 second
- [ ] No global state in codebase
- [ ] All data access through repository
- [ ] Monitoring dashboards live
- [ ] Team trained on architecture
- [ ] Operations runbook complete
- [ ] Incident response procedures tested

---

## Document Maintenance

**Last Updated:** December 14, 2025  
**Owner:** EmailIntelligence Architecture Team  
**Review Cycle:** Monthly  
**Next Review:** January 14, 2026

This is a living document. Update it as:
- New architecture decisions are made (add to relevant section)
- TODOs are completed (mark complete and remove)
- New blockers are identified (add to appropriate priority)
- Roadmap changes (update Phase timeline)

---

**End of Strategic Refactoring Guide**
