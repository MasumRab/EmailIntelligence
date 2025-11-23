# Terminal Jarvis Technology Stack

## Core Technologies

### Programming Language
- **Rust**: Primary language for the application, providing performance, memory safety, and reliability

### Build System
- **Cargo**: Rust's package manager and build tool

### CLI Framework
- **clap**: Command-line argument parsing library
  - Features: derive macros, environment variable integration, help text generation

### Async Runtime
- **tokio**: Asynchronous runtime for Rust
  - Full feature set including timers, networking, and multi-threading

### HTTP Client
- **reqwest**: High-level HTTP client library
  - JSON support built-in
  - Async/await support

### Serialization
- **serde**: Serialization/deserialization framework
  - Derive macros for automatic implementation
  - Support for multiple formats (JSON, TOML)

### Error Handling
- **anyhow**: Flexible error handling library
  - Rich error context and backtraces
  - Simplified error propagation

### Configuration
- **toml**: TOML file parsing library
  - Used for all configuration files
  - Strong typing with serde integration

### Interactive UI
- **inquire**: Library for creating interactive command-line prompts
  - Select menus, text inputs, confirmations
  - Themed UI components

### Progress Indicators
- **indicatif**: Progress bar and indicator library
  - Multiple progress bar styles
  - Multi-progress tracking

### Terminal Control
- **crossterm**: Cross-platform terminal library
  - Cursor control, styling, and input handling
  - Cross-platform compatibility

### Testing
- **tokio-test**: Testing utilities for async code
- **Unit tests**: Built-in Rust testing framework

## Dependencies

### Core Dependencies
```toml
clap = { version = "4.4", features = ["derive", "env", "wrap_help"] }
tokio = { version = "1.47", features = ["full"] }
reqwest = { version = "0.12.23", features = ["json"] }
serde = { version = "1.0", features = ["derive"] }
serde_json = "1.0"
anyhow = "1.0"
toml = "0.9.7"
dirs = "6.0.0"
inquire = "0.8.1"
futures = "0.3"
shell-words = "1.1"
terminal_size = "0.4"
indicatif = "0.18.0"
signal-hook = "0.3"
libc = { version = "0.2", optional = false }
slab = "0.4.11"
crossterm = "0.28"
unicode-width = "0.2"
tempfile = "3.8"
regex = "1.10"
chrono = { version = "0.4.42", features = ["serde"] }
```

### Development Dependencies
```toml
tokio-test = "0.4"
```

## External Tools Integration

### Package Managers
- **NPM**: Node.js package manager for NPM distribution
- **Cargo**: Rust package manager for Crates.io distribution
- **Homebrew**: macOS/Linux package manager for Homebrew distribution
- **uv**: Python package installer for Python-based tools

### Shell Utilities
- **which/where**: Tool detection commands
- **curl**: Download utility for installation scripts
- **sh**: Shell execution for complex installation processes

## NPM Package Dependencies

For the NPM wrapper package:
- **TypeScript**: For the wrapper script
- **Biome**: For linting and formatting (replaces ESLint)

## Platform Support

### Operating Systems
- **Linux**: Primary development and testing platform
- **macOS**: Full support with Homebrew integration
- **Windows**: Supported through WSL2

### Architectures
- **x86_64**: Primary target architecture
- **aarch64**: Apple Silicon and ARM Linux support

## Distribution Channels

### Crates.io
- Direct Rust installation with `cargo install terminal-jarvis`

### NPM
- Node.js ecosystem distribution with `npm install -g terminal-jarvis`

### Homebrew
- macOS/Linux package manager integration
- Multi-platform formula with platform-specific binaries

## Development Tools

### Code Quality
- **clippy**: Rust linting tool
- **rustfmt**: Rust code formatter
- **Biome**: TypeScript/JavaScript linting and formatting

### CI/CD
- **GitHub Actions**: For automated testing and deployment
- **Local Scripts**: Custom deployment scripts in `scripts/cicd/`

### Documentation
- **Markdown**: Primary documentation format
- **External Docs**: Comprehensive documentation site

## Version Management

### Semantic Versioning
- Follows semver conventions (MAJOR.MINOR.PATCH)
- Automated version synchronization across all distribution channels

### Release Process
- Programmatic version updates
- Automated consistency checking
- Multi-platform release asset generation