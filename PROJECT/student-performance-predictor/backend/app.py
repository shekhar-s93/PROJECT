from pathlib import Path
import pickle
from flask import Flask, jsonify, request, send_from_directory

BASE_DIR=Path(__file__).resolve().parent.parent
FRONTEND_DIR=BASE_DIR/"frontend"
MODEL_PATH=BASE_DIR/"backend"/"model"/"model.pkl"
app=Flask(__name__,static_folder=str(FRONTEND_DIR),static_url_path="")

with MODEL_PATH.open("rb") as f:
    model=pickle.load(f)

@app.get("/")
def home():
    return send_from_directory(FRONTEND_DIR,"index.html")

@app.post("/predict")
@app.post("/api/predict")
def predict():
    data=request.get_json(silent=True) or {}
    required=["study_hours","attendance","previous_score"]
    missing=[x for x in required if x not in data]
    if missing:return jsonify({"error":f"Missing fields: {', '.join(missing)}"}),400
    try:
        study_hours=float(data["study_hours"]); attendance=float(data["attendance"]); previous_score=float(data["previous_score"])
    except (TypeError,ValueError):
        return jsonify({"error":"All input values must be numbers."}),400
    if not 0<=study_hours<=12:return jsonify({"error":"Study hours must be between 0 and 12."}),400
    if not 0<=attendance<=100:return jsonify({"error":"Attendance must be between 0 and 100."}),400
    if not 0<=previous_score<=100:return jsonify({"error":"Previous score must be between 0 and 100."}),400
    prediction=model.predict([[study_hours,attendance,previous_score]])[0]
    predicted_score=round(float(max(0,min(100,prediction))),1)
    return jsonify({"predicted_score":predicted_score,"features_used":{"study_hours":study_hours,"attendance":attendance,"previous_score":previous_score}})

if __name__=="__main__":
    app.run(host="0.0.0.0",port=5000,debug=True)
