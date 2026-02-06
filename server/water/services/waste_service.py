from water.waste_detection.detector import detect_waste

def get_waste_report():
    items = detect_waste("water/waste_detection/test.jpg")

    report = {
        "waste_detected": len(items) > 0,
        "items": items,
        "severity": "low"
    }

    if len(items) > 3:
        report["severity"] = "high"
    elif len(items) > 0:
        report["severity"] = "medium"

    return report
