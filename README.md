
## Table of Contents

- [Project Overview](#project-overview)
- [Project Structure](#project-structure)
- [Quick Start](#quick-start)
- [Documentation](#documentation)
- [Prerequisites](#prerequisites)
- [Setup](#setup)
  - [AI Models Setup](#ai-models-setup)
  - [Database Setup for Development](#database-setup-for-development)
- [Configuration](#configuration)
- [Security Considerations](#security-considerations)
- [Gmail API Integration Setup](#gmail-api-integration-setup)
- [Running the Application](#running-the-application)
- [AI System Overview](#ai-system-overview)
- [Building for Production](#building-for-production)
- [Database](#database)
- [Extension System](#extension-system)
- [Debugging Hangs](#debugging-hangs)

## Project Overview


The Gradio UI acts as a full-featured client to the FastAPI backend.

```
Gradio UI (gradio_app.py)
==========================
|
├── 📈 Dashboard Tab
|   └── Calls GET /api/dashboard/stats ──> Displays key metrics & charts
|
├── 📥 Inbox Tab
|   ├── Calls GET /api/emails ─────> Displays searchable email list
|   └── Calls GET /api/categories ─> Populates category filter dropdown
|
├── 📧 Gmail Tab
|   └── Calls POST /api/gmail/sync ──> Triggers Gmail synchronization
|
├── 🔬 AI Lab Tab (Advanced Tools)
|   ├── Analysis Sub-Tab ──────────> Calls POST /api/ai/analyze
|   └── Model Management Sub-Tab ────> Calls GET/POST /api/models/*
|
└── ⚙️ System Status Tab
    ├── Calls GET /health ───────────> Displays system health
    └── Calls GET /api/gmail/performance -> Displays performance metrics
```

## Prerequisites

To successfully set up and run EmailIntelligence, you will need the following:

