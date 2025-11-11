# Master Constitution for Email Intelligence Platform

## Overview

This is the master constitution document for the Email Intelligence Platform. All repositories and projects must align with these principles. This document supersedes all other constitution files and serves as the single source of truth.

**Version**: 1.0.0 | **Ratified**: 2025-11-10 | **Last Amended**: 2025-11-10

---

## Core Principles

### I. Code Quality and Standards

All code must adhere to established style guidelines (PEP 8), maintain high readability through meaningful names and clear function structures, and be simple, concise, and maintainable while preserving full functionality. Include type hints for all public functions and maintain comprehensive but concise docstrings using Google style. Favor readable, straightforward implementations over clever optimizations. Implement consistent error handling with proper logging. Static analysis tools (e.g., Flake8, Pylint) and mandatory code reviews are integral to ensuring code quality.

### II. Test-Driven Development (TDD) and Testing Standards (NON-NEGOTIABLE)

Test-Driven Development is mandatory for all new feature development and bug fixes: Write tests before implementation, ensure tests fail initially (Red-Green-Refactor cycle), achieve minimum 90% code coverage with critical paths requiring 100%, and critical for validating smart agent outputs. All tests must pass in CI/CD pipeline before code can be merged. Comprehensive testing strategy including unit, integration, end-to-end, and performance tests. Test naming must be descriptive and clearly indicate what behavior is being tested and expected outcomes. Tests should be clear and easy to understand, avoiding over-complicated test setups while ensuring complete feature coverage. All new features must include corresponding tests before merging. Tests must be written and approved before implementation.

### III. User Experience Consistency

All interfaces must maintain consistent, simple design patterns and accessibility compliance (WCAG 2.1 AA) without compromising feature completeness. UI elements, workflows, and interactions should follow established patterns across the application. All features must be intuitive and accessible to users with diverse abilities and technical backgrounds. Maintain consistent visual design language across all user interfaces with standardized components, spacing, and typography. Ensure WCAG 2.1 AA compliance with proper ARIA labels, keyboard navigation, and screen reader support. Provide clear, actionable error messages that help users understand and resolve issues without technical jargon.

### IV. Performance and Efficiency

All system components must be efficient and lightweight without losing functionality: Maintain sub-200ms response times for user interactions and sub-2 second load times for pages, API responses under 200ms for 95th percentile, minimal resource usage, optimized database queries. Implement efficient algorithms with appropriate data structures, prevent memory leaks, and use appropriate caching strategies to ensure fast data access and horizontal scalability. System must handle expected load requirements: support 1000+ concurrent users, process 10,000+ requests per minute if applicable, maintain 90% uptime during business hours, complete batch operations within defined time windows. Performance metrics must be monitored continuously. Efficient code often means simpler code that avoids unnecessary operations while preserving all required functionality.

### V. Critical Thinking and Simplicity

Make evidence-based decisions using data and user feedback. Question complexity; always consider if a simpler approach would work without losing essential functionality. Validate approaches through experimentation, and prefer pragmatic solutions that balance idealism with practical constraints. When multiple solutions exist, favor the simplest that meets all requirements. Document reasoning for technical decisions with emphasis on why complexity was added or avoided, ensuring functionality is preserved.

### VI. Security by Design

All code must follow secure coding practices: validate and sanitize all inputs, implement proper authentication and authorization, encrypt sensitive data in transit and at rest, avoid injection vulnerabilities, conduct security reviews for new components. Dependencies must be regularly scanned for vulnerabilities. Security implementations should be as simple as possible while remaining effective and comprehensive. Security considerations must be integrated into every phase of the software development lifecycle, from design to deployment. Regular security audits and vulnerability assessments are required. All external dependencies must be reviewed for security vulnerabilities.

### VII. API-First Design and Modularity

All core functionalities must be exposed via well-defined Python APIs. This ensures interoperability and facilitates integration with other systems, including smart agent interfaces and external services. All components must be designed as independent, self-contained Python modules with clear, well-defined interfaces. This ensures maximum reusability, maintainability, and testability. Implement separation of concerns with well-defined interfaces between components. Facilitating smart agent scripting and experimentation.

### VIII. Continuous Integration/Continuous Deployment (CI/CD)

