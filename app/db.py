import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
load_dotenv()


# Usa DATABASE_URL desde variable de entorno (Railway, GitHub, local)
DATABASE_URL = os.getenv("DATABASE_URL")

def conectar():
    return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)

def insertar_tasa(fecha, url, monto):
    with conectar() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                INSERT INTO tasas (fecha, url, monto)
                VALUES (%s, %s, %s)
                ON CONFLICT (fecha)
                DO UPDATE SET url = EXCLUDED.url, monto = EXCLUDED.monto;
            ''', (fecha, url, monto))
        conn.commit()

def mostrar_ultima():
    with conectar() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                SELECT fecha, url, monto
                FROM tasas
                ORDER BY fecha DESC
                LIMIT 1;
            ''')
            return cur.fetchone()

def mostrar_por_fecha(fecha):
    with conectar() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                SELECT fecha, url, monto
                FROM tasas
                WHERE fecha = %s;
            ''', (fecha,))
            return cur.fetchone()

def mostrar_rango(desde, hasta):
    with conectar() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                SELECT fecha, url, monto
                FROM tasas
                WHERE fecha BETWEEN %s AND %s
                ORDER BY fecha ASC;
            ''', (desde, hasta))
            return cur.fetchall()

def quien_soy():
    with conectar() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT current_user;")
            print("[DEBUG] Usuario actual:", cur.fetchone()['current_user'])
