from flask import Flask
from app.routes import bp
import os

print("[DEBUG] Cargando __init__.py")
print("[DEBUG] DATABASE_URL:", os.getenv("DATABASE_URL"))

app = Flask(__name__)
app.register_blueprint(bp)
