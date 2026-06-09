"""
Creative Copilot — FastAPI Backend
Serves the React frontend and provides API endpoints for the storyboard pipeline.
"""

import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

from backend.routes.creative import router as creative_router
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup/shutdown events."""
    # Check Gemini API key (for Image generation)
    if os.getenv("GEMINI_API_KEY"):
        print("[OK] GEMINI_API_KEY is set")
    else:
        print("[WARN] GEMINI_API_KEY is not set in .env")
        print("   Image generation will not work without it.")
        
    # Check Groq API key (for Text generation)
    if os.getenv("GROQ_API_KEY"):
        print("[OK] GROQ_API_KEY is set")
    else:
        print("[WARN] GROQ_API_KEY is not set in .env")
        print("   Creative Copilot will not work without it.")

    # Setup LangGraph checkpointer Redis indices (only for Redis-backed checkpointers)
    try:
        from backend.services.graph import checkpointer
        if hasattr(checkpointer, 'setup'):
            await checkpointer.setup()
            print("[OK] LangGraph checkpointer indices created in Redis")
        else:
            print("[OK] Using in-memory checkpointer (no setup needed)")
    except Exception as e:
        print(f"[WARN] Checkpointer setup skipped: {e}")

    yield
    # Shutdown
    print("[INFO] Shutting down Creative Copilot")


app = FastAPI(
    title="Creative Copilot API",
    description="Turn a one-line ad idea into an annotated storyboard",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS — allow frontend dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routes
app.include_router(creative_router)


@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    gemini_ok = bool(os.getenv("GEMINI_API_KEY"))
    groq_ok = bool(os.getenv("GROQ_API_KEY"))
    return {
        "status": "ok",
        "gemini": "configured" if gemini_ok else "missing_key",
        "groq": "configured" if groq_ok else "missing_key",
    }
