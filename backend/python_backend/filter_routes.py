from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Any, Dict, List

from backend.node_engine.workflow_engine import workflow_engine, Workflow
from backend.node_engine.node_base import ExecutionContext

router = APIRouter()

class WorkflowPayload(BaseModel):
    workflow: Dict[str, Any]

@router.post("/api/workflows/run_filter")
async def run_filter_workflow(payload: WorkflowPayload):
    try:
        workflow_data = payload.workflow
        workflow = Workflow.from_dict(workflow_data)
        context = ExecutionContext()
        results = await workflow_engine.execute_workflow(workflow, {}, context)
        return {"results": results, "errors": context.get_errors()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
