from flask import Blueprint, request, jsonify
import folium
import openrouteservice
from openrouteservice import convert
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from config import WEATHER_API_KEY
from config import ORS_API_KEY
import requests


traffic_bp = Blueprint('traffic', __name__)

client = openrouteservice.Client(key=ORS_API_KEY)
@traffic_bp.route('/map', methods=['GET'])
def show_map():
    from_location = request.args.get('from')
    to_location = request.args.get('to')
    print(from_location, to_location)

    if not from_location or not to_location:
        return "Missing coordinates", 400

    client = openrouteservice.Client(key=ORS_API_KEY)

    # 🔄 Geocode using ORS
    from_coords = client.pelias_search(text=from_location)['features'][0]['geometry']['coordinates']  # [lon, lat]
    to_coords = client.pelias_search(text=to_location)['features'][0]['geometry']['coordinates']

    print(from_coords, to_coords)

    if not from_coords or not to_coords:
        return "Invalid locations", 400

    # ✅ Build route
    coords = [from_coords, to_coords]  # [ [lon, lat], [lon, lat] ]
    route = client.directions(coordinates=coords, profile='driving-car', format='geojson')
    geometry = route['features'][0]['geometry']['coordinates']

    # 🗺️ Build Map
    m = folium.Map(location=[from_coords[1], from_coords[0]], zoom_start=13)
    folium.Marker(location=[from_coords[1], from_coords[0]], popup='From').add_to(m)
    folium.Marker(location=[to_coords[1], to_coords[0]], popup='To').add_to(m)
    folium.PolyLine(locations=[(lat, lon) for lon, lat in geometry], color='blue').add_to(m)

    return m._repr_html_()




@traffic_bp.route('/api/traffic', methods=['POST'])
def get_traffic_data():
    data = request.get_json()
    from_location = data.get('from')
    to_location = data.get('to')
    if not from_location or not to_location:
        return jsonify({'error': 'Missing from or to location'}), 400
    geolocator = Nominatim(user_agent="traffic_map")
    start = geolocator.geocode(from_location)
    end = geolocator.geocode(to_location)

    if not start or not end:
        return jsonify({"error": "Invalid location(s)"}), 400

    start_latlon = (start.latitude, start.longitude)
    end_latlon = (end.latitude, end.longitude)

    client = openrouteservice.Client(key=ORS_API_KEY)
    coords = [(start.longitude, start.latitude), (end.longitude, end.latitude)]
    route = client.directions(coords)
    summary = route['routes'][0]['summary']

    distance_km = summary['distance'] / 1000
    duration_min = summary['duration'] / 60

    try:
        weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={to_location}&appid={WEATHER_API_KEY}&units=metric"
        weather_data = requests.get(weather_url).json()
        weather_data = {}
        temp = weather_data['main']['temp']
        humidity = weather_data['main']['humidity']
        description = weather_data['weather'][0]['description']
    except:
        temp = humidity = 0
        description = "unknown"

    # Simulated traffic logic
    speed = 15  # Simulated value
    free_flow = 30
    traffic_level = ((free_flow - speed) / free_flow) * 100
    congestion_level = free_flow / speed

    suggestion = "Traffic and weather are clear."
    if speed < 10 or congestion_level > 1.5:
        suggestion = "Heavy traffic, better to avoid right now."
    elif "rain" in description.lower() or humidity > 80:
        suggestion = "Weather is not good, consider delaying."

    return jsonify({
        "distance": round(distance_km, 2),
        "eta": round(duration_min, 2),
        "delay": round(traffic_level, 1),
        "speed": speed,
        "temperature": temp,
        "humidity": humidity,
        "weather": description,
        "suggestion": suggestion
    })
