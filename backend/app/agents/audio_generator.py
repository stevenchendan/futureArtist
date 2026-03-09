"""
Audio Generator Agent
Produces narration, sound effects, and background music
"""

from typing import Dict, Any
import structlog

from app.adk.config import ADKConfig
from app.models.story_request import StoryRequest

logger = structlog.get_logger()


class AudioGeneratorAgent:
    """Agent responsible for generating audio content"""

    def __init__(self, config: ADKConfig):
        self.config = config

    async def generate_audio(
        self, scene: Dict[str, Any], request: StoryRequest
    ) -> Dict[str, Any]:
        """
        Generate audio (narration, effects, music) for a scene

        Args:
            scene: Scene information from story plan
            request: Original story request

        Returns:
            Dictionary with generated audio data
        """
        logger.info(f"Generating audio for scene {scene.get('scene_number', 0)}")

        # Audio generation configuration
        audio_config = self._build_audio_config(scene, request)

        # Placeholder - actual implementation would use Google Cloud Text-to-Speech
        # or similar audio generation service
        return {
            "type": "audio",
            "data": {
                "scene_number": scene.get("scene_number"),
                "narration_text": scene.get("description"),
                "audio_config": audio_config,
                "metadata": {
                    "tone": scene.get("emotional_tone"),
                    "duration_estimate": self._estimate_duration(scene)
                }
            }
        }

    def _build_audio_config(
        self, scene: Dict[str, Any], request: StoryRequest
    ) -> Dict[str, Any]:
        """Build configuration for audio generation"""

        return {
            "voice_style": self._select_voice_style(request.target_audience),
            "speaking_rate": "normal",
            "pitch": "medium",
            "effects": scene.get("audio_effects", []),
            "background_music": self._select_background_music(
                scene.get("emotional_tone", "neutral")
            )
        }

    def _select_voice_style(self, target_audience: str) -> str:
        """Select appropriate voice style based on audience"""
        voice_map = {
            "children": "warm_friendly",
            "adults": "professional_clear",
            "professionals": "authoritative_confident",
            "general": "neutral_engaging"
        }
        return voice_map.get(target_audience, "neutral_engaging")

    def _select_background_music(self, emotional_tone: str) -> str:
        """Select background music based on emotional tone"""
        music_map = {
            "playful": "upbeat_cheerful",
            "serious": "subtle_thoughtful",
            "suspenseful": "tense_mysterious",
            "inspiring": "uplifting_hopeful",
            "neutral": "ambient_soft"
        }
        return music_map.get(emotional_tone, "ambient_soft")

    def _estimate_duration(self, scene: Dict[str, Any]) -> float:
        """Estimate audio duration in seconds"""
        # Rough estimate: ~150 words per minute
        text = scene.get("description", "")
        word_count = len(text.split())
        return (word_count / 150) * 60
