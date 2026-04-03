import requests
import pandas as pd
from datetime import datetime
from google.cloud import bigquery

PROJECT_ID = "stalwart-seat-484411-v0"
DATASET = "aqi_mlops"

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

aqi_rows = []
weather_rows = []

for city, (lat, lon) in cities.items():
    print("Fetching data:", city)

    # Air Quality API (includes AQI)
    aqi_url = (
        "https://air-quality-api.open-meteo.com/v1/air-quality"
        f"?latitude={lat}&longitude={lon}"
        "&hourly=pm10,pm2_5,carbon_monoxide,nitrogen_dioxide,sulphur_dioxide,ozone,us_aqi"
        "&timezone=auto"
    )

    # Weather API
    weather_url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}"
        "&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m"
        "&timezone=auto"
    )

    aqi_response = requests.get(aqi_url).json()
    weather_response = requests.get(weather_url).json()

    # Latest AQI + Pollutants
    if "hourly" in aqi_response:
        hourly = aqi_response["hourly"]

        df_aqi = pd.DataFrame({
            "timestamp": [pd.to_datetime(hourly["time"][-1])],
            "city": [city],
            "pm10": [hourly["pm10"][-1]],
            "pm25": [hourly["pm2_5"][-1]],
            "co": [hourly["carbon_monoxide"][-1]],
            "no2": [hourly["nitrogen_dioxide"][-1]],
            "so2": [hourly["sulphur_dioxide"][-1]],
            "o3": [hourly["ozone"][-1]],
            "aqi": [hourly["us_aqi"][-1]]
        })

        aqi_rows.append(df_aqi)

    # Latest Weather
    if "hourly" in weather_response:
        hourly_w = weather_response["hourly"]

        df_weather = pd.DataFrame({
            "timestamp": [pd.to_datetime(hourly_w["time"][-1])],
            "city": [city],
            "temperature": [hourly_w["temperature_2m"][-1]],
            "humidity": [hourly_w["relative_humidity_2m"][-1]],
            "wind_speed": [hourly_w["wind_speed_10m"][-1]]
        })

        weather_rows.append(df_weather)

# Combine
final_aqi = pd.concat(aqi_rows)
final_weather = pd.concat(weather_rows)

print("Uploading AQI data...")
bq_client = bigquery.Client()

aqi_table = f"{PROJECT_ID}.{DATASET}.raw_aqi"
weather_table = f"{PROJECT_ID}.{DATASET}.raw_weather"

# Append AQI
aqi_job = bq_client.load_table_from_dataframe(
    final_aqi,
    aqi_table,
    job_config=bigquery.LoadJobConfig(
        write_disposition="WRITE_APPEND",
        autodetect=True
    )
)
aqi_job.result()

print("Uploading Weather data...")

# Append Weather
weather_job = bq_client.load_table_from_dataframe(
    final_weather,
    weather_table,
    job_config=bigquery.LoadJobConfig(
        write_disposition="WRITE_APPEND",
        autodetect=True
    )
)
weather_job.result()

print("Live AQI + Weather data ingested successfully")