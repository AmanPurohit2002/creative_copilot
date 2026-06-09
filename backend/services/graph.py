"""
LangGraph-based multi-agent creative pipeline with agentic reflection.

Flow:
  START → creative_director → brainstormer → reviewer
      ↕ (reflection loop — max MAX_REVISIONS iterations)
  reviewer → (approved?) → interrupt for human concept selection → screenwriter → storyboard_artist → END
"""

import os
import json
from typing import TypedDict, Optional
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.redis.aio import AsyncRedisSaver

from backend.models import (
    BriefResponse,
    ConceptsResponse,
    ReviewerResponse,
    ScriptResponse,
    ImagePromptResponse,
)
from backend.services.llm import generate_structured_json
from backend.services.imagen import generate_all_panels
from backend.services.prompts import (
    BRIEF_SYSTEM_PROMPT,
    BRIEF_USER_TEMPLATE,
    CONCEPTS_SYSTEM_PROMPT,
    CONCEPTS_USER_TEMPLATE,
    CONCEPTS_RETRY_SYSTEM_PROMPT,
    CONCEPTS_RETRY_USER_TEMPLATE,
    REVIEWER_SYSTEM_PROMPT,
    REVIEWER_USER_TEMPLATE,
    SCRIPT_SYSTEM_PROMPT,
    SCRIPT_USER_TEMPLATE,
    IMAGE_PROMPT_SYSTEM,
    IMAGE_PROMPT_USER_TEMPLATE,
)


# Maximum number of brainstormer ↔ reviewer loops before we force-accept
MAX_REVISIONS = 3


# ─── State ──────────────────────────────────────────────────────────────────────

class CreativeState(TypedDict, total=False):
    """The state that flows through the entire creative pipeline."""
    # Inputs
    idea: str
    tone: str
    visual_style: str
    color_palette: str
    aspect_ratio: str

    # Outputs from each agent
    brief: Optional[dict]
    concepts: Optional[list[dict]]
    selected_concept: Optional[dict]
    script: Optional[list[dict]]
    panels: Optional[list[dict]]

    # Agentic reflection fields
    reviewer_feedback: Optional[str]       # Feedback from reviewer → brainstormer
    reviewer_reasoning: Optional[str]      # Chain-of-thought from reviewer
    revision_count: int                    # How many brainstormer iterations so far
    concepts_approved: Optional[bool]      # Whether the reviewer approved the concepts


# ─── Agent Nodes ────────────────────────────────────────────────────────────────

async def creative_director(state: CreativeState) -> CreativeState:
    """Agent 1: Converts raw idea into a structured creative brief."""
    print("[Agent] Creative Director — generating brief...")
    user_prompt = BRIEF_USER_TEMPLATE.format(idea=state["idea"])
    brief = await generate_structured_json(user_prompt, BRIEF_SYSTEM_PROMPT, BriefResponse)
    return {"brief": brief.model_dump(), "revision_count": 0, "reviewer_feedback": ""}


async def brainstormer(state: CreativeState) -> CreativeState:
    """Agent 2: Generates 3 creative concepts. Uses reviewer feedback on retries."""
    revision = state.get("revision_count", 0)
    brief_json = json.dumps(state["brief"], indent=2)

    if revision == 0 or not state.get("reviewer_feedback"):
        # First attempt — no feedback yet
        print(f"[Agent] Brainstormer — generating concepts (attempt {revision + 1})...")
        user_prompt = CONCEPTS_USER_TEMPLATE.format(brief_json=brief_json)
        result = await generate_structured_json(user_prompt, CONCEPTS_SYSTEM_PROMPT, ConceptsResponse)
    else:
        # Retry with feedback from reviewer
        print(f"[Agent] Brainstormer — RETRYING concepts with feedback (attempt {revision + 1})...")
        user_prompt = CONCEPTS_RETRY_USER_TEMPLATE.format(
            brief_json=brief_json,
            feedback=state["reviewer_feedback"],
        )
        result = await generate_structured_json(user_prompt, CONCEPTS_RETRY_SYSTEM_PROMPT, ConceptsResponse)

    return {
        "concepts": result.model_dump()["concepts"],
        "revision_count": revision + 1,
    }


