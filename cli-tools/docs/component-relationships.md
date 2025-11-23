# Terminal Jarvis Component Relationships

## System Overview

This document describes the relationships between different components in the Terminal Jarvis system, showing how they interact and depend on each other.

## Component Categories

### Core Components
- **CLI**: Command-line interface parser and router
- **CLI Logic**: Business logic and workflow coordination
- **Tools**: Tool management and execution
- **Configuration**: Configuration management
- **Authentication**: Credential and auth management
- **Services**: External service integrations
- **Theme**: Presentation and theming
- **Evals**: Evaluation and benchmarking

## Component Interaction Diagrams

### High-Level Component Relationships

```
[User] 
   ↓ (commands)
[CLI] 
   ↓ (parsed commands)
[CLI Logic] ↔ [Tools] ↔ [Configuration] ↔ [Authentication]
   ↓ (results)
[Theme] ← [All Components] (for presentation)
   ↓ (formatted output)
[User]
```

### Detailed Component Interactions

#### CLI ↔ CLI Logic
```
CLI (src/cli.rs)
   → Commands and arguments
   → Routing decisions
   → Error handling

CLI Logic (src/cli_logic/)
   → Business logic execution
   → Result formatting
   → Menu system management
```

#### CLI Logic ↔ Tools
```
CLI Logic
   → ToolManager::run_tool() (execution requests)
   → ToolManager::get_available_tools() (status queries)
   → ToolManager::check_tool_installed() (validation)
   → ToolManager::get_installed_tools() (listing)

Tools Domain
   → Tool execution with session continuation
   → Installation and update operations
   → Tool detection and status checking
   → Command mapping and argument processing
```

#### Tools ↔ Configuration
```
Tools Domain
   → get_tool_config_loader() (configuration access)
   → get_tool_definition() (tool specifications)
   → get_install_command() (installation instructions)

Configuration Domain
   → Tool definitions from TOML files
   → Installation/update command specifications
   → Feature and authentication configuration
```

#### Tools ↔ Authentication
```
Tools Domain
   → AuthManager::export_saved_env_vars() (credential export)
   → AuthManager::prepare_auth_safe_environment() (env setup)
   → AuthManager::get_tool_credentials() (credential retrieval)
   → AuthManager::restore_environment() (cleanup)

Authentication Domain
   → Credential storage and retrieval
   → Environment preparation and restoration
   → Secure credential management
```

#### All Components ↔ Theme
```
CLI Logic, Tools, Authentication, etc.
   → theme_global_config::current_theme() (get active theme)
   → theme.primary(), theme.secondary(), theme.accent() (formatting)
   → create_themed_select() (themed UI components)

Theme Domain
   → Theme definition and management
   → Text formatting and styling
   → Responsive display elements
```

#### CLI Logic ↔ Services
```
CLI Logic
   → PackageService for update operations
   → GitHubService for GitHub integrations
   → Other service operations

Services Domain
   → External service interactions
   → Package management operations
   → GitHub API calls and processing
```

#### CLI Logic ↔ Evals
```
CLI Logic
   → EvalManager for evaluation operations
   → Benchmark execution and management

Evals Domain
   → Tool comparison and benchmarking
   → Evaluation criteria management
   → Result export functionality
```

## Dependency Relationships

### Internal Dependencies

#### CLI Logic Dependencies
- **Depends on**: Tools, Configuration, Authentication, Theme, Services, Evals
- **Provides to**: CLI (results), User (interface)

#### Tools Dependencies
- **Depends on**: Configuration (tool definitions), Authentication (credentials), Theme (UI)
- **Provides to**: CLI Logic (execution), User (tool access)

#### Configuration Dependencies
- **Depends on**: None (independent)
- **Provides to**: All other domains (settings)

#### Authentication Dependencies
- **Depends on**: Configuration (auth definitions), Theme (UI)
- **Provides to**: Tools (credentials), CLI Logic (auth management)

#### Theme Dependencies
- **Depends on**: None (independent)
- **Provides to**: All other domains (styling)

### External Dependencies

#### Runtime Dependencies
- **tokio**: Async runtime for all async operations
- **clap**: CLI argument parsing for CLI module
- **inquire**: Interactive UI for CLI Logic and Tools
- **reqwest**: HTTP requests for Services and Evals

#### Build Dependencies
- **serde**: Configuration serialization/deserialization
- **toml**: Configuration file parsing
- **anyhow**: Error handling across all modules

## Data Flow Relationships

### Configuration-Driven Flow
```
Configuration → Tools (tool definitions)
Configuration → Authentication (auth requirements) 
Configuration → CLI Logic (feature flags)
```

### Authentication-Dependent Flow
```
Authentication → Tools (credential setup)
Tools → Authentication (credential validation)
CLI Logic → Authentication (auth menu operations)
```

### Theme-Integrated Flow
```
All Components → Theme (for presentation)
Theme → All Components (styling API)
```

## Cross-Domain Services

### Global Services
- **Theme Global Config**: Accessible by all components for theming
- **Tool Config Loader**: Singleton providing tool configuration access
- **Auth Manager**: Centralized authentication service

### Shared Utilities
- **Progress Context**: Used across CLI Logic and Tools
- **Error Handling**: Standardized across all components
- **Logging**: Consistent across all components

## Component Lifecycle

### Initialization
1. **Configuration**: Loads first (independent)
2. **Theme**: Initializes global theme
3. **Authentication**: Sets up credential storage
4. **Tools**: Configures tool manager
5. **CLI**: Sets up command routing
6. **CLI Logic**: Initializes business logic

### Runtime
1. **CLI** receives user input
2. **CLI Logic** coordinates operations
3. **Tools** manages tool execution
4. **Authentication** provides credentials as needed
5. **Configuration** provides settings on demand
6. **Theme** formats output for display

### Cleanup
1. **Authentication** restores environment
2. **Tools** completes execution
3. **CLI Logic** returns control
4. **Theme** ensures proper display cleanup

## Security Considerations

### Credential Flow
- Authentication domain handles all credential operations
- Credentials flow to Tools domain for execution
- Environment is cleaned up after tool execution
- No credentials stored in plain text

### Configuration Security
- Configuration files validated before loading
- Tool definitions validated for security
- Installation commands sanitized where possible

## Performance Considerations

### Caching Relationships
- Configuration data cached after first load
- Theme objects reused across operations
- Tool detection results cached when appropriate
- Authentication credentials cached during session

### Resource Management
- Async operations managed by tokio runtime
- Memory usage optimized through Rust ownership
- Concurrent operations limited to prevent overload
- Cleanup operations ensure resource recovery