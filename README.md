# EmailIntelligence

EmailIntelligence is a full-stack application that provides intelligent email analysis and management capabilities. It combines a Node.js/TypeScript backend, a Python FastAPI backend for AI/NLP tasks, and a React frontend to deliver a comprehensive email intelligence solution.

## Table of Contents

- [Project Overview](#project-overview)
- [Project Structure](#project-structure)
- [Quick Start](#quick-start)
- [Documentation](#documentation)
- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [Configuration](#configuration)
- [Security Considerations](#security-considerations)
- [Gmail API Integration Setup](#gmail-api-integration-setup)
- [Running the Application](#running-the-application)
- [AI System Overview](#ai-system-overview)
- [Building for Production](#building-for-production)
- [Database](#database)
- [Extension System](#extension-system)

## Project Overview

EmailIntelligence helps users analyze, categorize, and manage their emails more efficiently through:
- Sentiment analysis of email content
- Topic classification and categorization
- Intent recognition
- Urgency detection
- Smart filtering and organization

The project uses a modular architecture with a unified launcher system, comprehensive environment management, and an extensions framework for easy customization.

## Project Structure

The project is organized into the following main components:

- **client/** - React frontend application
- **server/** - Backend services
  - **server/python_nlp/** - Python NLP and AI components
  - **server/python_backend/** - Python FastAPI backend
- **deployment/** - Deployment configurations and scripts
- **extensions/** - Extension system for adding custom functionality
- **tests/** - Test suite for the application
- **launch.py**, **launch.bat**, **launch.sh** - Unified launcher scripts

## Quick Start

The easiest way to get started with EmailIntelligence is to use the unified launcher system:

### Windows

```bash
# Clone the repository
git clone <repository_url>
cd EmailIntelligence

# Run the application in development mode
launch.bat --stage dev
```

### Linux/macOS

```bash
# Clone the repository
git clone <repository_url>
cd EmailIntelligence

# Make the launcher script executable
chmod +x launch.sh

# Run the application in development mode
./launch.sh --stage dev
```

For more detailed setup instructions, see the [Prerequisites](#prerequisites) and [Setup](#setup) sections below.

## Documentation

This project includes several specialized documentation files:

- [Environment Management](README_ENV_MANAGEMENT.md) - Details about the Python environment management system
- [Launcher System](LAUNCHER.md) - Information about the unified launcher system
- [Deployment Frameworks](DEPLOYMENT.md) - Overview of deployment options and configurations
- [Python Style Guide](PYTHON_STYLE_GUIDE.md) - Coding standards for Python code in the project
- [Deployment README](deployment/README.md) - Specific deployment instructions and configurations

## Prerequisites

*   Node.js (v18 or later recommended)
*   npm
*   Python (v3.8 or later recommended)

## Setup

### 1. Frontend and Node.js Backend

Clone the repository:
```bash
git clone <repository_url>
cd <repository_directory>
```

Install Node.js dependencies:
```bash
npm install
```

### 2. Python Environment and AI Models

Set up the Python virtual environment, install dependencies, and prepare for AI models:
```bash
# For Linux/macOS
./launch.sh --stage dev

# For Windows
launch.bat --stage dev
```
This will run `launch.py` which handles Python environment setup.
**IMPORTANT**: The launch script (when run with `--stage dev` or during initial setup) creates placeholder AI model files (`.pkl`) in `server/python_nlp/`. For the application's AI features to function correctly, you **must** replace these with actual trained models. The system may attempt to run `server/python_nlp/ai_training.py` which could produce one sample model (e.g., `model_xxxxxxxxxxxx.pkl` in the project root); you will need to train models for all required types (sentiment, topic, intent, urgency) and rename/move them appropriately to:
*   `server/python_nlp/sentiment_model.pkl`
*   `server/python_nlp/topic_model.pkl`
*   `server/python_nlp/intent_model.pkl`
*   `server/python_nlp/urgency_model.pkl`

Refer to `server/python_nlp/ai_training.py` for details on model training. You may need to adapt this script or provide your own training data.

## Configuration

This section details important environment variables and configuration files used by the application.

*   **Name:** `DATABASE_URL`
    *   **Purpose:** Connection string for the PostgreSQL database.
    *   **Used By:** Node.js backend (via Prisma), Python FastAPI backend (via `DatabaseManager`).
    *   **Mandatory/Optional:** Mandatory for database operations.
    *   **Default Value:** None. Must be set.
    *   **Example/Format:** `postgresql://user:password@host:port/database_name`

*   **Name:** `GMAIL_CREDENTIALS_JSON`
    *   **Purpose:** Contains the entire JSON content of the OAuth 2.0 Client ID credentials downloaded from Google Cloud Console for accessing the Gmail API.
    *   **Used By:** Python FastAPI backend (`GmailAIService` via `GmailDataCollector` in `server/python_nlp/gmail_integration.py`).
    *   **Mandatory/Optional:** Mandatory for Gmail API integration if not using the `credentials.json` file alternative.
    *   **Default Value:** None.
    *   **Example/Format:** `'{"installed":{"client_id":"YOUR_CLIENT_ID.apps.googleusercontent.com", ...}}'` (The entire JSON string).

*   **Name:** `credentials.json` (File Alternative)
    *   **Purpose:** Alternative to `GMAIL_CREDENTIALS_JSON`. This is the downloaded OAuth 2.0 Client ID credentials file, renamed.
    *   **Used By:** Python FastAPI backend (`GmailAIService` via `GmailDataCollector`). It's typically loaded if `GMAIL_CREDENTIALS_JSON` is not set.
    *   **Placement:** Project root directory.
    *   **Mandatory/Optional:** Mandatory for Gmail API integration if `GMAIL_CREDENTIALS_JSON` is not set.

*   **Name:** `GMAIL_TOKEN_PATH`
    *   **Purpose:** Specifies the file path where the Gmail API OAuth 2.0 token (`token.json`) is stored after successful user authorization.
    *   **Used By:** Python FastAPI backend (`GmailAIService` via `GmailDataCollector`).
    *   **Mandatory/Optional:** Optional.
    *   **Default Value:** `token.json` (created in the current working directory, typically the project root when running the FastAPI app).
    *   **Example/Format:** `./config/gmail_token.json`

*   **Name:** `NLP_MODEL_DIR`
    *   **Purpose:** Specifies the directory where trained NLP models (e.g., sentiment, topic models) are stored.
    *   **Used By:** Python FastAPI backend (`AIEngine` and related NLP components in `server/python_nlp/`).
    *   **Mandatory/Optional:** Optional (though AI features will fail if models are not found at the expected paths).
    *   **Default Value:** Models are typically expected in `server/python_nlp/` (e.g., `server/python_nlp/sentiment_model.pkl`). The `setup_python.sh` script places placeholders there.
    *   **Example/Format:** `server/python_nlp/`

*   **Name:** `PORT`
    *   **Purpose:** Specifies the port on which the Python FastAPI server will run.
    *   **Used By:** Python FastAPI backend (`run_server.py`).
    *   **Mandatory/Optional:** Optional.
    *   **Default Value:** `8000`.
    *   **Example/Format:** `8001`

## Security Considerations

When deploying or running this application, especially in a production-like environment, please consider the following:

*   **API Authentication:** The Python FastAPI endpoints currently lack robust authentication and authorization mechanisms. For any sensitive operations or production use, you should implement proper API security (e.g., OAuth2, API keys) to protect your endpoints.

*   **Secret Management:**
    *   The `GMAIL_CREDENTIALS_JSON` environment variable (or the `credentials.json` file) contains sensitive information. Ensure it is managed securely. For production, avoid hardcoding secrets or committing them to version control.
    *   Use environment variables as a minimum. For more robust secret management in production, consider using a dedicated secret manager service (e.g., HashiCorp Vault, AWS Secrets Manager, Google Secret Manager).
    *   The `token.json` file, once generated, also contains sensitive access tokens and should be protected.

*   **Log Verbosity and Sensitive Information:** Review the logging configuration and log output (especially from the Python backend's structured logging) to ensure that sensitive information (e.g., detailed error messages, email content snippets in logs) is not excessively logged in a production environment, or that logs are stored securely.

*   **CORS Policy:** The current Cross-Origin Resource Sharing (CORS) policy in the Python FastAPI backend (`main.py`) is relatively permissive (`allow_origins=["http://localhost:5000", "https://*.replit.dev"]`, `allow_methods=["*"]`, `allow_headers=["*"]`). For production, you should restrict this to only allow requests from your specific frontend domain(s) and necessary methods/headers.

*   **Input Validation:** While Pydantic models provide some input validation, ensure all user-supplied data and data from external services (like Gmail) are thoroughly validated and sanitized, especially before being used in database queries or system commands.

## Gmail API Integration Setup

To enable the application to fetch and process emails directly from your Gmail account, you need to configure its access to the Gmail API. The core logic for this integration resides in `server/python_nlp/gmail_integration.py` (used by `GmailAIService` in the Python backend).

Follow these steps to set up the necessary credentials:

1.  **Google Cloud Console Configuration:**
    *   Navigate to the [Google Cloud Console](https://console.cloud.google.com/).
    *   Create a new project or select an existing one.
    *   In the navigation menu, go to "APIs & Services" > "Enabled APIs & services".
    *   Click "+ ENABLE APIS AND SERVICES", search for "Gmail API", and enable it for your project.
    *   Go to "APIs & Services" > "Credentials".
    *   Click "+ CREATE CREDENTIALS" and choose "OAuth 2.0 Client ID".
    *   If prompted, configure the OAuth consent screen. For "User Type", "External" is fine for testing. Provide an app name, user support email, and developer contact information. For scopes, you can leave it blank for now or add `../auth/gmail.readonly`.
    *   For "Application type", select "Desktop app". You can name the client (e.g., "GmailAISyncClient").
    *   Click "CREATE". You will see your client ID and client secret.
    *   Download the credentials JSON file by clicking the download icon next to your newly created OAuth 2.0 Client ID. The file will typically be named something like `client_secret_XXXX.json`.

2.  **Provide Credentials to the Application:**

    You have two options to make these credentials accessible to the application:

    *   **Option 1 (Recommended): Environment Variable**
        Set the `GMAIL_CREDENTIALS_JSON` environment variable to the *entire JSON content* of the file you downloaded.
        For example, in your shell:
        ```bash
        export GMAIL_CREDENTIALS_JSON='{"installed":{"client_id":"YOUR_CLIENT_ID.apps.googleusercontent.com", ...rest of the JSON content...}}'
        ```
        Ensure this variable is available in the environment where the Python backend (`server/python_backend/run_server.py`) is executed.

    *   **Option 2: Credentials File**
        Rename the downloaded JSON file to `credentials.json` and place it in the project's root directory. The application, when run, will look for this file if the `GMAIL_CREDENTIALS_JSON` environment variable is not set.

3.  **One-Time Authorization Process:**

    *   The first time the application attempts to access Gmail data (e.g., when you trigger a Gmail sync feature, or if you run `python server/python_nlp/gmail_integration.py` directly for testing), it will use these credentials to initiate an OAuth 2.0 authorization flow.
    *   The application will likely attempt to open a new tab or window in your web browser, prompting you to choose a Google account and grant permission for the application to access your Gmail data.
    *   Review the permissions and, if you agree, click "Allow".
    *   Upon successful authorization, a `token.json` file will be created. This file stores the OAuth 2.0 refresh and access tokens. By default, this `token.json` file is created in the directory from which the script requiring authorization is executed (e.g., the project root if running the FastAPI application, or alongside `gmail_integration.py` if run directly).
    *   This `token.json` file will be reused for subsequent API calls, so you typically only need to go through the browser authorization process once, unless the token is revoked or expires.

4.  **Scopes Used:**

    The application currently requests the following scope:
    *   `https://www.googleapis.com/auth/gmail.readonly`: This allows the application to read email content, labels, and metadata but not to make any changes to your mailbox.

With these steps completed, the application should be able to connect to your Gmail account.

## Running the Application

1.  **Activate Python Environment (if not already active in your terminal):**
    ```bash
    source .venv/bin/activate
    ```

2.  **Start the Python FastAPI AI Server:**
    Open a terminal and run:
    ```bash
    python server/python_backend/run_server.py
    ```
    This server typically runs on port 8000.

3.  **Start the Node.js Backend and Frontend Development Server:**
    Open another terminal and run:
    ```bash
    npm run dev
    ```
    This server typically runs on port 5000 and serves the client application.

## AI System Overview

The AI and NLP capabilities in this project are primarily based on:
*   Locally trained classification models (e.g., Naive Bayes, Logistic Regression) managed by scripts in `server/python_nlp/`.
*   Rule-based systems (regex, keyword matching) and heuristics.

It does not use external Large Language Models (LLMs) by default. The "prompts" referred to in the Python code (e.g., `PromptEngineer`) are typically structured templates for these local models or rules, not for services like OpenAI GPT or Anthropic Claude.

## Building for Production

```bash
npm run build
```
This will build the frontend and the Node.js backend. The Python server needs to be run separately in a production environment.

For more advanced deployment options, refer to the [Deployment Frameworks](DEPLOYMENT.md) documentation.

## Database

The application uses a database. Schema push/migrations can be handled by:
```bash
npm run db:push
```
Ensure your `DATABASE_URL` environment variable is correctly configured.

## Extension System

EmailIntelligence includes a powerful extension system that allows you to add custom functionality to the application. Extensions can enhance the AI capabilities, add new features, or modify existing functionality.

### Available Extensions

The project comes with an example extension that demonstrates how to use the extension system:

- **Example Extension**: Enhances sentiment analysis with emojis and detailed metrics

### Managing Extensions

You can manage extensions using the launcher script:

```bash
# List all installed extensions
python launch.py --list-extensions

# Install an extension from a Git repository
python launch.py --install-extension https://github.com/username/extension.git

# Create a new extension template
python launch.py --create-extension my_extension
```

For more information about the extension system, see the [Environment Management](README_ENV_MANAGEMENT.md#extension-system) documentation.

## Debugging Hangs

### Debugging Pytest Hangs

If `pytest` runs (e.g., via `python deployment/run_tests.py`) appear to hang:

*   **Increase Verbosity**: Run `pytest` with `-vvv` (or `-vv`) for more detailed output.
*   **Disable Capture**: Use `pytest --capture=no` to see `stdout` and `stderr` from tests in real-time. This can help identify if a test is printing lots of data or getting stuck in a loop.
*   **Specific Test File/Function**: Try to isolate the hang by running specific test files (`pytest tests/your_test_file.py`) or specific test functions (`pytest tests/your_test_file.py::test_name`).
*   **Debugger**: Insert `import pdb; pdb.set_trace()` (Python 3.6 and below) or `breakpoint()` (Python 3.7+) into a suspected test or fixture to step through the code.
*   **Timeouts**: The `run_tests.py` script now includes timeouts for test suites. If a timeout occurs, it will be logged, indicating a hang in that suite.

### Debugging NPM/Build Hangs

If `npm run build` or other `npm` commands hang:

*   **Verbose Output**: The `build` script in `package.json` has been updated to include `--debug` for Vite and `--log-level=verbose` for esbuild. Examine this output closely.
*   **Node.js Inspector**: For debugging `node` scripts (if you suspect a specific script invoked by npm), you can try to run it with the inspector: `node --inspect-brk your_script.js`. Then connect a debugger like Chrome DevTools.
*   **Resource Limits**: Frontend builds (especially minification, transpilation, and source map generation) can be memory and CPU intensive. Ensure your build environment (local machine, CI runner, Docker container) has adequate resources. Check for out-of-memory (OOM) errors in system logs if possible.
*   **Clean NPM Cache/Modules**: Rarely, a corrupted npm cache or `node_modules` can cause issues. Try `npm cache clean --force` (use with caution) and remove `node_modules` and `package-lock.json`, then run `npm install` again. Note that `npm ci` (used in `Dockerfile.frontend`) is generally preferred for CI/build environments as it performs cleaner installs.

### General Debugging on Linux

If hangs occur in a Linux environment (like Docker containers or CI runners):

*   **System Resource Monitoring**: Use tools like `top`, `htop`, or `vmstat` to check CPU, memory, and I/O usage during the suspected hang.
*   **System Calls**: `strace -p <PID>` can attach to a running process and show system calls, which might indicate what a process is waiting for (e.g., file I/O, network).
*   **Kernel Messages**: Check `dmesg -T` for any relevant kernel messages, such as OOM killer events.
*   **Disk Space**: Ensure there's adequate disk space in the build environment.
