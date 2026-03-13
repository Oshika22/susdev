from flask import Blueprint, request, jsonify

air_bp = Blueprint('airmap', __name__)

@air_bp.route("/api/air", methods=["POST"])
def get_air_data():

    data = request.get_json()
    city = data.get("city", "Jaipur")

    # ✅ 100% Guaranteed Demo Response
    return jsonify({
        "city": city,
        "aqi": 3,
        "aqi_text": "Moderate",
        "components": {"pm2_5": 42},
        "temperature": 29,
        "humidity": 65,
        "wind_speed": 4.2,
        "weather": "clear sky",
        "suggestion": "Moderate air quality. Reduce prolonged outdoor activity.",
        "lat": 26.9124,
        "lon": 75.7873,
        "map_html": ""
    })
