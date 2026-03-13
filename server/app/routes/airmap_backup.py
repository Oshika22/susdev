from flask import Blueprint, request, jsonify
import requests
import folium
from geopy.geocoders import Nominatim
from app.config import WEATHER_API_KEY

# ✅ Blueprint name MUST match import in __init__.py
air_bp = Blueprint('airmap', __name__)


# -----------------------------
# Helper: Get Coordinates
# -----------------------------
def get_coordinates(city_name):
    geolocator = Nominatim(user_agent="urban_optima_air")
    location = geolocator.geocode(f"{city_name}, India", exactly_one=True)

    if not location:
        raise Exception("City not found")

    return location.latitude, location.longitude


# -----------------------------
# Helper: AQI Color
# -----------------------------
def get_aqi_color(aqi):
    return {
        1: "green",
        2: "yellow",
        3: "orange",
        4: "red",
        5: "purple"
    }.get(aqi, "gray")


# -----------------------------
# MAIN AIR API
# -----------------------------
@air_bp.route("/api/air", methods=["POST"])
def get_air_data():

    data = request.get_json()
    city = data.get("city")

    if not city:
        return jsonify({"error": "City not provided"}), 400

    try:
        # Get coordinates
        lat, lon = get_coordinates(city)

        # API URLs
        aqi_url = f"https://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={WEATHER_API_KEY}"
        weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={WEATHER_API_KEY}&units=metric"

        # Fetch data
        aqi_res = requests.get(aqi_url).json()
        weather_res = requests.get(weather_url).json()

        # Extract data
        aqi = aqi_res["list"][0]["main"]["aqi"]
        components = aqi_res["list"][0]["components"]

        temperature = weather_res["main"]["temp"]
        humidity = weather_res["main"]["humidity"]
        wind_speed = weather_res["wind"]["speed"]
        weather_desc = weather_res["weather"][0]["description"]

        # AQI Text
        aqi_levels = {
            1: "Good",
            2: "Fair",
            3: "Moderate",
            4: "Poor",
            5: "Very Poor"
        }

        # Health Suggestion
        if aqi == 1:
            suggestion = "Air quality is excellent. Safe for all."
        elif aqi == 2:
            suggestion = "Air quality is fair. Sensitive groups should take care."
        elif aqi == 3:
            suggestion = "Moderate air quality. Reduce prolonged outdoor activity."
        else:
            suggestion = "Air quality is unhealthy. Limit outdoor exposure."

        # Create Map
        popup_text = f"""
        <b>📍 {city}</b><br>
        <b>AQI:</b> {aqi}<br>
        <b>PM2.5:</b> {components['pm2_5']} µg/m³<br>
        <b>Weather:</b> {weather_desc}<br>
        <b>Temp:</b> {temperature} °C<br>
        <b>Humidity:</b> {humidity}%<br>
        <b>Wind:</b> {wind_speed} m/s
        """

        m = folium.Map(location=[lat, lon], zoom_start=11)

        folium.Circle(
            location=[lat, lon],
            radius=10000,
            color=get_aqi_color(aqi),
            fill=True,
            fill_color=get_aqi_color(aqi),
            popup=folium.Popup(popup_text, max_width=300)
        ).add_to(m)

        map_html = m._repr_html_()

        # Return response
        return jsonify({
            "city": city,
            "aqi": aqi,
            "aqi_text": aqi_levels.get(aqi),
            "components": components,
            "temperature": temperature,
            "humidity": humidity,
            "wind_speed": wind_speed,
            "weather": weather_desc,
            "suggestion": suggestion,
            "lat": lat,
            "lon": lon,
            "map_html": map_html
        })

    except Exception as e:
        print("AIR API ERROR:", e)
        return jsonify({"error": "Failed to fetch air data"}), 500
