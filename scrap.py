# Version: 1.0a
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def scrapear_bcv():
    url = "https://www.bcv.org.ve/"
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, verify=False)

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
