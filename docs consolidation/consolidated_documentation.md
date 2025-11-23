# Consolidated Email Intelligence Platform Documentation

## Worktree-Based Setup Integration Guide

# Worktree-Based Setup Integration Guide

## Overview

This guide explains the worktree-based approach for managing setup files across different branches of the Email Intelligence Platform. The worktree system allows for seamless synchronization of shared setup components while maintaining branch independence.

## Worktree Structure

The current worktree setup includes:

1. **`launch-setup-fixes`** - Contains the canonical setup files that are shared across all branches
2. **`docs-main`** - Documentation for the main branch (**documentation-only**)
3. **`docs-scientific`** - Documentation for the scientific branch (**documentation-only**)
4. **`main`** - The main production branch
5. **`worktree-workflow-system`** - Workflow system branch

**Note:** The `docs-main` and `docs-scientific` worktrees are documentation-only and should NOT contain setup files.

## Setup Files Location

The shared setup files are located in:
```
worktrees/launch-setup-fixes/setup/
```

This directory contains essential launch and setup files that are synchronized to:
- `main` worktree
- `worktree-workflow-system` worktree
- Any other code worktrees that need shared setup components

**Note:** Setup files are NOT synchronized to documentation-only worktrees (`docs-main`, `docs-scientific`).

## Synchronization Process

### Automatic Synchronization

The worktree system uses Git hooks to automatically synchronize setup files:

1. **Pre-commit hook** - Validates that documentation files are in correct locations
2. **Post-commit hook** - Runs documentation synchronization when needed

### Manual Synchronization

To manually synchronize setup files between worktrees:

```bash
# Synchronize setup files (only to non-documentation worktrees)
bash scripts/sync_setup_worktrees.sh

# Show what would be synchronized without making changes
bash scripts/sync_setup_worktrees.sh --dry-run

# Synchronize with verbose output
bash scripts/sync_setup_worktrees.sh --verbose
```

**Note:** The synchronization script automatically excludes documentation-only worktrees (`docs-main`, `docs-scientific`) from receiving setup files.

## Adding New Worktrees

To add a new worktree for a branch:

```bash
# Create a new worktree for an existing branch
git worktree add worktrees/<branch-name> <branch-name>

# Create a new worktree for a new branch
git worktree add worktrees/<branch-name> -b <branch-name>
```

## Best Practices

1. **Always work in the appropriate worktree** - Use the worktree that corresponds to your branch
2. **Keep setup files in the canonical location** - Modify setup files only in the `launch-setup-fixes` worktree
3. **Synchronize regularly** - Run the sync script after making changes to setup files
4. **Test across worktrees** - Verify that changes work correctly in all relevant worktrees
5. **Use Git hooks** - Let the automated hooks handle routine synchronization tasks

## Troubleshooting

### Worktree Issues

If you encounter issues with worktrees:

1. **Check worktree status**:
   ```bash
   git worktree list
   ```

2. **Remove problematic worktrees**:
   ```bash
   git worktree remove <worktree-name>
   ```

3. **Prune stale worktree references**:
   ```bash
   git worktree prune
   ```

### Synchronization Issues

If synchronization is not working correctly:

1. **Verify worktree structure**:
   ```bash
   ls -la worktrees/
   ```

2. **Check setup directory in each worktree**:
   ```bash
   ls -la worktrees/*/setup/
   ```

3. **Run manual synchronization**:
   ```bash
   bash scripts/sync_setup_worktrees.sh --verbose
   ```

## Future Enhancements

Planned improvements to the worktree system include:

1. **Enhanced automation** - More sophisticated synchronization triggers
2. **Conflict resolution** - Better handling of merge conflicts in setup files
3. **Performance optimization** - Faster synchronization for large setups
4. **Cross-platform support** - Improved handling of platform-specific setup files

## Scientific Documentation

### README.md (Scientific Branch)

# EmailIntelligence Documentation

This directory contains comprehensive documentation for the EmailIntelligence project.

