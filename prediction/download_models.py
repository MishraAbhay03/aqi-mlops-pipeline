from google.cloud import storage
import os

PROJECT_ID = "stalwart-seat-484411-v0"
BUCKET_NAME = "aqi-mlops-bucket"

storage_client = storage.Client(project=PROJECT_ID)
bucket = storage_client.bucket(BUCKET_NAME)

os.makedirs("models", exist_ok=True)

pollutants = ["pm25", "pm10", "no2", "co", "so2", "o3", "aqi"]
models = ["rf", "lgbm", "xgb"]

for p in pollutants:
    for m in models:
        blob = bucket.blob(f"models/{m}_{p}.joblib")
        blob.download_to_filename(f"models/{m}_{p}.joblib")

print("All models downloaded during Docker build")