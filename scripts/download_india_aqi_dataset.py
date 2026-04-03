import requests
from google.cloud import storage, bigquery

PROJECT_ID = "stalwart-seat-484411-v0"
BUCKET_NAME = "aqi-mlops-bucket"
DATASET = "aqi_mlops"

url = "https://raw.githubusercontent.com/datameet/india-air-quality-data/master/data/india_air_quality.csv"

print("Downloading India AQI dataset...")
response = requests.get(url)

with open("india_aqi.csv", "wb") as f:
    f.write(response.content)

print("Uploading to Cloud Storage...")
storage_client = storage.Client()
bucket = storage_client.bucket(BUCKET_NAME)
bucket.blob("india_aqi.csv").upload_from_filename("india_aqi.csv")

print("Loading into BigQuery...")
bq_client = bigquery.Client()

job_config = bigquery.LoadJobConfig(
    autodetect=True,
    source_format=bigquery.SourceFormat.CSV,
    skip_leading_rows=1,
    write_disposition="WRITE_TRUNCATE"
)

bq_client.load_table_from_uri(
    f"gs://{BUCKET_NAME}/india_aqi.csv",
    f"{PROJECT_ID}.{DATASET}.raw_aqi",
    job_config=job_config
).result()

print("India AQI dataset loaded into BigQuery")