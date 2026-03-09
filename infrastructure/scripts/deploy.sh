#!/bin/bash

# Future Artist Deployment Script
# Deploys backend and frontend to Google Cloud Run

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 Future Artist Deployment Script${NC}"

# Check if PROJECT_ID is set
if [ -z "$GOOGLE_CLOUD_PROJECT" ]; then
    echo -e "${RED}Error: GOOGLE_CLOUD_PROJECT environment variable not set${NC}"
    echo "Please set it with: export GOOGLE_CLOUD_PROJECT=your-project-id"
    exit 1
fi

PROJECT_ID=$GOOGLE_CLOUD_PROJECT
REGION=${GCP_REGION:-us-central1}

echo -e "${YELLOW}Project ID: $PROJECT_ID${NC}"
echo -e "${YELLOW}Region: $REGION${NC}"

# Enable required APIs
echo -e "\n${GREEN}Enabling required Google Cloud APIs...${NC}"
gcloud services enable \
    run.googleapis.com \
    cloudbuild.googleapis.com \
    artifactregistry.googleapis.com \
    aiplatform.googleapis.com \
    storage.googleapis.com \
    secretmanager.googleapis.com \
    --project=$PROJECT_ID

# Create storage bucket for media
BUCKET_NAME="${PROJECT_ID}-futureartist-media"
echo -e "\n${GREEN}Creating storage bucket: $BUCKET_NAME${NC}"
gsutil mb -p $PROJECT_ID -l $REGION gs://$BUCKET_NAME/ || echo "Bucket already exists"

# Deploy Backend
echo -e "\n${GREEN}Deploying backend...${NC}"
cd backend
gcloud run deploy futureartist-backend \
    --source . \
    --region=$REGION \
    --platform=managed \
    --allow-unauthenticated \
    --set-env-vars="GOOGLE_CLOUD_PROJECT=$PROJECT_ID,CLOUD_STORAGE_BUCKET=$BUCKET_NAME" \
    --project=$PROJECT_ID

BACKEND_URL=$(gcloud run services describe futureartist-backend --region=$REGION --format='value(status.url)' --project=$PROJECT_ID)
echo -e "${GREEN}✓ Backend deployed: $BACKEND_URL${NC}"

# Deploy Frontend
echo -e "\n${GREEN}Deploying frontend...${NC}"
cd ../frontend
gcloud run deploy futureartist-frontend \
    --source . \
    --region=$REGION \
    --platform=managed \
    --allow-unauthenticated \
    --set-env-vars="NEXT_PUBLIC_API_URL=$BACKEND_URL" \
    --project=$PROJECT_ID

FRONTEND_URL=$(gcloud run services describe futureartist-frontend --region=$REGION --format='value(status.url)' --project=$PROJECT_ID)
echo -e "${GREEN}✓ Frontend deployed: $FRONTEND_URL${NC}"

# Summary
echo -e "\n${GREEN}========================================${NC}"
echo -e "${GREEN}Deployment Complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo -e "Backend URL:  ${YELLOW}$BACKEND_URL${NC}"
echo -e "Frontend URL: ${YELLOW}$FRONTEND_URL${NC}"
echo -e "${GREEN}========================================${NC}"
