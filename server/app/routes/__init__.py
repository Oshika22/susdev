from flask import Flask
from flask_cors import CORS


def create_app():
    print("CREATE_APP EXECUTED")
    app = Flask(__name__)
    CORS(app)

    @app.route("/")
    def home():
        return "Urban Optima Backend Running"

    # Register Blueprints
    from .routes.waste import waste_bp
    from .routes.airmap import air_bp
    from .routes.trafficmap import trafficmap_bp

    app.register_blueprint(waste_bp)
    app.register_blueprint(air_bp)
    app.register_blueprint(trafficmap_bp)

    print(app.url_map)

    return app
