from flask import Blueprint, request, jsonify
from app.db import mostrar_ultima as obtener_ultima_tasa, mostrar_por_fecha as obtener_tasa_por_fecha, mostrar_rango as obtener_tasas_en_rango
from datetime import datetime

bp = Blueprint("routes", __name__)

def serializar_tasa(tasa):
    return {
        "fecha": tasa["fecha"].strftime("%Y-%m-%d") if hasattr(tasa["fecha"], "strftime") else tasa["fecha"],
        "url": tasa["url"],
        "monto": tasa["monto"]
    }

@bp.route("/api/tasa", methods=["GET"])
def obtener_tasa():
    fecha = request.args.get("fecha")

    if not fecha:
        tasa = obtener_ultima_tasa()
    else:
        tasa = obtener_tasa_por_fecha(fecha)

    if tasa is None:
        return jsonify({"error": f"No hay tasa registrada para {fecha or 'hoy'}"}), 404

    return jsonify(serializar_tasa(tasa))

@bp.route("/api/tasa/rango", methods=["GET"])
def obtener_rango():
    desde = request.args.get("desde")
    hasta = request.args.get("hasta")

    if not desde or not hasta:
        return jsonify({"error": "Debes especificar los parametros 'desde' y 'hasta' en la url, por ejemplo: /api/tasa/rango?desde=YYYY-MM-DD&hasta=YYYY-MM-DD"}), 400

    try:
        datetime.strptime(desde, "%Y-%m-%d")
        datetime.strptime(hasta, "%Y-%m-%d")
    except ValueError:
        return jsonify({"error": "Formato de fecha inválido (usa YYYY-MM-DD)"}), 400

    tasas = obtener_tasas_en_rango(desde, hasta)

    for t in tasas:
        if hasattr(t['fecha'], "strftime"):
            t['fecha'] = t['fecha'].strftime("%Y-%m-%d")

    return jsonify(tasas)