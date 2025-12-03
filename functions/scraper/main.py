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
    print(f"[INFO] Starting BCV scrape at {datetime.now()}")
    
    try:
        tasa = scrapear_bcv()
        
        if tasa:
            insertar_tasa(tasa["fecha"], tasa["url"], tasa["monto"])
            print(f"[OK] Tasa guardada exitosamente: {tasa}")
            
            return {
                "status": "success",
                "message": "Rate scraped and stored successfully",
                "data": tasa
            }, 200
        else:
            print("[ERROR] No se pudo obtener la tasa desde BCV")
            return {
                "status": "error",
                "message": "Failed to scrape BCV website"
            }, 500
            
    except Exception as e:
        print(f"[ERROR] Exception during scraping: {e}")
        return {
            "status": "error",
            "message": str(e)
        }, 500
