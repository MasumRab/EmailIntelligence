# Project Title (Replace with Actual Title)

This project is a full-stack application with a Node.js/TypeScript backend, a Python FastAPI backend for AI/NLP tasks, and a React frontend.

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
bash setup_python.sh
```
**IMPORTANT**: The `setup_python.sh` script creates placeholder AI model files (`.pkl`) in `server/python_nlp/`. For the application's AI features to function correctly, you **must** replace these with actual trained models. The script runs `server/python_nlp/ai_training.py` which may produce one sample model (e.g., `model_xxxxxxxxxxxx.pkl` in the project root); you will need to train models for all required types (sentiment, topic, intent, urgency) and rename/move them appropriately to:
*   `server/python_nlp/sentiment_model.pkl`
*   `server/python_nlp/topic_model.pkl`
*   `server/python_nlp/intent_model.pkl`
*   `server/python_nlp/urgency_model.pkl`

Refer to `server/python_nlp/ai_training.py` for details on model training. You may need to adapt this script or provide your own training data.

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

## Database

The application uses a database. Schema push/migrations can be handled by:
```bash
npm run db:push
```
Ensure your `DATABASE_URL` environment variable is correctly configured.