## 📁 Directory Structure

### 📖 [guides/](guides/)
User guides, tutorials, and feature documentation
- Getting started guides
- Feature documentation  
- Module documentation
- Workflow guides

### 🏗️ [architecture/](architecture/)
Architecture and system design documentation
- System architecture overview
- Workflow system design
- Component architecture

### 💻 [development/](development/)
Development and contribution documentation
- Developer guides
- Coding standards
- Environment setup
- Extension development

### 🚀 [deployment/](deployment/)
Deployment and operations documentation
- Deployment guides
- Launch configuration
- Environment hardening

### 🔌 [api/](api/)
API documentation and references
- API reference
- Dashboard APIs
- Integration guides

### 📋 [project-management/](project-management/)
Project management and planning documentation
- Branch management
- Documentation workflow
- Task tracking
- Project reports

### 📝 [adr/](adr/)
Architecture Decision Records
- System design decisions
- Technology choices
- Implementation decisions

### 📋 [changelog/](changelog/)
Change logs and release notes

### 📝 [templates/](templates/)
Documentation templates and examples

## 🚀 Quick Start

1. **New to the project?** Start with [guides/getting_started.md](guides/getting_started.md)
2. **Want to contribute?** Read [development/DEVELOPER_GUIDE.md](development/DEVELOPER_GUIDE.md)
3. **Need API info?** Check [api/API_REFERENCE.md](api/API_REFERENCE.md)
4. **Planning features?** See [project-management/](project-management/)

## 📊 Documentation Health

This documentation is maintained in a single organized structure with branch-specific files consolidated.

- **Structure**: Categorized by purpose (guides, architecture, development, etc.)
- **Branch Integration**: Main and scientific branch documentation merged into organized folders
- **Maintenance**: Single source of truth for all project documentation

## 🤝 Contributing

When adding documentation:
1. Place files in the appropriate subdirectory based on content type
2. Follow the established naming conventions
3. Update this README if adding new sections
4. For branch-specific content, use descriptive suffixes (e.g., `-main.md`, `-scientific.md`)

All documentation is now maintained in this single organized structure.

### Workflow System Analysis (Scientific Branch)

# Node-Based Workflow System Analysis Report

## Overview
This document provides a comprehensive analysis of the node-based workflow system implementation in the Email Intelligence Platform. The analysis was conducted to assess the progress, quality, and completeness of the implementation against the design specifications.

## Implementation Review

### Core Architecture
The system includes:
- A core workflow engine in `src/core/advanced_workflow_engine.py`
- Security framework in `src/core/security.py` and `backend/node_engine/security_manager.py`
- Node implementations in `backend/node_engine/email_nodes.py`
- API routes in `backend/python_backend/advanced_workflow_routes.py`
- UI components in `backend/python_backend/workflow_editor_ui.py`
- Workflow manager in `backend/python_backend/workflow_manager.py`
- Comprehensive tests in `backend/node_engine/test_*.py` files

### Successfully Implemented Components

#### 1. Core Engine Components
- BaseNode abstract class with proper interfaces
- Workflow class for managing node collections
- Connection class for defining data flow between nodes
- WorkflowRunner for executing workflows with security and performance monitoring
- WorkflowManager for persistence and management

#### 2. Security Components
- SecurityManager with session management
- DataSanitizer for input/output sanitization
- ExecutionSandbox for controlled execution
- AuditLogger for tracking operations
- Security validation and permission checks

#### 3. Node Types
- EmailSourceNode for retrieving emails
- PreprocessingNode for cleaning and normalizing data
- AIAnalysisNode for NLP analysis
- FilterNode for applying filtering rules
- ActionNode for executing actions on emails

#### 4. API Endpoints
- Complete REST API for workflow management (CRUD operations)
- Execution endpoints with status tracking
- Node management endpoints
- Execution control endpoints (cancel, status check)

#### 5. UI Components
- Gradio-based workflow editor interface
- Node gallery for available processing types
- Performance metrics display
- Workflow visualization canvas

