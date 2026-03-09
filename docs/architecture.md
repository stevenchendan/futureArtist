# Future Artist - Architecture Documentation

## System Overview

Future Artist is a multimodal AI storytelling platform built for the Gemini Live Agent Challenge 2025. It leverages Gemini's native interleaved output capabilities to create rich, mixed-media narratives.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                           Frontend (Next.js)                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │ Story Creator│  │ Media Viewer │  │ Export Tools │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
│                          │                                       │
│                    WebSocket/HTTP                                │
└──────────────────────────┼──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Backend (FastAPI + ADK)                       │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              Orchestrator Agent                           │  │
│  │  (Coordinates all agents & manages interleaved output)    │  │
│  └────────────┬─────────────────────────────────────────────┘  │
│               │                                                  │
│    ┌──────────┴──────────────────────────────────┐            │
│    │                                              │             │
│    ▼              ▼              ▼               ▼             │
│  ┌────────┐  ┌────────┐  ┌────────┐  ┌────────────────┐      │
│  │Story   │  │Text    │  │Image   │  │Audio  │Video   │       │
│  │Planner │  │Gen     │  │Gen     │  │Gen    │Gen     │       │
│  └────────┘  └────────┘  └────────┘  └────────────────┘      │
│       │           │           │              │      │           │
│       └───────────┴───────────┴──────────────┴──────┘          │
│                           │                                      │
└───────────────────────────┼──────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Google Cloud Services                         │
│  ┌──────────┐  ┌───────────┐  ┌──────────┐  ┌──────────────┐ │
│  │ Gemini   │  │ Vertex AI │  │  Cloud   │  │    Secret    │ │
│  │ 2.0 API  │  │           │  │ Storage  │  │   Manager    │ │
│  └──────────┘  └───────────┘  └──────────┘  └──────────────┘ │
│                                                                  │
│  ┌──────────┐  ┌───────────┐                                   │
│  │  Cloud   │  │   Cloud   │                                   │
│  │   Run    │  │   Build   │                                   │
│  └──────────┘  └───────────┘                                   │
└─────────────────────────────────────────────────────────────────┘
```

## Component Architecture

### Frontend Layer

**Technology**: Next.js 14, React, TypeScript, Tailwind CSS

**Components**:
- **Story Creator**: User input interface for story configuration
- **Media Viewer**: Real-time display of interleaved content
- **Control Panel**: Story parameters and settings
- **Export Tools**: Export to various formats (PDF, HTML, JSON)

**State Management**: Zustand for global state, React hooks for local state

**Communication**: WebSocket for real-time streaming, REST API for exports

### Backend Layer

**Technology**: Python 3.11+, FastAPI, Google ADK

**Core Services**:

#### 1. Orchestrator Agent
- **Purpose**: Main coordinator for all specialized agents
- **Responsibilities**:
  - Story planning coordination
  - Parallel agent execution
  - Interleaved output management
  - Real-time streaming to frontend
- **Key Features**:
  - Async task management
  - Progress tracking
  - Error handling and recovery

#### 2. Story Planner Agent
- **Purpose**: Create narrative structure
- **Output**: StoryPlan with scenes, characters, narrative arc
- **Model**: Gemini 2.0 for creative planning

#### 3. Text Generator Agent
- **Purpose**: Generate narrative text and dialogue
- **Output**: Formatted text content per scene
- **Features**: Tone-aware, audience-appropriate content

#### 4. Image Generator Agent
- **Purpose**: Create visual content
- **Integration**: Gemini Imagen for image generation
- **Output**: Image prompts and generated images

#### 5. Audio Generator Agent
- **Purpose**: Produce narration and sound
- **Integration**: Google Cloud Text-to-Speech
- **Features**: Voice selection, tone matching

#### 6. Video Generator Agent
- **Purpose**: Create video sequences
- **Output**: Video specifications and rendered content
- **Features**: Storyboard creation, transitions

#### 7. Style Director Agent
- **Purpose**: Ensure visual and tonal consistency
- **Output**: Comprehensive style guide
- **Features**:
  - Color palette management
  - Typography selection
  - Brand consistency

## Data Flow

### Story Generation Flow

1. **User Input** → Frontend collects story parameters
2. **WebSocket Connection** → Establishes real-time channel
3. **Planning Phase**:
   - Story Planner creates narrative structure
   - Style Director defines visual guidelines
4. **Generation Phase** (Interleaved):
   - Orchestrator coordinates parallel agent execution
   - Text, Image, Audio, Video generated simultaneously
   - Content streamed as available (interleaved mode)
5. **Streaming Output**:
   - Frontend receives chunks in real-time
   - MediaViewer renders content progressively
6. **Completion**:
   - Final signal sent to frontend
   - Export options enabled

### Interleaved Output Strategy

**Key Innovation**: Unlike traditional sequential generation, Future Artist uses Gemini's interleaved output to stream different media types as they're created:

```
Timeline:
─────────────────────────────────────────────────────>
│       │         │         │         │         │
Plan    Text1     Image1    Text2     Audio1    Video1
        ↓         ↓         ↓         ↓         ↓
        Stream    Stream    Stream    Stream    Stream
```

This creates a more natural, real-time storytelling experience.

## Google Cloud Integration

### Required Services

1. **Gemini API** (Mandatory)
   - Model: gemini-2.0-flash-exp
   - Purpose: Core AI generation
   - Usage: All agents

2. **Vertex AI** (Mandatory)
   - Purpose: AI model orchestration
   - Integration: ADK framework

3. **Cloud Run** (Mandatory)
   - Services: Backend API, Frontend app
   - Configuration: Auto-scaling, HTTPS

4. **Cloud Storage** (Mandatory)
   - Purpose: Media file storage
   - Features: CORS enabled, public access

5. **Cloud Build**
   - Purpose: CI/CD pipeline
   - Triggers: Git push to main

6. **Secret Manager**
   - Purpose: API key management
   - Secrets: Gemini API key, service account credentials

## Security Considerations

### Authentication
- Service Account for GCP services
- API key management via Secret Manager
- CORS configuration for frontend

### Data Privacy
- No user data persistence (stateless)
- Media stored temporarily in Cloud Storage
- Optional data retention policies

### Rate Limiting
- Per-user request limits
- Concurrent agent execution limits
- Timeout configurations

## Scalability

### Horizontal Scaling
- Cloud Run auto-scales based on requests
- Stateless architecture enables multiple instances
- WebSocket connections load-balanced

### Performance Optimization
- Parallel agent execution
- Streaming reduces perceived latency
- CDN for static frontend assets
- Image optimization and lazy loading

## Monitoring & Logging

### Application Monitoring
- Structured logging (structlog)
- Cloud Logging integration
- Error tracking and alerting

### Metrics
- Story generation time
- Agent execution time
- Success/failure rates
- API usage statistics

## Deployment Models

### Option 1: Cloud Run (Recommended)
- Easiest deployment
- Auto-scaling
- Fully managed
- Cost-effective

### Option 2: Agent Engine
- ADK native deployment
- Advanced agent orchestration
- Enterprise features
- Higher complexity

## Future Enhancements

1. **Real-time Collaboration**: Multiple users on same story
2. **Template Library**: Pre-built story templates
3. **Advanced Exports**: Video compilation, interactive web pages
4. **User Accounts**: Save and manage stories
5. **API Platform**: Public API for integrations
6. **Multi-language Support**: Internationalization
7. **Advanced AI Models**: Custom fine-tuned models
