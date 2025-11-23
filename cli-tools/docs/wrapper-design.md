# Terminal Jarvis Wrapper Design

## Overview

Terminal Jarvis implements a **thin wrapper architecture** that provides a unified interface for multiple AI coding tools. The wrapper design focuses on passing natural language arguments directly to underlying tools while enhancing the user experience through environment management and execution context control.

## Wrapper Design Philosophy

### Thin Wrapper Approach
- **No Language Processing**: Natural language arguments are passed directly to underlying tools without modification
- **No Feature Replication**: Does not reimplement tool-specific features or capabilities
- **Enhanced UX**: Provides consistent interface, authentication management, and session continuity
- **Separation of Concerns**: Maintains clear boundaries between wrapper and tool functionality

### Command Abstraction Layer
```
User Input: terminal-jarvis run claude review src/
     ↓ (command mapping)
Tool Execution: claude review src/
```

## Natural Language Argument Handling

### Direct Pass-Through
The wrapper design ensures that natural language inputs are passed directly to underlying tools:

- `terminal-jarvis run claude review src/` → `claude review src/`
- `terminal-jarvis run gemini generate tests` → `gemini-cli generate tests`
- `terminal-jarvis run qwen explain algorithm.rs` → `qwen-code explain algorithm.rs`

### Argument Processing Flow
1. **Argument Capture**: All arguments after tool name are captured as-is
2. **No Parsing**: Arguments are not parsed or validated by wrapper
3. **Direct Pass-Through**: Arguments are passed directly to underlying tool
4. **Tool Processing**: Natural language understanding is handled entirely by the underlying tool

## Environment Management

### Authentication Flow
```
1. Credential Retrieval
   ↓
2. Environment Preparation
   ↓
3. Tool Execution
   ↓
4. Environment Restoration
```

### Credential Handling
- **Secure Storage**: Credentials are stored securely using AuthManager
- **Environment Export**: Credentials exported to appropriate environment variables before tool execution
- **Tool-Specific Mapping**: Different tools require different environment variable names
- **On-Demand Prompting**: Interactive credential prompts when needed

### Tool-Specific Environment Handling

#### Goose (Special Case)
- **Whitelisted Environment**: Only essential variables are passed to child process
- **Provider Integration**: Supports multiple AI providers (OpenAI, Anthropic, Gemini)
- **Credential Bridging**: Maps between different API key formats

#### Aider (Special Case)
- **Browser Control**: Sets `AIDER_NO_BROWSER=1` to prevent auto-browser opening
- **Terminal Control**: Reduces fancy terminal features in headless environments
- **Ctrl+C Handling**: Special signal processing to handle interruption properly

#### Qwen (Special Case)
- **Credential Flicker Prevention**: Reduces authentication prompts in headless environments
- **API Key Validation**: Heuristic validation for different provider key formats

## Execution Context Management

### Terminal State Management
- **OpenCode**: Special preparation to ensure proper input focus
- **Clean State**: Progress indicators cleared before tool execution
- **Cursor Management**: Cursor visibility restored after execution

### Interactive Features
- **Pause Before Execution**: User prompted to press Enter before tool launch (interactive environments)
- **Session Continuation**: Decision-making for whether to restart tool session after exit
- **Signal Handling**: Proper interruption handling for different tools

### Process Execution
- **Stdio Inheritance**: All tools inherit stdin, stdout, stderr for proper interaction
- **Special Execution Methods**: Different tools use different execution strategies
- **Exit Code Management**: Tool-specific exit code interpretation

## Session Continuation System

### Continuation Decision Logic
```rust
fn should_continue_session(args: &[String]) -> bool {
    // Check for explicit exit commands (never continue)
    let is_exit_command = args.iter().any(|arg| {
        matches!(arg.as_str(), "/exit" | "/quit" | "/bye" | "--exit" | "--quit")
    });
    
    if is_exit_command {
        return false;
    }
    
    // Continue for auth/setup commands only
    let explicit_auth_setup_args = args.iter().any(|arg| {
        matches!(arg.as_str(), "/auth" | "/login" | "--auth" | "/setup" | "/config")
    });
    
    explicit_auth_setup_args
}
```

### Continuation Benefits
- **Authentication Workflows**: Prevents users from being kicked out during auth processes
- **Workflow Continuity**: Maintains context during setup and configuration
- **User Experience**: Reduces friction in common workflows

## Error Handling and Recovery

### Tool-Specific Error Handling
- **Aider**: Treats non-zero exit codes as graceful termination
- **Goose**: Automatically runs `goose configure` if initial run fails due to missing provider
- **General Tools**: Provides meaningful error messages with recovery guidance

### Environment Cleanup
- **Credential Restoration**: Original environment restored after tool execution
- **Temporary State Cleanup**: Any temporary modifications are reverted
- **Resource Management**: Proper cleanup of system resources

## Configuration-Driven Flexibility

### Modular Tool Configuration
- **TOML-Based**: Each tool has its own configuration file in `config/tools/`
- **Dynamic Loading**: Tools auto-discovered from configuration directory
- **Extensible Design**: New tools can be added without code changes

### Feature Mapping
- **Command Mapping**: Tool display names mapped to actual CLI commands
- **Installation Commands**: Tool-specific installation instructions
- **Authentication Requirements**: Tool-specific credential requirements

## Benefits of Wrapper Design

### For Users
- **Consistent Interface**: Single command structure for all AI tools
- **Enhanced UX**: Beautiful interface with session continuity
- **Centralized Management**: Single point for all tool operations
- **No Learning Curve**: Natural language processing handled by tools themselves

### For Developers
- **Maintainability**: Thin wrapper reduces code complexity
- **Extensibility**: Easy to add new tools through configuration
- **Separation of Concerns**: Clear boundaries between wrapper and tool functionality
- **Reliability**: No risk of breaking changes in natural language processing

## Limitations

### Intentional Limitations
- **No Deep Integration**: Does not modify tool internals or add new features
- **No Orchestration**: Focuses on individual tool execution rather than multi-tool coordination
- **Tool Dependency**: Relies entirely on underlying tools for natural language understanding
- **No Feature Enhancement**: Does not modify or enhance tool capabilities

This wrapper design provides a clean separation between the enhanced user experience features and the core AI tool functionality, ensuring that Terminal Jarvis enhances rather than replaces the underlying tools' capabilities.