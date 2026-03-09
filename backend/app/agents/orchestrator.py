"""
Orchestrator Agent
Coordinates all specialized agents and manages interleaved output stream
"""

import asyncio
import json
from typing import AsyncGenerator, Dict, Any, List
from datetime import datetime
import uuid
import structlog
import google.generativeai as genai

from app.adk.config import ADKConfig
from app.models.story_request import StoryRequest, StoryChunk, StoryPlan
from app.agents.story_planner import StoryPlannerAgent
from app.agents.text_generator import TextGeneratorAgent
from app.agents.image_generator import ImageGeneratorAgent
from app.agents.audio_generator import AudioGeneratorAgent
from app.agents.video_generator import VideoGeneratorAgent
from app.agents.style_director import StyleDirectorAgent

logger = structlog.get_logger()


class OrchestratorAgent:
    """
    Main orchestration agent that coordinates all specialized agents
    and manages the interleaved output stream
    """

    def __init__(self, config: ADKConfig):
        self.config = config
        self.story_planner = StoryPlannerAgent(config)
        self.text_generator = TextGeneratorAgent(config)
        self.image_generator = ImageGeneratorAgent(config)
        self.audio_generator = AudioGeneratorAgent(config)
        self.video_generator = VideoGeneratorAgent(config)
        self.style_director = StyleDirectorAgent(config)

        # Initialize Gemini model for orchestration
        self.model = genai.GenerativeModel(config.gemini_model)

    async def generate_story(
        self, request: StoryRequest
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Generate a multimodal story with interleaved output

        This is the core method that:
        1. Creates a story plan
        2. Coordinates parallel agent execution
        3. Streams interleaved content in real-time
        """
        story_id = str(uuid.uuid4())
        sequence = 0

        try:
            # Phase 1: Story Planning
            logger.info(f"Starting story generation: {story_id}")
            yield self._create_chunk(
                story_id, "metadata", {"status": "planning", "phase": "initialization"}, sequence
            )
            sequence += 1

            # Generate story plan
            plan = await self.story_planner.create_plan(request)
            yield self._create_chunk(
                story_id, "metadata", {"status": "planning_complete", "plan": plan.dict()}, sequence
            )
            sequence += 1

            # Phase 2: Style Direction
            style_guide = await self.style_director.create_style_guide(request, plan)
            yield self._create_chunk(
                story_id, "metadata", {"status": "style_defined", "style": style_guide}, sequence
            )
            sequence += 1

            # Phase 3: Interleaved Content Generation
            # Generate content for each scene with interleaved output
            for scene_idx, scene in enumerate(plan.scenes):
                yield self._create_chunk(
                    story_id,
                    "metadata",
                    {"status": "generating_scene", "scene": scene_idx + 1, "total": len(plan.scenes)},
                    sequence
                )
                sequence += 1

                # Generate interleaved content for this scene
                async for chunk in self._generate_scene_content(
                    story_id, scene, request, style_guide, sequence
                ):
                    yield chunk
                    sequence += 1

            # Phase 4: Finalization
            yield self._create_chunk(
                story_id,
                "metadata",
                {"status": "complete", "story_id": story_id},
                sequence,
                is_final=True
            )

            logger.info(f"Story generation complete: {story_id}")

        except Exception as e:
            logger.error(f"Story generation failed: {e}")
            yield self._create_chunk(
                story_id,
                "metadata",
                {"status": "error", "message": str(e)},
                sequence,
                is_final=True
            )

    async def _generate_scene_content(
        self,
        story_id: str,
        scene: Dict[str, Any],
        request: StoryRequest,
        style_guide: Dict[str, Any],
        start_sequence: int
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Generate interleaved content for a single scene
        Text, images, audio, and video are generated in parallel and streamed
        """
        sequence = start_sequence
        tasks = []

        # Prepare parallel generation tasks
        if "text" in request.include_media:
            tasks.append(self.text_generator.generate_text(scene, request))

        if "images" in request.include_media:
            tasks.append(self.image_generator.generate_image(scene, style_guide))

        if "audio" in request.include_media:
            tasks.append(self.audio_generator.generate_audio(scene, request))

        if "video" in request.include_media:
            tasks.append(self.video_generator.generate_video(scene, style_guide))

        # Execute tasks and stream results as they complete
        if request.interleaved:
            # Interleaved mode: stream content as it's generated
            pending = [asyncio.create_task(task) for task in tasks]

            while pending:
                done, pending = await asyncio.wait(
                    pending, return_when=asyncio.FIRST_COMPLETED
                )

                for task in done:
                    try:
                        content = await task
                        yield self._create_chunk(
                            story_id,
                            content["type"],
                            content["data"],
                            sequence
                        )
                        sequence += 1
                    except Exception as e:
                        logger.error(f"Content generation error: {e}")
        else:
            # Sequential mode: wait for all content, then stream in order
            results = await asyncio.gather(*tasks, return_exceptions=True)

            for result in results:
                if isinstance(result, Exception):
                    logger.error(f"Generation error: {result}")
                    continue

                yield self._create_chunk(
                    story_id,
                    result["type"],
                    result["data"],
                    sequence
                )
                sequence += 1

    def _create_chunk(
        self,
        story_id: str,
        chunk_type: str,
        content: Any,
        sequence: int,
        is_final: bool = False
    ) -> Dict[str, Any]:
        """Create a standardized story chunk for streaming"""
        return {
            "story_id": story_id,
            "chunk_id": f"{story_id}-{sequence}",
            "chunk_type": chunk_type,
            "content": content,
            "sequence": sequence,
            "is_final": is_final,
            "timestamp": datetime.utcnow().isoformat()
        }
