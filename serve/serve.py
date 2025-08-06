from flask import Flask, request, jsonify, render_template_string
import pickle
import numpy as np
import pandas as pd
import os
from pathlib import Path
from datetime import datetime

# Store recent predictions
recent_predictions = []

# Robust model loading
def load_model():
    # Get script directory and build path to model
    script_dir = Path(__file__).parent
    model_path = script_dir.parent / "models" / "model.pkl"
    
    if model_path.exists():
        return pickle.load(open(model_path, "rb"))
    else:
        # Fallback to relative path from working directory
        fallback_path = "models/model.pkl"
        if os.path.exists(fallback_path):
            return pickle.load(open(fallback_path, "rb"))
        else:
            raise FileNotFoundError(f"Model not found at {model_path} or {fallback_path}")

# Load the model
model = load_model()

# Create Flask app
app = Flask(__name__)

# HTML template for dashboard
dashboard_html = """
<!DOCTYPE html>
<html>
<head>
    <title>ML Model Server</title>
    <meta http-equiv="refresh" content="2">
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .prediction { background: #f0f0f0; padding: 10px; margin: 5px 0; border-radius: 5px; }
        .diabetes { background: #ffebee; }
        .no-diabetes { background: #e8f5e8; }
    </style>
</head>
<body>
    <h1>🩺 Diabetes Prediction Model</h1>
    <p><strong>Status:</strong> Model is ready to predict!</p>
    <p><strong>Total Predictions:</strong> {{ total_predictions }}</p>
    
    <h2>Recent Predictions:</h2>
    {% if predictions %}
        {% for pred in predictions %}
        <div class="prediction {{ 'diabetes' if pred.result == 1 else 'no-diabetes' }}">
            <strong>{{ pred.timestamp }}</strong><br>
            Input: Age={{ pred.age }}, Glucose={{ pred.glucose }}, BMI={{ pred.bmi }}<br>
            <strong>Result: {{ '🔴 DIABETES RISK' if pred.result == 1 else '🟢 NO DIABETES' }}</strong>
        </div>
        {% endfor %}
    {% else %}
        <p>No predictions yet. Run some tests!</p>
    {% endif %}
    
    <p><em>Page auto-refreshes every 2 seconds</em></p>
</body>
</html>
"""

@app.route("/", methods=["GET"])
def index():
    return render_template_string(
        dashboard_html, 
        predictions=recent_predictions[-10:],  # Show last 10
        total_predictions=len(recent_predictions)
    )

@app.route("/predict", methods=["POST"])
def predict():
    try:
        input_data = request.get_json()
        df = pd.DataFrame([input_data])
        prediction = model.predict(df)
        
        # Store prediction for dashboard
        recent_predictions.append({
            'timestamp': datetime.now().strftime("%H:%M:%S"),
            'result': int(prediction[0]),
            'age': input_data.get('Age', 'N/A'),
            'glucose': input_data.get('Glucose', 'N/A'),
            'bmi': input_data.get('BMI', 'N/A'),
            'full_input': input_data
        })
        
        return jsonify({"prediction": prediction.tolist()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)