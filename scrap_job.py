from scrap import scrapear_bcv
from app.db import insertar_tasa
import os
from dotenv import load_dotenv

load_dotenv()

def scrapear_y_guardar():
    print("[INFO] Ejecutando scraping BCV...")
    try:
        tasa = scrapear_bcv()
        if tasa:
            insertar_tasa(tasa['fecha'], tasa['url'], tasa['monto'])
            print(f"[✅] Tasa registrada: {tasa['fecha']} = {tasa['monto']}")
        else:
            print("[⚠️] No se obtuvo tasa del BCV")
    except Exception as e:
        print(f"[❌] Error en scraping BCV: {e}")

if __name__ == "__main__":
    scrapear_y_guardar()
