from flask import Flask
from flask_cors import CORS
from water.services.water_service import get_water_metrics

def create_app():
    app = Flask(__name__)
    CORS(app)

    # -------------------------
    # ROOT TEST ROUTE
    # -------------------------
    @app.route("/")
    def home():
        return "Urban Optima Backend Running"

    # -------------------------
    # WATER METRICS ROUTE
    # -------------------------
    @app.route("/api/water")
    def water_metrics():
        return get_water_metrics()

    # -------------------------
    # EXISTING BLUEPRINTS
    # -------------------------
    from .routes.geocode import geocode_bp
    app.register_blueprint(geocode_bp, url_prefix='/api/geocode')

    return app



