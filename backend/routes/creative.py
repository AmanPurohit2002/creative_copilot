"""
Creative Copilot API routes.
Handles the multi-agent pipeline with agentic reflection:
  Brief → Brainstorm ↔ Review (autonomous loop) → Human picks concept → Script → Panels
"""

import json
import uuid
import io
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from backend.models import (
    IdeaRequest,
    ConceptsRequest,
    ScriptRequest,
    PanelsRequest,
    PdfExportRequest,
)
from backend.services.pdf_generator import generate_storyboard_pdf
from backend.services.graph import creative_graph

router = APIRouter(prefix="/api", tags=["creative"])

# Recursion limit for the graph (must be high enough to allow MAX_REVISIONS loops)
# Each loop is: brainstormer → reviewer → (conditional), so 3 revisions ≈ 6 node steps.
# Add headroom for other nodes. 25 is generous.
GRAPH_RECURSION_LIMIT = 25


@router.post("/brief")
async def generate_brief(request: IdeaRequest):
    """
    Step 1: Takes the raw idea, runs the autonomous agent loop:
      creative_director → brainstormer ↔ reviewer (reflection loop)
    
    The graph will run autonomously through the reflection loop and pause 
    at the interrupt_before=["screenwriter"] to let the human pick a concept.
    
    Returns the brief, the reviewed concepts, and reviewer reasoning.
    """
    try:
        thread_id = request.thread_id or str(uuid.uuid4())
        config = {
            "configurable": {"thread_id": thread_id},
            "recursion_limit": GRAPH_RECURSION_LIMIT,
        }

        # Run graph from START until it hits the interrupt before screenwriter
        result = await creative_graph.ainvoke({"idea": request.idea}, config)

        return {
            "thread_id": thread_id,
            "brief": result.get("brief", {}),
            "concepts": result.get("concepts", []),
            "revision_count": result.get("revision_count", 0),
            "reviewer_feedback": result.get("reviewer_feedback", ""),
            "reviewer_reasoning": result.get("reviewer_reasoning", ""),
            "concepts_approved": result.get("concepts_approved", False),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/script")
async def generate_script(request: ScriptRequest):
    """
    Step 2: Human has selected a concept. Update the graph state with their 
    choice and resume to run the screenwriter.
    
    The graph resumes from the interrupt before screenwriter, writes the script,
    then continues to storyboard_artist automatically.
    """
    try:
        config = {
            "configurable": {"thread_id": request.thread_id},
            "recursion_limit": GRAPH_RECURSION_LIMIT,
        }

        # Inject the human's selected concept into the graph state
        await creative_graph.aupdate_state(config, {"selected_concept": request.concept})

        # Resume graph — runs screenwriter → storyboard_artist → END
        result = await creative_graph.ainvoke(None, config)

        return {
            "shots": result.get("script", []),
            "panels": result.get("panels", []),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/export-pdf")
async def export_pdf(request: PdfExportRequest):
    """
    Generate a high-quality PDF storyboard from the generated panels.
    Returns the PDF file directly as a binary stream.
    """
    try:
        pdf_bytes = generate_storyboard_pdf(request.brief, [p.model_dump() for p in request.panels])
        return StreamingResponse(
            io.BytesIO(pdf_bytes),
            media_type="application/pdf",
            headers={
                "Content-Disposition": "attachment; filename=storyboard.pdf"
            },
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF Export failed: {str(e)}")
