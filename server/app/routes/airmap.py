# File: air_bp.py
from flask import Blueprint, request, jsonify
import requests
import folium
from geopy.geocoders import Nominatim
from config import WEATHER_API_KEY
air_bp = Blueprint('air', __name__)



def get_coordinates(city_name):
    geolocator = Nominatim(user_agent="aqi_app")
    location = geolocator.geocode(f"{city_name}, India", exactly_one=True)
    return location.latitude, location.longitude

def get_aqi_color(aqi):
    return {
        1: 'green',
        2: 'yellow',
        3: 'orange',
        4: 'red',
        5: 'purple'
    }.get(aqi, 'gray')

@air_bp.route('/api/air', methods=['POST'])
def get_air_data():
    data = request.get_json()
    city = data.get("city")
    if not city:
        return jsonify({"error": "City not provided"}), 400

    lat, lon = get_coordinates(city)

    aqi_url = f"https://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={WEATHER_API_KEY}"
    weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={WEATHER_API_KEY}&units=metric"

    try:
        aqi_res = requests.get(aqi_url).json()
        weather_res = requests.get(weather_url).json()



        # aqi_res = {
        #     "list": [
        #         {
        #             "main": {
        #                 "aqi": 3
        #             },
        #             "components": {
        #                 "co": 201.94,
        #                 "no": 0.02,
        #                 "no2": 0.77,
        #                 "o3": 68.66,
        #                 "so2": 0.64,
        #                 "pm2_5": 7.85,
        #                 "pm10": 12.29,
        #                 "nh3": 0.12
        #             }
        #         }
        #     ]
        # }
        # weather_res = {
        #     "main": {
        #         "temp": 31.5,
        #         "humidity": 62
        #     },
        #     "wind": {
        #         "speed": 4.3
        #     },
        #     "weather": [
        #         {
        #             "description": "scattered clouds"
        #         }
        #     ]
        # }

        aqi = aqi_res['list'][0]['main']['aqi']
        components = aqi_res['list'][0]['components']

        aqi_levels = {
            1: "Good",
            2: "Fair",
            3: "Moderate",
            4: "Poor",
            5: "Very Poor"
        }

        suggestions = ""

        # Health Suggestion
        if aqi == 1:
            suggestions = "Air quality is excellent today. Safe for all age groups and sensitive individuals."
        elif aqi == 2:
            suggestions = "Air quality is fair. Mild impact on very sensitive people with asthma or heart issues."
        else:
            suggestions = "Air quality may be unhealthy. Limit outdoor activities, especially for sensitive groups."

        # Travel Suggestion
        temp = weather_res['main']['temp']
        # humidity = weather_res['main']['humidity']
       
        # condition = weather_res['weather'][0]['description']

        # if "rain" in condition.lower():
        #     travel_note = "It may rain, so carry an umbrella and plan accordingly."
        # elif "cloud" in condition.lower():
        #     travel_note = "Partly cloudy skies make it pleasant for walks or light travel."
        # else:
        #     travel_note = "Great day for travel with clear skies."

        # comfort_note = ""
        # if temp < 15:
        #     comfort_note = " Slightly cold — consider a jacket."
        # elif temp > 30:
        #     comfort_note = " It’s a bit hot — wear light clothes and stay hydrated."

        # if humidity > 80:
        #     comfort_note += " Humidity is high, so it might feel warmer."

        # suggestions['travel'] = travel_note + comfort_note


        popup_text = f"""
        <b>📍 {city}</b><br>
        <b>AQI:</b> {aqi}<br>
        <b>PM2.5:</b> {components['pm2_5']} µg/m³<br>
        <b>Weather:</b> {weather_res['weather'][0]['description']}<br>
        <b>Temp:</b> {temp} °C<br>
        <b>Humidity:</b> {weather_res['main']['humidity']}%<br>
        <b>Wind:</b> {weather_res['wind']['speed']} m/s
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
        return jsonify({
            "aqi": aqi,
            "aqi_text": aqi_levels[aqi],
            "components": components,
            "temperature": weather_res['main']['temp'],
            "humidity": weather_res['main']['humidity'],
            "wind_speed": weather_res['wind']['speed'],
            "weather": weather_res['weather'][0]['description'],
            "city": city,
            "lat": lat,
            "lon": lon,
            "suggestion": suggestions,
            "map_html": map_html
        })

    except Exception as e:
        print(e)
        return jsonify({"error": "Could not fetch AQI or weather data"}), 500

# @air_bp.route('/map/air', methods=['GET'])
# def show_air_map():
#     city = request.args.get('city')
#     if not city:
#         return "City not provided", 400

#     lat, lon = get_coordinates(city)

#     aqi_url = f"https://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={WEATHER_API_KEY}"
#     weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={WEATHER_API_KEY}&units=metric"

#     aqi_res = requests.get(aqi_url).json()
#     weather_res = requests.get(weather_url).json()

#     aqi = aqi_res['list'][0]['main']['aqi']
#     components = aqi_res['list'][0]['components']

#     weather_main = weather_res['weather'][0]['description']
#     temperature = weather_res['main']['temp']
#     humidity = weather_res['main']['humidity']
#     wind_speed = weather_res['wind']['speed']

#     popup_text = f"""
#     <b>📍 {city}</b><br>
#     <b>AQI:</b> {aqi}<br>
#     <b>PM2.5:</b> {components['pm2_5']} µg/m³<br>
#     <b>Weather:</b> {weather_main}<br>
#     <b>Temp:</b> {temperature} °C<br>
#     <b>Humidity:</b> {humidity}%<br>
#     <b>Wind:</b> {wind_speed} m/s
#     """

#     m = folium.Map(location=[lat, lon], zoom_start=11)
#     folium.Circle(
#         location=[lat, lon],
#         radius=10000,
#         color=get_aqi_color(aqi),
#         fill=True,
#         fill_color=get_aqi_color(aqi),
#         popup=folium.Popup(popup_text, max_width=300)
#     ).add_to(m)

#     return m._repr_html_()
