"""
FastAPI application for EmailIntelligence task management
Separated from CLI to follow Single Responsibility Principle
"""
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, Dict, Any
import asyncio
from pathlib import Path

from src.application.conflict_resolution_app import ConflictResolutionApp

# Create the FastAPI app
app = FastAPI(
    title="EmailIntelligence API",
    description="AI-powered git worktree-based conflict resolution API",
    version="1.0.0"
)

# Add CORS middleware with restricted origins (not wildcard)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost", "http://127.0.0.1", "https://localhost", "https://127.0.0.1"],  # Restricted origins
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    # Remove allow_origins=["*"] which was a security vulnerability
)

# Initialize the conflict resolution app
repo_root = Path.cwd()
conflict_resolver = ConflictResolutionApp(repo_root)

@app.get("/")
async def root():
    """Root endpoint for the API"""
    return {"message": "EmailIntelligence API is running", "version": "1.0.0"}

@app.post("/setup-resolution/")
async def setup_resolution_endpoint(
    pr_number: int,
    source_branch: str,
    target_branch: str,
    constitution_files: Optional[str] = None,
    spec_files: Optional[str] = None,
    dry_run: bool = False
):
    """Endpoint to setup resolution workspace for a specific PR"""
    try:
        # Convert comma-separated strings to lists if provided
        constitution_list = constitution_files.split(",") if constitution_files else None
        spec_list = spec_files.split(",") if spec_files else None
        
        result = conflict_resolver.setup_resolution(
            pr_number=pr_number,
            source_branch=source_branch,
            target_branch=target_branch,
            constitution_files=constitution_list,
            spec_files=spec_list,
            dry_run=dry_run
        )
        
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid input: {str(e)}")
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": asyncio.get_event_loop().time()}

# Additional endpoints would go here...