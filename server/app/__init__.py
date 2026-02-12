from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Root test route
    @app.route("/")
    def home():
        return "Urban Optima Backend Running"

    # Register Blueprints
    from .routes.waste import waste_bp
    app.register_blueprint(waste_bp)

    return app
