import pandas as pd
import numpy as np
import joblib
import os

from google.cloud import bigquery
from sklearn.ensemble import RandomForestRegressor
from lightgbm import LGBMRegressor
from xgboost import XGBRegressor

PROJECT_ID = "stalwart-seat-484411-v0"

bq_client = bigquery.Client(project=PROJECT_ID)

query = """
SELECT *
FROM `stalwart-seat-484411-v0.aqi_mlops.training_data`
ORDER BY timestamp
"""

print("Loading training data...")
df = bq_client.query(query).to_dataframe()

# Cyclical features
df["sin_hour"] = np.sin(2 * np.pi * df["hour"] / 24)
df["cos_hour"] = np.cos(2 * np.pi * df["hour"] / 24)
df["sin_month"] = np.sin(2 * np.pi * df["month"] / 12)
df["cos_month"] = np.cos(2 * np.pi * df["month"] / 12)

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

targets = {
    "pm25":"target_pm25",
    "pm10":"target_pm10",
    "no2":"target_no2",
    "co":"target_co",
    "so2":"target_so2",
    "o3":"target_o3",
    "aqi":"target_aqi"
}

os.makedirs("/model", exist_ok=True)

for pollutant, target in targets.items():
    print("Training", pollutant)

    data = df.dropna(subset=[target])
    X = data[features]
    y = data[target]

    split = int(len(X)*0.8)
    X_train, X_test = X.iloc[:split], X.iloc[split:]
    y_train, y_test = y.iloc[:split], y.iloc[split:]

    rf = RandomForestRegressor(n_estimators=300,max_depth=20)
    rf.fit(X_train,y_train)

    lgbm = LGBMRegressor(n_estimators=1200,learning_rate=0.02)
    lgbm.fit(X_train,y_train)

    xgb = XGBRegressor(n_estimators=1200,learning_rate=0.02,max_depth=8)
    xgb.fit(X_train,y_train)

    joblib.dump(rf,f"/model/rf_{pollutant}.joblib")
    joblib.dump(lgbm,f"/model/lgbm_{pollutant}.joblib")
    joblib.dump(xgb,f"/model/xgb_{pollutant}.joblib")

print("Training finished")