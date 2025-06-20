from scrap import scrapear_bcv
from app.db import insertar_tasa, mostrar_ultima as ultima_tasa
from datetime import datetime
from app import app

def registrar_desde_bcv():
    print(f"[INFO] Ejecutando scraping BCV {datetime.now()}")
    tasa = scrapear_bcv()
    if tasa:
        insertar_tasa(tasa["fecha"], tasa["url"], tasa["monto"])
        print(f"[OK] Tasa guardada: {tasa}")
    else:
        print("[ERROR] No se pudo obtener la tasa desde BCV.")

def mostrar_ultima():
    tasa = ultima_tasa()
    if tasa:
        print(f"[CONSULTA] Última tasa registrada: {tasa}")
    else:
        print("[INFO] No hay tasas registradas.")

if __name__ == "__main__": 
    app.run(debug=True)
