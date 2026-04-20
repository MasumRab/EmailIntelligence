# EmailIntelligence Scientific Branch - Project Documentation

## Project Overview

EmailIntelligence is a sophisticated full-stack application designed to provide intelligent email analysis and management capabilities. The scientific branch implements a hybrid architecture that combines the best features from both local and remote architectural approaches, featuring:

- **AI-powered email analysis** with constitutional compliance checking
- **Git worktree-based conflict resolution** using constitutional/specification-driven analysis
- **Modular architecture** with interface-based design patterns
- **Advanced CLI tools** for intelligent branch merge conflict resolution
- **Context control systems** for enhanced security and performance
- **Semantic merging capabilities** for intelligent conflict resolution

## Architecture

### Core Components
- `src/main.py`: Factory pattern implementation with `create_app()` function for service compatibility
- `emailintelligence_cli.py`: Advanced CLI with constitutional analysis and conflict resolution
- `src/core/`: Core models, interfaces, and exception handling
- `src/git/`: Git operations and conflict detection modules
- `src/analysis/`: Conflict analysis and constitutional analysis engines
- `src/resolution/`: Resolution engines and semantic merging capabilities
- `src/strategy/`: Strategy generation and risk assessment modules
- `src/validation/`: Validation frameworks and compliance checking

### Interface-Based Architecture
The scientific branch implements a comprehensive interface-based architecture:
- `src/core/interfaces.py`: Core interfaces (IConflictDetector, IConstitutionalAnalyzer, etc.)
- `src/git/conflict_detector.py`: Implements IConflictDetector interface
- `src/analysis/constitutional/analyzer.py`: Implements constitutional analysis interface
- `src/resolution/auto_resolver.py`: Implements automated resolution interface

### CLI Framework
- `.cli_framework/`: Modular integration framework for safe feature adoption
- `emailintelligence_cli.py`: Main CLI application with constitutional analysis
- Advanced conflict resolution using constitutional/specification-driven analysis
- Spec-kit strategies for intelligent merge resolution

## Building and Running

### Prerequisites
- Python 3.12+
- Git with worktree support
- Node.js (for frontend components)
- Optional: CUDA-compatible GPU for enhanced AI processing

### Setup
```bash
# Clone the repository
git clone <repository-url>
cd EmailIntelligence

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# For development:
pip install -r requirements-dev.txt
```

### Running the Application
```bash
# Using the factory pattern (recommended for scientific branch)
uvicorn src.main:create_app --factory --host 0.0.0.0 --port 8000

# Or using the launch script
python launch.py

# For development with hot reloading
uvicorn src.main:create_app --factory --reload --host 0.0.0.0 --port 8000
```

### Running the CLI
```bash
# Setup resolution workspace
python emailintelligence_cli.py setup-resolution --pr 123 --source-branch feature/auth --target-branch main

# Analyze constitutional compliance
python emailintelligence_cli.py analyze-constitutional --pr 123 --constitution ./constitutions/auth.yaml

# Develop resolution strategy
python emailintelligence_cli.py develop-spec-kit-strategy --pr 123 --worktrees --interactive

# Execute content alignment
python emailintelligence_cli.py align-content --pr 123 --interactive --checkpoint-each-step

# Validate resolution
python emailintelligence_cli.py validate-resolution --pr 123 --comprehensive
```

## Key Features

### 1. Constitutional Analysis
- Advanced constitutional compliance checking using constitutional engines
- Specification-driven analysis for code quality and standards
- Requirement validation against predefined constitutional rules
- Risk assessment and mitigation strategies

### 2. Conflict Resolution
- Git worktree-based conflict detection and resolution
- Semantic merging capabilities for intelligent conflict handling
- Constitutional compliance validation during merge processes
- Multi-phase resolution strategies with risk assessment

### 3. Interface-Based Design
- Modular architecture with clear separation of concerns
- Testable components through dependency injection
- Extensible design patterns for future enhancements
- Consistent API contracts across modules

