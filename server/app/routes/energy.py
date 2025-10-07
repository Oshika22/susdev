# backend/energy.py
from flask import Blueprint, request, jsonify
import pandas as pd
import requests
from app.config import EMBER_API_KEY

energy_bp = Blueprint("energy", __name__)

BASE_URL = "https://api.ember-energy.org/v1"

def fetch_data(endpoint, params):
    url = f"{BASE_URL}/{endpoint}"
    params["api_key"] = EMBER_API_KEY
    response = requests.get(url, params=params)
    if response.status_code != 200:
        print(f"Error {response.status_code} from {url}: {response.text}")
        return pd.DataFrame()
    return pd.DataFrame(response.json().get("data", []))

def get_combined_data(region="IND", start="2025-01", end="2025-08"):
    # 1. Demand
    demand_df = fetch_data(
        "electricity-demand/monthly",
        {"entity_code": region, "start_date": start, "end_date": end},
    )
    if not demand_df.empty:
        print(demand_df)
        demand_df["date"] = pd.to_datetime(demand_df["date"])
        demand_df = demand_df[["date", "value"]].rename(columns={"value": "demand_twh"})

    # 2. Generation (filter "Total generation")
    gen_df = fetch_data(
        "electricity-generation/monthly",
        {"entity_code": region, "start_date": start, "end_date": end},
    )
    if not gen_df.empty:
        gen_df["date"] = pd.to_datetime(gen_df["date"])
        gen_df["date"] = pd.to_datetime(gen_df["date"])
        total_gen_df = gen_df[gen_df["series"] == "Total generation"]
        total_gen_df = total_gen_df[["date", "generation_twh"]]

    # 3. Emissions (filter "Total generation")
    co2_df = fetch_data(
        "power-sector-emissions/monthly",
        {"entity_code": region, "start_date": start, "end_date": end},
    )
    if not co2_df.empty:
        co2_df["date"] = pd.to_datetime(co2_df["date"])
        total_co2_df = co2_df[co2_df["series"] == "Total generation"]
        total_co2_df = total_co2_df[["date", "emissions_mtco2"]]



    # 5. Merge everything on "date"
    merged = demand_df
    if not total_gen_df.empty:
        merged = merged.merge(gen_df, on="date", how="left")
    if not total_co2_df.empty:
        merged = merged.merge(co2_df, on="date", how="left")

    return merged


@energy_bp.route("/api/energy", methods=["POST"])
def get_energy():
    req = request.json or {}
    region = req.get("region", "IND").upper()
    start = req.get("start_date", "2025-01")
    end = req.get("end_date", "2025-08")

    df = get_combined_data(region, start, end)
    return jsonify({"trend": df.to_dict(orient="records")})

# @energy_bp.route('/api/energy', methods=['POST'])
# def get_energy():
#     req = request.json
#     region = req.get("region", "India")

#     # TODO: filter by region if you have that column later
#     trend = df.to_dict(orient="records")

#     return jsonify({"trend": trend})