"""
Audio Generator Agent
Produces narration using Google Gemini TTS
"""

import base64
from typing import Dict, Any
import structlog
from google import genai
from google.genai import types

from app.adk.config import ADKConfig
from app.models.story_request import StoryRequest

logger = structlog.get_logger()


class AudioGeneratorAgent:
    """Agent responsible for generating audio content"""

    def __init__(self, config: ADKConfig):
        self.config = config
        self.client = genai.Client(api_key=config.gemini_api_key)

    async def generate_audio(
        self, scene: Dict[str, Any], request: StoryRequest
    ) -> Dict[str, Any]:
        """
        Generate narration audio for a scene using Gemini TTS

        Args:
            scene: Scene information from story plan
            request: Original story request

        Returns:
            Dictionary with generated audio data (base64 PCM)
        """
        logger.info(f"Generating audio for scene {scene.get('scene_number', 0)}")

        narration_text = scene.get("description", "")
        voice_name = self._select_voice(request.target_audience)

        response = await self.client.aio.models.generate_content(
            model="gemini-2.5-flash-preview-tts",
            contents=narration_text,
            config=types.GenerateContentConfig(
                response_modalities=["AUDIO"],
                speech_config=types.SpeechConfig(
                    voice_config=types.VoiceConfig(
                        prebuilt_voice_config=types.PrebuiltVoiceConfig(
                            voice_name=voice_name
                        )
                    )
                ),
            ),
        )

        audio_data = response.candidates[0].content.parts[0].inline_data.data
        audio_b64 = base64.b64encode(audio_data).decode("utf-8")

        return {
            "type": "audio",
            "data": {
                "scene_number": scene.get("scene_number"),
                "narration_text": narration_text,
                "audio_data": audio_b64,
                "mime_type": "audio/wav",
                "metadata": {
                    "tone": scene.get("emotional_tone"),
                    "duration_estimate": self._estimate_duration(scene),
                    "voice": voice_name,
                }
            }
        }

    def _select_voice(self, target_audience: str) -> str:
        """Select a Gemini TTS voice based on target audience"""
        voice_map = {
            "children": "Kore",
            "adults": "Charon",
            "professionals": "Fenrir",
            "general": "Aoede",
        }
        return voice_map.get(target_audience, "Aoede")

    def _estimate_duration(self, scene: Dict[str, Any]) -> float:
        """Estimate audio duration in seconds (~150 words per minute)"""
        text = scene.get("description", "")
        word_count = len(text.split())
        return round((word_count / 150) * 60, 1)
