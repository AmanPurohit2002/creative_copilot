"""
Pydantic models for request/response validation across the Creative Copilot API.
"""

from pydantic import BaseModel, Field
from typing import Optional


# ─── Request Models ───────────────────────────────────────────────────────────

class IdeaRequest(BaseModel):
    idea: str
    thread_id: Optional[str] = None


class ConceptsRequest(BaseModel):
    thread_id: str
    brief: dict


class ScriptRequest(BaseModel):
    thread_id: str
    concept: dict


class PanelsRequest(BaseModel):
    thread_id: str
    shots: list[dict]
    aspect_ratio: str = "16:9"
    tone: str = ""
    visual_style: str = ""
    color_palette: str = ""


# ─── Response Models ────────────────────────────────────────────────────────

class BriefResponse(BaseModel):
    title: str = Field(description="A catchy, concise title for the campaign (max 5 words)")
    format: str = Field(description="The primary ad format (e.g., YouTube Pre-Roll, Instagram Reel, TV Commercial)")
    duration: str = Field(description="Expected duration (e.g., 15 seconds, 30 seconds)")
    platform: str = Field(description="Target platforms (e.g., Instagram, YouTube, TikTok)")
    audience: str = Field(description="Target audience demographics and psychographics")
    tone: str = Field(description="The emotional tone of the ad (e.g., Comedic, Dramatic, Urgent)")
    product: str = Field(description="The core product or service being advertised")
    goal: str = Field(description="The primary objective (e.g., Brand Awareness, Direct Response, App Installs)")
    cta: str = Field(description="The primary Call To Action")
    key_message: str = Field(description="The single most important message to convey in one sentence")


class Concept(BaseModel):
    title: str = Field(description="A catchy name for this creative concept")
    logline: str = Field(description="A one-sentence summary of the ad's plot or core hook")
    visual_style: str = Field(description="The visual aesthetic (e.g., Cinematic, User Generated Content, Animation, Bright and Colorful)")
    color_palette: str = Field(description="3-4 specific colors that dominate the visuals (e.g., Neon Pink, Deep Blue, High-contrast B&W)")
    description: str = Field(description="A paragraph describing how the ad unfolds from start to finish")


class ConceptsResponse(BaseModel):
    concepts: list[Concept]


class ReviewerResponse(BaseModel):
    """Output of the Reviewer agent that critiques brainstormed concepts."""
    approved: bool = Field(description="True if the concepts are diverse, creative, and aligned with the brief. False if they need rework.")
    feedback: str = Field(description="If not approved: specific, actionable feedback on what to improve. If approved: a brief praise note.")
    reasoning: str = Field(description="Step-by-step reasoning for the decision. Explain which concepts are strong/weak and why.")


class ScriptShot(BaseModel):
    visual: str = Field(description="Detailed description of what is seen on screen")
    camera: str = Field(description="Camera angle and movement (e.g., Close-up pan, Wide establishing shot)")
    duration: str = Field(description="Duration of this specific shot (e.g., 3 seconds)")
    voiceover: Optional[str] = Field(description="Spoken dialogue or voiceover for this shot. Leave null if none.")
    text_overlay: Optional[str] = Field(description="On-screen text graphics for this shot. Leave null if none.")
    transition: str = Field(description="How this shot transitions to the next (e.g., Cut, Fade, Wipe)")


class ScriptResponse(BaseModel):
    shots: list[ScriptShot]


class ImagePromptResponse(BaseModel):
    image_prompt: str = Field(description="A detailed, comma-separated image generation prompt optimized for cinematic storyboard panels")


class ShotPanel(BaseModel):
    """A fully generated shot panel with its image base64"""
    shot_number: int
    visual: str
    camera: str
    duration: str
    voiceover: Optional[str] = None
    text_overlay: Optional[str] = None
    transition: str
    image_prompt: str
    image_base64: Optional[str] = None
    error: Optional[str] = None


class PdfExportRequest(BaseModel):
    """Payload for generating a PDF storyboard"""
    brief: dict
    panels: list[ShotPanel]


class Panel(BaseModel):
    shot_number: int
    image_base64: str
    duration: str
    camera: str
    visual: str
    text_overlay: str = ""
    voiceover: str = ""
    transition: str = "Cut"


class PanelsResponse(BaseModel):
    panels: list[Panel]
