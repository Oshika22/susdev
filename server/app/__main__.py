from flask import Flask, request, jsonify
from flask_cors import CORS
import os

from water.services.water_service import get_water_metrics
from water.services.waste_service import get_waste_report
from water.services.cleaning_service import verify_cleaning, trigger_cleaning

app = Flask(__name__)
CORS(app)

# ----------------------
# PATH CONFIG
# ----------------------
UPLOAD_FOLDER = "water/waste_detection"
BEFORE_IMAGE = os.path.join(UPLOAD_FOLDER, "before.jpg")
AFTER_IMAGE = os.path.join(UPLOAD_FOLDER, "after.jpg")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ----------------------
# ROOT
# ----------------------
@app.route("/")
def home():
    return "Urban Optima Backend Running"

# ----------------------
# WATER QUALITY API
# ----------------------
@app.route("/api/water")
def water():
    return jsonify(get_water_metrics())

# ----------------------
# WASTE CHECK (SINGLE IMAGE)
# ----------------------
@app.route("/api/waste")
def waste():
    return jsonify(get_waste_report(BEFORE_IMAGE))

# ----------------------
# UPLOAD BEFORE IMAGE
# ----------------------
@app.route("/api/upload-before", methods=["POST"])
def upload_before():
    if "image" not in request.files:
        return jsonify({"error": "No image provided"}), 400

    file = request.files["image"]
    file.save(BEFORE_IMAGE)

    return jsonify({
        "message": "Before image uploaded successfully",
        "path": BEFORE_IMAGE
    })

# ----------------------
# UPLOAD AFTER IMAGE
# ----------------------
@app.route("/api/upload-after", methods=["POST"])
def upload_after():
    if "image" not in request.files:
        return jsonify({"error": "No image provided"}), 400

    file = request.files["image"]
    file.save(AFTER_IMAGE)

    return jsonify({
        "message": "After image uploaded successfully",
        "path": AFTER_IMAGE
    })

# ----------------------
# VERIFY CLEANING ONLY
# ----------------------
@app.route("/api/verify-cleaning")
def verify():
    return jsonify(
        verify_cleaning(BEFORE_IMAGE, AFTER_IMAGE)
    )

# ----------------------
# FULL AUTOMATED CYCLE
# ----------------------
@app.route("/api/waste/full-cycle")
def full_cycle():
    # 1. Detect waste BEFORE cleaning
    before = get_waste_report(BEFORE_IMAGE)

    # 2. Trigger cleaning if needed
    cleaning_action = trigger_cleaning(before)

    # 3. Detect waste AFTER cleaning
    after = get_waste_report(AFTER_IMAGE)

    # 4. Verify cleaning success
    verification = verify_cleaning(BEFORE_IMAGE, AFTER_IMAGE)

    return jsonify({
        "before": {
            "waste_detected": before["waste_detected"],
            "severity": before["severity"]
        },
        "cleaning_action": cleaning_action,
        "after": {
            "waste_detected": after["waste_detected"]
        },
        "verification": {
            "cleaning_successful": verification["cleaning_successful"]
        }
    })

# ----------------------
# RUN SERVER
# ----------------------
if __name__ == "__main__":
    app.run(debug=True)
