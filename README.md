# 📈 BCV Exchange Rate API / API de tasas del BCV

Consulta actualizada y automática del tipo de cambio oficial en Venezuela publicado por el BCV. Esta API permite obtener la tasa más reciente o consultar tasas históricas a partir de una base de datos alimentada por un scrapper diario.

Automatically updated API to consult the official exchange rate in Venezuela, published by the BCV. It provides access to the latest rate or historical data, populated via a daily scraping job.

---

## Endpoints disponibles / Available Endpoints

### Última tasa / Latest Rate

```
GET /api/tasa
```

Retorna la tasa más reciente registrada.

Returns the most recent rate available.

---

### Tasa por fecha / Rate by Date

```
GET /api/tasa?fecha=YYYY-MM-DD
```

Ejemplo / Example:
```
GET /api/tasa?fecha=2025-06-10
```

---

### Rango de fechas / Date Range

```
GET /api/tasa?rango=YYYY-MM-DD_YYYY-MM-DD
```

Ejemplo / Example:
```
GET /api/tasa?rango?desde=2025-06-01&hasta=2025-06-10
```

---

##  Configuración del entorno / Environment Configuration

Define tu variable `DATABASE_URL` en un archivo `.env`:

```env
DATABASE_URL=postgresql://usuario:contraseña@host:puerto/tasa_bcv
```

You must define `DATABASE_URL` in your `.env` file or environment variables.

---

## Despliegue automático / Automated Deployment

La API puede desplegarse en [Railway](https://railway.app/) o cualquier servicio compatible con Gunicorn.  
El scrapper se ejecuta automáticamente mediante [GitHub Actions](https://github.com/features/actions) configurado con cron.

The API can be deployed via Railway or any Gunicorn-compatible host.  
The scrapper runs automatically using GitHub Actions + cron job.

---

## Requisitos / Requirements

- Python 3.11+
- PostgreSQL (Railway recomendado)
- Gunicorn
- Flask
- Requests
- python-dotenv
- psycopg2-binary

Instalación:

```bash
pip install -r requirements.txt
```

---

## Estructura del Proyecto / Project Structure

```
.
├── app/
│   ├── __init__.py
│   ├── routes.py
│   └── db.py
├── scrap_job.py          ← Scrapper que guarda en PostgreSQL
├── run.py                ← Lanza el servidor Flask
├── requirements.txt
├── .env                  ← Configuración local
├── .github/
│   └── workflows/
│       └── scrap_job.yml ← Cron para scraping diario
```

---

## Autor / Author

Rafael Ortiz  
[https://github.com/hailtr](https://github.com/hailtr)

---

## Licencia / License

MIT License
