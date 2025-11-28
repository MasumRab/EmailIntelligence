# Task ID: 34

**Title:** Create Integration Migration Guide for Context Control Module Refactoring

**Status:** pending

**Dependencies:** 30, 31 ⏸

**Priority:** medium

**Description:** Develop a comprehensive migration guide for the 'context_control' module, documenting breaking changes from static to instance methods, providing code examples, a migration checklist, common pitfalls, and a testing strategy for its new dependency injection architecture.

**Details:**

This task involves creating a detailed migration guide for developers transitioning their codebases to the refactored `context_control` module, specifically addressing the shift from static class methods to instance methods and the introduction of Dependency Injection (DI). The guide should be located in `docs/migration_guides/context_control_migration.md` and must cover the following sections:

1.  **List of Breaking Changes:** Clearly delineate the fundamental architectural shift from static methods (e.g., `BranchMatcher.find_profile_for_branch()`) to instance-based methods (e.g., `BranchMatcher(branch_name).find_profile_for_branch()`). Explain the necessity of instantiating classes and injecting dependencies. Reference `REFACTORING_ANALYSIS.md` for the deeper rationale behind these changes.

2.  **Side-by-Side Code Examples:** Provide clear, concise examples illustrating the old (static) usage versus the new (instance-based, DI-enabled) usage for key components and methods within `src/backend/context_control/context_control.py`. For instance, show how `BranchMatcher.find_profile_for_branch()` used to be called compared to `branch_matcher = BranchMatcher(branch_name); branch_matcher.find_profile_for_branch()`, and how dependencies might now be passed into the constructor. Refer to `REFACTORING_QUICK_REFERENCE.md` for existing code snippets and patterns.

3.  **Step-by-Step Migration Checklist:** Offer an actionable checklist for developers, including steps such as:
    *   Identify all calls to static `context_control` methods using `git grep -r "context_control\.[A-Za-z_]+\(" -- "*.py"`.
    *   Update import statements if necessary.
    *   Refactor code to instantiate `context_control` classes (e.g., `BranchMatcher`, `EnvironmentTypeDetector`) and call their instance methods.
    *   Implement dependency injection for any required services or configurations, typically in the constructor (`__init__`) or via a factory.
    *   Remove temporary deprecation shims and suppressions for `DeprecationWarning` introduced by Task 33 once migration is complete.

4.  **Common Pitfalls and How to Avoid Them:** Discuss potential issues like forgetting to instantiate objects, incorrect dependency wiring, improper mocking in tests, or failing to remove deprecation warnings. Provide solutions and best practices.

5.  **Testing Strategy for the New DI-based Architecture:** Detail how to effectively test code that uses the new DI patterns. This section should build upon and reference the comprehensive test suite developed in Task 32. Emphasize unit testing with mock objects for dependencies, and integration testing for components working together through DI.

### Tags:
- `work_type:documentation`
- `component:context-control`
- `scope:architectural`
- `scope:developer-experience`
- `purpose:stability`

**Test Strategy:**

1.  **Internal Review:** Circulate the draft migration guide among the development team and key stakeholders for review, ensuring accuracy, clarity, and completeness. Focus on whether the instructions are easy to follow and resolve potential confusion.
2.  **Pilot Migration Test:** Select a small, representative code segment or feature that uses the old `context_control` methods. Have a developer (not the author of the guide) attempt to migrate it following the guide's instructions. Collect feedback on pain points, missing information, or unclear

## Subtasks

### 34.1. Draft Migration Guide Structure and Initial Content

**Status:** pending  
**Dependencies:** None  

Create the `context_control_migration.md` file in the specified directory and populate it with the main section headers for the guide, including an introduction.

**Details:**

Create the file `docs/migration_guides/context_control_migration.md`. Include a general introduction to the refactoring and placeholders for the following sections: 'List of Breaking Changes', 'Side-by-Side Code Examples', 'Step-by-Step Migration Checklist', 'Common Pitfalls and How to Avoid Them', and 'Testing Strategy for the New DI-based Architecture'.

### 34.2. Detail Breaking Changes and Provide Code Examples

**Status:** pending  
**Dependencies:** None  

Write the 'List of Breaking Changes' section, explaining the architectural shift from static to instance methods and the introduction of DI. Provide clear side-by-side code examples illustrating old vs. new usage.

**Details:**

Clearly delineate the fundamental architectural shift from static methods to instance-based methods and the necessity of instantiating classes and injecting dependencies. Include side-by-side code examples for `BranchMatcher.find_profile_for_branch()` and other key `context_control` components, showing old static usage versus new instance-based, DI-enabled usage. Reference `REFACTORING_ANALYSIS.md` for rationale and `REFACTORING_QUICK_REFERENCE.md` for existing snippets.

### 34.3. Develop Step-by-Step Migration Checklist

**Status:** pending  
**Dependencies:** None  

Create an actionable, ordered checklist for developers to follow when migrating their codebases. This includes steps for identifying old calls, refactoring, and implementing dependency injection.

**Details:**

Develop a comprehensive, step-by-step migration checklist. Include items such as: using `git grep` to identify static `context_control` method calls, updating import statements, refactoring to instantiate classes (`BranchMatcher`, `EnvironmentTypeDetector`), implementing dependency injection (e.g., via constructor), and removing temporary deprecation shims/suppressions introduced by Task 33 once migration is complete.

### 34.4. Outline Common Migration Pitfalls and Avoidance Strategies

**Status:** pending  
**Dependencies:** None  

Identify potential issues developers might encounter during the migration to the refactored module and provide best practices and solutions to avoid or resolve them.

**Details:**

Discuss common pitfalls such as forgetting to instantiate objects, incorrect dependency wiring, improper mocking in tests, or failing to remove deprecation warnings. For each pitfall, provide clear solutions and best practices, e.g., strategies for DI container usage, clear factory patterns, or specific mocking examples for testing.

### 34.5. Define Testing Strategy for New DI Architecture

**Status:** pending  
**Dependencies:** None  

Document how to effectively test code that utilizes the new dependency injection patterns, building upon the comprehensive test suite developed in Task 32.

**Details:**

Detail the testing approach for the new DI architecture. Emphasize strategies for unit testing with mock objects for dependencies (e.g., using `pytest-mock`) and integration testing for components working together through DI. Reference and build upon the comprehensive test suite developed in Task 32 to illustrate best practices and relevant examples.
