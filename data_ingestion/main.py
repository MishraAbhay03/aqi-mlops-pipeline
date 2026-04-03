from flask import Flask
from fetch_aqi import fetch_aqi
from fetch_weather import fetch_weather
from bigquery_insert import insert_rows

app = Flask(__name__)

@app.route("/")
def run_pipeline():
    try:
        aqi_data = fetch_aqi()
        weather_data = fetch_weather()

        insert_rows("raw_aqi", aqi_data)
        insert_rows("raw_weather", weather_data)

        return "Live ingestion successful"

    except Exception as e:
        return str(e)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)