#### 6. Testing Framework
- Unit tests for individual nodes
- Integration tests for the complete workflow
- Security tests for validating security features
- Scalability tests for concurrent execution

#### 7. Documentation
- Architecture documentation
- Node type specifications
- API documentation
- Security implementation details

## Missing or Incomplete Components

### 1. JavaScript-based Visualization
- The UI uses a simple HTML canvas for visualization, but a full-featured implementation would require a JavaScript library like React Flow for drag-and-drop functionality
- The current visualization is basic and doesn't support actual node manipulation

### 2. Advanced Performance Metrics
- While the system mentions performance metrics, the actual implementation of real-time metrics dashboard is basic
- More detailed performance tracking would be needed for production use

### 3. Distributed Processing Support
- The documentation mentions "Distributed processing support (future)" but this is not implemented
- The current system runs on a single node

### 4. Workflow Sharing and Collaboration
- The documentation mentions workflow sharing features but these are not implemented
- No multi-user collaboration functionality exists

### 5. Advanced Node Types
- While core node types exist, there may be additional specialized nodes that could be developed
- Integration with more external services could be expanded

### 6. Plugin System Integration
- While the architecture supports plugins, the actual implementation is basic
- More sophisticated plugin management could be added

## Quality Assessment

### Code Quality
- The implementation follows good Python practices with proper type hints, docstrings, and naming conventions
- The code adheres to the project guidelines specified in AGENTS.md
- Proper error handling with meaningful error messages is implemented
- Security best practices are followed throughout the implementation

### Security Implementation
- Comprehensive security features including input sanitization, execution sandboxing, and audit logging
- Session-based authentication and authorization
- Data access controls and execution context isolation
- Encrypted data transmission for sensitive information

### Testing Coverage
- Well-structured test suite covering all major components
- Proper separation of unit and integration tests
- Security and scalability tests included
- Tests follow the project's testing patterns and requirements

## Completeness Assessment

### Core Functionality
- All basic functionality described in the documentation is implemented
- Node types match the specifications
- API endpoints are complete and functional
- UI components provide the basic workflow editing capabilities
- Persistence system works as specified

### Advanced Features
- Most enterprise-grade security features are implemented
- Performance monitoring is integrated as specified
- Resource management is functional
- Plugin system architecture supports extensibility

## Design Specification Alignment

### Architecture Principles
- Follows node-based architecture as specified
- Modular structure as described in documentation
- Security-first design approach implemented
- Extensibility through plugin system

### Feature Implementation
- Core workflow functionality matches design specifications
- API design follows the documented endpoints
- UI components implement the described visual design
- Performance monitoring features are included

### Design Patterns
- Architecture follows patterns similar to ComfyUI and other frameworks as specified
- Enterprise focus with security and scalability features
- Extensibility through plugin system as described

## Conclusion

The node-based workflow system implementation in the Email Intelligence Platform is well-progressed with core functionality implemented and documented. The system follows the design specifications closely and implements all security features described in the design documentation.

There are some advanced features still to be implemented, but the system is robust and ready for use for basic to intermediate workflow processing tasks. The implementation successfully achieves the project's goal of creating a modular, extensible AI processing platform with enterprise-grade security.

## Recommendations

### For Future Development
1. Implement a full-featured JavaScript visualization library for the workflow editor
2. Add distributed processing capabilities for scalability
3. Develop workflow sharing and collaboration features
4. Enhance the plugin system with more sophisticated management capabilities
5. Implement more detailed real-time performance metrics
6. Expand the range of available node types for specific use cases

### For Documentation
1. Update the documentation to reflect the current implementation status
2. Add usage examples for different workflow types
3. Document the security features and best practices
4. Provide guidelines for extending the system with custom nodes

### Unified Architectural Plan (Scientific Branch)

# Unified Architectural Plan: Email Intelligence Platform

## Executive Summary

