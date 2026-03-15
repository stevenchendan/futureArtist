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

    # Per story type: writing persona, format rules, and example style cues
    TYPE_INSTRUCTIONS = {
        "storybook": """You are a children's book author. Write in a warm, imaginative narrator voice.
- Use simple, vivid language a child can picture
- Short sentences and short paragraphs (2-4 sentences each)
- Embrace wonder, magic, and emotion
- Add gentle rhyme or rhythm where natural
- Avoid jargon; every word should feel cozy and fun
- End each scene with a sense of anticipation or warmth""",

        "marketing": """You are a brand copywriter. Write punchy, persuasive marketing copy.
- Lead with a bold hook or headline (1 line)
- Focus on benefits, not features
- Use active voice and power words (discover, unlock, transform, imagine)
- Build emotional desire — make the reader feel the outcome
- Include a soft call-to-action at the end of the scene (e.g. "Ready to find out more?")
- Keep paragraphs short (1-2 sentences); use line breaks for emphasis
- Tone: confident, energetic, aspirational""",

        "educational": """You are an engaging educational content writer. Write clear, structured lesson content.
- Open with a curiosity hook or intriguing question
- Explain concepts step-by-step in plain language
- Use analogies and real-world examples
- Highlight key terms or facts (bold them with **asterisks**)
- End with a reflection question or key takeaway summary
- Tone: friendly, authoritative, encouraging
- Appropriate for the specified audience level""",

        "social": """You are a social media content creator. Write short, punchy, scroll-stopping content.
- Maximum 3-4 short sentences per scene
- Start with a strong hook (question, bold statement, or surprising fact)
- Conversational, upbeat voice — like talking to a friend
- Use line breaks between ideas for easy scanning
- End with an engaging question or call-to-action
- No fluff — every word earns its place
- Tone: relatable, fun, shareable""",
    }

    AUDIENCE_INSTRUCTIONS = {
        "children": """AUDIENCE: Young children (ages 4–10).
- Vocabulary: simple everyday words only; no words a child would need to look up
- Sentence length: very short (5–10 words max per sentence)
- Concepts: concrete and familiar (home, play, animals, friendship)
- Tone: warm, encouraging, wonder-filled
- Avoid: death, violence, complex emotions, sarcasm, abstract ideas
- Use: repetition, sound words (whoosh, splat, giggle), character names often""",

        "adults": """AUDIENCE: General adult readers.
- Vocabulary: rich and varied; use precise, expressive words
- Sentence length: mixed — short punchy sentences for impact, longer ones for description
- Concepts: nuanced emotions, complex relationships, moral ambiguity are welcome
- Tone: mature, layered, emotionally resonant
- Can include: subtext, irony, complex inner monologue
- Avoid: being condescending or over-explaining""",

        "professionals": """AUDIENCE: Working professionals in a business or specialist context.
- Vocabulary: industry-appropriate, precise, and credible
- Sentence structure: clear and efficient — no fluff
- Concepts: data, outcomes, ROI, strategy, expertise are natural here
- Tone: authoritative, respectful of the reader's intelligence and time
- Use: concrete examples, logical structure, actionable insights
- Avoid: whimsy, childish language, vague platitudes""",

        "general": """AUDIENCE: General audience — all ages, all backgrounds.
- Vocabulary: accessible but not dumbed down; aim for a comfortable reading level
- Sentence length: moderate; easy to follow
- Concepts: universal themes — family, discovery, challenge, connection
- Tone: inclusive, warm, relatable
- Avoid: jargon, niche references, overly complex language""",
    }

    def _build_text_prompt(
        self, scene: Dict[str, Any], request: StoryRequest
    ) -> str:
        """Build prompt for text generation"""

        type_instructions = self.TYPE_INSTRUCTIONS.get(
            request.story_type, self.TYPE_INSTRUCTIONS["storybook"]
        )
        audience_instructions = self.AUDIENCE_INSTRUCTIONS.get(
            request.target_audience, self.AUDIENCE_INSTRUCTIONS["general"]
        )

        return f"""
{type_instructions}

{audience_instructions}

Now write the text for this scene:

**Scene**: {scene.get('description', '')}
**Actions**: {', '.join(scene.get('actions', []))}
**Emotional Tone**: {scene.get('emotional_tone', 'neutral')}
**Story Tone**: {request.tone}
{f"**Dialogue cue**: {scene.get('dialogue')}" if scene.get('dialogue') else ""}

Write ONLY the scene text — no headings, no labels, no meta-commentary. Just the content itself.
"""
