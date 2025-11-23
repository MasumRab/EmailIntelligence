# Terminal Jarvis Data Flow

## Overview

Terminal Jarvis follows a layered architecture with clear data flow paths from user input to tool execution. The system is designed to provide a unified interface while maintaining separation between different functional domains.

## High-Level Data Flow

```
User Input → CLI Parser → Business Logic → Tool Management → External Tools → Output
     ↑                                                                      ↓
     └────────────────── Configuration ←─────────────────── Authentication ←─┘
```

## Detailed Data Flow

### 1. User Input Processing

1. **Command Entry**: User runs `terminal-jarvis [command] [options]`
2. **CLI Parsing**: `src/cli.rs` uses `clap` to parse arguments
3. **Command Routing**: Arguments are routed to appropriate CLI logic handlers

### 2. Business Logic Execution

1. **Handler Selection**: CLI logic modules determine the appropriate action
2. **Data Retrieval**: Configuration and authentication data are loaded as needed
3. **Processing**: Business logic is executed using data from various domains
4. **State Management**: Application state is maintained throughout the process

### 3. Tool Management Flow

1. **Tool Detection**: Tools domain checks if requested tool is installed
2. **Configuration Loading**: Tool-specific configuration is loaded from `config/tools/`
3. **Authentication Setup**: Auth domain prepares environment with saved credentials
4. **Execution Preparation**: Tools domain prepares command and arguments
5. **Environment Preparation**: Authentication-safe environment is set up with exported credentials
6. **Terminal State Management**: Proper terminal preparation for tools requiring special handling
7. **Interactive Pause**: User confirmation prompt before tool execution (interactive environments)
8. **Tool Launch**: External tool is executed with proper environment setup and stdio inheritance
9. **Session Continuation Check**: Post-execution analysis determines if session should continue
10. **Environment Restoration**: Original environment is restored after tool execution

### 4. Configuration Flow

1. **Config Discovery**: Config domain searches for configuration files
2. **File Loading**: TOML configuration files are parsed and validated
3. **Data Merging**: User preferences are merged with default configurations
4. **Runtime Access**: Other domains access configuration data through ConfigManager API

### 5. Authentication Flow

1. **Credential Retrieval**: Auth domain loads saved credentials from secure storage
2. **Environment Setup**: Authentication-safe environment is prepared
3. **Browser Warning**: Users are warned if browser authentication might be triggered
4. **Credential Export**: Credentials are exported to environment variables for tools
5. **Environment Restoration**: Original environment is restored after tool execution

### 6. Theme and Presentation Flow

1. **Theme Selection**: Current theme is retrieved from global configuration
2. **UI Element Creation**: Themed UI components are created using inquire library
3. **Text Formatting**: Content is formatted according to theme specifications
4. **Output Rendering**: Formatted content is displayed to the user

## Component Interactions

### CLI ↔ CLI Logic
- CLI parses user input and routes to appropriate CLI logic handlers
- CLI logic returns results for display

### CLI Logic ↔ Tools
- CLI logic requests tool operations (run, install, list, etc.)
- Tools domain provides tool status and execution capabilities

### Tools ↔ Configuration
- Tools domain loads tool-specific configuration data
- Configuration domain provides unified access to settings

### Tools ↔ Authentication
- Tools domain requests authentication setup for tool execution
- Authentication domain provides environment preparation and credential management

### All Components ↔ Theme
- All UI components use theme domain for consistent presentation
- Theme domain provides styling and formatting utilities

## Session Continuation Data Flow

### Normal Tool Execution
```
User Command → Tool Execution → Tool Exits → Return to Menu
```

### Session Continuation Case
```
User Command → Tool Execution → Internal Command Detection → 
Tool Exits → Session Continuation Check → Restart Tool → 
Tool Exits → Return to Menu
```

### Key Decision Points
1. **Command Analysis**: Determine if command was internal (auth, config) or exit
2. **Execution Time**: Quick completions are treated differently
3. **Tool Type**: Some tools have special handling requirements

## Wrapper Execution Details

### Argument Passing
- Natural language arguments are passed directly to underlying tools without parsing or modification
- Example: `terminal-jarvis run claude review src/` becomes `claude review src/`
- All additional arguments beyond the tool name are passed through unchanged

### Environment Management Flow
```
Tool Request → Credential Retrieval → Environment Setup → Tool Execution → Environment Restoration
     ↑              ↓                        ↓                  ↓                   ↓
Secure Storage  Auth Variables      Export to Env       Stdio Inheritance    Original Env
```

### Special Tool Handling
- **OpenCode**: Special terminal preparation for input focus management
- **Aider**: Environment variables set to prevent browser auto-opening and handle Ctrl+C properly
- **Goose**: Whitelisted environment with only essential variables for provider integration
- **Qwen**: Credential flickering prevention in headless/Codespaces environments

### Execution Context Management
1. **Stdio Inheritance**: All tools inherit stdin, stdout, and stderr for proper interaction
2. **Signal Handling**: Special handling for tools with known signal processing issues
3. **Process Management**: Different execution methods for different tools (direct status vs. specialized runners)
4. **Error Recovery**: Graceful handling of tool-specific exit codes and failure modes

## Error Handling Flow

1. **Error Detection**: Errors are caught at various levels
2. **Context Enrichment**: Error messages are enhanced with context
3. **User Notification**: Clear error messages are displayed
4. **Graceful Degradation**: System continues to function where possible
5. **Recovery Options**: Users are provided with recovery paths

## Data Persistence

### Configuration Files
- **Location**: `config/` directory and user config directories
- **Format**: TOML files
- **Access**: Read at startup, cached in memory

### Authentication Data
- **Location**: Secure storage in user config directories
- **Format**: Encrypted/secure storage mechanism
- **Access**: On-demand loading for tool execution

### Cache Data
- **Location**: User cache directories
- **Format**: Serialized data structures
- **Access**: Version cache for performance optimization

## External Integrations Data Flow

### GitHub Integration
1. **API Request**: Services domain makes GitHub API calls
2. **Authentication**: GitHub tokens are used from auth domain
3. **Data Processing**: Response data is processed and formatted
4. **User Presentation**: Results are displayed through theme domain

### NPM Operations
1. **Command Execution**: Services domain executes NPM commands
2. **Output Capture**: Command output is captured and parsed
3. **Result Processing**: Results are formatted for display
4. **Error Handling**: NPM errors are handled and presented

## Asynchronous Operations

### Async/Await Pattern
- Used throughout for non-blocking operations
- Particularly important for HTTP requests and file operations
- Tool execution uses async patterns where appropriate

### Concurrency Management
- Tokio runtime manages concurrent operations
- Progress indicators update independently
- Multiple operations can run in parallel when safe

## Performance Considerations

### Caching Strategy
- Configuration data is cached after initial load
- Version information is cached to avoid repeated lookups
- Theme data is cached for consistent performance

### Lazy Loading
- Components are loaded only when needed
- Configuration files are parsed on first access
- Tool detection happens on demand

### Memory Management
- Rust's ownership system ensures efficient memory usage
- Temporary data is cleaned up automatically
- Large data structures are processed efficiently