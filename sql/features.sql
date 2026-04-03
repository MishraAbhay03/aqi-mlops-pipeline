CREATE OR REPLACE TABLE `stalwart-seat-484411-v0.aqi_mlops.features` AS
SELECT
    *,
    
    -- Pollutant lag features
    LAG(pm25, 1) OVER(PARTITION BY city ORDER BY timestamp) AS pm25_lag1,
    LAG(pm25, 2) OVER(PARTITION BY city ORDER BY timestamp) AS pm25_lag2,
    LAG(pm25, 24) OVER(PARTITION BY city ORDER BY timestamp) AS pm25_lag24,
    LAG(pm25, 168) OVER(PARTITION BY city ORDER BY timestamp) AS pm25_lag168,

    LAG(pm10, 24) OVER(PARTITION BY city ORDER BY timestamp) AS pm10_lag24,
    LAG(no2, 24) OVER(PARTITION BY city ORDER BY timestamp) AS no2_lag24,
    LAG(co, 24) OVER(PARTITION BY city ORDER BY timestamp) AS co_lag24,
    LAG(so2, 24) OVER(PARTITION BY city ORDER BY timestamp) AS so2_lag24,
    LAG(o3, 24) OVER(PARTITION BY city ORDER BY timestamp) AS o3_lag24,

    -- AQI lag features
    LAG(aqi, 1) OVER(PARTITION BY city ORDER BY timestamp) AS aqi_lag1,
    LAG(aqi, 2) OVER(PARTITION BY city ORDER BY timestamp) AS aqi_lag2,
    LAG(aqi, 24) OVER(PARTITION BY city ORDER BY timestamp) AS aqi_lag24,
    LAG(aqi, 168) OVER(PARTITION BY city ORDER BY timestamp) AS aqi_lag168,

    -- Rolling features
    AVG(pm25) OVER(PARTITION BY city ORDER BY timestamp ROWS BETWEEN 24 PRECEDING AND CURRENT ROW) AS pm25_roll24,
    AVG(pm25) OVER(PARTITION BY city ORDER BY timestamp ROWS BETWEEN 72 PRECEDING AND CURRENT ROW) AS pm25_roll72,
    AVG(pm25) OVER(PARTITION BY city ORDER BY timestamp ROWS BETWEEN 168 PRECEDING AND CURRENT ROW) AS pm25_roll168,

    AVG(aqi) OVER(PARTITION BY city ORDER BY timestamp ROWS BETWEEN 24 PRECEDING AND CURRENT ROW) AS aqi_roll24,
    AVG(aqi) OVER(PARTITION BY city ORDER BY timestamp ROWS BETWEEN 72 PRECEDING AND CURRENT ROW) AS aqi_roll72,
    AVG(aqi) OVER(PARTITION BY city ORDER BY timestamp ROWS BETWEEN 168 PRECEDING AND CURRENT ROW) AS aqi_roll168,

    AVG(temperature) OVER(PARTITION BY city ORDER BY timestamp ROWS BETWEEN 24 PRECEDING AND CURRENT ROW) AS temp_roll24,
    AVG(wind_speed) OVER(PARTITION BY city ORDER BY timestamp ROWS BETWEEN 24 PRECEDING AND CURRENT ROW) AS wind_roll24,

    -- Time features
    EXTRACT(HOUR FROM timestamp) AS hour,
    EXTRACT(DAYOFWEEK FROM timestamp) AS day_of_week,
    EXTRACT(DAY FROM timestamp) AS day_of_month,
    EXTRACT(MONTH FROM timestamp) AS month,
    EXTRACT(DAYOFYEAR FROM timestamp) AS day_of_year,
    EXTRACT(WEEK FROM timestamp) AS week_of_year,

    -- Cyclical features
    SIN(2 * PI() * EXTRACT(HOUR FROM timestamp) / 24) AS sin_hour,
    COS(2 * PI() * EXTRACT(HOUR FROM timestamp) / 24) AS cos_hour,
    SIN(2 * PI() * EXTRACT(MONTH FROM timestamp) / 12) AS sin_month,
    COS(2 * PI() * EXTRACT(MONTH FROM timestamp) / 12) AS cos_month

FROM `stalwart-seat-484411-v0.aqi_mlops.base_data`;