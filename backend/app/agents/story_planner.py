"""
Story Planner Agent
Develops narrative structure, character arcs, and scene breakdown
"""

from typing import Dict, Any
import structlog
import google.generativeai as genai

from app.adk.config import ADKConfig
from app.models.story_request import StoryRequest, StoryPlan

logger = structlog.get_logger()


class StoryPlannerAgent:
    """Agent responsible for creating story structure and narrative planning"""

    def __init__(self, config: ADKConfig):
        self.config = config
        self.model = genai.GenerativeModel(config.gemini_model)

    async def create_plan(self, request: StoryRequest) -> StoryPlan:
        """
        Create a comprehensive story plan based on the request

        Returns:
            StoryPlan with narrative structure, scenes, and character info
        """
        logger.info(f"Creating story plan for: {request.story_type}")

        # Build prompt for story planning
        planning_prompt = self._build_planning_prompt(request)

        # Generate plan using Gemini
        response = await self.model.generate_content_async(planning_prompt)

        # Parse response into StoryPlan
        plan = self._parse_plan_response(response.text, request)

        logger.info(f"Story plan created: {plan.title}")
        return plan

    def _build_planning_prompt(self, request: StoryRequest) -> str:
        """Build the prompt for story planning"""

        length_map = {
            "short": "3-5 scenes",
            "medium": "6-10 scenes",
            "long": "11-15 scenes"
        }

        prompt = f"""
You are a creative story planner. Create a detailed story plan based on the following requirements:

**Story Prompt**: {request.prompt}
**Story Type**: {request.story_type}
**Target Audience**: {request.target_audience}
**Tone**: {request.tone}
**Length**: {length_map.get(request.length, "medium")}
**Visual Style**: {request.style}

Please create a comprehensive story plan that includes:

1. **Title**: A compelling title for the story
2. **Outline**: High-level story outline (beginning, middle, end)
3. **Scenes**: Detailed breakdown of each scene including:
   - Scene description
   - Key actions/events
   - Dialogue (if applicable)
   - Visual elements needed
   - Emotional tone
4. **Characters**: For EVERY named character, provide a detailed visual character sheet with exact physical attributes so they can be drawn consistently across all scenes.
5. **Narrative Arc**: Story progression (setup, conflict, climax, resolution)

Format your response as a structured JSON object with the following schema:
{{
    "title": "Story Title",
    "outline": ["Beginning summary", "Middle summary", "End summary"],
    "scenes": [
        {{
            "scene_number": 1,
            "description": "Scene description",
            "actions": ["action 1", "action 2"],
            "dialogue": "Optional dialogue",
            "visual_elements": ["element 1", "element 2"],
            "emotional_tone": "tone",
            "characters_in_scene": ["Character Name 1", "Character Name 2"]
        }}
    ],
    "character_sheets": [
        {{
            "name": "Character Name",
            "role": "protagonist/antagonist/supporting",
            "skin_tone": "e.g. light peach, medium brown, dark brown, olive",
            "hair": "e.g. short curly black hair",
            "eyes": "e.g. round brown eyes",
            "clothing": "e.g. red hoodie, blue jeans, white sneakers",
            "distinctive_features": "e.g. freckles on nose, always wears a yellow backpack",
            "body_type": "e.g. small child, tall adult, chubby toddler",
            "age_appearance": "e.g. looks about 8 years old"
        }}
    ],
    "character_descriptions": ["Character 1 summary", "Character 2 summary"],
    "narrative_arc": {{
        "setup": "Setup description",
        "conflict": "Conflict description",
        "climax": "Climax description",
        "resolution": "Resolution description"
    }},
    "visual_style": "{request.style}"
}}

{f"Additional Instructions: {request.additional_instructions}" if request.additional_instructions else ""}
"""
        return prompt

    def _parse_plan_response(self, response_text: str, request: StoryRequest) -> StoryPlan:
        """Parse Gemini response into StoryPlan object"""
        import json

        try:
            # Try to extract JSON from response
            start_idx = response_text.find("{")
            end_idx = response_text.rfind("}") + 1

            if start_idx >= 0 and end_idx > start_idx:
                json_str = response_text[start_idx:end_idx]
                plan_data = json.loads(json_str)

                return StoryPlan(
                    title=plan_data.get("title", "Untitled Story"),
                    outline=plan_data.get("outline", []),
                    scenes=plan_data.get("scenes", []),
                    character_descriptions=plan_data.get("character_descriptions"),
                    character_sheets=plan_data.get("character_sheets"),
                    visual_style=plan_data.get("visual_style", request.style or "modern"),
                    narrative_arc=plan_data.get("narrative_arc", {})
                )
            else:
                # Fallback: create basic plan from text
                return self._create_fallback_plan(response_text, request)

        except json.JSONDecodeError:
            logger.warning("Failed to parse JSON response, using fallback")
            return self._create_fallback_plan(response_text, request)

    def _create_fallback_plan(self, text: str, request: StoryRequest) -> StoryPlan:
        """Create a basic plan when JSON parsing fails"""
        return StoryPlan(
            title="Generated Story",
            outline=["Beginning", "Middle", "End"],
            scenes=[
                {
                    "scene_number": 1,
                    "description": text[:500],
                    "actions": [],
                    "visual_elements": [],
                    "emotional_tone": request.tone or "neutral"
                }
            ],
            visual_style=request.style or "modern",
            narrative_arc={
                "setup": "Story begins",
                "conflict": "Challenge arises",
                "climax": "Peak moment",
                "resolution": "Story concludes"
            }
        )
