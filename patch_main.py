import re

with open("src/main.py", "r") as f:
    content = f.read()

# Add # noqa: E402 to imports not at top
content = re.sub(r'^(import argparse)', r'\1  # noqa: E402', content, flags=re.MULTILINE)
content = re.sub(r'^(import logging)', r'\1  # noqa: E402', content, flags=re.MULTILINE)
content = re.sub(r'^(import gradio as gr)', r'\1  # noqa: E402', content, flags=re.MULTILINE)
content = re.sub(r'^(import uvicorn)', r'\1  # noqa: E402', content, flags=re.MULTILINE)
content = re.sub(r'^(import psutil)', r'\1  # noqa: E402', content, flags=re.MULTILINE)
content = re.sub(r'^(import platform)', r'\1  # noqa: E402', content, flags=re.MULTILINE)
content = re.sub(r'^(from datetime import datetime)', r'\1  # noqa: E402', content, flags=re.MULTILINE)
content = re.sub(r'^(import requests)', r'\1  # noqa: E402', content, flags=re.MULTILINE)
content = re.sub(r'^(from fastapi import FastAPI, HTTPException, Request)', r'\1  # noqa: E402', content, flags=re.MULTILINE)
content = re.sub(r'^(from fastapi\.middleware\.cors import CORSMiddleware)', r'\1  # noqa: E402', content, flags=re.MULTILINE)
content = re.sub(r'^(from fastapi\.responses import JSONResponse, RedirectResponse)', r'\1  # noqa: E402', content, flags=re.MULTILINE)
content = re.sub(r'^(from pydantic import ValidationError)', r'\1  # noqa: E402', content, flags=re.MULTILINE)
content = re.sub(r'^(from \.core\.module_manager import ModuleManager)', r'\1  # noqa: E402', content, flags=re.MULTILINE)
content = re.sub(r'^(from \.core\.middleware import create_security_middleware, create_security_headers_middleware)', r'\1  # noqa: E402', content, flags=re.MULTILINE)
content = re.sub(r'^(from \.core\.audit_logger import audit_logger, AuditEventType, AuditSeverity)', r'\1  # noqa: E402', content, flags=re.MULTILINE)
content = re.sub(r'^(from \.core\.performance_monitor import performance_monitor)', r'\1  # noqa: E402', content, flags=re.MULTILINE)

with open("src/main.py", "w") as f:
    f.write(content)
