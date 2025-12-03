# 📈 BCV Exchange Rate API - Community Edition 🇻🇪

**Consulta actualizada y automática del tipo de cambio oficial en Venezuela.** <br>
Free, public API for Venezuelan Central Bank (BCV) official exchange rates.

[![Run on Google Cloud](https://deploy.cloud.run/button.svg)](https://deploy.cloud.run)

---

## 🌍 Public Community API

**Use it for free - no signup needed!**

```bash
# Get latest rate
curl https://tasa-bcv-api-XXXXXX.run.app/api/tasa

# Get rate for specific date
curl https://tasa-bcv-api-XXXXXX.run.app/api/tasa?fecha=2025-12-02

# Get range
curl https://tasa-bcv-api-XXXXXX.run.app/api/tasa/rango?desde=2025-12-01&hasta=2025-12-10
```

### 📊 Interactive Documentation
Visit `/docs` on any deployed instance for full Swagger UI documentation.

### ⚡ Rate Limits
- **Anonymous**: 100 requests/hour per IP
- **Shared pool**: 500K requests/month for the community
- **Cached responses**: Latest rate cached for 1 hour

---

## 🚀 Deploy Your Own (100% Free!)

**Need more requests? Deploy your own instance in 2 minutes:**

### Option 1: One-Click Deploy

[![Run on Google Cloud](https://deploy.cloud.run/button.svg)](https://deploy.cloud.run)

### Option 2: CLI Deploy

```bash
# Clone the repo
git clone https://github.com/yourname/tasa-bcv
cd tasa-bcv

# Run setup script
chmod +x scripts/setup-gcp.sh
./scripts/setup-gcp.sh YOUR_PROJECT_ID

# Done! 🎉
```

**Requirements:**
- Free GCP account ([create one here](https://cloud.google.com/free))
- `gcloud` CLI installed ([install guide](https://cloud.google.com/sdk/docs/install))

**Your free tier includes:**
- 2M API requests/month (Cloud Run)
- 10GB storage + 1TB queries/month (BigQuery)
- Daily automated scraping (Cloud Functions + Scheduler)

**Total cost: $0/month** 💰

---

## 📖 API Endpoints

### Latest Rate
```http
GET /api/tasa
```

**Response:**
```json
{
  "fecha": "2025-12-02",
  "url": "https://www.bcv.org.ve/",
  "monto": 45.67
}
```

---

### Rate by Date
```http
GET /api/tasa?fecha=YYYY-MM-DD
```

**Example:**
```bash
curl https://your-api.run.app/api/tasa?fecha=2025-06-10
```

---

### Date Range
```http
GET /api/tasa/rango?desde=YYYY-MM-DD&hasta=YYYY-MM-DD
```

**Example:**
```bash
curl "https://your-api.run.app/api/tasa/rango?desde=2025-06-01&hasta=2025-06-10"
```

**Response:**
```json
[
  {"fecha": "2025-06-01", "url": "...", "monto": 45.12},
  {"fecha": "2025-06-02", "url": "...", "monto": 45.34},
  ...
]
```

---

### Health Check
```http
GET /health
```

Check API and database status.

---

### Metrics
```http
GET /metrics
```

Get simple usage metrics.

---

## 🏗️ Architecture

**Stack:**
- **API**: FastAPI (Python 3.11) on Cloud Run
- **Database**: BigQuery (partitioned by date)
- **Scraper**: Cloud Functions (daily at 9 AM UTC)
- **Scheduler**: Cloud Scheduler
- **Rate Limiting**: SlowAPI (in-memory)
- **Caching**: In-memory (1 hour TTL for latest rate)

**Why BigQuery?**
- 10GB storage free (enough for decades of daily rates)
- 1TB queries/month free (millions of API calls)
- Serverless, zero maintenance
- Perfect for time-series data

**Why Cloud Run?**
- Scales to zero (pay nothing when idle)
- 2M requests/month free
- Auto-scales with traffic
- HTTPS included

---

## 🛠️ Local Development

```bash
# Clone repo
git clone https://github.com/yourname/tasa-bcv
cd tasa-bcv

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env with your GCP project ID

# Run locally
uvicorn app.main:app --reload

# Visit http://localhost:8000/docs
```

---

## 📝 Configuration

Create a `.env` file:

```env
GCP_PROJECT_ID=your-project-id
BIGQUERY_DATASET=tasa_bcv
```

For local development with Application Default Credentials:
```bash
gcloud auth application-default login
```

---

## 🤝 Community Guidelines

This is a **free community resource**. Please:

✅ Use responsibly  
✅ Respect rate limits  
✅ Deploy your own if you need more requests  
✅ Contribute improvements via PR  
✅ Report issues on GitHub  

❌ Don't abuse the service  
❌ Don't resell the raw data  
❌ Don't hammer the BCV website directly  

---

## 🔄 How It Works

1. **Cloud Scheduler** triggers Cloud Function daily at 9 AM UTC
2. **Cloud Function** scrapes BCV website
3. **BigQuery** stores the exchange rate
4. **Cloud Run API** serves cached/fresh data
5. **Rate limiter** ensures fair usage

---

## 📊 Monitoring

**GCP Console Links:**
- [BigQuery Console](https://console.cloud.google.com/bigquery)
- [Cloud Run Console](https://console.cloud.google.com/run)
- [Cloud Scheduler Console](https://console.cloud.google.com/cloudscheduler)
- [Cloud Functions Console](https://console.cloud.google.com/functions)
- [Cloud Logging](https://console.cloud.google.com/logs)

---

## 🚧 Maintenance

**Update deployment:**
```bash
./scripts/deploy.sh YOUR_PROJECT_ID
```

**Manually trigger scraper:**
```bash
gcloud scheduler jobs run bcv-daily-scraper --location=us-central1
```

**Check logs:**
```bash
gcloud run logs tail tasa-bcv-api
gcloud functions logs read scrape_bcv_rate
```

---

## 🙋 FAQ

**Q: Is this really free?**  
A: Yes! Stays within GCP free tier for moderate usage.

**Q: What if I exceed free tier?**  
A: Cloud Run charges $0.40 per million requests after 2M. Still super cheap!

**Q: Can I use this commercially?**  
A: Yes! It's public BCV data. Just be respectful.

**Q: How often is data updated?**  
A: Daily at 9 AM UTC (5 AM VET).

**Q: Can I change the scraping schedule?**  
A: Yes! Edit the cron expression in Cloud Scheduler.

---

## 📜 License

MIT License - See LICENSE file

Data source: [Banco Central de Venezuela](https://www.bcv.org.ve/)

---

## 👨‍💻 Author

Rafael Ortiz  
[GitHub](https://github.com/hailtr)

---

## 🌟 Contributing

PRs welcome! Please:
1. Fork the repo
2. Create a feature branch
3. Test your changes
4. Submit a PR

---

**Made with ❤️ for the Venezuelan community** 🇻🇪
