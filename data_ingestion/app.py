from flask import Flask
import subprocess

app = Flask(__name__)

@app.route("/")
def run_pipeline():
    subprocess.run(["python", "fetch_aqi.py"])
    return "AQI ingestion completed"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)