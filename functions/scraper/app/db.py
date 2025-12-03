import os
from google.cloud import bigquery
from google.api_core import retry
from dotenv import load_dotenv
import time
from datetime import datetime, date

load_dotenv()

# Configuration
PROJECT_ID = os.getenv("GCP_PROJECT_ID", "tasa-bcv-api")
DATASET_ID = os.getenv("BIGQUERY_DATASET", "tasa_bcv")
TABLE_ID = "tasas"
FULL_TABLE_ID = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"

# Create BigQuery client
client = bigquery.Client(project=PROJECT_ID)

def insertar_tasa(fecha, url, monto):
    """Insert or update a rate for a specific date"""
    try:
        # BigQuery uses MERGE (upsert) pattern
        query = f"""
        MERGE `{FULL_TABLE_ID}` T
        USING (SELECT @fecha as fecha, @url as url, @monto as monto) S
        ON T.fecha = S.fecha
        WHEN MATCHED THEN
            UPDATE SET url = S.url, monto = S.monto
        WHEN NOT MATCHED THEN
            INSERT (fecha, url, monto) VALUES (S.fecha, S.url, S.monto)
        """
        
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("fecha", "DATE", fecha),
                bigquery.ScalarQueryParameter("url", "STRING", url),
                bigquery.ScalarQueryParameter("monto", "FLOAT64", float(monto)),
            ]
        )
        
        query_job = client.query(query, job_config=job_config)
        query_job.result()  # Wait for completion
        print(f"[OK] Tasa insertada/actualizada: {fecha} = {monto}")
        
    except Exception as e:
        print(f"[ERROR] Error al insertar tasa: {e}")
        raise

def mostrar_ultima():
    """Get the most recent exchange rate"""
    try:
        query = f"""
        SELECT fecha, url, monto
        FROM `{FULL_TABLE_ID}`
        ORDER BY fecha DESC
        LIMIT 1
        """
        
        query_job = client.query(query)
        results = list(query_job.result())
        
        if results:
            row = results[0]
            return {
                "fecha": row.fecha.isoformat() if isinstance(row.fecha, date) else row.fecha,
                "url": row.url,
                "monto": float(row.monto)
            }
        return None
        
    except Exception as e:
        print(f"[ERROR] Error al consultar última tasa: {e}")
        return None

def mostrar_por_fecha(fecha):
    """Get exchange rate for a specific date"""
    try:
        query = f"""
        SELECT fecha, url, monto
        FROM `{FULL_TABLE_ID}`
        WHERE fecha = @fecha
        """
        
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("fecha", "DATE", fecha),
            ]
        )
        
        query_job = client.query(query, job_config=job_config)
        results = list(query_job.result())
        
        if results:
            row = results[0]
            return {
                "fecha": row.fecha.isoformat() if isinstance(row.fecha, date) else row.fecha,
                "url": row.url,
                "monto": float(row.monto)
            }
        return None
        
    except Exception as e:
        print(f"[ERROR] Error al consultar tasa por fecha: {e}")
        return None

def mostrar_rango(desde, hasta):
    """Get exchange rates for a date range"""
    try:
        query = f"""
        SELECT fecha, url, monto
        FROM `{FULL_TABLE_ID}`
        WHERE fecha BETWEEN @desde AND @hasta
        ORDER BY fecha ASC
        """
        
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("desde", "DATE", desde),
                bigquery.ScalarQueryParameter("hasta", "DATE", hasta),
            ]
        )
        
        query_job = client.query(query, job_config=job_config)
        results = query_job.result()
        
        return [
            {
                "fecha": row.fecha.isoformat() if isinstance(row.fecha, date) else row.fecha,
                "url": row.url,
                "monto": float(row.monto)
            }
            for row in results
        ]
        
    except Exception as e:
        print(f"[ERROR] Error al consultar rango de tasas: {e}")
        return []

def health_check():
    """Check BigQuery connection health"""
    try:
        query = f"SELECT COUNT(*) as count FROM `{FULL_TABLE_ID}`"
        query_job = client.query(query)
        result = list(query_job.result())[0]
        return {"status": "healthy", "records": result.count}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}