All code changes must pass through automated CI/CD pipelines before merging: automated testing, security scanning, performance validation, and deployment verification. Changes should be small, frequent, and easily reversible. Maintain deployment readiness at all times with all tests passing in main branch. CD automation should be reliable, efficient, and provide clear feedback on deployment status. Automated CI/CD pipelines must be established for all code changes, ensuring continuous testing, building, and deployment to staging and production environments. This includes automated validation of smart agent contributions.

### IX. Branching and Orchestration Strategy (NON-NEGOTIABLE)

A clear branching strategy (e.g., GitFlow, GitHub Flow, Trunk-Based Development) must be defined and adhered to. The orchestration of CI/CD, testing, and deployment processes, including smart agent-driven workflows, must be automated and clearly documented to ensure consistency, efficiency, and traceability. The `orchestration-tools` branch serves as the central hub for development environment tooling, configuration management, scripts, and Git hooks that ensure consistency across all project branches. This branch is the single source of truth for shared configurations and orchestration tools. The following design decisions are key to this strategy:

- **Separation of Concerns**: Orchestration tools and configurations are managed separately from application code
- **File Ownership Matrix**: Clear delineation of which files belong in which branches:
  - Orchestration-only files (scripts/, scripts/hooks/, orchestration config) reside only in orchestration-tools branch
  - Orchestration-managed files (setup/, pyproject.toml, .gitignore) are synced TO other branches from orchestration-tools
  - Branch-specific files (tsconfig.json, package.json, application source) remain branch-local
- **Automated Synchronization**: Git hooks automatically handle file synchronization between branches via post-checkout, post-merge, post-push, and pre-commit hooks
- **Development Flow**: Orchestration development happens exclusively in orchestration-tools branch, with changes automatically propagated to other branches through the hook system
- **This principle supersedes feature development priorities when conflicts arise.**

---

## Extension Modules

### Extension A: AI Agent Integration Requirements

For repositories with AI agent functionalities:
- All user-facing interfaces, including CLI tools and agent interaction patterns, must adhere to a consistent design language
- Performance testing and monitoring are mandatory to ensure responsiveness and scalability under load, particularly for computationally intensive agent tasks
- Special attention to agent-generated code and data handling in security audits
- AI agents must operate within isolated contexts based on branch environments
- Context contamination between agents or environments is strictly prohibited
- All context switches must be logged and auditable
- Agents require explicit context validation before execution

### Extension B: Verification and Validation Requirements

For repositories requiring comprehensive verification:
- **Verification-First Development**: All changes to orchestration tools must pass comprehensive verification before merging
- **Verification results** must be transparent and auditable
- **Verification failures** generate detailed reports but do not block merges (business continuity)
- **Context-Aware Verification**: Verification includes environment variables, dependency versions, configuration files, and infrastructure state
- **System validates** compatibility with target branches before allowing merges
- **Orchestration-tools changes** tested against 50% more scenarios than current test suite
- **95% of pull requests** pass verification checks before merging to main
- **Verification completion time** reduced by 30% compared to manual review

### Extension C: Access Control and Integration

For repositories with specialized access control:
- **Role-Based Access Control**: Any authorized user can run tests; only designated reviewers can approve verification results before merge operations
- **API key-based authentication** for all operations
- **99.9% authentication success rate** for all system operations
- **Secure handling** of environment variables and configuration files
- **Support for multiple target branch** scenarios (minimum 3)
- **Easy extension** of test scenarios without system modification

---

## Implementation Constraints

### Quality Gates

All PRs must pass automated checks before human review: code linting, security scanning, test coverage verification, performance benchmarks. Only after passing automated checks should PRs proceed to peer review. All constitution principles must be validated during the review process.

### Architecture Requirements

- **Loose Coupling, High Cohesion**: Integration with external systems through well-defined interfaces; verification scenarios should be independent and testable in isolation; user role management separate from verification logic
- **Service-Oriented Architecture**: Verification service as a distinct component; integration adapters for CI/CD and version control systems; user management as a separate service or module
- **Event-Driven Communication**: Verification events trigger appropriate actions; status updates propagate through well-defined channels; asynchronous processing where appropriate
- **Configuration Over Code**: Verification rules defined in configuration rather than code where possible; environment-specific settings externalized; easy modification of verification parameters without code changes

