from datetime import datetime, timedelta
from historico import construir_urls_elcaribe
from app.db import obtener_tasa as obtener_tasa_por_fecha, insertar_tasa
import os
import requests
from bs4 import BeautifulSoup

def verificar_cobertura(desde: str, hasta: str):

    f_ini = datetime.strptime(desde, "%Y-%m-%d")
    f_fin = datetime.strptime(hasta, "%Y-%m-%d")

    faltantes = []

    actual = f_ini
    while actual <= f_fin:
        fecha_str = actual.strftime("%Y-%m-%d")

        tasa = obtener_tasa_por_fecha(fecha_str)
        if not tasa:
            print(f"[❌] {fecha_str} falta")
            faltantes.append(fecha_str)
        else:
            print(f"[✔] {fecha_str} presente")

        actual += timedelta(days=1)

    print(f"\nTotal faltantes: {len(faltantes)}")
    return faltantes

    #guardar faltantes en un .txt

def guardar_faltantes(faltantes, filename="faltantes.txt"):
    with open(filename, "w") as file:
        for fecha in faltantes:
            file.write(f"{fecha}\n")
    print(f"[✔] Faltantes guardados en {filename}")

guardar_faltantes(verificar_cobertura("2025-01-01", "2025-06-12"))


tasa = {
            "fecha": "2025-06-07",
            "url": "",
            "monto": "99.0900"
        }

# insertar_tasa(tasa["fecha"], tasa["url"], tasa["monto"])
