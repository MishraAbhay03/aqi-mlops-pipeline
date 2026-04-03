import requests
import pandas as pd
from google.cloud import storage, bigquery

PROJECT_ID = "stalwart-seat-484411-v0"
BUCKET_NAME = "aqi-mlops-bucket"
DATASET = "aqi_mlops"

url = "https://raw.githubusercontent.com/plotly/datasets/master/2016-weather-data-seattle.csv"

print("Downloading dataset...")
df = pd.read_csv(url)

# Simulate AQI dataset format
df = df.rename(columns={
    "Date": "timestamp",
    "Mean_TemperatureC": "pm25",
    "Max_TemperatureC": "pm10"
})

df["city"] = "Delhi"

df = df[["timestamp", "city", "pm25", "pm10"]]

df.to_csv("india_aqi_clean.csv", index=False)

print("Uploading to GCS...")
storage_client = storage.Client()
bucket = storage_client.bucket(BUCKET_NAME)
bucket.blob("india_aqi_clean.csv").upload_from_filename("india_aqi_clean.csv")

print("Loading into BigQuery...")
bq_client = bigquery.Client()

job_config = bigquery.LoadJobConfig(
    schema=[
        bigquery.SchemaField("timestamp", "STRING"),
        bigquery.SchemaField("city", "STRING"),
        bigquery.SchemaField("pm25", "FLOAT"),
        bigquery.SchemaField("pm10", "FLOAT"),
    ],
    skip_leading_rows=1,
    source_format=bigquery.SourceFormat.CSV,
    write_disposition="WRITE_TRUNCATE"
)

bq_client.load_table_from_uri(
    f"gs://{BUCKET_NAME}/india_aqi_clean.csv",
    f"{PROJECT_ID}.{DATASET}.raw_aqi",
    job_config=job_config
).result()

print("AQI data loaded into BigQuery")