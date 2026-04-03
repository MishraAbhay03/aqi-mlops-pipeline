CREATE OR REPLACE TABLE `stalwart-seat-484411-v0.aqi_mlops.base_data` AS
SELECT
    a.timestamp,
    a.city,
    a.pm25,
    a.pm10,
    a.no2,
    a.co,
    a.so2,
    a.o3,
    w.temperature,
    w.wind_speed
FROM `stalwart-seat-484411-v0.aqi_mlops.raw_aqi_clean` a
LEFT JOIN `stalwart-seat-484411-v0.aqi_mlops.raw_weather` w
ON a.city = w.city
AND TIMESTAMP_TRUNC(a.timestamp, HOUR) = TIMESTAMP_TRUNC(w.timestamp, HOUR)
WHERE a.pm25 IS NOT NULL;