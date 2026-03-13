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
        colors = ", ".join(style_guide.get("color_palette", []))

        prompt = f"""
Create an illustration for this scene:

Scene: {scene.get('description', '')}
Visual Elements: {visual_elements}
Style: {style}
Color Palette: {colors}
Emotional Tone: {scene.get('emotional_tone', 'neutral')}

The image should be {style} style and include: {visual_elements}.
Maintain consistency with the established visual style.
"""
        return prompt.strip()
