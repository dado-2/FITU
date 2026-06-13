from flask import Flask, jsonify, request
from flask_cors import CORS

from nutrition_app import load_models, predict_goal, predict_calories, recommend_plan

app = Flask(__name__)
app.config["CORS_HEADERS"] = "Content-Type"
CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)

MODELS = load_models(base_path=".")

REQUIRED_FIELDS = [
    "Gender",
    "Age",
    "Weight (kg)",
    "Height (m)",
    "Water_Intake (liters)",
    "Experience_Level",
    "Workout_Frequency (days/week)",
    "Resting_BPM",
]


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify(
        {
            "status": "ok",
            "models": {
                "goal_loaded": MODELS.get("goal") is not None,
                "calories_loaded": MODELS.get("calories") is not None,
            },
        }
    )


@app.route("/api/predict", methods=["POST"])
def predict():
    payload = request.get_json(silent=True)
    if not payload:
        return jsonify({"error": "JSON body required"}), 400

    missing = [field for field in REQUIRED_FIELDS if field not in payload]
    if missing:
        return jsonify({"error": "Missing required input fields", "missing": missing}), 400

    user_input = {field: payload[field] for field in REQUIRED_FIELDS}

    goal_pred = predict_goal(MODELS.get("goal"), user_input)
    calories_pred = predict_calories(MODELS.get("calories"), user_input)
    plan = recommend_plan(user_input, goal_pred, calories_pred)

    return jsonify(plan)


if __name__ == "__main__":
    import os
    import socket

    def _find_free_port(start=5000, end=5100):
        for p in range(start, end + 1):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                try:
                    s.bind(("0.0.0.0", p))
                    return p
                except OSError:
                    continue
        return None

    port = int(os.environ.get("PORT", 0)) or _find_free_port(5000, 5100)
    if not port:
        print("No free port found in range 5000-5100. Exiting.")
        raise SystemExit(1)

    print(f"Starting API on 0.0.0.0:{port}")
    app.run(host="0.0.0.0", port=port, debug=False)
