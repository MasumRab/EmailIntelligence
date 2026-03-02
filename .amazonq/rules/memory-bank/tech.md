# EmailIntelligence - Technology Stack

## Programming Languages & Versions

### Primary Languages
- **Python 3.11+**: Main application language with modern async/await support
- **Bash/Shell**: Cross-platform automation scripts and Git hooks
- **PowerShell**: Windows-specific automation and setup scripts
- **JavaScript/TypeScript**: Frontend components and Node.js tooling
- **YAML/JSON**: Configuration files and data serialization

### Language-Specific Features
- **Python**: Type hints, dataclasses, async/await, context managers
- **Shell**: POSIX compliance, error handling, cross-platform compatibility
- **PowerShell**: Windows integration, .NET framework access

## Core Technology Stack

### Web Framework & API
```python
# Core web stack
fastapi>=0.115.12          # High-performance async web framework
uvicorn[standard]>=0.34.3  # ASGI server with WebSocket support
pydantic>=2.11.5           # Data validation and serialization
python-multipart>=0.0.20   # File upload support
httpx>=0.28.1              # Async HTTP client
```

### Machine Learning & NLP
```python
# ML/AI stack (optional installation)
transformers>=4.52.4       # Hugging Face transformers
torch>=2.7.1               # PyTorch (CPU-optimized)
nltk>=3.9.1                # Natural language processing
textblob>=0.19.0           # Simple NLP operations
scikit-learn>=1.7.0        # Traditional ML algorithms
accelerate>=1.7.0          # Model acceleration
sentencepiece>=0.2.0       # Tokenization
```

### Data & Database
```python
# Data handling
aiosqlite>=0.20.0          # Async SQLite operations
pandas>=2.0.0              # Data manipulation (optional)
numpy>=1.26.0              # Numerical computing (optional)
psycopg2-binary>=2.9.10    # PostgreSQL adapter (optional)
redis>=5.0.0               # Redis client (optional)
```

### UI & Visualization
```python
# User interface
gradio>=4.0.0              # Interactive web UI
matplotlib>=3.8.0          # Plotting (optional)
seaborn>=0.13.0            # Statistical visualization (optional)
plotly>=5.18.0             # Interactive plots (optional)
```

## Build System & Dependency Management

### Package Management
- **Primary**: `uv` (ultra-fast Python package installer)
- **Fallback**: `pip` with requirements.txt files
- **Configuration**: `pyproject.toml` with conditional dependencies

### Dependency Strategy
```toml
[project.optional-dependencies]
ml = ["transformers", "torch", "nltk", "scikit-learn"]
data = ["pandas", "numpy", "scipy"]
viz = ["matplotlib", "seaborn", "plotly"]
db = ["psycopg2-binary", "redis", "notmuch"]
google = ["google-api-python-client", "google-auth"]
dev = ["pytest", "black", "flake8", "mypy"]
```

### Installation Profiles
- **Minimal**: Core web framework only (~50MB)
- **Standard**: Core + basic ML (~500MB)
- **Full**: All features including heavy ML models (~2GB)

## Development Tools & Quality

### Code Quality
```python
# Linting and formatting
black>=25.1.0              # Code formatting
flake8>=7.2.0              # Style guide enforcement
isort>=6.0.1               # Import sorting
pylint>=3.3.7              # Static analysis
mypy>=1.16.0               # Type checking
unimport>=1.3.0            # Unused import detection
```

### Testing Framework
```python
# Testing stack
pytest>=8.4.0             # Test framework
pytest-cov>=6.0.0         # Coverage reporting
pytest-asyncio>=1.2.0     # Async test support
```

### Configuration Files
- `.flake8`: Linting configuration with project-specific rules
- `.pylintrc`: Pylint configuration with custom checks
- `pyproject.toml`: Modern Python project configuration
- `pytest.ini`: Test configuration and markers

## Development Commands

### Environment Setup
```bash
# Quick setup (minimal dependencies)
python setup/launch.py --setup minimal

# Full development setup
python setup/launch.py --setup dev

# ML-enabled setup
python setup/launch.py --setup ml
```

### Development Workflow
```bash
# Install Git hooks
scripts/install-hooks.sh

# Run application
python setup/launch.py --run

# Run tests
python -m pytest tests/

# Code quality checks
python -m black src/
python -m flake8 src/
python -m mypy src/
```

### Build & Distribution
```bash
# Build package
python -m build

# Install in development mode
pip install -e .

# Install with specific features
pip install -e ".[ml,dev]"
```

## Platform Support & Compatibility

### Operating Systems
- **Windows 10/11**: Native support with PowerShell integration
- **Linux**: Ubuntu 20.04+, RHEL 8+, Debian 11+
- **WSL**: Windows Subsystem for Linux (WSL2 recommended)
- **macOS**: macOS 11+ (limited testing)

### Python Environments
- **System Python**: 3.11+ with virtual environment isolation
- **Conda**: Full compatibility with conda environments
- **Docker**: Containerized deployment support
- **Virtual Environments**: venv, virtualenv, pipenv support

### Cross-Platform Features
- **Unified Launcher**: `setup/launch.py` works across all platforms
- **Shell Scripts**: POSIX-compliant with Windows compatibility layer
- **Path Handling**: Cross-platform path resolution and normalization
- **Environment Detection**: Automatic platform and environment detection

## Performance & Optimization

### CPU-First Architecture
- **PyTorch CPU**: Optimized for CPU-only inference
- **Async Operations**: Non-blocking I/O for web requests
- **Memory Management**: Efficient memory usage with streaming
- **Caching**: Multi-layer caching for ML models and data

### Monitoring & Profiling
- **Performance Metrics**: Built-in performance logging
- **Resource Monitoring**: CPU, memory, and disk usage tracking
- **Bottleneck Detection**: Automated performance issue identification
- **Health Checks**: System health monitoring and alerting

## Integration & APIs

### External Services
- **Google Workspace**: Gmail API, Google Drive integration
- **Email Providers**: IMAP/SMTP support for various providers
- **Database Systems**: SQLite, PostgreSQL, Redis
- **Git Integration**: Advanced Git operations and hook management

### Agent Integration
- **Claude Code**: MCP server integration with custom tools
- **Cursor IDE**: Custom commands and context control
- **GitHub Copilot**: Enhanced with project-specific context
- **Multiple Agents**: Support for 10+ AI development tools

### API Design
- **RESTful APIs**: FastAPI with OpenAPI documentation
- **WebSocket Support**: Real-time communication capabilities
- **Authentication**: JWT and OAuth2 support
- **Rate Limiting**: Built-in request throttling and quotas