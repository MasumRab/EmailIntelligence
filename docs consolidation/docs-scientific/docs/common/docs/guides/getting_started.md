# Getting Started Guide for New Developers

This comprehensive guide will help new developers set up the EmailIntelligence project and start contributing in under 30 minutes.

## Prerequisites

Before you begin, ensure you have the following installed on your system:

### Required Software
- **Python 3.11+**: The backend requires Python 3.11 or higher
- **Node.js 16+**: Required for the frontend development
- **Git**: For version control

### System Requirements
- **RAM**: At least 8GB recommended (16GB for better performance)
- **Disk Space**: 5GB free space for dependencies and data
- **OS**: Linux, macOS, or Windows (WSL recommended for Windows)

## Quick Setup (Recommended)

The fastest way to get started is using the automated setup script:

### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd EmailIntelligence
```

### Step 2: Run Automated Setup
```bash
# For Linux/macOS
python3 launch.py --setup

# For Windows
python launch.py --setup
```

This command will:
- ✅ Detect your Python environment
- ✅ Install system dependencies (if on Ubuntu/WSL)
- ✅ Create a virtual environment
- ✅ Install Python dependencies with uv
- ✅ Download required NLTK data
- ✅ Install Node.js dependencies
- ✅ Set up the database

### Step 3: Start Development Environment
```bash
python launch.py --stage dev
```

This will start:
- **FastAPI Backend**: http://localhost:8000
- **React Frontend**: http://localhost:5173
- **API Documentation**: http://localhost:8000/docs

## Manual Setup (Alternative)

If the automated setup doesn't work for your environment:

### 1. Install System Dependencies

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install python3-dev python3-pip python3-venv build-essential git curl wget
```

**macOS:**
```bash
# Install Homebrew if not installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install dependencies
brew install python@3.11 node git
```

**Windows:**
Use WSL2 with Ubuntu, then follow Ubuntu instructions above.

### 2. Set Up Python Environment
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install uv
uv sync
```

### 3. Install Node.js Dependencies
```bash
npm install
```

### 4. Set Up Environment Variables
Create a `.env` file in the project root:
```bash
# Database
DATA_DIR=data

# Development
DEBUG=true
LOG_LEVEL=INFO

# Optional: Redis for caching (if available)
ENABLE_REDIS_CACHE=false
REDIS_URL=redis://localhost:6379
```

## Project Structure Overview

```
EmailIntelligence/
├── backend/                 # Python backend services
│   ├── python_backend/     # FastAPI application
│   └── python_nlp/         # AI/NLP components
├── client/                 # React frontend (Vite)
├── src/                    # Shared Python code
│   ├── core/              # Core business logic
│   └── modules/           # Pluggable features
├── data/                   # Application data and models
├── docs/                   # Documentation
├── tests/                  # Test suites
└── config/                 # Configuration files
```

## First Development Tasks

### 1. Explore the API
Visit http://localhost:8000/docs to see the interactive API documentation.

### 2. Run the Tests
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/core/test_security.py

# Run with coverage
pytest --cov=src --cov-report=html
```

### 3. Make Your First Change
1. Create a new branch: `git checkout -b feature/my-first-change`
2. Make a small change (e.g., update a comment)
3. Run tests: `pytest`
4. Commit: `git commit -am "My first change"`
5. Push: `git push origin feature/my-first-change`

## Development Workflow

### Daily Development
```bash
# Start development servers
python launch.py --stage dev

# In another terminal, run tests
pytest --watch

# Format code
black .
isort .

# Lint code
flake8 src/
mypy src/
```

### Code Quality
- **Formatting**: Use Black for Python, Prettier for JavaScript/TypeScript
- **Linting**: flake8 for Python, ESLint for JavaScript/TypeScript
- **Type Checking**: mypy for Python, TypeScript compiler for TypeScript
- **Testing**: pytest for Python, Jest for JavaScript

### Git Workflow
1. Create feature branch from `main`
2. Make changes with tests
3. Run full test suite
4. Create pull request
5. Code review and merge

## Common Issues and Solutions

### Python Environment Issues
```bash
# If you get import errors
source venv/bin/activate
pip install -e .

# If uv fails
pip install -r requirements.txt
```

### Node.js Issues
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

### Database Issues
```bash
# Reset database
rm data/*.db
python launch.py --stage dev  # Will recreate database
```

### Permission Issues
```bash
# Fix script permissions
chmod +x launch.sh launch.py
```

## Next Steps

1. **Read the Architecture Overview**: `docs/architecture_overview.md`
2. **Explore Core Components**: Start with `src/core/`
3. **Check Existing Issues**: Look at the backlog for tasks
4. **Join the Community**: Check contribution guidelines

## Getting Help

- **Documentation**: Check `docs/` directory
- **API Docs**: http://localhost:8000/docs
- **Issues**: Create GitHub issues for bugs/features
- **Discussions**: Use GitHub discussions for questions

## Key Concepts to Understand

- **Node-based Workflows**: The system uses a visual workflow editor
- **AI Integration**: Local models for email analysis
- **Security Framework**: Built-in authentication and authorization
- **Plugin System**: Extensible architecture
- **Caching**: Redis support for performance

Welcome to the EmailIntelligence team! 🚀