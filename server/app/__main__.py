from flask import Flask
from flask_cors import CORS
from app.routes.trafficmap import traffic_bp
from app.routes.airmap import air_bp
from app.routes.aqiForecast import airForecast_bp

def create_app():
    app = Flask(__name__)
    CORS(app) 
    app.register_blueprint(traffic_bp)
    app.register_blueprint(air_bp)
    app.register_blueprint(airForecast_bp)
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