### 4. Context Control
- Enhanced security through context isolation
- Performance optimization with context-aware operations
- Resource management with context boundaries
- Multi-tenant support with proper isolation

## Development Conventions

### Code Structure
- All source code in `src/` directory following consistent import paths
- Interface-based design with clear contracts in `src/core/interfaces.py`
- Modular components organized by functionality in subdirectories
- Test files co-located with source files in `tests/` directories

### Git Workflow
- Use worktree-based development for complex merge scenarios
- Follow constitutional analysis for code compliance
- Implement feature flags for experimental functionality
- Maintain backward compatibility during refactors

### Testing
- Unit tests for all core functionality
- Integration tests for multi-component interactions
- Constitutional compliance validation as part of CI
- Performance benchmarks for critical paths

## Factory Command Structure

The scientific branch implements a factory pattern in `src/main.py` with the `create_app()` function that is compatible with service startup expectations:

```bash
# Standard factory startup (expected by remote branch patterns)
uvicorn src.main:create_app --factory --host 0.0.0.0 --port 8000

# With additional options
uvicorn src.main:create_app --factory --host 0.0.0.0 --port 8000 --workers 4 --log-level info

# For development with reload
uvicorn src.main:create_app --factory --reload --host 0.0.0.0 --port 8000
```

This factory pattern allows the application to:
- Meet remote branch service startup expectations
- Preserve all local branch functionality
- Integrate context control patterns from both architectures
- Maintain compatibility with different deployment scenarios

## CLI Integration Framework

The scientific branch includes a comprehensive CLI framework that can be used by other branches:

### Installation Options
```bash
# Install in minimal mode (core CLI functionality only)
./.cli_framework/install.sh minimal

# Install in full mode (all features with constitutional analysis)
./.cli_framework/install.sh full

# Install in custom mode (selected components)
./.cli_framework/install.sh custom
```

### Safe Branch Integration
```bash
# Merge CLI features to another branch with backup creation
./.cli_framework/merge_to_branch.sh --target <branch_name> --mode <minimal|full>
```

### Non-Interference Policy
- Preserves existing functionality in target branches
- Creates automatic backups before modifications
- Implements modular installation approach
- Provides rollback capabilities

## Troubleshooting

### Common Issues
1. **Import Path Issues**: Ensure all imports use the `src/` structure consistently
2. **Service Startup Failures**: Verify factory pattern implementation with `--factory` option
3. **Constitutional Analysis Failures**: Check constitution files and compliance requirements
4. **Context Control Issues**: Validate context isolation and security configurations

### Validation Commands
```bash
# Verify factory function exists and works
python -c "from src.main import create_app; app = create_app(); print('Factory function works')"

# Test constitutional analysis
python -c "from emailintelligence_cli import EmailIntelligenceCLI; cli = EmailIntelligenceCLI(); print('CLI initialized successfully')"

# Check interface implementations
python -c "from src.core.interfaces import IConflictDetector; print('Interfaces available')"
```

## Branch-Specific Considerations

The scientific branch represents a mature implementation that:
- Combines architectural patterns from multiple development streams
- Maintains all functionality from both local and remote branches
- Implements advanced constitutional analysis and conflict resolution
- Provides a stable foundation for further development
- Includes comprehensive documentation and validation tools

## Key Files and Directories

- `src/main.py`: Factory pattern implementation for service compatibility
- `emailintelligence_cli.py`: Advanced CLI with constitutional analysis
- `src/core/`: Core interfaces, models, and exceptions
- `src/git/`: Git operations and conflict detection
- `src/analysis/`: Analysis engines and constitutional analyzers
- `src/resolution/`: Resolution engines and semantic mergers
- `src/strategy/`: Strategy generation and risk assessment
- `src/validation/`: Validation frameworks and compliance checkers
- `.cli_framework/`: Modular CLI integration framework
- `guidance/`: Comprehensive documentation and merge guidance
- `docs/`: Detailed documentation and architectural guides