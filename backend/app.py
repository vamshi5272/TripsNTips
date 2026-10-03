from pathlib import Path
import json
from flask import Flask, jsonify, request
from flask_cors import CORS
from optimizer.engine import optimize

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "demo_routes.json"
app = Flask(__name__)
CORS(app)


def load_data():
    with DATA_PATH.open(encoding="utf-8") as f:
        return json.load(f)


@app.get("/api/health")
def health():
    return jsonify({"status": "ok", "app": "TripsNTips API", "data_mode": "demo"})


@app.get("/api/cities")
def cities():
    data = load_data()
    return jsonify({"locations": data["locations"], "notice": data["notice"]})


@app.post("/api/optimize")
def optimize_route():
    payload = request.get_json(silent=True) or {}
    try:
        result = optimize(load_data(), payload)
        return jsonify(result), 200
    except (ValueError, TypeError) as exc:
        return jsonify({"error": str(exc)}), 400


@app.post("/api/compare")
def compare():
    payload = request.get_json(silent=True) or {}
    routes = payload.get("routes", [])
    if not isinstance(routes, list) or not routes:
        return jsonify({"error": "Provide a non-empty routes array."}), 400
    return jsonify({"routes": routes, "note": "Comparison uses the supplied calculated route results."})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
