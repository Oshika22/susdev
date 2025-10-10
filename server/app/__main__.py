from flask import Flask
from flask_cors import CORS
from app.routes.trafficmap import traffic_bp
from app.routes.airmap import air_bp
from app.routes.aqiForecast import airForecast_bp
from app.routes.energy import energy_bp
from app.routes.overall import overall_bp
from app.routes.chatBotroute import chatbot_bp

def create_app():
    app = Flask(__name__)
    CORS(app) 
    app.register_blueprint(traffic_bp)
    app.register_blueprint(air_bp)
    app.register_blueprint(airForecast_bp)
    app.register_blueprint(energy_bp)
    app.register_blueprint(overall_bp)
    app.register_blueprint(chatbot_bp)
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
