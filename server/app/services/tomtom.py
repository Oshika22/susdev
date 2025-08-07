import requests
from app.config import TOMTOM_API_KEY

def get_coordinates(location):
    url = f"https://api.tomtom.com/search/2/geocode/{location}.json?key={TOMTOM_API_KEY}"
    response = requests.get(url).json()

    if response.get("results"):
        position = response["results"][0]["position"]
        return {"lat": position["lat"], "lon": position["lon"]}
    return None