This comprehensive plan outlines the consolidation and enhancement of the Email Intelligence Platform, focusing on unifying three competing workflow systems, enhancing security and performance, and preparing for production deployment. The plan addresses critical architectural improvements while maintaining backward compatibility and system stability.

## Current Architecture State

### Three Competing Workflow Systems (To Be Consolidated)

1. **Basic System** (`src/core/workflow_engine.py`, `backend/python_backend/workflow_engine.py`)
   - Synchronous DAG execution
   - No security features
   - Simple node/workflow/runner classes

2. **Node Engine** (`backend/node_engine/`)
   - **TARGET SYSTEM** - Async execution with security
   - Enterprise-grade security (path traversal protection, input sanitization)
   - Modular node implementations with comprehensive testing

3. **Advanced Core** (`src/core/advanced_workflow_engine.py`)
   - NetworkX graph operations for complex workflows
   - Security context integration
   - Performance monitoring and execution tracking

### Key Architectural Components

- **Backend**: Python FastAPI with modular architecture
- **Frontend**: React (Vite) + Gradio UI for scientific development
- **NLP Engine**: Custom AI models with sentiment, topic, intent analysis
- **Database**: SQLite with JSON file caching
- **Security**: Multi-layer validation, audit logging, sandboxing
- **Deployment**: Unified launcher with environment management

## Phase 1: Workflow System Consolidation (2-3 weeks)

### Objective
Unify three competing workflow systems into a single, secure Node Engine architecture.

### Tasks

#### 1.1 Feature Integration into Node Engine
- Integrate NetworkX graph operations from Advanced Core
- Add security context support to BaseNode
- Implement performance monitoring in WorkflowRunner
- Migrate EmailInputNode, NLPProcessorNode, EmailOutputNode
- Add topological sorting with cycle detection

#### 1.2 Import Consolidation
Update all imports across 26+ files to use Node Engine as primary:
```python
# Before
from src.core.workflow_engine import Node, Workflow, WorkflowRunner
from src.core.advanced_workflow_engine import WorkflowManager

# After
from backend.node_engine.workflow_engine import Node, Workflow, WorkflowRunner
from backend.node_engine.workflow_manager import WorkflowManager
```

#### 1.3 Deprecation Implementation
- Add `warnings.warn()` deprecation notices
- Maintain 1-2 release compatibility
- Update docstrings with Node Engine references

#### 1.4 Migration Utilities Development
- Automated conversion tools for existing workflows
- Node type mapping and configuration translation
- CLI batch migration interface
- Validation of converted workflows

#### 1.5 Testing Simplification
- Remove redundant test files
- Regenerate tests for unified system
- Add integration tests for consolidated workflows

### Success Criteria
- Single workflow system of record
- All imports updated to Node Engine
- Full test suite passes
- No performance regressions
- Comprehensive migration documentation

## Phase 2: Security & Performance Hardening (2-3 weeks)

### Objective
Enhance enterprise-grade security and performance monitoring.

### Tasks

#### 2.1 Security Enhancement
- Advanced audit logging with comprehensive event tracking
- Fine-tune execution sandboxing for security levels
- Implement rate limiting for API endpoints
- Security validation for all workflow execution paths
- Enhanced SecurityManager with granular permissions

#### 2.2 Performance Optimization
- Optimize performance metrics collection
- Implement caching mechanisms for frequently accessed data
- Resource-aware scheduling and memory management
- Performance monitoring dashboard with real-time metrics

#### 2.3 Code Quality Improvements
- Address identified code quality issues:
  - Split large NLP modules (smart_filters.py: 1598 lines, smart_retrieval.py: 1198 lines)
  - Reduce code duplication in AI engine modules
  - Break down high-complexity functions (setup_dependencies: complexity 21)

### Success Criteria
- Security audit passes with no critical vulnerabilities
- Performance benchmarks meet requirements (<2s average execution)
- Code complexity reduced by 40%
- Comprehensive audit logging implemented

