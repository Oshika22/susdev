from flask import Blueprint, request, jsonify
import pandas as pd
import openmeteo_requests
from geopy.geocoders import Nominatim
import requests_cache
from retry_requests import retry

airForecast_bp = Blueprint('airForecast', __name__)

@airForecast_bp.route('/api/airForecast', methods=['GET'])
def airForecast():
    city = request.args.get("city")
    if not city:
        return jsonify({"error": "City not provided"}), 400

    # Step 1: Get coordinates using geopy
    geolocator = Nominatim(user_agent="aqi_app")
    location = geolocator.geocode(f"{city}, India", exactly_one=True)
    if not location:
        return jsonify({"error": "City not found"}), 404
    lat, lon = location.latitude, location.longitude

    # Step 2: Setup Open-Meteo API client
    cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    url = "https://air-quality-api.open-meteo.com/v1/air-quality"
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": [
            "pm10", "pm2_5", "carbon_monoxide", "ozone",
            "ammonia", "sulphur_dioxide", "nitrogen_dioxide"
        ],
        "current": [
            "ozone", "sulphur_dioxide", "nitrogen_dioxide",
            "carbon_monoxide", "pm2_5", "pm10", "ammonia"
        ]
    }

    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]

    hourly = response.Hourly()
    hourly_data = {
        "date": pd.date_range(
            start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
            end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=hourly.Interval()),
            inclusive="left"
        ),
        "pm10": hourly.Variables(0).ValuesAsNumpy(),
        "pm2_5": hourly.Variables(1).ValuesAsNumpy(),
        "carbon_monoxide": hourly.Variables(2).ValuesAsNumpy(),
        "ozone": hourly.Variables(3).ValuesAsNumpy(),
        "ammonia": hourly.Variables(4).ValuesAsNumpy(),
        "sulphur_dioxide": hourly.Variables(5).ValuesAsNumpy(),
        "nitrogen_dioxide": hourly.Variables(6).ValuesAsNumpy()
    }

    df = pd.DataFrame(hourly_data)

    # Step 3: Filter next 3 days

    # Get forecast starting date
    forecast_start = df["date"].iloc[0].normalize()
    
    # Define the desired 3 dates: 2, 3, 4 August
    start_date = forecast_start + pd.Timedelta(days=2)
    end_date = start_date + pd.Timedelta(days=4)
    
    # Filter rows where the date is in the desired range
    df_filtered = df[(df["date"] >= start_date) & (df["date"] < end_date)].copy()


    # Step 4: Indian AQI calculation
    breakpoints = {
        "pm2_5": [(0, 30, 0, 50), (31, 60, 51, 100), (61, 90, 101, 200), (91, 120, 201, 300), (121, 250, 301, 400), (251, 350, 401, 500)],
        "pm10": [(0, 50, 0, 50), (51, 100, 51, 100), (101, 250, 101, 200), (251, 350, 201, 300), (351, 430, 301, 400), (431, 500, 401, 500)],
        "nitrogen_dioxide": [(0, 40, 0, 50), (41, 80, 51, 100), (81, 180, 101, 200), (181, 280, 201, 300), (281, 400, 301, 400), (401, 500, 401, 500)],
        "sulphur_dioxide": [(0, 40, 0, 50), (41, 80, 51, 100), (81, 380, 101, 200), (381, 800, 201, 300), (801, 1600, 301, 400), (1601, 2000, 401, 500)],
        "carbon_monoxide": [(0, 1, 0, 50), (1.1, 2, 51, 100), (2.1, 10, 101, 200), (10.1, 17, 201, 300), (17.1, 34, 301, 400), (34.1, 50, 401, 500)],
        "ozone": [(0, 50, 0, 50), (51, 100, 51, 100), (101, 168, 101, 200), (169, 208, 201, 300), (209, 748, 301, 400), (749, 1000, 401, 500)]
    }

    def calc_sub_index(value, bp_list):
        for (c_low, c_high, i_low, i_high) in bp_list:
            if c_low <= value <= c_high:
                return ((i_high - i_low) / (c_high - c_low)) * (value - c_low) + i_low
        return None

    def compute_india_aqi(row):
        sub_indices = []
        mapping = {
            "pm2_5": "pm2_5",
            "pm10": "pm10",
            "no2": "nitrogen_dioxide",
            "so2": "sulphur_dioxide",
            "co": "carbon_monoxide",
            "o3": "ozone"
        }
        for aqi_name, col in mapping.items():
            val = row[col]
            if pd.notnull(val):
                sub_idx = calc_sub_index(val, breakpoints[col])
                if sub_idx is not None:
                    sub_indices.append(sub_idx)
        return max(sub_indices) if sub_indices else None
    

    df_filtered["india_aqi"] = df_filtered.apply(compute_india_aqi, axis=1)
    df_filtered["date_str"] = df_filtered["date"].dt.strftime("%d %b")

    def map_to_openweather_scale(aqi):
        if pd.isnull(aqi):
            return None
        if aqi <= 50:
            return 1  # Good
        elif aqi <= 100:
            return 2  # Fair
        elif aqi <= 200:
            return 3  # Moderate
        elif aqi <= 300:
            return 4  # Poor
        else:
            return 5  # Very Poor

    df_filtered["aqi_range"] = df_filtered["india_aqi"].apply(map_to_openweather_scale)
    result = df_filtered.groupby("date_str").apply(
    lambda group: pd.Series({
        "exp_aqi": round(group["india_aqi"].max(), 0),
        "aqi_range": int(group[group["india_aqi"] == group["india_aqi"].max()]["aqi_range"].iloc[0])
    })
    ).reset_index()

    return jsonify(result.to_dict(orient="records"))
