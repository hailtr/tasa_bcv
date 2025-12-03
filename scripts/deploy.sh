#!/bin/bash

# BCV API - Quick Deploy Script
# Updates existing deployments

set -e

PROJECT_ID="${1:-tasa-bcv-api}"
REGION="us-central1"

echo "🚀 Deploying updates to $PROJECT_ID..."

# Deploy API
echo "📦 Deploying API to Cloud Run..."
gcloud run deploy tasa-bcv-api \
  --source=. \
  --platform=managed \
  --region=$REGION \
  --project=$PROJECT_ID \
  --quiet

API_URL=$(gcloud run services describe tasa-bcv-api --region=$REGION --project=$PROJECT_ID --format="value(status.url)")

echo "✅ Deployment complete!"
echo "🌐 API URL: $API_URL"
echo "📖 Docs: $API_URL/docs"
