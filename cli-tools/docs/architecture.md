# Terminal Jarvis Architecture Overview

## System Overview

Terminal Jarvis is a unified command center for AI coding tools written in Rust. It provides a thin wrapper that manages and runs multiple AI coding assistants through a beautiful terminal interface with session continuation capabilities. The wrapper design passes natural language arguments directly to underlying tools while providing enhanced user experience through environment management and execution context control.

## Core Architecture Patterns

The project follows a **domain-based modular architecture** pattern, where functionality is organized into focused domains rather than generic modules. This approach promotes:

1. **Separation of Concerns**: Each domain handles a specific aspect of the application
2. **Maintainability**: Changes to one domain don't affect others
3. **Testability**: Domains can be tested independently
4. **Scalability**: New features can be added as new domains

## Key Components

### 1. Main Entry Point (`src/main.rs`)
- Simple entry point that initializes the CLI and runs it
- Delegates all functionality to the CLI module

### 2. CLI Layer (`src/cli.rs`)
- Uses `clap` for command-line argument parsing
- Defines all available commands: run, install, update, list, info, auth, templates, config, cache, benchmark
- Routes commands to appropriate CLI logic handlers

### 3. CLI Logic Domain (`src/cli_logic/`)
This is the core business logic layer with multiple focused modules:

- **Entry Point** (`cli_logic_entry_point.rs`): Coordinates menu systems and main workflows
- **Interactive Interface** (`cli_logic_interactive.rs`): Handles the T.JARVIS themed interface
- **Tool Execution** (`cli_logic_tool_execution.rs`): Manages tool launching
- **Update Operations** (`cli_logic_update_operations.rs`): Handles tool updates
- **Info Operations** (`cli_logic_info_operations.rs`): Displays tool information
- **List Operations** (`cli_logic_list_operations.rs`): Lists available tools
- **Auth Operations** (`cli_logic_auth_operations.rs`): Manages authentication
- **Template Operations** (`cli_logic_template_operations.rs`): Handles templates
- **Config Management** (`cli_logic_config_management.rs`): Manages configuration
- **Benchmark Operations** (`cli_logic_benchmark_operations.rs`): Handles benchmarking
- **Welcome System** (`cli_logic_welcome.rs`): Displays welcome screen
- **Responsive Display** (`cli_logic_responsive_display.rs`): Handles responsive UI elements
- **Responsive Menu** (`cli_logic_responsive_menu.rs`): Manages themed menus

### 4. Tools Domain (`src/tools/`)
Manages all tool-related functionality:

- **Entry Point** (`tools_entry_point.rs`): Main ToolManager API
- **Command Mapping** (`tools_command_mapping.rs`): Maps display names to CLI commands
- **Detection** (`tools_detection.rs`): Detects tool installation status
- **Display** (`tools_display.rs`): Unified tool information display
- **Execution Engine** (`tools_execution_engine.rs`): Runs tools with session continuation
- **Process Management** (`tools_process_management.rs`): Handles process execution
- **Startup Guidance** (`tools_startup_guidance.rs`): Provides tool-specific guidance
- **Configuration** (`tools_config.rs`): Loads tool configurations from modular files

### 5. Configuration Domain (`src/config/`)
Handles all configuration management:

- **Entry Point** (`config_entry_point.rs`): Main Config API
- **Manager** (`config_manager.rs`): Configuration loading and management
- **File Operations** (`config_file_operations.rs`): File-based configuration operations
- **Structures** (`config_structures.rs`): Configuration data structures
- **Version Cache** (`config_version_cache.rs`): Caching for version information

### 6. Authentication Domain (`src/auth_manager/`)
Manages authentication for all tools:

- **Entry Point** (`auth_entry_point.rs`): Main AuthManager API
- **API Key Management** (`auth_api_key_management.rs`): Handles API keys
- **Credentials Store** (`auth_credentials_store.rs`): Stores credentials securely
- **Environment Detection** (`auth_environment_detection.rs`): Detects auth environment
- **Environment Setup** (`auth_environment_setup.rs`): Sets up auth environment
- **Warning System** (`auth_warning_system.rs`): Warns about auth issues

### 7. Services Domain (`src/services/`)
Handles external service integrations:

