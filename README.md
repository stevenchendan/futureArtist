# Future Artist - Creative Storyteller AI Agent

## Gemini Live Agent Challenge 2025 Submission

A multimodal AI storytelling platform that leverages Gemini's interleaved output capabilities to create rich, mixed-media narratives combining text, images, audio, and video in a single, fluid output stream.

## Track: Creative Storyteller ✍️

**Focus**: Multimodal Storytelling with Interleaved Output

## Overview

Future Artist is an AI-powered creative director that seamlessly weaves together multiple media types to generate:
- Interactive storybooks with inline generated illustrations
- Marketing assets (copy + visuals + video) in one cohesive flow
- Educational content with narration and diagrams
- Social media content packages (captions + images + hashtags)

## Architecture

```
├── backend/                    # Python/FastAPI with ADK
│   ├── app/
│   │   ├── adk/               # Agent Development Kit integration
│   │   │   ├── main.py        # ADK entry point
│   │   │   └── config.py      # ADK configuration
│   │   ├── agents/            # Specialized agents
│   │   │   ├── orchestrator.py    # Main orchestration agent
│   │   │   ├── story_planner.py   # Story structure & narrative arc
│   │   │   ├── text_generator.py  # Text content generation
│   │   │   ├── image_generator.py # Image creation & prompts
│   │   │   ├── audio_generator.py # Audio/narration generation
│   │   │   ├── video_generator.py # Video creation
│   │   │   └── style_director.py  # Visual consistency & branding
│   │   ├── api/               # FastAPI routes
│   │   ├── models/            # Data models
│   │   ├── services/          # Business logic
│   │   └── utils/             # Helper functions
│   ├── requirements.txt
│   ├── Dockerfile
│   └── cloudbuild.yaml        # Cloud Build configuration
│
├── frontend/                   # React/Next.js
│   ├── src/
│   │   ├── app/               # Next.js app directory
│   │   ├── components/        # React components
│   │   │   ├── StoryCreator/  # Main story creation interface
│   │   │   ├── MediaViewer/   # Multimodal content display
│   │   │   ├── ControlPanel/  # Story customization controls
│   │   │   └── ExportTools/   # Export & share functionality
│   │   ├── hooks/             # Custom React hooks
│   │   ├── lib/               # Utilities
│   │   └── styles/            # CSS/Tailwind styles
│   ├── public/
│   ├── package.json
│   ├── Dockerfile
│   └── next.config.js
│
├── infrastructure/             # Infrastructure as Code
│   ├── terraform/             # Terraform configurations
│   └── scripts/               # Deployment scripts
│
├── docs/                       # Documentation
│   ├── architecture.md
│   ├── api.md
│   └── deployment.md
│
└── .github/
    └── workflows/             # CI/CD pipelines
```

## Tech Stack

### Mandatory Technologies ✅

- **Gemini Model**: Gemini 2.0 with native interleaved output
- **Agent Framework**: Google ADK (Agent Development Kit)
- **Google Cloud Services**:
  - Cloud Run (Backend & Frontend hosting)
  - Vertex AI (Gemini API integration)
  - Cloud Storage (Media storage)
  - Cloud Build (CI/CD)
  - Secret Manager (API keys & credentials)

### Backend
- Python 3.11+
- FastAPI
- Google GenAI SDK / ADK
- Pydantic for data validation

### Frontend
- Next.js 14+ (React)
- TypeScript
- Tailwind CSS
- Shadcn/ui components

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- Google Cloud SDK
- Docker (for containerized deployment)

### Local Development

#### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Set environment variables
cp .env.example .env
# Edit .env with your credentials

# Run locally
python -m app.adk.main
```

#### Frontend Setup

```bash
cd frontend
npm install

# Set environment variables
cp .env.local.example .env.local
# Edit .env.local with your backend URL

# Run development server
npm run dev
```

Visit `http://localhost:3000` to see the application.

### Google Cloud Deployment

#### Option 1: Cloud Run (Recommended)

```bash
# Deploy backend
cd backend
gcloud run deploy futureartist-backend \
  --source . \
  --region us-central1 \
  --allow-unauthenticated

# Deploy frontend
cd frontend
gcloud run deploy futureartist-frontend \
  --source . \
  --region us-central1 \
  --allow-unauthenticated
```

#### Option 2: Agent Engine

```bash
# Deploy using ADK to Agent Engine
cd backend
adk deploy --project YOUR_PROJECT_ID
```

## Agent Architecture

### 1. Orchestrator Agent
Coordinates all specialized agents and manages the interleaved output stream.

### 2. Story Planner Agent
Develops narrative structure, character arcs, and scene breakdown.

### 3. Text Generator Agent
Creates compelling narrative text, dialogue, and descriptions.

### 4. Image Generator Agent
Generates contextual illustrations using Gemini's image generation.

### 5. Audio Generator Agent
Produces narration, sound effects, and background music.

### 6. Video Generator Agent
Creates video sequences and animations from storyboards.

### 7. Style Director Agent
Ensures visual and tonal consistency across all generated media.

## Environment Variables

### Backend (.env)
```
GOOGLE_CLOUD_PROJECT=your-project-id
GEMINI_API_KEY=your-api-key
GOOGLE_APPLICATION_CREDENTIALS=path/to/service-account.json
CLOUD_STORAGE_BUCKET=your-bucket-name
PORT=8000
```

### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_NAME=Future Artist
```

## Development Workflow

1. **Create a Story Request**: User provides a prompt or theme
2. **Orchestrator Plans**: Story structure is created
3. **Parallel Generation**: Text, images, audio, video generated simultaneously
4. **Interleaved Assembly**: Content woven together in real-time
5. **Stream to Frontend**: User sees story unfold progressively
6. **Export Options**: Save as PDF, web page, video, or social posts

## Submission Requirements

- [x] Leverages Gemini model
- [x] Built using Google ADK
- [x] Uses multiple Google Cloud services
- [x] Implements interleaved/mixed output capabilities
- [ ] Public code repository with setup instructions
- [ ] Google Cloud deployment proof (screen recording)
- [ ] Architecture diagram
- [ ] Demo video (under 4 minutes)

## Demo Ideas

1. **Interactive Children's Storybook**: Generate "The Lost Robot" with illustrations, narration, and animations
2. **Marketing Campaign Generator**: Create complete product launch materials
3. **Educational Explainer**: "How Photosynthesis Works" with diagrams and voiceover
4. **Social Media Campaign**: Week-long content series with consistent branding

## License

MIT License - See LICENSE file for details

## Team
Steven(Liang) Chen
Kuan Yu

## Acknowledgments

Built for the Gemini Live Agent Challenge 2026 - Creative Storyteller Track
