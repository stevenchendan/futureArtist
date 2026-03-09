# Deployment Guide

## Prerequisites

Before deploying Future Artist, ensure you have:

1. **Google Cloud Account** with billing enabled
2. **Google Cloud SDK** (gcloud) installed
3. **Docker** installed (for local testing)
4. **Node.js 18+** and **Python 3.11+**
5. **Gemini API Key** from [Google AI Studio](https://aistudio.google.com/app/apikey)

## Initial Setup

### 1. Create Google Cloud Project

```bash
# Create a new project
gcloud projects create your-project-id --name="Future Artist"

# Set as active project
gcloud config set project your-project-id

# Enable billing (required)
# Do this via Cloud Console: https://console.cloud.google.com/billing
```

### 2. Run Setup Script

```bash
cd infrastructure/scripts
chmod +x setup-gcp.sh
./setup-gcp.sh your-project-id us-central1
```

This script will:
- Enable all required Google Cloud APIs
- Create service account with appropriate permissions
- Create Cloud Storage bucket for media
- Configure CORS settings

### 3. Store Gemini API Key

```bash
# Get API key from: https://aistudio.google.com/app/apikey
# Store in Secret Manager
echo -n 'YOUR_GEMINI_API_KEY' | gcloud secrets create gemini-api-key \
  --data-file=- \
  --replication-policy="automatic"
```

### 4. Download Service Account Key

```bash
# Create and download service account key
SA_EMAIL="futureartist-sa@your-project-id.iam.gserviceaccount.com"
gcloud iam service-accounts keys create service-account.json \
  --iam-account=$SA_EMAIL

# Move to backend directory
mv service-account.json backend/
```

## Local Development

### Backend

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your credentials

# Run locally
python -m app.adk.main
```

Backend will be available at `http://localhost:8000`

### Frontend

```bash
cd frontend

# Install dependencies
npm install

# Set up environment variables
cp .env.local.example .env.local
# Edit .env.local

# Run development server
npm run dev
```

Frontend will be available at `http://localhost:3000`

## Cloud Deployment

### Option 1: Automated Deployment (Recommended)

```bash
# Set environment variable
export GOOGLE_CLOUD_PROJECT=your-project-id

# Run deployment script
cd infrastructure/scripts
chmod +x deploy.sh
./deploy.sh
```

This will:
1. Enable required APIs
2. Create Cloud Storage bucket
3. Build and deploy backend to Cloud Run
4. Build and deploy frontend to Cloud Run
5. Configure environment variables
6. Output deployment URLs

### Option 2: Manual Deployment

#### Deploy Backend

```bash
cd backend

# Deploy to Cloud Run
gcloud run deploy futureartist-backend \
  --source . \
  --region us-central1 \
  --platform managed \
  --allow-unauthenticated \
  --set-env-vars="GOOGLE_CLOUD_PROJECT=your-project-id,GEMINI_API_KEY=$(gcloud secrets versions access latest --secret=gemini-api-key)"

# Get backend URL
BACKEND_URL=$(gcloud run services describe futureartist-backend \
  --region us-central1 \
  --format='value(status.url)')
echo "Backend URL: $BACKEND_URL"
```

#### Deploy Frontend

```bash
cd frontend

# Deploy to Cloud Run
gcloud run deploy futureartist-frontend \
  --source . \
  --region us-central1 \
  --platform managed \
  --allow-unauthenticated \
  --set-env-vars="NEXT_PUBLIC_API_URL=$BACKEND_URL"

# Get frontend URL
FRONTEND_URL=$(gcloud run services describe futureartist-frontend \
  --region us-central1 \
  --format='value(status.url)')
echo "Frontend URL: $FRONTEND_URL"
```

### Option 3: Using Cloud Build

#### Setup Cloud Build Triggers

```bash
# Connect your repository
gcloud beta builds triggers create github \
  --repo-name=futureArtist \
  --repo-owner=your-github-username \
  --branch-pattern="^main$" \
  --build-config=backend/cloudbuild.yaml

gcloud beta builds triggers create github \
  --repo-name=futureArtist \
  --repo-owner=your-github-username \
  --branch-pattern="^main$" \
  --build-config=frontend/cloudbuild.yaml
```

Now deployments happen automatically on push to main branch.

## Environment Configuration

### Backend Environment Variables

```bash
# Set via Cloud Run
gcloud run services update futureartist-backend \
  --region us-central1 \
  --set-env-vars="
GOOGLE_CLOUD_PROJECT=your-project-id,
GEMINI_API_KEY=$(gcloud secrets versions access latest --secret=gemini-api-key),
CLOUD_STORAGE_BUCKET=your-project-id-futureartist-media,
LOG_LEVEL=INFO
"
```

### Frontend Environment Variables

```bash
# Set via Cloud Run
gcloud run services update futureartist-frontend \
  --region us-central1 \
  --set-env-vars="
NEXT_PUBLIC_API_URL=https://futureartist-backend-xxxxx.run.app,
NEXT_PUBLIC_WS_URL=wss://futureartist-backend-xxxxx.run.app
"
```

## Verification

### Test Deployment

```bash
# Test backend health
curl https://your-backend-url.run.app/health

# Expected response:
# {"status":"healthy","services":{"gemini":"connected","storage":"connected"}}

# Test frontend
curl https://your-frontend-url.run.app
# Should return HTML
```

### Generate a Test Story

1. Open frontend URL in browser
2. Enter a story prompt: "A robot learning to paint"
3. Select story type: "Interactive Storybook"
4. Click "Generate Story"
5. Watch interleaved content stream in real-time

## Monitoring

### View Logs

```bash
# Backend logs
gcloud run services logs read futureartist-backend \
  --region us-central1 \
  --limit 50

# Frontend logs
gcloud run services logs read futureartist-frontend \
  --region us-central1 \
  --limit 50
```

### Cloud Console

Visit Cloud Console for detailed monitoring:
- **Cloud Run**: https://console.cloud.google.com/run
- **Cloud Storage**: https://console.cloud.google.com/storage
- **Logs**: https://console.cloud.google.com/logs

## Troubleshooting

### Common Issues

#### 1. "Permission denied" errors

```bash
# Ensure service account has required permissions
gcloud projects add-iam-policy-binding your-project-id \
  --member="serviceAccount:futureartist-sa@your-project-id.iam.gserviceaccount.com" \
  --role="roles/aiplatform.user"
```

#### 2. "API not enabled" errors

```bash
# Enable all required APIs
gcloud services enable \
  run.googleapis.com \
  cloudbuild.googleapis.com \
  aiplatform.googleapis.com \
  generativelanguage.googleapis.com
```

#### 3. WebSocket connection failures

- Ensure Cloud Run allows WebSocket connections
- Check CORS configuration
- Verify WS_URL uses `wss://` not `ws://`

#### 4. Out of memory errors

```bash
# Increase Cloud Run memory
gcloud run services update futureartist-backend \
  --region us-central1 \
  --memory 2Gi
```

## Updating Deployment

### Update Backend

```bash
cd backend
gcloud run deploy futureartist-backend \
  --source . \
  --region us-central1
```

### Update Frontend

```bash
cd frontend
gcloud run deploy futureartist-frontend \
  --source . \
  --region us-central1
```

## Cost Optimization

### Cloud Run
- Use minimum instances: 0
- Set max instances based on expected load
- Use CPU throttling when idle

```bash
gcloud run services update futureartist-backend \
  --region us-central1 \
  --min-instances 0 \
  --max-instances 10 \
  --cpu-throttling
```

### Cloud Storage
- Set lifecycle rules to delete old files
- Use Standard storage class

```bash
# Create lifecycle rule
cat > lifecycle.json << EOF
{
  "lifecycle": {
    "rule": [
      {
        "action": {"type": "Delete"},
        "condition": {"age": 7}
      }
    ]
  }
}
EOF

gsutil lifecycle set lifecycle.json gs://your-bucket-name
```

## Security Best Practices

1. **Never commit credentials**: Use Secret Manager
2. **Enable authentication**: For production use
3. **Use HTTPS only**: Cloud Run provides this by default
4. **Regular updates**: Keep dependencies updated
5. **Monitor access logs**: Review Cloud Run logs regularly

## Next Steps

After deployment:

1. **Custom Domain**: Configure custom domain for frontend
2. **CDN**: Enable Cloud CDN for better performance
3. **Monitoring**: Set up Cloud Monitoring alerts
4. **Backup**: Configure backup strategies for critical data
5. **CI/CD**: Set up automated testing and deployment
