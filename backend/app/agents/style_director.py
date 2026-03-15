"""
Style Director Agent
Ensures visual and tonal consistency across all generated media
"""

from typing import Dict, Any
import structlog

from app.adk.config import ADKConfig
from app.models.story_request import StoryRequest, StoryPlan

logger = structlog.get_logger()


class StyleDirectorAgent:
    """Agent responsible for maintaining visual and tonal consistency"""

    def __init__(self, config: ADKConfig):
        self.config = config

    async def create_style_guide(
        self, request: StoryRequest, plan: StoryPlan
    ) -> Dict[str, Any]:
        """
        Create a comprehensive style guide for the story

        Args:
            request: Original story request
            plan: Generated story plan

        Returns:
            Style guide dictionary
        """
        logger.info("Creating style guide")

        style_guide = {
            "visual_style": plan.visual_style,
            "color_palette": self._generate_color_palette(request, plan),
            "typography": self._select_typography(request.story_type),
            "character_sheets": plan.character_sheets or [],
            "visual_consistency": {
                "character_designs": self._create_character_design_rules(plan),
                "environment_rules": self._create_environment_rules(plan),
                "lighting": self._select_lighting_style(plan)
            },
            "tonal_consistency": {
                "narrative_voice": self._define_narrative_voice(request),
                "pacing": self._define_pacing(request.length),
                "emotional_progression": self._map_emotional_progression(plan)
            },
            "brand_elements": self._create_brand_elements(request)
        }

        return style_guide

    def _generate_color_palette(
        self, request: StoryRequest, plan: StoryPlan
    ) -> list:
        """Generate or use provided color palette"""
        if request.color_palette:
            return request.color_palette

        # Auto-generate palette based on story type and tone
        palette_map = {
            "storybook": {
                "playful": ["#FF6B9D", "#C44569", "#FFA07A", "#FFD93D"],
                "neutral": ["#6C5B7B", "#C06C84", "#F67280", "#F8B195"]
            },
            "marketing": {
                "professional": ["#2C3E50", "#3498DB", "#E74C3C", "#ECF0F1"],
                "inspiring": ["#FF6B6B", "#4ECDC4", "#45B7D1", "#FFA07A"]
            },
            "educational": {
                "neutral": ["#4A90E2", "#50E3C2", "#F5A623", "#7ED321"]
            },
            "social": {
                "playful": ["#FF006E", "#FFBE0B", "#8338EC", "#3A86FF"]
            }
        }

        return palette_map.get(request.story_type, {}).get(
            request.tone, ["#4A90E2", "#50E3C2", "#F5A623", "#7ED321"]
        )

    def _select_typography(self, story_type: str) -> Dict[str, str]:
        """Select appropriate typography"""
        typography_map = {
            "storybook": {
                "heading": "Fredoka One",
                "body": "Quicksand",
                "accent": "Pacifico"
            },
            "marketing": {
                "heading": "Montserrat Bold",
                "body": "Open Sans",
                "accent": "Playfair Display"
            },
            "educational": {
                "heading": "Lato Bold",
                "body": "Roboto",
                "accent": "Merriweather"
            },
            "social": {
                "heading": "Poppins Bold",
                "body": "Inter",
                "accent": "Permanent Marker"
            }
        }

        return typography_map.get(story_type, typography_map["storybook"])

    def _create_character_design_rules(self, plan: StoryPlan) -> Dict[str, Any]:
        """Create rules for consistent character design"""
        return {
            "style": plan.visual_style,
            "consistency_requirements": [
                "Maintain character proportions",
                "Keep color schemes consistent",
                "Preserve distinctive features"
            ]
        }

    def _create_environment_rules(self, plan: StoryPlan) -> Dict[str, Any]:
        """Create rules for environment consistency"""
        return {
            "style": plan.visual_style,
            "requirements": [
                "Consistent perspective",
                "Unified lighting direction",
                "Coherent scale and proportions"
            ]
        }

    def _select_lighting_style(self, plan: StoryPlan) -> str:
        """Select lighting style based on visual style"""
        lighting_map = {
            "cartoon": "flat_bright",
            "realistic": "naturalistic",
            "minimalist": "soft_ambient",
            "modern": "balanced_contrast"
        }
        return lighting_map.get(plan.visual_style, "balanced_contrast")

    def _define_narrative_voice(self, request: StoryRequest) -> str:
        """Define the narrative voice style"""
        voice_map = {
            "children": "warm_conversational",
            "adults": "sophisticated_engaging",
            "professionals": "authoritative_clear",
            "general": "accessible_friendly"
        }
        return voice_map.get(request.target_audience, "accessible_friendly")

    def _define_pacing(self, length: str) -> str:
        """Define story pacing"""
        pacing_map = {
            "short": "brisk",
            "medium": "moderate",
            "long": "leisurely"
        }
        return pacing_map.get(length, "moderate")

    def _map_emotional_progression(self, plan: StoryPlan) -> list:
        """Map emotional progression across the story"""
        arc = plan.narrative_arc

        return [
            {"phase": "setup", "emotion": "curiosity"},
            {"phase": "conflict", "emotion": "tension"},
            {"phase": "climax", "emotion": "excitement"},
            {"phase": "resolution", "emotion": "satisfaction"}
        ]

    def _create_brand_elements(self, request: StoryRequest) -> Dict[str, Any]:
        """Create brand elements for consistency"""
        return {
            "logo_placement": "bottom_right" if request.story_type == "marketing" else None,
            "watermark": False,
            "signature_style": request.style
        }
