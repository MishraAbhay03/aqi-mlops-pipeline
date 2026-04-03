import pandas as pd
import numpy as np
import joblib
import os

from flask import Flask, jsonify
from google.cloud import bigquery

app = Flask(__name__)

PROJECT_ID = "stalwart-seat-484411-v0"
DATASET = "aqi_mlops"

bq_client = bigquery.Client(project=PROJECT_ID)

MODEL_NAMES = ["rf", "lgbm", "xgb"]
POLLUTANTS = ["pm25", "pm10", "no2", "co", "so2", "o3", "aqi"]

features = [
    "pm25","pm10","no2","so2","co","o3",
    "temperature","humidity","wind_speed",

    "pm25_lag1","pm25_lag3","pm25_lag6","pm25_lag12",
    "pm25_lag24","pm25_lag48","pm25_lag72","pm25_lag168",

    "pm10_lag24","no2_lag24","co_lag24","so2_lag24","o3_lag24",

    "aqi_lag1","aqi_lag24",

    "pm25_roll24","pm25_roll72","pm25_roll168",
    "pm25_std24","aqi_std24",

    "hour","day_of_week","day_of_month","month","day_of_year","week_of_year",
    "sin_hour","cos_hour","sin_month","cos_month"
]

models = {}

# -----------------------------
# Load models
# -----------------------------
def load_models():
    print("Loading models...")
    for pollutant in POLLUTANTS:
        models[pollutant] = {
            "rf": joblib.load(f"models/rf_{pollutant}.joblib"),
            "lgbm": joblib.load(f"models/lgbm_{pollutant}.joblib"),
            "xgb": joblib.load(f"models/xgb_{pollutant}.joblib"),
        }
    print("Models loaded")

load_models()

# -----------------------------
# Routes
# -----------------------------
@app.route("/")
def home():
    return "AQI Prediction API Running"

@app.route("/predict")
def predict():
    try:
        print("Starting prediction for all cities...")

        # Latest feature row per city
        query = f"""
        SELECT *
        FROM `{PROJECT_ID}.{DATASET}.features`
        QUALIFY ROW_NUMBER() OVER(PARTITION BY city ORDER BY timestamp DESC) = 1
        """

        rows = list(bq_client.query(query))
        df_all = pd.DataFrame([dict(row) for row in rows])

        if df_all.empty:
            return "No feature data found"

        all_predictions = []

        # Loop each city
        for _, row in df_all.iterrows():

            current = row.copy()

            for col in features:
                if col not in current:
                    current[col] = 0

            current = current.fillna(0)

            # 24-hour recursive forecast
            for step in range(24):

                X = pd.DataFrame([current[features]])
                X = X.fillna(0)

                predictions = {}

                for pollutant in POLLUTANTS:
                    rf = models[pollutant]["rf"]
                    lgbm = models[pollutant]["lgbm"]
                    xgb = models[pollutant]["xgb"]

                    pred = (
                        rf.predict(X)[0]
                        + lgbm.predict(X)[0]
                        + xgb.predict(X)[0]
                    ) / 3

                    predictions[pollutant] = float(pred)

                future_time = pd.Timestamp.utcnow() + pd.Timedelta(hours=step+1)

                all_predictions.append({
                    "timestamp": future_time,
                    "city": current["city"],
                    "pm25": predictions["pm25"],
                    "pm10": predictions["pm10"],
                    "no2": predictions["no2"],
                    "co": predictions["co"],
                    "so2": predictions["so2"],
                    "o3": predictions["o3"],
                    "aqi": predictions["aqi"]
                })

                # Recursive update
                alpha = 0.6
                for p in POLLUTANTS:
                    current[p] = alpha * current[p] + (1 - alpha) * predictions[p]

                # Time features update
                future_time = pd.Timestamp.utcnow() + pd.Timedelta(hours=step+1)
                current["hour"] = future_time.hour
                current["day_of_week"] = future_time.dayofweek
                current["day_of_month"] = future_time.day
                current["month"] = future_time.month
                current["day_of_year"] = future_time.dayofyear
                current["week_of_year"] = int(future_time.isocalendar().week)

                current["sin_hour"] = np.sin(2 * np.pi * current["hour"] / 24)
                current["cos_hour"] = np.cos(2 * np.pi * current["hour"] / 24)
                current["sin_month"] = np.sin(2 * np.pi * current["month"] / 12)
                current["cos_month"] = np.cos(2 * np.pi * current["month"] / 12)

        # Delete old forecasts
        delete_query = f"""
        DELETE FROM `{PROJECT_ID}.{DATASET}.forecast`
        WHERE timestamp > CURRENT_TIMESTAMP()
        """
        bq_client.query(delete_query).result()

        # Insert forecast
        forecast_df = pd.DataFrame(all_predictions)

        table_id = f"{PROJECT_ID}.{DATASET}.forecast"

        job = bq_client.load_table_from_dataframe(
            forecast_df,
            table_id,
            job_config=bigquery.LoadJobConfig(
                write_disposition="WRITE_APPEND"
            )
        )
        job.result()

        print("Forecast inserted for all cities")

        return jsonify(all_predictions)

    except Exception as e:
        print("ERROR:", str(e))
        return str(e)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)