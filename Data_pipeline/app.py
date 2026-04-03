from flask import Flask
import subprocess

app = Flask(__name__)

@app.route("/")
def run_sql_pipeline():
    subprocess.run(["python", "pipeline_sql.py"])
    return "SQL Feature Pipeline Completed"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)