### Quality Attributes

- **Reliability**: Zero production incidents from changes passing verification process; consistent verification behavior across different environments; resilient failure reporting under load
- **Maintainability**: Clear separation of concerns between verification components; modular design allowing easy addition of new test scenarios; comprehensive logging for debugging purposes
- **Scalability**: Support for multiple concurrent verification processes; ability to handle increased test scenario volume; efficient resource utilization during verification

### Orchestration System Components

The orchestration system consists of several key components that must be maintained:

- **Git Hooks**: pre-commit, post-checkout, post-merge, post-push hooks that enforce workflow standards and automate synchronization
- **Synchronization Scripts**: scripts in `/scripts/` that handle worktree synchronization and reverse sync operations
- **Launch System**: unified launcher system in `/setup/` and root `/launch.py` wrapper for backward compatibility
- **Configuration Files**: shared configurations like `pyproject.toml`, `requirements*.txt`, `.gitignore` that ensure environment consistency

### File Ownership Matrix

Key design decision: Files are strictly categorized into three types:
- **Orchestration-only**: `scripts/`, `scripts/lib/`, `scripts/hooks/`, `scripts/install-hooks.sh`, `scripts/cleanup*.sh`, `scripts/sync_setup_worktrees.sh`, `scripts/reverse_sync_orchestration.sh`, `scripts/architectural_rule_engine.py`
- **Orchestration-managed**: `setup/`, `deployment/`, `docs/orchestration*.md`, `docs/env_management.md`, `docs/git_workflow_plan.md`, `docs/guides/`, `docs/critical_files_check.md`, `pyproject.toml`, `requirements*.txt`, `uv.lock`, `.gitignore`, `.gitattributes`, `launch.py`
- **Branch-specific**: `tsconfig.json`, `package.json`, `tailwind.config.ts`, `vite.config.ts`, `drizzle.config.ts`, `components.json`, all application source code

---

## Development Workflow

### Code Review Process

All changes must undergo rigorous code review before merging. Reviewers must verify: functionality preservation, code simplicity and conciseness, test coverage adequacy, performance considerations, security best practices, consistency with user experience standards. When reviewing orchestration changes, special attention must be paid to the impact on all other branches and the synchronization mechanism. Emphasis should be placed on challenging unnecessary complexity while ensuring no functionality is lost and promoting simpler solutions.

### Orchestration Change Process

When modifying orchestration tools:
1. Work exclusively in the `orchestration-tools` branch
2. Test synchronization to other branches before committing
3. Update documentation in `/docs/` to reflect any workflow changes
4. Ensure backward compatibility for existing development environments
5. Consider the impact on all other branches when making changes

### Verification Process

For repositories implementing verification requirements:
1. **Verification-First Development**: Changes must pass comprehensive verification before merging
2. **Context-Aware Verification**: Include environment variables, dependency versions, and infrastructure state
3. **Generate detailed reports** for verification failures but allow merges to proceed (fail-safe)
4. **All verification results** must be logged for audit and debugging purposes
5. **Success criteria** include measurable metrics (verification time reduction, pass rates)

---

## Documentation Standards

Every public function, class, and module must include comprehensive docstrings following Google-style documentation conventions. Maintain updated README files and API documentation to ensure new contributors can easily understand and contribute to the project. Update documentation in `/docs/` to reflect workflow changes. Use project guidance files for runtime development guidance.

---

## Deployment and Operations

All deployments must follow documented procedures. Monitoring and logging solutions must be in place for all production services to ensure operational visibility and rapid incident response. Monitor performance metrics continuously. Implement comprehensive performance monitoring with alerts for deviations.

---

## Governance

### Change Categories

#### Minor Changes
- Typo corrections
- Formatting improvements
- Clarification of existing principles without changing their meaning
- Updates to version or date information

#### Major Changes
- Addition of new principles
- Modification of existing principles
- Removal of existing principles
- Changes that affect implementation practices

#### Critical Changes
- Changes that require updates to existing code or processes
- Changes that impact multiple repositories significantly
- Changes that may break existing implementations

### Change Request Process

#### 1. Proposal Submission
- Create a GitHub issue describing the proposed change
- Include rationale for the change
- Specify which repositories will be affected
- Identify potential impact on existing implementations

