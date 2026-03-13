from flask import Blueprint, request, jsonify

# MUST match __init__.py import
air_forecast_bp = Blueprint("air_forecast", __name__)


@air_forecast_bp.route("/api/airForecast", methods=["GET"])
def air_forecast():
    city = request.args.get("city")

    if not city:
        return jsonify({"error": "City not provided"}), 400

    # Temporary simple response (to verify blueprint works)
    return jsonify([
        {"date_str": "Day 1", "exp_aqi": 85},
        {"date_str": "Day 2", "exp_aqi": 92},
        {"date_str": "Day 3", "exp_aqi": 110}
    ])

