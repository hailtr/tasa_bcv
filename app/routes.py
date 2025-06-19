from flask import Blueprint, request, jsonify
from app.db import obtener_ultima_tasa, obtener_tasa as obtener_tasa_por_fecha, obtener_tasas_en_rango
from datetime import datetime

bp = Blueprint("routes", __name__)

@bp.route("/api/tasa", methods=["GET"])
def obtener_tasa():
    fecha = request.args.get("fecha")

    if not fecha:
        tasa = obtener_ultima_tasa()
        if tasa:
            return jsonify(tasa)
        return jsonify({"error": "No hay tasa registrada"}), 404

    tasa = obtener_tasa_por_fecha(fecha)

    if tasa is None:
        return jsonify({"error": f"No hay tasa registrada para {fecha}"}), 404
    else: 
        return jsonify({
            "fecha": tasa[0],
            "url": tasa[1],
            "monto": tasa[2]
        })

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
    return jsonify(tasas)