#### 2. Review Process
- The change proposal must be reviewed by at least 2 core contributors
- Reviews should be completed within 5 business days
- Reviewers should consider:
  - Alignment with project goals
  - Impact on existing implementations
  - Consistency with other principles
  - Need for corresponding documentation updates

#### 3. Approval Process
- Minor changes: Approval by 1 core contributor
- Major changes: Approval by 2 core contributors
- Critical changes: Approval by 3 core contributors and team consensus

#### 4. Implementation
- Update the master constitution file first: `~/.aiglobal/constitution.md`
- Run the synchronization script: `python sync_constitution.py`
- Verify all constitution files are updated correctly
- Update any related documentation if needed

#### 5. Verification
- Run the synchronization script to ensure all files are consistent
- Test any affected processes or workflows
- Verify that all repositories continue to function as expected

### Synchronization Process

#### Master File Management
- The master constitution file is located at: `~/.aiglobal/constitution.md`
- All changes must be made to the master file first
- The synchronization script copies content from the master to all other constitution files

#### Post-Change Synchronization
1. Update the master constitution file with the approved changes
2. Run the synchronization script: `python sync_constitution.py`
3. Verify that all constitution files have been updated correctly
4. Commit changes to all repositories with consistent commit messages
5. Update the version information in the constitution files if appropriate

### Roles and Responsibilities

#### Core Contributors
- Review constitution change proposals
- Approve changes based on change category requirements
- Ensure changes align with project goals and principles

#### Project Maintainers
- Have final authority on constitution changes
- Responsible for maintaining the master constitution file
- Ensure proper synchronization across all repositories

#### Change Requesters
- Submit clear and well-documented change proposals
- Participate in the review and approval process
- Implement changes as approved

### Quality Assurance

#### Pre-Commit Checks
- Verify that the master constitution file is syntactically correct
- Run the synchronization script to ensure it completes successfully
- Check that all constitution files are identical after synchronization

#### Post-Commit Verification
- Ensure all constitution files in all repositories are updated
- Verify that the changes don't introduce any formatting or syntax issues
- Confirm that the version information is consistent across all files

### Version Management

#### Version Numbering
- Use semantic versioning: MAJOR.MINOR.PATCH
- MAJOR: Significant changes to core principles
- MINOR: New principles or substantial modifications
- PATCH: Minor clarifications, typo fixes, formatting changes

#### Version Update Process
- Update the version in the master constitution file during implementation
- The synchronization process will automatically update all other files
- Include version change information in commit messages

### Emergency Changes

#### Emergency Process
- For urgent changes that cannot follow the standard process:
  1. Notify all core contributors immediately
  2. Get verbal or written approval from project maintainers
  3. Implement the change following the standard implementation steps
  4. Document the emergency change in the commit message
  5. Follow up with a formal change request to document the rationale

### Rollback Procedures

#### When to Rollback
- If changes cause critical issues in any repository
- If synchronization fails across multiple repositories
- If changes were made without proper approval

#### Rollback Process
1. Revert the master constitution file to the previous version
2. Run the synchronization script to propagate the rollback
3. Verify that all constitution files have been restored
4. Document the reason for the rollback
5. Investigate and resolve the issues before attempting to reapply changes

### Compliance Verification

#### Regular Checks
- Periodically verify that all constitution files remain synchronized
- Check that the master file is the correct source of truth
- Ensure all repositories follow the constitution principles

#### Monitoring
- Implement automated checks if possible to verify consistency
- Report any deviations from the standard constitution immediately
- Maintain compliance records for audit purposes

---

## Conclusion

This Master Constitution serves as the foundational governance document for all repositories in the Email Intelligence Platform. The constitution supersedes all other practices. Amendments require documentation, team consensus, and approval with clear justification. All PRs and reviews must verify compliance with these principles. Deviations must be formally justified and approved. Amendments require formal proposal, review by at least two core contributors, and a majority vote.

Key principles for maintenance:
- Complexity must be justified through clear benefits that significantly outweigh maintenance costs
- Simple solutions are preferred over complex ones
- No functionality should be sacrificed for simplicity
- All constitution files across repositories must remain synchronized with this master document
