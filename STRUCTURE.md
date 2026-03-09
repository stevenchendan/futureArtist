# Project Structure

## Complete Directory Tree

```
futureArtist/
│
├── 📄 README.md                        # Main project documentation
├── 📄 QUICKSTART.md                    # Quick start guide
├── 📄 PROJECT_SUMMARY.md               # Hackathon submission summary
├── 📄 CONTRIBUTING.md                  # Contribution guidelines
├── 📄 STRUCTURE.md                     # This file
├── 📄 LICENSE                          # MIT License
├── 📄 .gitignore                       # Git ignore rules
│
├── 📂 backend/                         # Python Backend (FastAPI + ADK)
│   ├── 📂 app/
│   │   ├── 📄 __init__.py
│   │   │
│   │   ├── 📂 adk/                     # Agent Development Kit Integration
│   │   │   ├── 📄 __init__.py
│   │   │   ├── 📄 main.py              # FastAPI application entry point
│   │   │   └── 📄 config.py            # Configuration management
│   │   │
│   │   ├── 📂 agents/                  # 7 Specialized AI Agents
│   │   │   ├── 📄 __init__.py
│   │   │   ├── 📄 orchestrator.py      # Main coordination agent
│   │   │   ├── 📄 story_planner.py     # Narrative structure creation
│   │   │   ├── 📄 text_generator.py    # Text content generation
│   │   │   ├── 📄 image_generator.py   # Image generation
│   │   │   ├── 📄 audio_generator.py   # Audio/narration generation
│   │   │   ├── 📄 video_generator.py   # Video creation
│   │   │   └── 📄 style_director.py    # Visual consistency
│   │   │
│   │   ├── 📂 api/                     # (To be implemented)
│   │   │   └── REST API routes
│   │   │
│   │   ├── 📂 models/                  # Data Models
│   │   │   ├── 📄 __init__.py
│   │   │   └── 📄 story_request.py     # Request/Response models
│   │   │
│   │   ├── 📂 services/                # (To be implemented)
│   │   │   └── Business logic
│   │   │
│   │   └── 📂 utils/                   # (To be implemented)
│   │       └── Helper functions
│   │
│   ├── 📄 requirements.txt             # Python dependencies
│   ├── 📄 Dockerfile                   # Container image definition
│   ├── 📄 cloudbuild.yaml              # Cloud Build configuration
│   ├── 📄 .dockerignore                # Docker ignore rules
│   ├── 📄 .env.example                 # Environment variables template
│   └── 📄 .gitignore                   # Backend-specific ignores
│
├── 📂 frontend/                        # Next.js Frontend (React + TypeScript)
│   ├── 📂 src/
│   │   ├── 📂 app/                     # Next.js 14 App Directory
│   │   │   ├── 📄 layout.tsx           # Root layout
│   │   │   ├── 📄 page.tsx             # Home page
│   │   │   └── 📄 globals.css          # Global styles
│   │   │
│   │   ├── 📂 components/              # React Components
│   │   │   ├── 📂 StoryCreator/
│   │   │   │   └── 📄 index.tsx        # Main story creation UI
│   │   │   ├── 📂 MediaViewer/
│   │   │   │   └── 📄 index.tsx        # Multimodal content display
│   │   │   ├── 📂 ControlPanel/
│   │   │   │   └── 📄 index.tsx        # Story configuration panel
│   │   │   └── 📂 ExportTools/
│   │   │       └── 📄 index.tsx        # Export functionality
│   │   │
│   │   ├── 📂 hooks/                   # Custom React Hooks
│   │   │   └── 📄 useStoryGeneration.ts # Story generation hook
│   │   │
│   │   ├── 📂 lib/                     # Utilities & Helpers
│   │   │   └── 📄 types.ts             # TypeScript type definitions
│   │   │
│   │   └── 📂 styles/                  # (To be implemented)
│   │       └── Additional styles
│   │
│   ├── 📂 public/                      # Static Assets
│   │   └── (images, icons, etc.)
│   │
│   ├── 📄 package.json                 # npm dependencies
│   ├── 📄 tsconfig.json                # TypeScript configuration
│   ├── 📄 tailwind.config.ts           # Tailwind CSS config
│   ├── 📄 postcss.config.js            # PostCSS configuration
│   ├── 📄 next.config.js               # Next.js configuration
│   ├── 📄 Dockerfile                   # Container image definition
│   ├── 📄 cloudbuild.yaml              # Cloud Build configuration
│   ├── 📄 .dockerignore                # Docker ignore rules
│   ├── 📄 .env.local.example           # Environment variables template
│   └── 📄 .gitignore                   # Frontend-specific ignores
│
├── 📂 infrastructure/                  # Infrastructure as Code
│   └── 📂 scripts/
│       ├── 📄 deploy.sh                # Automated deployment script
│       └── 📄 setup-gcp.sh             # GCP project setup script
│
├── 📂 docs/                            # Documentation
│   ├── 📄 architecture.md              # System architecture & design
│   ├── 📄 api.md                       # API documentation
│   └── 📄 deployment.md                # Deployment guide
│
└── 📂 .github/                         # GitHub Configuration
    └── 📂 workflows/
        └── 📄 deploy.yml               # CI/CD pipeline (GitHub Actions)
```

