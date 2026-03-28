sed -i 's/import gradio as gr/import gradio as gr\ntopic_chart = None\nsentiment_chart = None/g' src/backend/python_backend/gradio_app.py
sed -i 's/from fastapi import FastAPI, HTTPException, Request/from fastapi import FastAPI, HTTPException, Request, Depends/g' src/backend/python_backend/training_routes.py
sed -i 's/import subprocess/import subprocess\nimport importlib.util/g' src/backend/python_backend/plugin_manager.py
sed -i 's/from src.core.database import DatabaseManager, get_db/from src.core.database import DatabaseManager, get_db/g' src/backend/python_backend/main.py
