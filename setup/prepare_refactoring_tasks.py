import json

tasks = [
    {
        "id": 8,
        "title": "Refactoring Phase 0: Discovery & Planning",
        "description": "Initial discovery phase to audit existing code, plan integration, and validate feasibility via spikes.",
        "priority": "critical",
        "status": "pending",
        "dependencies": [],
        "subtasks": [
            {
                "id": 1,
                "title": "Audit existing codebase",
                "description": "Document all modules in src/, identify overlaps with proposed architecture, and map dependencies.",
                "status": "pending",
                "priority": "critical",
                "estimated_hours": 16
            },
            {
                "id": 2,
                "title": "Create integration strategy",
                "description": "Decide on merge vs replace vs coexist strategies, design adapter layers, and plan data migration.",
                "status": "pending",
                "priority": "critical",
                "estimated_hours": 12
            },
            {
                "id": 3,
                "title": "Technical spikes",
                "description": "Run spikes for AST-based constitutional analysis, real conflict detection, and performance benchmarking.",
                "status": "pending",
                "priority": "critical",
                "estimated_hours": 40
            },
            {
                "id": 4,
                "title": "Revise estimates",
                "description": "Update timeline based on spikes, identify knowledge gaps, and adjust scope.",
                "status": "pending",
                "priority": "high",
                "estimated_hours": 8
            }
        ]
    },
    {
        "id": 9,
        "title": "Refactoring Phase 1: Foundation",
        "description": "Establish the core architecture, interfaces, and data models.",
        "priority": "critical",
        "status": "pending",
        "dependencies": [8],
        "subtasks": [
            {
                "id": 1,
                "title": "Create Directory Structure",
                "description": "Create new src/ directory structure with all module folders and __init__.py files.",
                "status": "pending",
                "priority": "critical",
                "estimated_hours": 2
            },
            {
                "id": 2,
                "title": "Implement Core Interfaces",
                "description": "Define abstract base classes for IConflictDetector, IConstitutionalAnalyzer, etc. in src/core/interfaces.py.",
                "status": "pending",
                "priority": "critical",
                "estimated_hours": 8
            },
            {
                "id": 3,
                "title": "Implement Data Models",
                "description": "Create dataclasses for Conflict, AnalysisResult, etc. in src/core/models.py.",
                "status": "pending",
                "priority": "critical",
                "estimated_hours": 6
            },
            {
                "id": 4,
                "title": "Implement Configuration Management",
                "description": "Create configuration loading and validation in src/core/config.py.",
                "status": "pending",
                "priority": "high",
                "estimated_hours": 4
            },
            {
                "id": 5,
                "title": "Implement Custom Exceptions",
                "description": "Define custom exception hierarchy in src/core/exceptions.py.",
                "status": "pending",
                "priority": "medium",
                "estimated_hours": 2
            },
            {
                "id": 6,
                "title": "Implement Metadata Storage",
                "description": "Create metadata persistence layer in src/storage/.",
                "status": "pending",
                "priority": "high",
                "estimated_hours": 6
            },
            {
                "id": 7,
                "title": "Implement Logging Utilities",
                "description": "Set up structured logging in src/utils/logger.py.",
                "status": "pending",
                "priority": "medium",
                "estimated_hours": 3
            },
            {
                "id": 8,
                "title": "Set Up Testing Framework",
                "description": "Configure pytest, fixtures, and coverage reporting.",
                "status": "pending",
                "priority": "critical",
                "estimated_hours": 4
            }
        ]
    },
    {
        "id": 10,
        "title": "Refactoring Phase 2: Git Operations",
        "description": "Implement git operations, worktree management, and conflict detection.",
        "priority": "critical",
        "status": "pending",
        "dependencies": [9],
        "subtasks": [
            {
                "id": 1,
                "title": "Implement WorktreeManager",
                "description": "Extract worktree management to src/git/worktree.py.",
                "status": "pending",
                "priority": "critical",
                "estimated_hours": 8
            },
            {
                "id": 2,
                "title": "Implement GitConflictDetector",
                "description": "Real conflict detection using git merge-tree in src/git/conflict_detector.py.",
                "status": "pending",
                "priority": "critical",
                "estimated_hours": 12
            },
            {
                "id": 3,
                "title": "Implement GitMerger",
                "description": "Git merge operations wrapper in src/git/merger.py.",
                "status": "pending",
                "priority": "high",
                "estimated_hours": 8
            },
            {
                "id": 4,
                "title": "Implement Repository Operations",
                "description": "Common git repository operations in src/git/repository.py.",
                "status": "pending",
                "priority": "medium",
                "estimated_hours": 6
            }
        ]
    },
    {
        "id": 11,
        "title": "Refactoring Phase 3: Analysis Layer",
        "description": "Implement AST analysis, requirement checking, and enhancement detection.",
        "priority": "critical",
        "status": "pending",
        "dependencies": [9],
        "subtasks": [
            {
                "id": 1,
                "title": "Implement AST Code Analyzer",
                "description": "Python AST-based code analysis in src/analysis/code/ast_analyzer.py.",
                "status": "pending",
                "priority": "critical",
                "estimated_hours": 16
            },
            {
                "id": 2,
                "title": "Implement Requirement Checkers",
                "description": "Real constitutional requirement checking in src/analysis/constitutional/.",
                "status": "pending",
                "priority": "critical",
                "estimated_hours": 20
            },
            {
                "id": 3,
                "title": "Implement Constitutional Analyzer",
                "description": "Orchestrate requirement checking in src/analysis/constitutional/analyzer.py.",
                "status": "pending",
                "priority": "critical",
                "estimated_hours": 12
            },
            {
                "id": 4,
                "title": "Implement Code Similarity Metrics",
                "description": "Measure code similarity in src/analysis/code/similarity.py.",
                "status": "pending",
                "priority": "high",
                "estimated_hours": 10
            },
            {
                "id": 5,
                "title": "Implement Enhancement Detector",
                "description": "Detect actual enhancements in branches in src/analysis/enhancement/.",
                "status": "pending",
                "priority": "high",
                "estimated_hours": 12
            },
            {
                "id": 6,
                "title": "Implement Code Complexity Analyzer",
                "description": "Calculate code complexity metrics in src/analysis/code/complexity.py.",
                "status": "pending",
                "priority": "medium",
                "estimated_hours": 8
            }
        ]
    },
    {
        "id": 12,
        "title": "Refactoring Phase 4: Strategy & Resolution",
        "description": "Implement strategy selection, risk assessment, and resolution execution.",
        "priority": "critical",
        "status": "pending",
        "dependencies": [10, 11],
        "subtasks": [
            {
                "id": 1,
                "title": "Implement Strategy Selector",
                "description": "Intelligent strategy selection in src/strategy/selector.py.",
                "status": "pending",
                "priority": "critical",
                "estimated_hours": 16
            },
            {
                "id": 2,
                "title": "Implement Risk Assessor",
                "description": "Real risk assessment in src/strategy/risk_assessor.py.",
                "status": "pending",
                "priority": "critical",
                "estimated_hours": 14
            },
            {
                "id": 3,
                "title": "Implement Strategy Generator",
                "description": "Generate multi-phase resolution strategies in src/strategy/generator.py.",
                "status": "pending",
                "priority": "high",
                "estimated_hours": 12
            },
            {
                "id": 4,
                "title": "Implement Auto Resolver",
                "description": "Automatically resolve simple conflicts in src/resolution/auto_resolver.py.",
                "status": "pending",
                "priority": "critical",
                "estimated_hours": 16
            },
            {
                "id": 5,
                "title": "Implement Semantic Merger",
                "description": "Semantic-aware merge strategies in src/resolution/semantic_merger.py.",
                "status": "pending",
                "priority": "high",
                "estimated_hours": 20
            },
            {
                "id": 6,
                "title": "Implement Resolution Executor",
                "description": "Orchestrate resolution execution in src/resolution/executor.py.",
                "status": "pending",
                "priority": "critical",
                "estimated_hours": 10
            },
            {
                "id": 7,
                "title": "Implement Interactive Resolver",
                "description": "Interactive conflict resolution UI in src/resolution/interactive.py.",
                "status": "pending",
                "priority": "medium",
                "estimated_hours": 12
            }
        ]
    },
    {
        "id": 13,
        "title": "Refactoring Phase 5: Validation",
        "description": "Implement test running, security scanning, and quality checking.",
        "priority": "high",
        "status": "pending",
        "dependencies": [12],
        "subtasks": [
            {
                "id": 1,
                "title": "Implement Test Runner",
                "description": "Execute real test suites in src/validation/test_runner.py.",
                "status": "pending",
                "priority": "critical",
                "estimated_hours": 12
            },
            {
                "id": 2,
                "title": "Implement Security Scanner",
                "description": "Integrate security scanning tools in src/validation/security_scanner.py.",
                "status": "pending",
                "priority": "high",
                "estimated_hours": 8
            },
            {
                "id": 3,
                "title": "Implement Quality Checker",
                "description": "Code quality validation in src/validation/quality_checker.py.",
                "status": "pending",
                "priority": "high",
                "estimated_hours": 8
            },
            {
                "id": 4,
                "title": "Implement Validation Orchestrator",
                "description": "Coordinate all validation checks in src/validation/validator.py.",
                "status": "pending",
                "priority": "high",
                "estimated_hours": 6
            }
        ]
    },
    {
        "id": 14,
        "title": "Refactoring Phase 6: CLI Refactoring",
        "description": "Refactor CLI commands, argument parsing, and output formatting.",
        "priority": "critical",
        "status": "pending",
        "dependencies": [13],
        "subtasks": [
            {
                "id": 1,
                "title": "Implement Command Handlers",
                "description": "Refactor CLI commands to use new modules in src/cli/commands.py.",
                "status": "pending",
                "priority": "critical",
                "estimated_hours": 12
            },
            {
                "id": 2,
                "title": "Implement Argument Parsing",
                "description": "Clean argument parsing layer in src/cli/arguments.py.",
                "status": "pending",
                "priority": "high",
                "estimated_hours": 6
            },
            {
                "id": 3,
                "title": "Implement Output Formatting",
                "description": "Consistent output formatting in src/cli/output.py.",
                "status": "pending",
                "priority": "medium",
                "estimated_hours": 6
            },
            {
                "id": 4,
                "title": "Create New CLI Entry Point",
                "description": "New eai.py entry point wiring up all commands.",
                "status": "pending",
                "priority": "critical",
                "estimated_hours": 4
            },
            {
                "id": 5,
                "title": "Implement Backward Compatibility",
                "description": "Ensure old CLI still works and provide migration guide.",
                "status": "pending",
                "priority": "high",
                "estimated_hours": 6
            }
        ]
    },
    {
        "id": 15,
        "title": "Refactoring Phase 7: Testing & Documentation",
        "description": "Achieve test coverage goals, write documentation, and plan release.",
        "priority": "high",
        "status": "pending",
        "dependencies": [14],
        "subtasks": [
            {
                "id": 1,
                "title": "Achieve Test Coverage Goals",
                "description": "Write tests to reach 80%+ coverage.",
                "status": "pending",
                "priority": "critical",
                "estimated_hours": 20
            },
            {
                "id": 2,
                "title": "Write Module Documentation",
                "description": "Comprehensive documentation for all modules.",
                "status": "pending",
                "priority": "high",
                "estimated_hours": 16
            },
            {
                "id": 3,
                "title": "Create Migration Guide",
                "description": "Guide for migrating from old to new CLI.",
                "status": "pending",
                "priority": "high",
                "estimated_hours": 8
            },
            {
                "id": 4,
                "title": "Performance Testing",
                "description": "Benchmark and optimize performance.",
                "status": "pending",
                "priority": "medium",
                "estimated_hours": 12
            },
            {
                "id": 5,
                "title": "Create Release Plan",
                "description": "Plan for production release.",
                "status": "pending",
                "priority": "high",
                "estimated_hours": 4
            }
        ]
    }
]

with open('REFACTORING_TASKS_FOR_IMPORT.json', 'w') as f:
    json.dump({"tasks": tasks}, f, indent=2)

print("Successfully created REFACTORING_TASKS_FOR_IMPORT.json with 8 phases and 47+ subtasks.")