## File Count Summary

### Backend
- **Python Files**: 13
- **Config Files**: 6
- **Total Lines**: ~2,500

### Frontend
- **TypeScript/TSX Files**: 10
- **Config Files**: 7
- **Total Lines**: ~1,800

### Infrastructure & Docs
- **Scripts**: 2
- **Documentation**: 7
- **Total Lines**: ~2,000

### Total Project
- **Source Files**: 30+
- **Documentation Files**: 7
- **Configuration Files**: 13
- **Estimated Total Lines**: ~6,300

## Key Files Explained

### Root Level
- **README.md**: Main project documentation with setup instructions
- **QUICKSTART.md**: Get started in under 10 minutes
- **PROJECT_SUMMARY.md**: Hackathon submission overview
- **CONTRIBUTING.md**: Guidelines for contributors

### Backend (`backend/`)
- **app/adk/main.py**: FastAPI application with WebSocket & REST endpoints
- **app/adk/config.py**: Configuration management using Pydantic
- **app/agents/orchestrator.py**: Main coordinator for all agents
- **app/agents/*.py**: 6 specialized agents for different tasks
- **app/models/story_request.py**: Pydantic models for requests/responses

### Frontend (`frontend/`)
- **src/app/page.tsx**: Landing page with story creator
- **src/components/StoryCreator/**: Main UI component
- **src/components/MediaViewer/**: Displays interleaved content
- **src/components/ControlPanel/**: Story configuration interface
- **src/hooks/useStoryGeneration.ts**: WebSocket connection management

### Infrastructure (`infrastructure/`)
- **scripts/setup-gcp.sh**: One-command GCP project setup
- **scripts/deploy.sh**: Automated Cloud Run deployment

### Documentation (`docs/`)
- **architecture.md**: Detailed system design (2,500+ words)
- **api.md**: Complete API reference with examples
- **deployment.md**: Step-by-step deployment guide

## Technology Breakdown

### Backend Technologies
- Python 3.11+
- FastAPI (async web framework)
- Google ADK (Agent Development Kit)
- Google Gemini 2.0 API
- Pydantic (data validation)
- Uvicorn (ASGI server)
- Structlog (logging)

### Frontend Technologies
- Next.js 14 (React framework)
- TypeScript 5 (type safety)
- Tailwind CSS (styling)
- Shadcn/ui (UI components)
- Framer Motion (animations)
- React Markdown (content rendering)
- WebSocket (real-time communication)

### Google Cloud Services
- Cloud Run (hosting)
- Vertex AI (Gemini API)
- Cloud Storage (media storage)
- Cloud Build (CI/CD)
- Secret Manager (credentials)
- Cloud Logging (monitoring)

### Development Tools
- Docker (containerization)
- Git (version control)
- GitHub Actions (CI/CD)
- Black (Python formatting)
- Ruff (Python linting)
- Prettier (TypeScript formatting)
- ESLint (TypeScript linting)

## Next Steps to Complete

### For Hackathon Submission
1. ✅ Code implementation
2. ✅ Documentation
3. ✅ Deployment scripts
4. ⏳ Deploy to Google Cloud
5. ⏳ Create demo video (< 4 minutes)
6. ⏳ Create architecture diagram
7. ⏳ Screen recording of deployment
8. ⏳ Test all functionality

### Future Enhancements (Post-Hackathon)
1. Add actual image generation (Imagen integration)
2. Implement real audio synthesis (Cloud TTS)
3. Add video compilation features
4. Create user authentication
5. Build story library/templates
6. Add export to more formats
7. Implement collaborative editing
8. Add analytics and tracking

## Getting Started

```bash
# Clone repository
git clone https://github.com/your-username/futureArtist.git
cd futureArtist

# Quick start (see QUICKSTART.md)
cd infrastructure/scripts
./setup-gcp.sh your-project-id
./deploy.sh
```

For detailed instructions, see:
- [QUICKSTART.md](QUICKSTART.md) - Quick setup guide
- [docs/deployment.md](docs/deployment.md) - Detailed deployment
- [README.md](README.md) - Full documentation
