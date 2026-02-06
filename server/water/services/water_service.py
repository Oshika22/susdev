# water_service.py

from water.models.wqi_model import calculate_wqi, classify_wqi


def get_water_metrics():
    # Temporary sample values (later from sensors or dataset)
    ph = 7.2
    turbidity = 4.5
    tds = 120
    dissolved_oxygen = 6.8
    temperature = 26

    wqi = calculate_wqi(ph, turbidity, tds, dissolved_oxygen, temperature)
    status = classify_wqi(wqi)

    return {
        "ph": ph,
        "turbidity": turbidity,
        "tds": tds,
        "dissolved_oxygen": dissolved_oxygen,
        "temperature": temperature,
        "wqi": wqi,
        "status": status
    }
