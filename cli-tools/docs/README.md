# Terminal Jarvis Documentation

This directory contains comprehensive documentation for the Terminal Jarvis project, covering its architecture, technology stack, data flow, and component relationships.

## Documentation Files

### [architecture.md](architecture.md)
High-level overview of the Terminal Jarvis system architecture, including:
- Core architecture patterns
- Key components and their responsibilities
- Data flow through the system
- Key features like session continuation and modular configuration

### [technology-stack.md](technology-stack.md)
Detailed breakdown of the technologies, libraries, and tools used in Terminal Jarvis:
- Core technologies (Rust, Tokio, Clap, etc.)
- Dependencies and their versions
- External tool integrations
- Platform support information

### [data-flow.md](data-flow.md)
Comprehensive documentation of how data moves through the system:
- User input processing
- Business logic execution
- Tool management workflows
- Configuration and authentication flows
- Session continuation mechanisms
- Error handling processes

### [component-relationships.md](component-relationships.md)
Detailed analysis of how different components interact:
- Component interaction diagrams
- Dependency relationships
- Cross-domain services
- Security and performance considerations

### [modular-architecture.md](modular-architecture.md)
In-depth explanation of the domain-based modular architecture:
- Domain-based architecture principles
- Implementation patterns and examples
- Cross-domain communication
- Testing strategies
- Refactoring guidelines

### [wrapper-design.md](wrapper-design.md)
Detailed documentation of the thin wrapper architecture:
- Natural language argument handling
- Environment management and authentication flow
- Execution context management
- Session continuation system
- Tool-specific handling and error recovery

## Architecture Overview

Terminal Jarvis follows a **domain-based modular architecture** where functionality is organized into focused domains rather than generic modules. This approach promotes:

1. **Separation of Concerns**: Each domain handles a specific aspect of the application
2. **Maintainability**: Changes to one domain don't affect others
3. **Testability**: Domains can be tested independently
4. **Scalability**: New features can be added as new domains

The system also implements a **thin wrapper design** that provides a unified interface for multiple AI coding tools while passing natural language arguments directly to underlying tools. This approach enhances user experience through environment management, authentication handling, and session continuation without interfering with the core tool functionality.

## Key Domains

1. **CLI Layer**: Command-line interface using clap
2. **CLI Logic**: Business logic and workflow coordination
3. **Tools**: Tool management and execution with session continuation
4. **Configuration**: Settings and configuration management
5. **Authentication**: Credential and auth management
6. **Services**: External service integrations
7. **Theme**: Presentation and theming
8. **Evals**: Evaluation and benchmarking

## Getting Started

To understand the Terminal Jarvis architecture, start with [architecture.md](architecture.md) for a high-level overview, then explore the specific aspects that interest you most.

For developers looking to contribute, [modular-architecture.md](modular-architecture.md) provides detailed guidance on the architectural patterns used throughout the codebase.