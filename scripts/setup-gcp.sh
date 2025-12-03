#!/bin/bash

# BCV API - GCP Setup Script
# This script sets up the entire infrastructure on Google Cloud Platform

set -e  # Exit on error

PROJECT_ID="${1:-tasa-bcv-api}"
REGION="us-central1"
DATASET="tasa_bcv"
TABLE="tasas"

echo "================================================"
echo "BCV API - GCP Setup"
echo "================================================"
echo "Project ID: $PROJECT_ID"
echo "Region: $REGION"
echo "================================================"

# Set project
echo "📋 Setting GCP project..."
gcloud config set project $PROJECT_ID

# Enable required APIs
echo "🔧 Enabling required APIs..."
gcloud services enable bigquery.googleapis.com \
  cloudfunctions.googleapis.com \
  run.googleapis.com \
  cloudscheduler.googleapis.com \
  cloudbuild.googleapis.com \
  --quiet

echo "✅ APIs enabled"

# Create BigQuery dataset
echo "📊 Creating BigQuery dataset..."
bq mk --dataset --location=US --description="BCV exchange rates" $PROJECT_ID:$DATASET 2>/dev/null || echo "Dataset already exists"

# Create BigQuery table
echo "📊 Creating BigQuery table..."
bq mk --table \
  --description="BCV exchange rates time series" \
  $PROJECT_ID:$DATASET.$TABLE \
  fecha:DATE,url:STRING,monto:FLOAT64,created_at:TIMESTAMP \
  2>/dev/null || echo "Table already exists"

echo "✅ BigQuery setup complete"

# Deploy Cloud Function (Scraper)
echo "☁️  Deploying Cloud Function (scraper)..."
gcloud functions deploy scrape_bcv_rate \
  --gen2 \
  --runtime=python311 \
  --region=$REGION \
  --source=./functions/scraper \
  --entry-point=scrape_bcv_rate \
  --trigger-http \
  --allow-unauthenticated \
  --set-env-vars GCP_PROJECT_ID=$PROJECT_ID,BIGQUERY_DATASET=$DATASET \
  --quiet

# Get function URL
FUNCTION_URL=$(gcloud functions describe scrape_bcv_rate --region=$REGION --gen2 --format="value(serviceConfig.uri)")
echo "✅ Cloud Function deployed: $FUNCTION_URL"

# Create Cloud Scheduler job
echo "⏰ Creating Cloud Scheduler job (daily at 9 AM UTC)..."
gcloud scheduler jobs delete bcv-daily-scraper --location=$REGION --quiet 2>/dev/null || true
gcloud scheduler jobs create http bcv-daily-scraper \
  --location=$REGION \
  --schedule="0 9 * * *" \
  --uri="$FUNCTION_URL" \
  --http-method=GET \
  --time-zone="UTC" \
  --description="Daily BCV exchange rate scraper" \
  --quiet

echo "✅ Cloud Scheduler job created"

# Deploy Cloud Run (API)
echo "🚀 Deploying Cloud Run (API)..."
gcloud run deploy tasa-bcv-api \
  --source=. \
  --platform=managed \
  --region=$REGION \
  --allow-unauthenticated \
  --set-env-vars GCP_PROJECT_ID=$PROJECT_ID,BIGQUERY_DATASET=$DATASET \
  --quiet

# Get Cloud Run URL
API_URL=$(gcloud run services describe tasa-bcv-api --region=$REGION --format="value(status.url)")

echo ""
echo "================================================"
echo "✅ DEPLOYMENT COMPLETE!"
echo "================================================"
echo "🌐 API URL: $API_URL"
echo "📖 Docs: $API_URL/docs"
echo "🔍 Health: $API_URL/health"
echo ""
echo "📊 BigQuery: https://console.cloud.google.com/bigquery?project=$PROJECT_ID"
echo "☁️  Functions: https://console.cloud.google.com/functions?project=$PROJECT_ID"
echo "⏰ Scheduler: https://console.cloud.google.com/cloudscheduler?project=$PROJECT_ID"
echo ""
echo "Test the API:"
echo "  curl $API_URL/api/tasa"
echo ""
echo "Manually trigger scraper:"
echo "  gcloud scheduler jobs run bcv-daily-scraper --location=$REGION"
echo "================================================"
