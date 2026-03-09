"""
Text Generator Agent
Creates compelling narrative text, dialogue, and descriptions
"""

from typing import Dict, Any
import structlog
import google.generativeai as genai

from app.adk.config import ADKConfig
from app.models.story_request import StoryRequest

logger = structlog.get_logger()


class TextGeneratorAgent:
    """Agent responsible for generating narrative text content"""

    def __init__(self, config: ADKConfig):
        self.config = config
        self.model = genai.GenerativeModel(config.gemini_model)

    async def generate_text(
        self, scene: Dict[str, Any], request: StoryRequest
    ) -> Dict[str, Any]:
        """
        Generate narrative text for a scene

        Args:
            scene: Scene information from story plan
            request: Original story request for context

        Returns:
            Dictionary with generated text content
        """
        logger.info(f"Generating text for scene {scene.get('scene_number', 0)}")

        prompt = self._build_text_prompt(scene, request)
        response = await self.model.generate_content_async(prompt)

        return {
            "type": "text",
            "data": {
                "scene_number": scene.get("scene_number"),
                "text": response.text,
                "metadata": {
                    "tone": scene.get("emotional_tone"),
                    "word_count": len(response.text.split())
                }
            }
        }

    def _build_text_prompt(
        self, scene: Dict[str, Any], request: StoryRequest
    ) -> str:
        """Build prompt for text generation"""

        return f"""
You are a skilled storyteller. Write compelling narrative text for this scene:

**Scene Description**: {scene.get('description', '')}
**Actions**: {', '.join(scene.get('actions', []))}
**Emotional Tone**: {scene.get('emotional_tone', 'neutral')}
**Target Audience**: {request.target_audience}
**Story Tone**: {request.tone}

Write the narrative text for this scene. Make it engaging and appropriate for the target audience.
Include vivid descriptions and maintain the specified emotional tone.

{f"Dialogue: {scene.get('dialogue')}" if scene.get('dialogue') else ""}
"""
