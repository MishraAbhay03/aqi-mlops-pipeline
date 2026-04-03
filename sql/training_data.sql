CREATE OR REPLACE TABLE `stalwart-seat-484411-v0.aqi_mlops.training_data` AS
SELECT
    *,
    LEAD(pm25, 1) OVER(PARTITION BY city ORDER BY timestamp) AS target_pm25,
    LEAD(pm10, 1) OVER(PARTITION BY city ORDER BY timestamp) AS target_pm10,
    LEAD(no2, 1) OVER(PARTITION BY city ORDER BY timestamp) AS target_no2,
    LEAD(co, 1) OVER(PARTITION BY city ORDER BY timestamp) AS target_co,
    LEAD(so2, 1) OVER(PARTITION BY city ORDER BY timestamp) AS target_so2,
    LEAD(o3, 1) OVER(PARTITION BY city ORDER BY timestamp) AS target_o3
FROM `stalwart-seat-484411-v0.aqi_mlops.features`;