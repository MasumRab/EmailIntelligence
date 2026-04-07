# Deploying to Render (Free Tier)

This guide explains how to deploy the Email Intelligence Platform to Render's Free Tier (512MB RAM, 0.1 CPU).

## Optimized Architecture

To fit within the free tier limits, this deployment uses:
*   **Single Service**: The Python backend serves the built React frontend as static files.
*   **Lite Mode**: Heavy AI libraries (PyTorch, Transformers, Scikit-learn) are **disabled** to save memory.
*   **Ephemeral Storage**: Data is stored in local JSON files which **will be lost** on restart/redeploy.

## Deployment Steps

1.  **Create a New Web Service** on [Render Dashboard](https://dashboard.render.com/).
2.  Connect your GitHub repository.
3.  Select **"Manual Deployment"** (if prompted) or proceed to configuration.
4.  Configure the service details:

    *   **Name**: `email-intelligence` (or your choice)
    *   **Region**: Any (e.g., Oregon)
    *   **Branch**: `main` (or your working branch)
    *   **Root Directory**: `.` (leave empty)
    *   **Runtime**: **Python 3**
    *   **Build Command**: `./setup_env.sh`
    *   **Start Command**: `uvicorn src.backend.python_backend.main:app --host 0.0.0.0 --port $PORT`

5.  **Environment Variables**:
    Add the following environment variables:

    | Key | Value | Description |
    | :--- | :--- | :--- |
    | `RENDER` | `true` | Activates "Lite Mode" and triggers frontend build. |
    | `PYTHON_VERSION` | `3.11.0` | Ensures correct Python version. |
    | `NODE_VERSION` | `20.0.0` | Ensures correct Node.js version for frontend build. |
    | `PORT` | `10000` | (Render sets this automatically, but good to know). |

6.  **Create Web Service**.

## Verification

Once deployed:
*   Navigate to your Render URL (e.g., `https://email-intelligence.onrender.com`).
*   The React frontend should load.
*   The `/api/health` (if exists) or other API endpoints should work.
*   **Note**: Local AI features will be disabled.

## Troubleshooting

*   **Build Failures**: Check the logs. Ensure `client/package.json` dependencies are compatible with Node 20.
*   **Memory Issues**: If the app crashes with "Out of Memory", ensure `RENDER=true` is set.
*   **Data Loss**: Remember that data is not persistent. For persistence, you would need to connect a managed PostgreSQL database (paid or external free tier).
