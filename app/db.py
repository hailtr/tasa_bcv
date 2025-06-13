import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "tasas.db"

def conectar():
    return sqlite3.connect(DB_PATH)

def inicializar_db():
    with conectar() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS tasas (
            fecha TEXT PRIMARY KEY,     -- 'YYYY-MM-DD'
            url TEXT NOT NULL,
            monto REAL NOT NULL)
                ''')
        conn.commit()

def insertar_tasa(fecha, url, monto):
    with conectar() as conn:
        conn.execute('''
            INSERT OR REPLACE INTO tasas (fecha, url, monto)
            VALUES (?, ?, ?)
        ''', (fecha, url, monto))
        conn.commit()

def obtener_tasa(fecha):
    with conectar() as conn:
        cur = conn.execute('SELECT fecha, url, monto FROM tasas WHERE fecha = ?', (fecha,))
        return cur.fetchone()

def obtener_ultima_tasa():
    with conectar() as conn:
        cur = conn.execute('SELECT fecha, url, monto FROM tasas ORDER BY fecha DESC LIMIT 1')
        fila = cur.fetchone()
        if fila:
            return {"fecha": fila[0], "url": fila[1], "monto": fila[2]}
        return None

def obtener_todas_las_tasas():
    with conectar() as conn:
        cur = conn.execute('SELECT fecha, url, monto FROM tasas ORDER BY fecha DESC')
        return cur.fetchall()

#funcion para ver todas las tasas
def ver_todas_las_tasas():
    tasas = obtener_todas_las_tasas()
    if tasas:
        for fecha, url, monto in tasas:
            print(f"{fecha} - {url} - {monto}")
    else:
        print("No hay tasas registradas.")

# ver_todas_las_tasas()

def obtener_tasas_en_rango(desde, hasta):
    with conectar() as conn:
        cur = conn.execute('''
            SELECT fecha, url, monto
            FROM tasas
            WHERE fecha BETWEEN ? AND ?
            ORDER BY fecha ASC
        ''', (desde, hasta))
        filas = cur.fetchall()
        return [
            {"fecha": fila[0], "url": fila[1], "monto": fila[2]}
            for fila in filas
        ]
