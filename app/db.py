import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
load_dotenv()
import time

# Usa DATABASE_URL desde variable de entorno (Railway, GitHub, local)
DATABASE_URL = os.getenv("DATABASE_URL")

def conectar(max_reintentos=5, espera_inicial=1):
    intento = 0
    while intento < max_reintentos:
        try:
            conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
            return conn
        except psycopg2.OperationalError as e:
            intento += 1
            espera = espera_inicial * (2 ** (intento - 1))  # Exponencial
            print(f"[ERROR] Fallo al conectar (intento {intento}/{max_reintentos}): {e}")
            if intento < max_reintentos:
                print(f"[INFO] Reintentando en {espera:.1f} segundos...")
                time.sleep(espera)
            else:
                raise Exception("No se pudo conectar a la base de datos después de varios intentos") from e


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
