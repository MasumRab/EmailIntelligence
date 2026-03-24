# EmailIntelligence

Intelligent email management platform with AI-powered filtering, categorization, and analysis.

## Quick Start

**Prerequisites:**
- Python 3.11+
- Node.js 18+
- Git

**Step 1: Clone the repository**
```bash
git clone https://github.com/MasumRab/EmailIntelligence.git
cd EmailIntelligence
```

**Step 2: Install dependencies**
```bash
# For Ubuntu/WSL environments
./setup_environment_wsl.sh

# For other environments
npm install
```

**Step 3: Database Setup**
The application uses SQLite. The database file (`sqlite.db`) is created automatically in the `backend` directory.

**Step 4: Run the Application**
```bash
# Windows
launch.bat --stage dev

# Linux/macOS
./launch.sh --stage dev

# Or with Python directly
python launch.py --stage dev
```

The application will be available at http://localhost:5173

## Documentation

Comprehensive guides in the `docs/` directory:

- **[Deployment Guide](docs/deployment_guide.md)**: Local, Docker, staging, and production deployment
- **[Launcher Guide](docs/launcher_guide.md)**: Unified launcher system and CLI options
- **[Environment Management Guide](docs/env_management.md)**: Python environment setup and management
- **[Extensions Guide](docs/extensions_guide.md)**: Using and developing extensions
- **[Client Development Guide](docs/client_development.md)**: Frontend development
- **[Server Development Guide](docs/server_development.md)**: Backend development
- **[Python Style Guide](docs/python_style_guide.md)**: Python coding standards

## AI Models Setup

The AI features (sentiment analysis, topic classification, etc.) use trained models in `backend/python_nlp/`.

**Placeholder Models:** Running `launch.py --stage dev` creates empty placeholder `.pkl` files. These won't provide actual AI functionality.

**Training Actual Models:** To enable AI features, train models using `backend/python_nlp/ai_training.py`. You'll need to:
1. Prepare labeled datasets (emails with topics, sentiments, etc.)
2. Configure `ModelConfig` for each model type
3. Train and save models with expected filenames (`topic_model.pkl`, `sentiment_model.pkl`, etc.)

See `docs/ai_model_training_guide.md` (TODO: create) for detailed guidance.

## Configuration

Set environment variables in `.env` or your shell:

- `DATABASE_URL`: Database connection (SQLite: `sqlite:backend/sqlite.db`)
- `GMAIL_CREDENTIALS_JSON`: Gmail API OAuth credentials JSON
- `credentials.json`: Alternative - place credentials file in project root
- `GMAIL_TOKEN_PATH`: Token storage path (default: `jsons/token.json`)
- `NLP_MODEL_DIR`: NLP models directory (default: `backend/python_nlp/`)
- `PORT`: FastAPI server port (default: `8000`)

## Running the Application

**Development mode:**
```bash
python launch.py --stage dev
```

Starts:
- Python FastAPI AI Server (port 8000)
- React Frontend (port 5173)

**Gradio Scientific UI:**
```bash
python launch.py --gradio-ui --host 0.0.0.0 --port 7860
```

**Environment Support:**
- Conda: Auto-detected, use `--conda-env <name>` to specify
- Virtual Environment: Created automatically if conda not found

## Gmail API Integration

1. **Enable Gmail API** in Google Cloud Console
2. **Create OAuth 2.0 Client ID** (Desktop app)
3. **Download credentials JSON**
4. **Provide credentials:**
   - Set `GMAIL_CREDENTIALS_JSON` env var, OR
   - Place as `credentials.json` in project root
5. **Authorize:** Browser authorization on first use creates `token.json`

**Scopes:** `https://www.googleapis.com/auth/gmail.readonly`

## Security Considerations

- **JWT Authentication:** Implemented for sensitive API endpoints
- **Secret Management:** Use environment variables, never commit secrets
- **CORS Policy:** Restrict in production (`backend/python_backend/main.py`)
- **Input Validation:** Sanitize all user/external data

## Deployment

**Docker:**
```bash
# Build
python deployment/deploy.py prod build

# Start
python deployment/deploy.py prod up -d

# Stop
python deployment/deploy.py prod down
```

See [Deployment Guide](docs/deployment_guide.md) for comprehensive deployment instructions.

## Building for Production

```bash
# Build frontend
npm run build

# Run backend with ASGI server (e.g., Gunicorn/Uvicorn)
```

## Extension System

Manage extensions with the launcher:
```bash
python launch.py --list-extensions
python launch.py --install-extension <path>
```

See [Extensions Guide](docs/extensions_guide.md) for development details.

## Debugging

**Pytest hangs:**
```bash
pytest -vvv --capture=no
pytest path/to/test_file.py::test_name
```

**NPM/Build hangs:**
- Clean cache: `npm cache clean --force`
- Remove `node_modules` & `package-lock.json`, then `npm install`

**System monitoring:**
```bash
top, htop, vmstat
strace -p <PID>
dmesg -T
```

## Known Vulnerabilities

**esbuild vulnerabilities (moderate severity):**
- `drizzle-kit` dependencies require vulnerable `esbuild` versions (0.18.20, 0.19.12)
- Overrides attempted but ineffective due to version incompatibilities
- Requires `drizzle-kit` update to resolve

**Updated packages:**
- `vite@6.3.5` and `@vitejs/plugin-react@4.5.2` updated successfully

## Orchestration Tools

This project uses orchestration tools for environment management and Git hooks:

- **Setup scripts:** `setup/` directory
- **Git hooks:** `scripts/hooks/`
- **Shared libraries:** `scripts/lib/`

**Important:**
- Root `launch.py` is essential for backward compatibility
- `setup/` directory is critical for environment setup
- Git hooks in `scripts/hooks/` are essential for orchestration workflow
- Changes to orchestration-managed files require PRs through the automated system

See `docs/orchestration_summary.md` for details.
