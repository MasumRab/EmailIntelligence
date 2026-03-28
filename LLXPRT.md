# LLXPRT – EmailIntelligenceGem Project Overview

---
## Table of Contents

- [Project Summary](#project-summary)
- [High‑Level Architecture](#high-level-architecture)
- [Core Components](#core-components)
  - [Python Backend (FastAPI)](#python-backend-fastapi)
  - [Frontend (React + Vite)](#frontend-react--vite)
  - [Node‑Based Workflow Engine](#node-based-workflow-engine)
  - [AI/NLP Engine](#ainlp-engine)
  - [Security Framework](#security-framework)
  - [Performance Monitoring](#performance-monitoring)
  - [Extension System](#extension-system)
- [Data Storage](#data-storage)
- [Running the System (Local Development)](#running-the-system-local-development)
- [Running the System (Production / Docker)](#running-the-system-production--docker)
- [Testing](#testing)
- [Coding Conventions & Project Layout](#coding-conventions--project-layout)
- [Glossary & Terminology](#glossary--terminology)
- [Open Questions & Future Work](#open-questions--future-work)
- [References & Further Reading](#references--further-reading)
---

## Project Summary

**EmailIntelligenceGem** is a modular, extensible platform that provides intelligent email processing, categorisation, sentiment analysis and workflow automation.  It combines a **FastAPI** Python backend, a **React/Vite** frontend, a **node‑based workflow engine** inspired by ComfyUI/Stable Diffusion, and a suite of **AI/NLP models** for natural‑language understanding.

Key capabilities include:
- Integration with the Gmail API for real‑time email ingestion.
- Rich, extensible **workflow graphs** where each node performs a distinct transformation (e.g., preprocessing, AI analysis, filtering, actions).
- **Security‑by‑design** – fine‑grained permissions, data sanitisation, execution sandboxing, and audit logging.
- **Performance dashboard** with real‑time CPU, memory, disk, model latency, and error‑rate metrics.
- **Extension system** for plug‑and‑play custom functionality.
- **Gradio UI** for scientific exploration and model debugging.

---