## Phase 3: UI Enhancement & User Experience (3-4 weeks)

### Objective
Implement modern, interactive workflow editing interface.

### Tasks

#### 3.1 JavaScript-based Visual Editor
- Implement drag-and-drop node placement
- Create connection lines with visual feedback
- Add zoom and pan functionality
- Workflow validation before execution

#### 3.2 Enhanced User Experience
- Node templates and presets for common workflows
- Real-time validation and error feedback
- Workflow sharing and collaboration features
- Integration with existing Gradio UI

#### 3.3 Accessibility & Usability
- Keyboard navigation support
- Screen reader compatibility
- Mobile-responsive design considerations

### Success Criteria
- Fully interactive workflow editor
- User satisfaction score >4.5/5.0
- Workflow creation time <5 minutes for basic workflows

## Phase 4: Advanced Features & Scalability (4-6 weeks)

### Objective
Implement enterprise-grade features for production scalability.

### Tasks

#### 4.1 Distributed Processing
- Support for distributed workflow execution
- Clustering capabilities for high-throughput processing
- Load balancing and failover mechanisms

#### 4.2 Advanced Node Ecosystem
- Custom node creation via plugin system
- Integration with external AI services and APIs
- Advanced node types for specialized operations

#### 4.3 Workflow Management
- Workflow versioning and rollback capabilities
- Multi-user collaboration features
- Workflow execution queuing and recovery

#### 4.4 Resource Management
- Enhanced memory management for large datasets
- Configurable concurrency limits
- Resource monitoring and alerting

### Success Criteria
- Support 100+ concurrent workflow executions
- Plugin system supports custom node development
- Workflow execution recovery after failures

## Phase 5: Testing, Documentation & Quality Assurance (3-4 weeks)

### Objective
Achieve production-ready quality and comprehensive documentation.

### Tasks

#### 5.1 Testing Enhancement
- Automated testing coverage >95%
- Performance testing and benchmarks
- Security testing and penetration testing
- End-to-end workflow testing

#### 5.2 Documentation Completion
- Complete API documentation for all endpoints
- Comprehensive user guides for workflow creation
- Developer documentation for system extension
- Video tutorials for workflow editor usage

#### 5.3 Quality Gates
- Automated code quality checks
- Pre-commit hooks for quality enforcement
- CI/CD pipeline integration with quality metrics

### Success Criteria
- Test coverage >95% for core components
- Complete documentation suite
- Zero critical security vulnerabilities
- All high-priority code quality issues resolved

## Phase 6: Production Deployment & Operations (2-3 weeks)

### Objective
Prepare for production deployment with monitoring and operational readiness.

### Tasks

#### 6.1 Production Infrastructure
- Production deployment configurations
- Docker container optimization
- Database backup and disaster recovery
- Environment-specific configuration management

#### 6.2 Monitoring & Alerting
- Comprehensive monitoring and alerting system
- Performance metrics collection and visualization
- Error tracking and incident response
- Resource usage monitoring

#### 6.3 Operational Procedures
- Deployment automation scripts
- Rollback procedures and version management
- Backup and restore procedures
- Maintenance and update procedures

### Success Criteria
- Production deployment configurations validated
- Monitoring covers all critical system components
- Incident response procedures documented
- Automated deployment pipeline operational

## Critical Bug Fixes & Immediate Actions

### High Priority (Next 1-2 weeks)
1. **Fix pytest-asyncio Configuration**
   - Resolve test environment issues preventing async test execution
   - Update pyproject.toml configuration
   - Validate test execution across all components

2. **Implement Proper Workflow Selection**
   - Address missing workflow selection in email_routes.py
   - Ensure proper workflow routing and execution
   - Add validation and error handling

3. **Security Hardening - Path Traversal**
   - Secure SQLite database paths to prevent path traversal attacks
   - Implement secure path validation functions
   - Update database path handling throughout system

### Medium Priority (Next 2-4 weeks)
4. **Fix setup_linting.py FIXME**
   - Address W0511 fixme marker
   - Improve linting configuration and error handling

5. **Gmail API Authentication for Non-Interactive Environments**
   - Implement authentication handling for automated deployments
   - Support service account authentication
   - Add configuration for different authentication modes

## Risk Assessment & Mitigation

### Technical Risks
- **Migration Complexity**: Phased approach with rollback capabilities
- **Performance Impact**: Comprehensive benchmarking and optimization
- **Security Vulnerabilities**: Regular security audits and penetration testing
- **Integration Issues**: Extensive testing and validation at each phase

### Operational Risks
- **Downtime**: Zero-downtime deployment strategies
- **Data Loss**: Comprehensive backup and recovery procedures
- **User Impact**: Feature flags and backward compatibility
- **Resource Constraints**: Scalable architecture with resource management

### Mitigation Strategies
- **Incremental Deployment**: Each phase can be deployed independently
- **Comprehensive Testing**: Automated testing at all levels
- **Monitoring**: Real-time monitoring and alerting
- **Rollback Plans**: Documented procedures for each component
- **Stakeholder Communication**: Regular updates and feedback sessions

## Success Metrics

### Technical Metrics
- **Performance**: <2s average workflow execution time
- **Security**: Pass security audit with zero critical vulnerabilities
- **Scalability**: Support 100+ concurrent executions
- **Reliability**: 99.9% uptime with <1% error rate
- **Code Quality**: >95% test coverage, complexity reduction by 40%

### Business Metrics
- **User Adoption**: >70% utilization of workflow features
- **User Satisfaction**: >4.5/5.0 satisfaction score
- **Time Savings**: >50% reduction in manual email processing time
- **Cost Efficiency**: Reduced maintenance overhead through consolidation

## Timeline & Resource Requirements

### Overall Timeline: 16-24 weeks
- **Phase 1**: 2-3 weeks (Workflow Consolidation)
- **Phase 2**: 2-3 weeks (Security & Performance)
- **Phase 3**: 3-4 weeks (UI Enhancement)
- **Phase 4**: 4-6 weeks (Advanced Features)
- **Phase 5**: 3-4 weeks (Testing & Documentation)
- **Phase 6**: 2-3 weeks (Production Deployment)

### Team Resources
- **Core Team**: 2-3 developers (architect, backend, frontend)
- **Security Specialist**: 1 resource for security hardening phases
- **DevOps Engineer**: 1 resource for deployment and operations
- **QA Engineer**: 1 resource for testing and quality assurance
- **Technical Writer**: 1 resource for documentation

### Dependencies
- Node Engine architecture stabilization (completed)
- Security framework implementation (completed)
- Basic testing infrastructure (completed)
- CI/CD pipeline availability
- Production infrastructure provisioning

## Implementation Readiness Assessment

### Completed Prerequisites ✅
- Core Node Engine architecture implemented
- Security framework with input sanitization
- Primary node types (EmailSource, Preprocessing, AIAnalysis, Filter, Action)
- Basic REST API for workflow management
- Gradio UI foundation
- Comprehensive test suite framework

### Ready for Implementation 🟢
- Migration utilities design completed
- Security hardening specifications ready
- UI enhancement plans documented
- Production deployment architecture defined
- Testing and documentation frameworks established

### Next Steps
1. Begin Phase 1 workflow consolidation
2. Address high-priority bug fixes immediately
3. Establish development cadence and milestones
4. Set up monitoring and progress tracking
5. Begin security hardening alongside workflow migration

---

## Conclusion

This unified architectural plan provides a comprehensive roadmap for transforming the Email Intelligence Platform into a production-ready, enterprise-grade system. The phased approach ensures stability while delivering significant improvements in security, performance, and user experience. By consolidating competing systems and addressing identified issues, the platform will achieve the robustness and scalability required for production deployment.

The plan balances technical excellence with practical implementation, ensuring that each phase delivers tangible value while building toward the overall vision of a unified, secure, and performant email intelligence system.

