# Terminal Jarvis Modular Architecture

## Overview

Terminal Jarvis follows a domain-based modular architecture pattern that emphasizes separation of concerns, maintainability, and scalability. This approach organizes code into focused domains rather than generic modules, with each domain handling a specific aspect of the application's functionality.

## Domain-Based Architecture Principles

### 1. Functional Separation
Each domain is responsible for a specific functional area of the application:
- **CLI Logic**: Business logic and workflows
- **Tools**: Tool management and execution
- **Configuration**: Settings and configuration management
- **Authentication**: Credential and auth management
- **Services**: External service integrations
- **Theme**: Presentation and theming
- **Evals**: Evaluation and benchmarking

### 2. Loose Coupling
Domains interact through well-defined APIs rather than direct dependencies:
- Each domain exposes a public API through its entry point module
- Cross-domain communication happens through these APIs
- Implementation details are hidden within each domain

### 3. High Cohesion
Within each domain, related functionality is grouped together:
- Modules within a domain focus on similar concerns
- Shared utilities and data structures are domain-specific
- Cross-cutting concerns are handled by dedicated domains

## Domain Structure

### Standard Domain Layout
```
domain_name/
├── mod.rs                    # Domain entry point and re-exports
├── domain_name_entry_point.rs # Main API and coordination
├── domain_name_module1.rs    # Specific functionality
├── domain_name_module2.rs    # Specific functionality
└── domain_name_module3.rs    # Specific functionality
```

### Entry Point Pattern
Each domain follows a consistent entry point pattern:
1. **Entry Point Module**: Exposes public API
2. **Re-exports**: Makes internal modules available
3. **Coordination**: Handles interactions between internal modules

## Benefits of Domain-Based Architecture

### 1. Maintainability
- Changes to one domain don't affect others
- Clear boundaries make it easier to understand code
- Easier to locate relevant functionality
- Reduced risk of unintended side effects

### 2. Testability
- Domains can be tested independently
- Mocking dependencies is straightforward
- Clear APIs make unit testing easier
- Integration testing can focus on domain interactions

### 3. Scalability
- New features can be added as new domains
- Existing domains can be extended without restructuring
- Team members can work on different domains in parallel
- Codebase can grow without becoming unwieldy

### 4. Reusability
- Well-defined APIs make domains reusable
- Cross-project sharing of domains is possible
- Common patterns emerge across domains

## Implementation Examples

### Tools Domain
The Tools domain demonstrates the domain-based approach:

**Structure:**
```
src/tools/
├── mod.rs                    # Entry point
├── tools_entry_point.rs     # Main ToolManager API
├── tools_command_mapping.rs # Command mapping
├── tools_detection.rs       # Tool detection
├── tools_display.rs         # Tool display
├── tools_execution_engine.rs # Tool execution
├── tools_process_management.rs # Process management
├── tools_startup_guidance.rs # Startup guidance
└── tools_config.rs          # Configuration
```

**Entry Point (`tools_entry_point.rs`):**
```rust
pub struct ToolManager;

impl ToolManager {
    pub fn get_available_tools() -> BTreeMap<&'static str, ToolInfo> {
        get_available_tools()
    }
    
    pub fn run_tool(display_name: &str, args: &[String]) -> Result<()> {
        run_tool(display_name, args).await
    }
    
    // Other public methods...
}
```

### CLI Logic Domain
The CLI Logic domain shows how complex business logic can be organized:

**Structure:**
```
src/cli_logic/
├── mod.rs                           # Entry point
├── cli_logic_entry_point.rs        # Main coordination
├── cli_logic_auth_operations.rs    # Auth operations
├── cli_logic_benchmark_operations.rs # Benchmark ops
├── cli_logic_config_management.rs  # Config management
├── cli_logic_evals_operations.rs   # Evals operations
├── cli_logic_info_operations.rs    # Info operations
├── cli_logic_interactive.rs        # Interactive mode
├── cli_logic_list_operations.rs    # List operations
├── cli_logic_responsive_display.rs # Responsive display
├── cli_logic_responsive_menu.rs    # Responsive menu
├── cli_logic_template_operations.rs # Template ops
├── cli_logic_tool_execution.rs     # Tool execution
├── cli_logic_update_operations.rs  # Update operations
├── cli_logic_utilities.rs          # Utilities
└── cli_logic_welcome.rs           # Welcome screen
```

