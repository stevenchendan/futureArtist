# Future Artist - Quick Start Guide

Get Future Artist up and running in under 10 minutes!

## Prerequisites

- Google Cloud account with billing enabled
- Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey)
- [Google Cloud SDK](https://cloud.google.com/sdk/docs/install) installed
- Python 3.11+ and Node.js 18+ (for local development)

## 🚀 Cloud Deployment (Fastest)

### Step 1: Setup Google Cloud Project

```bash
# Set your project ID
export GOOGLE_CLOUD_PROJECT=your-project-id

# Run setup script
cd infrastructure/scripts
chmod +x setup-gcp.sh
./setup-gcp.sh $GOOGLE_CLOUD_PROJECT
```

### Step 2: Store Gemini API Key

```bash
# Get API key from: https://aistudio.google.com/app/apikey
echo -n 'YOUR_GEMINI_API_KEY' | gcloud secrets create gemini-api-key --data-file=-
```

### Step 3: Deploy

```bash
chmod +x deploy.sh
./deploy.sh
```

**Done!** Your app is now live. URLs will be displayed at the end.

## 💻 Local Development

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate (Linux/Mac)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add:
# - GEMINI_API_KEY=your-key
# - GOOGLE_CLOUD_PROJECT=your-project

# Run server
python -m app.adk.main
```

Backend runs at: `http://localhost:8000`

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Configure environment
cp .env.local.example .env.local
# Edit .env.local and set:
# - NEXT_PUBLIC_API_URL=http://localhost:8000

# Run development server
npm run dev
```

Frontend runs at: `http://localhost:3000`

## 🎨 Create Your First Story

1. Open frontend URL in browser
2. Enter a story prompt:
   ```
   A brave little robot learning to paint in an art studio
   ```
3. Select options:
   - **Story Type**: Interactive Storybook
   - **Target Audience**: Children
   - **Tone**: Playful
   - **Length**: Medium
   - **Style**: Cartoon
   - **Include Media**: Text ✓, Images ✓
4. Click **Generate Story**
5. Watch your story come to life! ✨

## 📚 Example Prompts

### Children's Story
```
A curious kitten discovers a magical garden where flowers sing
```

### Marketing Campaign
```
Launch a new eco-friendly water bottle brand targeting millennials
```

### Educational Content
```
Explain how the solar system works for elementary school students
```

### Social Media
```
Create a week-long fitness motivation series with workout tips
```

## 🔧 Troubleshooting

### "Permission denied" errors
```bash
# Grant necessary permissions
gcloud projects add-iam-policy-binding $GOOGLE_CLOUD_PROJECT \
  --member="serviceAccount:futureartist-sa@$GOOGLE_CLOUD_PROJECT.iam.gserviceaccount.com" \
  --role="roles/aiplatform.user"
```

### "API not enabled" errors
```bash
# Enable required APIs
gcloud services enable run.googleapis.com cloudbuild.googleapis.com aiplatform.googleapis.com
```

### WebSocket connection fails
- Ensure you're using `wss://` for HTTPS endpoints
- Check CORS settings in backend
- Verify frontend environment variables

### Backend won't start locally
- Check Python version: `python --version` (needs 3.11+)
- Verify all environment variables are set
- Ensure Gemini API key is valid

### Frontend build fails
- Check Node version: `node --version` (needs 18+)
- Clear cache: `rm -rf .next node_modules && npm install`
- Verify API URL is correct in `.env.local`

## 📖 Next Steps

- Read [Architecture Documentation](docs/architecture.md) to understand the system
- Check [API Documentation](docs/api.md) for integration details
- Review [Deployment Guide](docs/deployment.md) for advanced configurations
- Explore the code and customize agents for your use case

## 🆘 Getting Help

- Check [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines
- Review [docs/](docs/) for detailed documentation
- Open an issue on GitHub

## 🎯 Key Endpoints

- **Frontend**: `http://localhost:3000` (local) or Cloud Run URL
- **Backend API**: `http://localhost:8000` (local) or Cloud Run URL
- **API Docs**: `http://localhost:8000/docs` (FastAPI auto-generated)
- **Health Check**: `http://localhost:8000/health`

## 🌟 Features to Try

1. **Different Story Types**: Try all 4 story types
2. **Media Combinations**: Mix text, images, audio, video
3. **Style Variations**: Experiment with visual styles
4. **Length Options**: Compare short vs long stories
5. **Custom Palettes**: Define your color schemes
6. **Real-time Streaming**: Watch content generate live

## 📊 What's Happening Behind the Scenes

1. **Story Planning**: AI creates narrative structure
2. **Style Definition**: Visual guidelines established
3. **Parallel Generation**: Multiple agents work simultaneously
4. **Interleaved Streaming**: Content flows as it's created
5. **Real-time Display**: Frontend updates progressively

Enjoy creating amazing stories with Future Artist! 🎨🤖
