from water.services.water_service import get_water_metrics
from water.services.waste_service import get_waste_report
from flask import Flask
from flask_cors import CORS
from app.routes.trafficmap import traffic_bp
from app.routes.airmap import air_bp
from app.routes.aqiForecast import airForecast_bp
from app.routes.energy import energy_bp
from app.routes.overall import overall_bp
from app.routes.chatBotroute import chatbot_bp
from water.services.water_service import get_water_metrics

def create_app():
    app = Flask(__name__)
    CORS(app)

    # ----------------------
    # ROOT ROUTE
    # ----------------------
    @app.route("/")
    def home():
        return "Urban Optima Backend Running"

    # ----------------------
    # WATER QUALITY API
    # ----------------------
    @app.route("/api/water")
    def water():
        return get_water_metrics()

    # ----------------------
    # WASTE API
    # ----------------------
    @app.route("/api/waste")
    def waste():
        return get_waste_report()

    # ----------------------
    # EXISTING BLUEPRINTS
    # ----------------------
    app.register_blueprint(traffic_bp)
    app.register_blueprint(air_bp)
    app.register_blueprint(airForecast_bp)
    app.register_blueprint(energy_bp)
    app.register_blueprint(overall_bp)
    app.register_blueprint(chatbot_bp)

    print(app.url_map)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
