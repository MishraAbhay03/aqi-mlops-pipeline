from google.cloud import bigquery, storage
from sklearn.metrics import mean_squared_error
from sklearn.ensemble import RandomForestRegressor
from lightgbm import LGBMRegressor
from xgboost import XGBRegressor
import pandas as pd
import numpy as np
import joblib
import json
import os

PROJECT_ID = "stalwart-seat-484411-v0"
BUCKET_NAME = "aqi-mlops-bucket"

bq = bigquery.Client()
storage_client = storage.Client()
bucket = storage_client.bucket(BUCKET_NAME)

POLLUTANTS = ["pm25","pm10","no2","co","so2","o3","aqi"]
MODEL_NAMES = ["rf","lgbm","xgb"]

# Load training data
query = """
SELECT * FROM `stalwart-seat-484411-v0.aqi_mlops.training_data`
WHERE target_pm25 IS NOT NULL
"""
df = bq.query(query).to_dataframe()

targets = {
    "pm25": "target_pm25",
    "pm10": "target_pm10",
    "no2": "target_no2",
    "co": "target_co",
    "so2": "target_so2",
    "o3": "target_o3",
    "aqi": "target_aqi"
}

feature_cols = [col for col in df.columns if col.startswith("pm") or col in [
    "temperature","humidity","wind_speed",
    "hour","day_of_week","day_of_month","month","day_of_year","week_of_year"
]]

# Download previous RMSE
metrics_blob = bucket.blob("models/metrics.json")
if metrics_blob.exists():
    old_metrics = json.loads(metrics_blob.download_as_text())
else:
    old_metrics = {}

new_metrics = {}

for pollutant in POLLUTANTS:
    print("Training", pollutant)

    X = df[feature_cols].fillna(0)
    y = df[targets[pollutant]]

    split = int(len(X)*0.8)
    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]

    models = {
        "rf": RandomForestRegressor(),
        "lgbm": LGBMRegressor(),
        "xgb": XGBRegressor()
    }

    for name, model in models.items():
        model.fit(X_train, y_train)
        preds = model.predict(X_test)
        rmse = np.sqrt(mean_squared_error(y_test, preds))

        print(name, pollutant, rmse)
        new_metrics[f"{name}_{pollutant}"] = rmse

        # Compare RMSE
        old_rmse = old_metrics.get(f"{name}_{pollutant}", 9999)

        if rmse < old_rmse:
            print("Uploading better model:", name, pollutant)
            joblib.dump(model, f"{name}_{pollutant}.joblib")
            blob = bucket.blob(f"models/{name}_{pollutant}.joblib")
            blob.upload_from_filename(f"{name}_{pollutant}.joblib")

# Upload new metrics
metrics_blob.upload_from_string(json.dumps(new_metrics))

print("Training pipeline completed")