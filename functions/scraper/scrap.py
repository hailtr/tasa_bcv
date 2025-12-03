# Version: 1.0a
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def scrapear_bcv():
    url = "https://www.bcv.org.ve/"
    try:
        # More realistic browser headers to avoid anti-bot detection
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "es-VE,es;q=0.9,en;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1"
        }
        response = requests.get(url, headers=headers, verify=False, timeout=30)

        if response.status_code != 200:
            raise ConnectionError(f"BCV no respondió correctamente. Status: {response.status_code}")

        soup = BeautifulSoup(response.text, "html.parser")
        dolar_div = soup.find("div", id="dolar")

        if not dolar_div:
            raise ValueError("No se encontró el div con id 'dolar'.")

        valor_strong = dolar_div.find("strong")
        if not valor_strong:
            raise ValueError("No se encontró el valor del dólar dentro de 'strong'.")

        monto = float(valor_strong.text.strip().replace(",", "."))

        return {
            "fecha": datetime.now().strftime("%Y-%m-%d"),
            "url": url,
            "monto": round(monto, 4)
        }

    except Exception as e:
        print(f"[ERROR BCV] {e}")
        return None
