from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)  # allow React to call Flask APIs

    from .routes.geocode import geocode_bp
    app.register_blueprint(geocode_bp, url_prefix='/api/geocode')

    # future blueprints: AQI, traffic, city, etc.
    return app
