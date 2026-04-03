import requests
import pandas as pd
from datetime import datetime, timedelta
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

# Last 1 Year
end_date = datetime.today().date()
start_date = end_date - timedelta(days=365)

aqi_data = []
weather_data = []

# AQI Calculation Function
def calculate_aqi(pm25):
    if pm25 <= 12:
        return pm25 * 4.17
    elif pm25 <= 35:
        return pm25 * 2.4
    elif pm25 <= 55:
        return pm25 * 1.8
    elif pm25 <= 150:
        return pm25 * 1.2
    else:
        return pm25 * 1

for city, (lat, lon) in cities.items():
    print("Fetching historical data for:", city)

    # Air Quality Historical
    aqi_url = (
        "https://air-quality-api.open-meteo.com/v1/air-quality"
        f"?latitude={lat}&longitude={lon}"
        f"&start_date={start_date}&end_date={end_date}"
        "&hourly=pm10,pm2_5,carbon_monoxide,nitrogen_dioxide,sulphur_dioxide,ozone"
        "&timezone=auto"
    )

    # Weather Historical
    weather_url = (
        "https://archive-api.open-meteo.com/v1/archive"
        f"?latitude={lat}&longitude={lon}"
        f"&start_date={start_date}&end_date={end_date}"
        "&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m"
        "&timezone=auto"
    )

    aqi_response = requests.get(aqi_url).json()
    weather_response = requests.get(weather_url).json()

    # AQI Data
    if "hourly" in aqi_response:
        hourly = aqi_response["hourly"]

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

        # Calculate AQI
        df_aqi["aqi"] = df_aqi["pm25"].apply(calculate_aqi)

        aqi_data.append(df_aqi)

    # Weather Data
    if "hourly" in weather_response:
        hourly_w = weather_response["hourly"]

        df_weather = pd.DataFrame({
            "timestamp": pd.to_datetime(hourly_w["time"]),
            "city": city,
            "temperature": hourly_w["temperature_2m"],
            "humidity": hourly_w["relative_humidity_2m"],
            "wind_speed": hourly_w["wind_speed_10m"]
        })

        weather_data.append(df_weather)

# Combine
final_aqi = pd.concat(aqi_data)
final_weather = pd.concat(weather_data)

print("Uploading historical AQI data...")
bq_client = bigquery.Client()

aqi_table = f"{PROJECT_ID}.{DATASET}.raw_aqi"
weather_table = f"{PROJECT_ID}.{DATASET}.raw_weather"

# Overwrite tables
aqi_job = bq_client.load_table_from_dataframe(
    final_aqi,
    aqi_table,
    job_config=bigquery.LoadJobConfig(
        write_disposition="WRITE_TRUNCATE",
        autodetect=True
    )
)
aqi_job.result()

weather_job = bq_client.load_table_from_dataframe(
    final_weather,
    weather_table,
    job_config=bigquery.LoadJobConfig(
        write_disposition="WRITE_TRUNCATE",
        autodetect=True
    )
)
weather_job.result()

print("Historical 1 Year AQI + Weather uploaded successfully")