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


    def _build_image_prompt(
        self, scene: Dict[str, Any], style_guide: Dict[str, Any]
    ) -> str:
        """Build detailed prompt for image generation"""

        visual_elements = ", ".join(scene.get("visual_elements", []))
        style = style_guide.get("visual_style", "modern")
        colors = self._describe_palette(style_guide.get("color_palette", []))

        prompt = f"""
Create an illustration for this scene:

Scene: {scene.get('description', '')}
Visual Elements: {visual_elements}
Style: {style}
Color Mood: {colors}
Emotional Tone: {scene.get('emotional_tone', 'neutral')}

The image should be {style} style and include: {visual_elements}.
Maintain consistency with the established visual style.
Do not include any text, labels, color swatches, or hex codes in the image.
"""
        return prompt.strip()

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
