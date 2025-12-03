import functions_framework
from datetime import datetime

# Import from local copies
from scrap import scrapear_bcv
from app.db import insertar_tasa

@functions_framework.http
def scrape_bcv_rate(request):
    """
    HTTP Cloud Function triggered by Cloud Scheduler
    Scrapes BCV website and stores rate in BigQuery
    """
    print(f"[CHECKPOINT 1] Function triggered at {datetime.now()}")
    
    try:
        print("[CHECKPOINT 2] Starting scraper...")
        tasa = scrapear_bcv()
        
        if not tasa:
            print("[CHECKPOINT 3] Scraper returned None - BCV scraping failed")
            return {
                "status": "error",
                "checkpoint": 3,
                "message": "Failed to scrape BCV website - check if site is accessible"
            }, 500
        
        print(f"[CHECKPOINT 4] Scraper succeeded! Data: {tasa}")
        
        print("[CHECKPOINT 5] Attempting to save to BigQuery...")
        insertar_tasa(tasa["fecha"], tasa["url"], tasa["monto"])
        
        print(f"[CHECKPOINT 6] BigQuery save successful!")
        return {
            "status": "success",
            "checkpoint": 6,
            "message": "Rate scraped and stored successfully",
            "data": tasa
        }, 200
            
    except Exception as e:
        error_msg = str(e)
        print(f"[CHECKPOINT ERROR] Exception: {error_msg}")
        return {
            "status": "error",
            "checkpoint": "exception",
            "message": error_msg,
            "error_type": type(e).__name__
        }, 500