## Cross-Domain Communication

### API Contracts
Domains communicate through explicit APIs:
```rust
// Tools domain API
pub struct ToolManager;
impl ToolManager {
    pub fn get_available_tools() -> BTreeMap<&'static str, ToolInfo> { ... }
    pub fn run_tool(display_name: &str, args: &[String]) -> Result<()> { ... }
}

// CLI Logic using Tools domain
use crate::tools::ToolManager;
async fn handle_run_tool(tool: &str, args: &[String]) -> Result<()> {
    ToolManager::run_tool(tool, args).await
}
```

### Dependency Management
Dependencies between domains are explicit:
```rust
// CLI Logic depends on Tools
use crate::tools::ToolManager;

// Tools depends on Configuration
use crate::config::ConfigManager;

// Tools depends on Authentication
use crate::auth_manager::AuthManager;
```

## Data Flow Patterns

### Request-Response Pattern
Domains provide services through request-response interactions:
```
CLI Logic → Tools::run_tool() → Tools Execution
CLI Logic ← Result ← Tools Execution
```

### Event-Driven Pattern
Some interactions follow event-driven patterns:
```
Tool Execution → Authentication::prepare_environment()
Tool Execution ← Environment Ready ← Authentication
```

## Testing Strategy

### Unit Testing Within Domains
Each domain can be tested independently:
```rust
#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_tool_detection() {
        // Test tool detection logic within Tools domain
    }
}
```

### Integration Testing Between Domains
Cross-domain interactions are tested through integration tests:
```rust
// tests/integration_tests.rs
#[tokio::test]
async fn test_tool_execution_with_auth() {
    // Test interaction between Tools and Authentication domains
}
```

## Refactoring Guidelines

### Domain Extraction Process
When refactoring large modules:

1. **Identify Functional Areas**: Group related functions by purpose
2. **Create New Domain**: Establish domain structure with entry point
3. **Move Functionality**: Transfer related code to new modules
4. **Establish API**: Define clear public interface
5. **Update Dependencies**: Modify cross-domain references
6. **Verify Integration**: Ensure all functionality works correctly

### Example Refactoring
Before:
```rust
// cli_logic.rs (1000+ lines)
fn handle_tool_run() { ... }
fn handle_tool_install() { ... }
fn handle_auth_menu() { ... }
fn handle_config_show() { ... }
```

After:
```rust
// cli_logic/cli_logic_tool_execution.rs
pub fn handle_tool_run() { ... }

// cli_logic/cli_logic_update_operations.rs
pub fn handle_tool_install() { ... }

// cli_logic/cli_logic_auth_operations.rs
pub fn handle_auth_menu() { ... }

// cli_logic/cli_logic_config_management.rs
pub fn handle_config_show() { ... }
```

## Best Practices

### 1. Clear Boundaries
- Each domain should have a single, well-defined purpose
- Avoid cross-domain code duplication
- Keep domain APIs focused and consistent

### 2. Explicit Dependencies
- Import only what you need from other domains
- Document cross-domain interactions
- Use dependency inversion where appropriate

### 3. Consistent Patterns
- Follow the same structure across all domains
- Use consistent naming conventions
- Maintain similar API patterns

### 4. Incremental Development
- Add new functionality as new domains when appropriate
- Refactor existing code into domains gradually
- Test each change thoroughly

## Future Considerations

### Domain Evolution
As the system grows:
- Domains may be split into sub-domains
- New domains may be added for emerging functionality
- Domain boundaries may shift as requirements change

### Technology Integration
- New technologies can be integrated at the domain level
- Cross-cutting concerns can be handled by new domains
- Legacy systems can be integrated through adapter domains

This domain-based modular architecture provides Terminal Jarvis with a solid foundation for maintainable, scalable, and testable code organization.