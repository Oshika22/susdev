from flask import Blueprint, request, jsonify
import folium
import openrouteservice
from geopy.geocoders import Nominatim
from app.config import WEATHER_API_KEY, ORS_API_KEY
import requests

# ✅ Blueprint name MUST match __init__.py import
trafficmap_bp = Blueprint('trafficmap', __name__)

# ORS client
client = openrouteservice.Client(key=ORS_API_KEY)


# ---------------------------------------------------
# MAP ROUTE (HTML MAP)
# ---------------------------------------------------
@trafficmap_bp.route('/map', methods=['GET'])
def show_map():

    from_location = request.args.get('from')
    to_location = request.args.get('to')

    if not from_location or not to_location:
        return "Missing locations", 400

    try:
        # Geocode using ORS
        from_coords = client.pelias_search(text=from_location)['features'][0]['geometry']['coordinates']
        to_coords = client.pelias_search(text=to_location)['features'][0]['geometry']['coordinates']

        coords = [from_coords, to_coords]

        route = client.directions(coordinates=coords, profile='driving-car', format='geojson')
        geometry = route['features'][0]['geometry']['coordinates']

        # Build map
        m = folium.Map(location=[from_coords[1], from_coords[0]], zoom_start=13)

        folium.Marker([from_coords[1], from_coords[0]], popup="From").add_to(m)
        folium.Marker([to_coords[1], to_coords[0]], popup="To").add_to(m)

        folium.PolyLine(
            locations=[(lat, lon) for lon, lat in geometry],
            color='blue'
        ).add_to(m)

        return m._repr_html_()

    except Exception as e:
        print("MAP ERROR:", e)
        return "Error generating map", 500


# ---------------------------------------------------
# TRAFFIC API (JSON RESPONSE)
# ---------------------------------------------------
@trafficmap_bp.route('/api/traffic', methods=['POST'])
def get_traffic_data():

    data = request.get_json()

    from_location = data.get('from')
    to_location = data.get('to')

    if not from_location or not to_location:
        return jsonify({'error': 'Missing from or to location'}), 400

    try:
        # Geocode using Nominatim
        geolocator = Nominatim(user_agent="urban_optima_traffic")

        start = geolocator.geocode(from_location)
        end = geolocator.geocode(to_location)

        if not start or not end:
            return jsonify({"error": "Invalid location(s)"}), 400

        coords = [
            (start.longitude, start.latitude),
            (end.longitude, end.latitude)
        ]

        # Get route from ORS
        route = client.directions(coords)
        summary = route['routes'][0]['summary']

        distance_km = summary['distance'] / 1000
        duration_min = summary['duration'] / 60

        # Fetch weather data
        weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={to_location}&appid={WEATHER_API_KEY}&units=metric"
        weather_data = requests.get(weather_url).json()

        temp = weather_data['main']['temp']
        humidity = weather_data['main']['humidity']
        description = weather_data['weather'][0]['description']

        # Simulated traffic logic
        speed = 20  # simulated
        free_flow = 40

        traffic_level = ((free_flow - speed) / free_flow) * 100
        congestion_level = free_flow / speed

        suggestion = "Traffic conditions are normal."

        if speed < 15:
            suggestion = "Heavy congestion detected. Consider alternate route."
        elif "rain" in description.lower():
            suggestion = "Rain expected. Drive carefully."
        elif humidity > 85:
            suggestion = "High humidity and possible fog. Be cautious."

        return jsonify({
            "distance": round(distance_km, 2),
            "eta": round(duration_min, 2),
            "delay_percent": round(traffic_level, 1),
            "speed": speed,
            "temperature": temp,
            "humidity": humidity,
            "weather": description,
            "suggestion": suggestion
        })

    except Exception as e:
        print("TRAFFIC API ERROR:", e)
        return jsonify({"error": "Traffic calculation failed"}), 500
