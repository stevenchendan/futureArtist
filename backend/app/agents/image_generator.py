"""
Image Generator Agent
Generates contextual illustrations using Gemini's image generation
"""

import base64
from typing import Dict, Any
import structlog
from google import genai
from google.genai import types

from app.adk.config import ADKConfig

logger = structlog.get_logger()


class ImageGeneratorAgent:
    """Agent responsible for generating images and illustrations"""

    def __init__(self, config: ADKConfig):
        self.config = config
        # Use Gemini model with image generation capabilities
        self.model = "gemini-3.1-flash-image-preview"
        self.client = genai.Client(api_key=config.gemini_api_key)

    async def generate_image(
        self, scene: Dict[str, Any], style_guide: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate an image for a scene

        Args:
            scene: Scene information from story plan
            style_guide: Visual style guidelines

        Returns:
            Dictionary with generated image data
        """
        logger.info(f"Generating image for scene {scene.get('scene_number', 0)}")

        # Build image generation prompt
        image_prompt = self._build_image_prompt(scene, style_guide)

        response = await self.client.aio.models.generate_content(
            model=self.model,
            contents=[image_prompt],
            config=types.GenerateContentConfig(
                candidate_count=1,
                response_modalities=["Image"],
                image_config=types.ImageConfig(
                    aspect_ratio="16:9",
                    image_size="1K"  # Options: 1K, 2K, 4K
                )
            )
        )
        return {
            "type": "image",
            "data": {
                "scene_number": scene.get("scene_number"),
                "prompt": image_prompt,
                "style": style_guide.get("visual_style"),
                "generated_data": base64.b64encode(response.candidates[0].content.parts[0].inline_data.data).decode('utf-8'),
                "metadata": {
                    "visual_elements": scene.get("visual_elements", []),
                    "color_palette": style_guide.get("color_palette")
                }
            }
        }


    STYLE_INSTRUCTIONS = {
        "cartoon": (
            "2D cartoon illustration style. "
            "Bold black outlines, flat solid colors, cel-shaded with no photorealism. "
            "Exaggerated, expressive character proportions (big eyes, round heads). "
            "Bright saturated colors, simple clean backgrounds. "
            "Lighting: flat and bright — no complex shadows or gradients."
        ),
        "realistic": (
            "Photorealistic digital painting style. "
            "Naturalistic proportions, detailed textures, and lifelike skin. "
            "Soft natural lighting with realistic shadows and highlights. "
            "Rich depth of field, cinematic composition. "
            "High detail on faces, clothing, and environment."
        ),
        "minimalist": (
            "Flat minimalist illustration style. "
            "Clean geometric shapes, very limited detail, generous negative space. "
            "Maximum 3 colors used in the entire image. "
            "No outlines or thin hairline strokes only. "
            "Soft ambient lighting — subtle and even. "
            "Simple, iconic representations of subjects."
        ),
        "modern": (
            "Contemporary digital illustration style. "
            "Semi-flat design with subtle drop shadows and soft gradients. "
            "Polished, professional look with clean lines. "
            "Balanced contrast lighting — not too dramatic, not flat. "
            "Smooth color transitions, modern color palette, refined composition."
        ),
    }

    def _build_image_prompt(
        self, scene: Dict[str, Any], style_guide: Dict[str, Any]
    ) -> str:
        """Build detailed prompt for image generation"""

        visual_elements = ", ".join(scene.get("visual_elements", []))
        style_key = style_guide.get("visual_style", "modern")
        style_instructions = self.STYLE_INSTRUCTIONS.get(style_key, self.STYLE_INSTRUCTIONS["modern"])
        colors = self._describe_palette(style_guide.get("color_palette", []))
        character_ref = self._build_character_reference(
            scene.get("characters_in_scene", []),
            style_guide.get("character_sheets", [])
        )

        prompt = f"""
Create an illustration for this scene:

Scene: {scene.get('description', '')}
Visual Elements: {visual_elements}
Color Mood: {colors}
Emotional Tone: {scene.get('emotional_tone', 'neutral')}
{character_ref}
RENDERING STYLE: {style_instructions}

Draw the image in the above rendering style. Include: {visual_elements}.
Every character MUST match their character reference exactly — same skin tone, hair, clothing, and features as specified. Do not deviate from the character reference.
Do not include any text, labels, color swatches, or hex codes in the image.
"""
        return prompt.strip()

    def _build_character_reference(
        self, characters_in_scene: list, character_sheets: list
    ) -> str:
        """Build a character reference block for consistent character appearance"""
        if not character_sheets:
            return ""

        # Filter to only characters in this scene, or use all if not specified
        if characters_in_scene:
            sheets = [s for s in character_sheets if s.get("name", "") in characters_in_scene]
        else:
            sheets = character_sheets

        if not sheets:
            return ""

        lines = ["\nCHARACTER REFERENCE (draw exactly as described, do not change):"]
        for s in sheets:
            lines.append(
                f"- {s.get('name', 'Character')}: {s.get('age_appearance', '')}, "
                f"{s.get('body_type', '')}, skin tone: {s.get('skin_tone', '')}, "
                f"hair: {s.get('hair', '')}, eyes: {s.get('eyes', '')}, "
                f"wearing: {s.get('clothing', '')}, "
                f"distinctive features: {s.get('distinctive_features', '')}"
            )
        return "\n".join(lines) + "\n"

    def _describe_palette(self, palette: list) -> str:
        """Convert hex color codes to descriptive color language for the prompt"""
        if not palette:
            return "vibrant and balanced colors"

        hex_to_name = {
            "#FF6B9D": "pink", "#C44569": "deep rose", "#FFA07A": "light salmon",
            "#FFD93D": "golden yellow", "#6C5B7B": "muted purple", "#C06C84": "mauve",
            "#F67280": "soft coral", "#F8B195": "peach", "#2C3E50": "dark navy",
            "#3498DB": "sky blue", "#E74C3C": "red", "#ECF0F1": "light grey",
            "#FF6B6B": "coral red", "#4ECDC4": "teal", "#45B7D1": "light blue",
            "#4A90E2": "blue", "#50E3C2": "mint green", "#F5A623": "amber",
            "#7ED321": "green", "#FF006E": "hot pink", "#FFBE0B": "yellow",
            "#8338EC": "violet", "#3A86FF": "bright blue",
        }

        names = [hex_to_name.get(c.upper(), "warm tone") for c in palette]
        return ", ".join(names)
