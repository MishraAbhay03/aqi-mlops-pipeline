from google.cloud import bigquery

PROJECT_ID = "stalwart-seat-484411-v0"
DATASET = "aqi_mlops"

client = bigquery.Client()

def run_query(query, name):
    print(f"Running {name}...")
    job = client.query(query)
    job.result()
    print(f"{name} completed.")


# 1 Clean AQI Data
clean_query = f"""
CREATE OR REPLACE TABLE `{PROJECT_ID}.{DATASET}.raw_aqi_clean` AS
SELECT *
FROM `{PROJECT_ID}.{DATASET}.raw_aqi`
WHERE pm25 IS NOT NULL
AND pm10 IS NOT NULL
"""


# 2 Base Data
base_query = f"""
CREATE OR REPLACE TABLE `{PROJECT_ID}.{DATASET}.base_data` AS
SELECT
    a.timestamp,
    a.city,
    a.pm25,
    a.pm10,
    a.co,
    a.no2,
    a.so2,
    a.o3,
    a.aqi,
    w.temperature,
    w.humidity,
    w.wind_speed
FROM `{PROJECT_ID}.{DATASET}.raw_aqi_clean` a
LEFT JOIN `{PROJECT_ID}.{DATASET}.raw_weather` w
ON a.city = w.city
AND a.timestamp = w.timestamp
"""


# 3 Feature Engineering (Improved)
feature_query = f"""
CREATE OR REPLACE TABLE `{PROJECT_ID}.{DATASET}.features` AS
SELECT
    base.*,

    -- PM25 Lag Features
    LAG(pm25,1) OVER(PARTITION BY city ORDER BY timestamp) AS pm25_lag1,
    LAG(pm25,3) OVER(PARTITION BY city ORDER BY timestamp) AS pm25_lag3,
    LAG(pm25,6) OVER(PARTITION BY city ORDER BY timestamp) AS pm25_lag6,
    LAG(pm25,12) OVER(PARTITION BY city ORDER BY timestamp) AS pm25_lag12,
    LAG(pm25,24) OVER(PARTITION BY city ORDER BY timestamp) AS pm25_lag24,
    LAG(pm25,48) OVER(PARTITION BY city ORDER BY timestamp) AS pm25_lag48,
    LAG(pm25,72) OVER(PARTITION BY city ORDER BY timestamp) AS pm25_lag72,
    LAG(pm25,168) OVER(PARTITION BY city ORDER BY timestamp) AS pm25_lag168,

    -- Other Pollutant Lags
    LAG(pm10,24) OVER(PARTITION BY city ORDER BY timestamp) AS pm10_lag24,
    LAG(no2,24) OVER(PARTITION BY city ORDER BY timestamp) AS no2_lag24,
    LAG(co,24) OVER(PARTITION BY city ORDER BY timestamp) AS co_lag24,
    LAG(so2,24) OVER(PARTITION BY city ORDER BY timestamp) AS so2_lag24,
    LAG(o3,24) OVER(PARTITION BY city ORDER BY timestamp) AS o3_lag24,

    -- AQI Lag
    LAG(aqi,1) OVER(PARTITION BY city ORDER BY timestamp) AS aqi_lag1,
    LAG(aqi,24) OVER(PARTITION BY city ORDER BY timestamp) AS aqi_lag24,

    -- Rolling Mean
    AVG(pm25) OVER(PARTITION BY city ORDER BY timestamp ROWS BETWEEN 24 PRECEDING AND CURRENT ROW) AS pm25_roll24,
    AVG(pm25) OVER(PARTITION BY city ORDER BY timestamp ROWS BETWEEN 72 PRECEDING AND CURRENT ROW) AS pm25_roll72,
    AVG(pm25) OVER(PARTITION BY city ORDER BY timestamp ROWS BETWEEN 168 PRECEDING AND CURRENT ROW) AS pm25_roll168,

    AVG(aqi) OVER(PARTITION BY city ORDER BY timestamp ROWS BETWEEN 24 PRECEDING AND CURRENT ROW) AS aqi_roll24,

    -- Rolling Std Dev
    STDDEV(pm25) OVER(PARTITION BY city ORDER BY timestamp ROWS BETWEEN 24 PRECEDING AND CURRENT ROW) AS pm25_std24,
    STDDEV(aqi) OVER(PARTITION BY city ORDER BY timestamp ROWS BETWEEN 24 PRECEDING AND CURRENT ROW) AS aqi_std24,

    -- Time Features
    EXTRACT(HOUR FROM timestamp) AS hour,
    EXTRACT(DAYOFWEEK FROM timestamp) AS day_of_week,
    EXTRACT(DAY FROM timestamp) AS day_of_month,
    EXTRACT(MONTH FROM timestamp) AS month,
    EXTRACT(DAYOFYEAR FROM timestamp) AS day_of_year,
    EXTRACT(WEEK FROM timestamp) AS week_of_year

FROM `{PROJECT_ID}.{DATASET}.base_data` base;
"""


# 4 Training Data
training_query = f"""
CREATE OR REPLACE TABLE `aqi_mlops.training_data` AS
SELECT
    *,
    LEAD(pm25,1) OVER(PARTITION BY city ORDER BY timestamp) AS target_pm25,
    LEAD(pm10,1) OVER(PARTITION BY city ORDER BY timestamp) AS target_pm10,
    LEAD(no2,1) OVER(PARTITION BY city ORDER BY timestamp) AS target_no2,
    LEAD(co,1) OVER(PARTITION BY city ORDER BY timestamp) AS target_co,
    LEAD(so2,1) OVER(PARTITION BY city ORDER BY timestamp) AS target_so2,
    LEAD(o3,1) OVER(PARTITION BY city ORDER BY timestamp) AS target_o3,
    LEAD(aqi,1) OVER(PARTITION BY city ORDER BY timestamp) AS target_aqi
FROM `aqi_mlops.features`
WHERE pm25_lag24 IS NOT NULL;
"""


run_query(clean_query, "Clean Data")
run_query(base_query, "Base Data")
run_query(feature_query, "Feature Engineering")
run_query(training_query, "Training Data")

print("SQL Feature Pipeline Completed Successfully")