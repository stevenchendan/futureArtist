"""
Story Request and Response Models
"""

from typing import Optional, List, Dict, Any, Literal
from pydantic import BaseModel, Field
from datetime import datetime


class StoryRequest(BaseModel):
    """Request model for story generation"""

    prompt: str = Field(..., description="Main story prompt or theme")
    story_type: Literal["storybook", "marketing", "educational", "social"] = Field(
        default="storybook",
        description="Type of story to generate"
    )
    target_audience: Optional[str] = Field(
        default="general",
        description="Target audience (e.g., children, adults, professionals)"
    )
    tone: Optional[str] = Field(
        default="neutral",
        description="Story tone (e.g., playful, professional, inspiring)"
    )
    length: Literal["short", "medium", "long"] = Field(
        default="medium",
        description="Desired story length"
    )
    style: Optional[str] = Field(
        default="modern",
        description="Visual style for images (e.g., cartoon, realistic, minimalist)"
    )
    include_media: List[Literal["text", "images", "audio", "video"]] = Field(
        default=["text", "images"],
        description="Types of media to include in the output"
    )
    interleaved: bool = Field(
        default=True,
        description="Generate interleaved output (text + media together)"
    )
    color_palette: Optional[List[str]] = Field(
        default=None,
        description="Preferred color palette for visuals"
    )
    additional_instructions: Optional[str] = Field(
        default=None,
        description="Additional instructions or constraints"
    )


class MediaContent(BaseModel):
    """Model for media content chunks"""

    type: Literal["text", "image", "audio", "video"]
    content: Any  # Can be text string, base64, or URL
    metadata: Optional[Dict[str, Any]] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class StoryChunk(BaseModel):
    """Model for streamed story chunks"""

    chunk_id: str
    chunk_type: Literal["text", "image", "audio", "video", "metadata"]
    content: Any
    sequence: int
    is_final: bool = False


class StoryResponse(BaseModel):
    """Response model for complete story"""

    story_id: str
    title: Optional[str] = None
    content: List[MediaContent]
    metadata: Dict[str, Any]
    created_at: datetime = Field(default_factory=datetime.utcnow)
    generation_time: Optional[float] = None


class StoryPlan(BaseModel):
    """Internal model for story planning"""

    title: str
    outline: List[str]
    scenes: List[Dict[str, Any]]
    character_descriptions: Optional[List[str]] = None
    character_sheets: Optional[List[Dict[str, Any]]] = None
    visual_style: str
    narrative_arc: Dict[str, str]
