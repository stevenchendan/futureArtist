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

    AUDIENCE_CONTEXT = {
        "children": """AUDIENCE — Young children (ages 4–10):
- Keep scene descriptions short and action-focused (what happens, not complex feelings)
- Characters should have simple, clear motivations (hungry, scared, curious, happy)
- Avoid scenes with conflict that is scary or violent; keep challenges gentle
- Visual elements: bright, simple, expressive — animals, toys, nature, magic
- Each scene should end on a clear, satisfying note a child can understand""",

        "adults": """AUDIENCE — Adults:
- Scenes can have emotional complexity, ambiguity, and depth
- Characters can have layered motivations, flaws, and inner conflict
- Subplots and nuance are welcome
- Visual elements can be sophisticated, atmospheric, or realistic
- Pacing can include slower reflective moments""",

        "professionals": """AUDIENCE — Professionals:
- Scene descriptions should be concise and purposeful — no filler
- Characters are competent people facing credible challenges
- Focus on stakes, decisions, and outcomes
- Visual elements: clean, credible, business-appropriate settings
- Each scene should have a clear purpose tied to the main message""",

        "general": """AUDIENCE — General (all ages, all backgrounds):
- Keep concepts accessible and universally relatable
- Characters face challenges anyone can empathize with
- Visual elements: inviting, clear, not niche or culture-specific
- Balance emotional appeal with clarity""",
    }

    TYPE_CONTEXT = {
        "storybook": """This is a CHILDREN'S STORYBOOK.
- Structure scenes as classic story beats: introduction → adventure/challenge → resolution → lesson
- Characters should be relatable, expressive, and have clear personalities
- Each scene should advance the story with a small emotional beat
- Visual elements should be whimsical, colorful, and imaginative
- The narrative arc should feel warm and satisfying""",

        "marketing": """This is a MARKETING CAMPAIGN / BRAND STORY.
- Structure scenes as: problem/pain point → brand solution introduction → transformation → call to action
- Focus on customer journey and emotional transformation
- Each scene should build desire and trust
- Visual elements should feel aspirational, clean, and on-brand
- Characters represent the target customer persona""",

        "educational": """This is an EDUCATIONAL LESSON / EXPLAINER.
- Structure scenes as: hook/question → concept introduction → worked example → practice/reflection → summary
- Each scene should teach one clear concept or fact
- Use characters as learners or guides (e.g. teacher + student)
- Visual elements should illustrate concepts clearly (diagrams, demonstrations, settings)
- End with a key takeaway or discussion question per scene""",

        "social": """This is SOCIAL MEDIA CONTENT (short-form posts / reels).
- Structure scenes as punchy stand-alone moments — each scene is its own micro-story
- Scenes should be very short and high-impact
- Lead with a scroll-stopping hook in each scene
- Visual elements should be bold, eye-catching, and shareable
- Characters and actions should be relatable and culturally relevant""",
    }

    def _build_planning_prompt(self, request: StoryRequest) -> str:
        """Build the prompt for story planning"""

        length_map = {
            "short": "3-5 scenes",
            "medium": "6-10 scenes",
            "long": "11-15 scenes"
        }

        type_context = self.TYPE_CONTEXT.get(request.story_type, self.TYPE_CONTEXT["storybook"])
        audience_context = self.AUDIENCE_CONTEXT.get(request.target_audience, self.AUDIENCE_CONTEXT["general"])

        prompt = f"""
You are a creative story planner. Create a detailed story plan based on the following requirements:

**Story Prompt**: {request.prompt}
**Story Type**: {request.story_type}
**Target Audience**: {request.target_audience}
**Tone**: {request.tone}
**Length**: {length_map.get(request.length, "medium")}
**Visual Style**: {request.style}

{type_context}

{audience_context}

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
