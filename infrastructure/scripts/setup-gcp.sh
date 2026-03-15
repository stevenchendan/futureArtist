#!/bin/bash

# Future Artist - Google Cloud Project Setup
# This script sets up all required Google Cloud resources

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}🔧 Future Artist - GCP Setup${NC}"

# Check if PROJECT_ID is set
if [ -z "$1" ]; then
    echo -e "${RED}Error: Please provide a project ID${NC}"
    echo "Usage: ./setup-gcp.sh YOUR_PROJECT_ID"
    exit 1
fi

PROJECT_ID=$1
REGION=${2:-us-central1}

echo -e "${YELLOW}Project ID: $PROJECT_ID${NC}"
echo -e "${YELLOW}Region: $REGION${NC}"

# Set the project
echo -e "\n${GREEN}Setting active project...${NC}"
gcloud config set project $PROJECT_ID

# Enable required APIs
echo -e "\n${GREEN}Enabling Google Cloud APIs...${NC}"
gcloud services enable \
    run.googleapis.com \
    cloudbuild.googleapis.com \
    artifactregistry.googleapis.com \
    aiplatform.googleapis.com \
    generativelanguage.googleapis.com \
    storage.googleapis.com \
    secretmanager.googleapis.com \
    cloudresourcemanager.googleapis.com

# Create service account
echo -e "\n${GREEN}Creating service account...${NC}"
SA_NAME="futureartist-sa"
SA_EMAIL="${SA_NAME}@${PROJECT_ID}.iam.gserviceaccount.com"

gcloud iam service-accounts create $SA_NAME \
    --display-name="Future Artist Service Account" \
    --description="Service account for Future Artist application" \
    || echo "Service account already exists"

# Grant necessary roles
echo -e "\n${GREEN}Granting IAM roles...${NC}"
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$SA_EMAIL" \
    --role="roles/aiplatform.user"

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$SA_EMAIL" \
    --role="roles/storage.admin"

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$SA_EMAIL" \
    --role="roles/secretmanager.secretAccessor"

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$SA_EMAIL" \
    --role="roles/cloudbuild.serviceAgent"

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$SA_EMAIL" \
    --role="roles/serviceusage.serviceUsageConsumer"

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$SA_EMAIL" \
    --role="roles/artifactregistry.writer"

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$SA_EMAIL" \
    --role="roles/run.admin"

PROJECT_NUMBER=$(gcloud projects describe $(gcloud config get-value project) --format="value(projectNumber)")
gcloud iam service-accounts add-iam-policy-binding \
    $PROJECT_NUMBER-compute@developer.gserviceaccount.com \
    --member="serviceAccount:$SA_EMAIL" \
    --role="roles/iam.serviceAccountUser"

# Create storage bucket
echo -e "\n${GREEN}Creating Cloud Storage bucket...${NC}"
BUCKET_NAME="${PROJECT_ID}-futureartist-media"
gsutil mb -p $PROJECT_ID -l $REGION gs://$BUCKET_NAME/ || echo "Bucket already exists"

# Set CORS on bucket
echo -e "\n${GREEN}Configuring CORS...${NC}"
cat > /tmp/cors.json << EOF
[
  {
    "origin": ["*"],
    "method": ["GET", "HEAD", "PUT", "POST"],
    "responseHeader": ["Content-Type"],
    "maxAgeSeconds": 3600
  }
]
EOF
gsutil cors set /tmp/cors.json gs://$BUCKET_NAME/

# Create Gemini API key secret (if not exists)
echo -e "\n${GREEN}Setup complete!${NC}"
echo -e "\n${YELLOW}Next steps:${NC}"
echo -e "1. Get your Gemini API key from: https://aistudio.google.com/app/apikey"
echo -e "2. Store it in Secret Manager:"
echo -e "   ${GREEN}echo -n 'YOUR_API_KEY' | gcloud secrets create gemini-api-key --data-file=-${NC}"
echo -e "3. Download service account key:"
echo -e "   ${GREEN}gcloud iam service-accounts keys create service-account.json --iam-account=$SA_EMAIL${NC}"
echo -e "4. Run deployment script:"
echo -e "   ${GREEN}./deploy.sh${NC}"