async def reviewer(state: CreativeState) -> CreativeState:
    """Agent 3: Evaluates concepts against the brief. Routes back to brainstormer or approves."""
    revision = state.get("revision_count", 0)
    print(f"[Agent] Reviewer — evaluating concepts (revision {revision}/{MAX_REVISIONS})...")

    brief_json = json.dumps(state["brief"], indent=2)
    concepts_json = json.dumps(state.get("concepts", []), indent=2)

    user_prompt = REVIEWER_USER_TEMPLATE.format(
        brief_json=brief_json,
        concepts_json=concepts_json,
    )
    result = await generate_structured_json(user_prompt, REVIEWER_SYSTEM_PROMPT, ReviewerResponse)

    print(f"[Agent] Reviewer verdict: {'APPROVED ✓' if result.approved else 'REJECTED ✗'}")
    if not result.approved:
        print(f"[Agent] Reviewer feedback: {result.feedback}")

    return {
        "concepts_approved": result.approved,
        "reviewer_feedback": result.feedback,
        "reviewer_reasoning": result.reasoning,
    }


def should_retry_concepts(state: CreativeState) -> str:
    """Conditional edge: decide whether to loop back to brainstormer or proceed.

    Routes to:
      - "brainstormer" if rejected AND under the revision limit
      - "screenwriter" if approved OR revision limit reached (force-accept)
    """
    approved = state.get("concepts_approved", False)
    revision = state.get("revision_count", 0)

    if approved:
        print(f"[Router] Concepts approved — proceeding to human selection & screenwriter")
        return "screenwriter"

    if revision >= MAX_REVISIONS:
        print(f"[Router] Revision limit ({MAX_REVISIONS}) reached — force-accepting concepts")
        return "screenwriter"

    print(f"[Router] Concepts rejected — routing back to brainstormer for revision {revision + 1}")
    return "brainstormer"


async def screenwriter(state: CreativeState) -> CreativeState:
    """Agent 4: Writes the shot-by-shot script from brief + selected concept."""
    print("[Agent] Screenwriter — writing shot-by-shot script...")
    brief_json = json.dumps(state["brief"], indent=2)
    concept_json = json.dumps(state.get("selected_concept", {}), indent=2)
    user_prompt = SCRIPT_USER_TEMPLATE.format(
        brief_json=brief_json,
        concept_json=concept_json,
    )
    result = await generate_structured_json(user_prompt, SCRIPT_SYSTEM_PROMPT, ScriptResponse)
    return {"script": result.model_dump()["shots"]}


async def storyboard_artist(state: CreativeState) -> CreativeState:
    """Agent 5: Generates image prompts and AI images for each shot."""
    print("[Agent] Storyboard Artist — generating image panels...")
    shots_with_prompts = []
    for i, shot in enumerate(state["script"]):
        user_prompt = IMAGE_PROMPT_USER_TEMPLATE.format(
            visual=shot.get("visual", ""),
            camera=shot.get("camera", ""),
            tone=state.get("tone", ""),
            visual_style=state.get("visual_style", ""),
            color_palette=state.get("color_palette", ""),
        )
        prompt_result = await generate_structured_json(user_prompt, IMAGE_PROMPT_SYSTEM, ImagePromptResponse)
        shots_with_prompts.append({
            **shot,
            "shot_number": i + 1,
            "image_prompt": prompt_result.image_prompt,
        })

    panels = await generate_all_panels(
        shots_with_prompts,
        aspect_ratio=state.get("aspect_ratio", "16:9"),
    )
    return {"panels": panels}


# ─── Build & Compile Graph ──────────────────────────────────────────────────────

redis_url = os.environ.get("REDIS_URL", "redis://redis:6379/0")
checkpointer = AsyncRedisSaver(redis_url=redis_url)

builder = StateGraph(CreativeState)

# Register nodes
builder.add_node("creative_director", creative_director)
builder.add_node("brainstormer", brainstormer)
builder.add_node("reviewer", reviewer)
builder.add_node("screenwriter", screenwriter)
builder.add_node("storyboard_artist", storyboard_artist)

# Edges
builder.add_edge(START, "creative_director")
builder.add_edge("creative_director", "brainstormer")
builder.add_edge("brainstormer", "reviewer")

# Conditional edge: reviewer decides whether to loop back or proceed
builder.add_conditional_edges(
    "reviewer",
    should_retry_concepts,
    {
        "brainstormer": "brainstormer",
        "screenwriter": "screenwriter",
    },
)

builder.add_edge("screenwriter", "storyboard_artist")
builder.add_edge("storyboard_artist", END)

# Compile with:
#   - interrupt_before screenwriter: this is the HUMAN-IN-THE-LOOP pause
#     where the user selects their preferred concept before the script is written.
#   - The brainstormer ↔ reviewer loop runs autonomously (no interrupt).
creative_graph = builder.compile(
    checkpointer=checkpointer,
    interrupt_before=["screenwriter"],
)