### Git Subtree Integration for Scientific Branch Guide

# Git Subtree Integration for Scientific Branch

## Overview

This document explains how to properly implement and use git subtrees for managing shared launch and setup files in the scientific branch of the Email Intelligence Platform.

## Purpose

The goal of using git subtrees in the scientific branch is to:

1. Maintain shared launch and setup files with other branches
2. Allow the scientific branch to continue its specialized development
3. Provide a mechanism to receive setup improvements from the central setup
4. Maintain consistency in launch procedures across branches

## Implementation Process

### For Scientific Branch Setup

1. Add the setup subtree from launch-setup-fixes branch:

```bash
git subtree add --prefix=setup origin/launch-setup-fixes --squash
```

2. This creates a single commit that contains all the files from the launch-setup-fixes branch as a subdirectory

### Updating Subtrees in Scientific Branch

To pull updates from the setup branch to the scientific branch:

```bash
git subtree pull --prefix=setup origin/launch-setup-fixes --squash
```

### Pushing Changes from Scientific Branch

To push changes made in the scientific branch back to the setup branch:

```bash
git subtree push --prefix=setup origin launch-setup-fixes
```

## Scientific Branch Considerations

- The scientific branch may have additional dependencies beyond the standard setup
- Ensure that any scientific-specific configurations are properly integrated with the shared launch infrastructure
- Test that scientific-specific features continue to work after subtree integration

## Benefits for Scientific Branch

- Consistent setup experience with other branches
- Access to centralized launch improvements
- Reduced maintenance overhead for setup files
- Maintained independence for scientific-specific features

## Main Documentation

### README.md (Main Branch)

# EmailIntelligence Documentation

This directory contains comprehensive documentation for the EmailIntelligence project.

## 📁 Directory Structure

### 📖 [guides/](guides/)
User guides, tutorials, and feature documentation
- Getting started guides
- Feature documentation  
- Module documentation
- Workflow guides

### 🏗️ [architecture/](architecture/)
Architecture and system design documentation
- System architecture overview
- Workflow system design
- Component architecture

### 💻 [development/](development/)
Development and contribution documentation
- Developer guides
- Coding standards
- Environment setup
- Extension development

### 🚀 [deployment/](deployment/)
Deployment and operations documentation
- Deployment guides
- Launch configuration
- Environment hardening

### 🔌 [api/](api/)
API documentation and references
- API reference
- Dashboard APIs
- Integration guides

### 📋 [project-management/](project-management/)
Project management and planning documentation
- Branch management
- Documentation workflow
- Task tracking
- Project reports

### 📝 [adr/](adr/)
Architecture Decision Records
- System design decisions
- Technology choices
- Implementation decisions

### 📋 [changelog/](changelog/)
Change logs and release notes

### 📝 [templates/](templates/)
Documentation templates and examples

## 🚀 Quick Start

1. **New to the project?** Start with [guides/getting_started.md](guides/getting_started.md)
2. **Want to contribute?** Read [development/DEVELOPER_GUIDE.md](development/DEVELOPER_GUIDE.md)
3. **Need API info?** Check [api/API_REFERENCE.md](api/API_REFERENCE.md)
4. **Planning features?** See [project-management/](project-management/)

## 📊 Documentation Health

This documentation is maintained in a single organized structure with branch-specific files consolidated.

- **Structure**: Categorized by purpose (guides, architecture, development, etc.)
- **Branch Integration**: Main and scientific branch documentation merged into organized folders
- **Maintenance**: Single source of truth for all project documentation

## 🤝 Contributing

When adding documentation:
1. Place files in the appropriate subdirectory based on content type
2. Follow the established naming conventions
3. Update this README if adding new sections
4. For branch-specific content, use descriptive suffixes (e.g., `-main.md`, `-scientific.md`)

All documentation is now maintained in this single organized structure.

### Main Branch Documentation File

# Main Branch Documentation

This is the main branch documentation file.