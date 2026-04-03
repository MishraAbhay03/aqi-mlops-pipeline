import requests
import pandas as pd
from datetime import datetime, timedelta
from google.cloud import bigquery

PROJECT_ID = "stalwart-seat-484411-v0"
DATASET = "aqi_mlops"
WAQI_TOKEN = "996c03c3b5630f5fc8093f3222cb79ca0ae3fd29"

cities = {
    "Delhi": (28.61, 77.23),
    "Mumbai": (19.07, 72.87),
    "Bangalore": (12.97, 77.59),
    "Kolkata": (22.57, 88.36),
    "Chennai": (13.08, 80.27),
    "Hyderabad": (17.38, 78.48),
    "Pune": (18.52, 73.85),
    "Ahmedabad": (23.02, 72.57),
    "Jaipur": (26.91, 75.79),
    "Lucknow": (26.85, 80.95)
}

# Last 30 days
end_date = datetime.today().date()
start_date = end_date - timedelta(days=30)

aqi_data = []
weather_data = []

for city, (lat, lon) in cities.items():
    print("Fetching AQI:", city)

    url = (
        "https://air-quality-api.open-meteo.com/v1/air-quality"
        f"?latitude={lat}&longitude={lon}"
        f"&start_date={start_date}&end_date={end_date}"
        "&hourly=pm10,pm2_5,carbon_monoxide,nitrogen_dioxide,sulphur_dioxide,ozone"
    )

    response = requests.get(url).json()

    if "hourly" in response:
        hourly = response["hourly"]

        df_aqi = pd.DataFrame({
            "timestamp": pd.to_datetime(hourly["time"]),
            "city": city,
            "pm10": hourly["pm10"],
            "pm25": hourly["pm2_5"],
            "co": hourly["carbon_monoxide"],
            "no2": hourly["nitrogen_dioxide"],
            "so2": hourly["sulphur_dioxide"],
            "o3": hourly["ozone"]
        })

        aqi_data.append(df_aqi)

    # Weather from WAQI
    print("Fetching Weather:", city)
    waqi_url = f"https://api.waqi.info/feed/{city}/?token={WAQI_TOKEN}"
    waqi_response = requests.get(waqi_url).json()

    if waqi_response["status"] == "ok":
        weather = waqi_response["data"]["iaqi"]

        df_weather = pd.DataFrame({
            "timestamp": [datetime.now()],
            "city": [city],
            "temperature": [weather.get("t", {}).get("v")],
            "humidity": [weather.get("h", {}).get("v")],
            "wind_speed": [weather.get("w", {}).get("v")]
        })

        weather_data.append(df_weather)

# Combine
final_aqi = pd.concat(aqi_data)
final_weather = pd.concat(weather_data)

print("Uploading AQI data...")
bq_client = bigquery.Client()

aqi_table = f"{PROJECT_ID}.{DATASET}.raw_aqi"
weather_table = f"{PROJECT_ID}.{DATASET}.raw_weather"

aqi_job = bq_client.load_table_from_dataframe(
    final_aqi,
    aqi_table,
    job_config=bigquery.LoadJobConfig(
        write_disposition="WRITE_TRUNCATE",
        autodetect=True
    )
)
aqi_job.result()

print("Uploading Weather data...")

weather_job = bq_client.load_table_from_dataframe(
    final_weather,
    weather_table,
    job_config=bigquery.LoadJobConfig(
        write_disposition="WRITE_APPEND",
        autodetect=True
    )
)
weather_job.result()

print("Last 1 Month AQI + Weather loaded successfully")