- **Entry Point** (`services_entry_point.rs`): Main service APIs
- **GitHub Integration** (`services_github_integration.rs`): GitHub integration
- **NPM Operations** (`services_npm_operations.rs`): NPM package operations
- **Package Operations** (`services_package_operations.rs`): Package management
- **Tool Configuration** (`services_tool_configuration.rs`): Tool configuration services

### 8. Theme Domain (`src/theme/`)
Manages theming and visual presentation:

- **Entry Point** (`theme_entry_point.rs`): Main Theme API
- **Definitions** (`theme_definitions.rs`): Theme data structures
- **Config** (`theme_config.rs`): Theme configuration
- **Global Config** (`theme_global_config.rs`): Global theme management
- **Text Formatting** (`theme_text_formatting.rs`): Text formatting utilities
- **Background Layout** (`theme_background_layout.rs`): Background layout management
- **Utilities** (`theme_utilities.rs`): Theme utilities

### 9. Evals Domain (`src/evals/`)
Handles evaluation and benchmarking of AI tools:

- **Entry Point** (`evals_entry_point.rs`): Main evaluation API
- **Criteria** (`evals_criteria.rs`): Evaluation criteria management
- **Data** (`evals_data.rs`): Evaluation data structures
- **Export** (`evals_export.rs`): Export functionality
- **Metrics** (`evals_metrics.rs`): Evaluation metrics
- **Scoring** (`evals_scoring.rs`): Scoring and ranking logic
- **Benchmarks** (`benchmarks/`): Benchmark-specific functionality

## Data Flow

1. **User Input**: User runs a command through CLI
2. **Command Parsing**: `cli.rs` parses arguments and routes to appropriate handler
3. **Business Logic**: CLI logic modules coordinate the requested operation
4. **Tool Management**: Tools domain handles tool-specific operations
5. **Configuration**: Config domain provides configuration data
6. **Authentication**: Auth domain manages credentials and environment
7. **Services**: Services domain handles external integrations
8. **Presentation**: Theme domain handles visual presentation
9. **Output**: Results are displayed to the user

## Key Features

### Wrapper Design and Execution Context Management
- **Thin Wrapper Architecture**: Natural language arguments are passed directly to underlying tools without modification
- **Environment Preparation**: Authentication credentials are securely loaded and exported to environment variables before tool execution
- **Browser Authentication Handling**: Users are warned when tools are likely to open browser windows for authentication
- **Special Tool Handling**: Different tools receive specialized environment setup (Aider, Goose, Qwen, etc.)
- **Terminal State Management**: Proper terminal state preparation for tools like OpenCode to ensure input focus
- **Session Continuation System**: Prevents users from being kicked out during authentication workflows
- **Intelligent Command Detection**: Distinguishes between internal commands and exits
- **Interactive Pause**: Users are prompted before tool execution in interactive environments
- **Execution Context Management**: Proper stdio inheritance and signal handling for different tools
- **Infinite Loop Prevention**: Ensures proper exit handling and prevents recursive session continuation

### Modular Tool Configuration
- Tools are configured through individual TOML files in `config/tools/`
- Automatic discovery of new tools without code changes
- Unified display system for consistent tool information

### Multi-Platform Distribution
- Available through NPM, Crates.io, and Homebrew
- Automated release process with version synchronization
- Homebrew integration with platform-specific archives

### Authentication Management
- Secure credential storage and retrieval
- Environment preparation for different tools
- Browser authentication warnings and guidance

### Themed Interface
- Multiple theme options (Default, Minimal, Terminal)
- Consistent styling across all UI elements
- Responsive design for different terminal sizes

## Technology Stack

- **Language**: Rust
- **CLI Framework**: clap
- **Async Runtime**: tokio
- **HTTP Client**: reqwest
- **Serialization**: serde
- **Error Handling**: anyhow
- **Configuration**: toml
- **Interactive UI**: inquire
- **Progress Indicators**: indicatif
- **Terminal Control**: crossterm
- **Testing**: tokio-test

## Configuration System

The configuration system uses a modular approach:
- Global configuration in `config.toml`
- Tool-specific configurations in `config/tools/*.toml`
- User preferences in `terminal-jarvis.toml`
- Automatic loading and validation of configurations

## Testing Strategy

- Unit tests within each module using `#[cfg(test)]`
- Integration tests in the `tests/` directory
- Test-driven development for bug fixes
- Comprehensive validation before releases