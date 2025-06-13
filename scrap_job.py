from scrapper import scrapear_bcv
from app.db import inicializar_db, insertar_tasa
from datetime import datetime
import os

DB_PATH = "tasas.db"

if not os.path.exists(DB_PATH):
    print("[INFO] Creando base de datos...")
    inicializar_db()

if __name__ == "__main__":
    print(f"[INFO] Ejecutando scraping BCV {datetime.now()}")
    tasa = scrapear_bcv()
    if tasa:
        insertar_tasa(tasa["fecha"], tasa["url"], tasa["monto"])
        print(f"[OK] Tasa guardada: {tasa}")
    else:
        print("[ERROR] No se pudo obtener la tasa desde BCV.")
