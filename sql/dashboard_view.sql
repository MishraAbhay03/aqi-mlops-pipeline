CREATE OR REPLACE VIEW `stalwart-seat-484411-v0.aqi_mlops.dashboard_data` AS

-- ACTUAL DATA
SELECT
    timestamp,
    city,
    pm25,
    pm10,
    no2,
    so2,
    co,
    o3,
    GREATEST(
        pm25 * 4,
        pm10 * 2,
        no2 * 1.5,
        so2 * 1.2,
        co * 0.1,
        o3 * 1.3
    ) AS aqi,
    'actual' AS type
FROM `stalwart-seat-484411-v0.aqi_mlops.base_data`

UNION ALL

-- FORECAST DATA
SELECT
    timestamp,
    city,
    pm25,
    pm10,
    no2,
    so2,
    co,
    o3,
    GREATEST(
        pm25 * 4,
        pm10 * 2,
        no2 * 1.5,
        so2 * 1.2,
        co * 0.1,
        o3 * 1.3
    ) AS aqi,
    'forecast' AS type
FROM `stalwart-seat-484411-v0.aqi_mlops.forecast`;