import json
import math
import pickle
from http.server import BaseHTTPRequestHandler
from pathlib import Path


MODEL_PATH = Path(__file__).resolve().parent.parent / "backend" / "model" / "model.pkl"

with MODEL_PATH.open("rb") as model_file:
    model = pickle.load(model_file)


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers.get("Content-Length", "0"))
            data = json.loads(self.rfile.read(content_length))
        except (ValueError, UnicodeDecodeError, json.JSONDecodeError):
            return self._json_response(400, {"error": "Request body must be valid JSON."})

        if not isinstance(data, dict):
            return self._json_response(400, {"error": "Request body must be a JSON object."})

        required = ["study_hours", "attendance", "previous_score"]
        missing = [field for field in required if field not in data]
        if missing:
            return self._json_response(400, {"error": f"Missing fields: {', '.join(missing)}"})

        try:
            study_hours, attendance, previous_score = (
                float(data[field]) for field in required
            )
        except (TypeError, ValueError):
            return self._json_response(400, {"error": "All input values must be numbers."})

        values = (study_hours, attendance, previous_score)
        if not all(math.isfinite(value) for value in values):
            return self._json_response(400, {"error": "All input values must be finite numbers."})
        if not 0 <= study_hours <= 12:
            return self._json_response(400, {"error": "Study hours must be between 0 and 12."})
        if not 0 <= attendance <= 100:
            return self._json_response(400, {"error": "Attendance must be between 0 and 100."})
        if not 0 <= previous_score <= 100:
            return self._json_response(400, {"error": "Previous score must be between 0 and 100."})

        prediction = model.predict([[study_hours, attendance, previous_score]])[0]
        predicted_score = round(float(max(0, min(100, prediction))), 1)
        return self._json_response(200, {
            "predicted_score": predicted_score,
            "features_used": {
                "study_hours": study_hours,
                "attendance": attendance,
                "previous_score": previous_score,
            },
        })

    def do_GET(self):
        return self._json_response(405, {"error": "Use POST to request a prediction."})

    def _json_response(self, status, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)
