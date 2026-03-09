"""
ADK Entry Point for Future Artist
Handles agent initialization and orchestration using Google ADK
"""

import os
import asyncio
from typing import AsyncGenerator, Dict, Any
from dotenv import load_dotenv
import google.generativeai as genai
from fastapi import FastAPI, WebSocket, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import structlog

from app.adk.config import ADKConfig
from app.agents.orchestrator import OrchestratorAgent
from app.models.story_request import StoryRequest, StoryResponse

# Load environment variables
load_dotenv()

# Configure logging
logger = structlog.get_logger()

# Initialize FastAPI app
app = FastAPI(
    title="Future Artist API",
    description="Multimodal Storytelling AI Agent using Gemini",
    version="0.1.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize ADK configuration
config = ADKConfig()

# Initialize Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    logger.info("Starting Future Artist backend")
    logger.info(f"Using Gemini model: {config.gemini_model}")
    logger.info(f"Google Cloud Project: {config.gcp_project}")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Shutting down Future Artist backend")


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "online",
        "service": "Future Artist",
        "version": "0.1.0",
        "gemini_model": config.gemini_model
    }


@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "services": {
            "gemini": "connected",
            "storage": "connected" if config.storage_bucket else "not configured"
        }
    }


@app.post("/api/v1/story/generate")
async def generate_story(request: StoryRequest):
    """
    Generate a multimodal story with interleaved output

    Args:
        request: Story generation parameters

    Returns:
        StreamingResponse with interleaved content
    """
    try:
        # Initialize orchestrator agent
        orchestrator = OrchestratorAgent(config)

        # Generate story with streaming
        async def story_stream():
            async for chunk in orchestrator.generate_story(request):
                yield chunk

        return StreamingResponse(
            story_stream(),
            media_type="application/x-ndjson"
        )

    except Exception as e:
        logger.error(f"Story generation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.websocket("/ws/story")
async def websocket_story_generation(websocket: WebSocket):
    """
    WebSocket endpoint for real-time story generation with interleaved output
    """
    await websocket.accept()

    try:
        # Receive story request
        data = await websocket.receive_json()
        request = StoryRequest(**data)

        # Initialize orchestrator
        orchestrator = OrchestratorAgent(config)

        # Stream story generation
        async for chunk in orchestrator.generate_story(request):
            await websocket.send_json(chunk)

        # Send completion signal
        await websocket.send_json({"type": "complete", "status": "success"})

    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        await websocket.send_json({
            "type": "error",
            "message": str(e)
        })
    finally:
        await websocket.close()


@app.post("/api/v1/story/export")
async def export_story(story_id: str, format: str = "pdf"):
    """
    Export generated story to various formats

    Args:
        story_id: ID of the generated story
        format: Export format (pdf, html, video, social)
    """
    # TODO: Implement export functionality
    return {
        "story_id": story_id,
        "format": format,
        "status": "pending",
        "message": "Export functionality coming soon"
    }


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")

    uvicorn.run(
        "app.adk.main:app",
        host=host,
        port=port,
        reload=os.getenv("DEBUG", "false").lower() == "true"
    )
