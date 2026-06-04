# 🌫️ AQI MLOps Pipeline

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![XGBoost](https://img.shields.io/badge/XGBoost-FF6600?style=for-the-badge&logo=xgboost&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![GCP](https://img.shields.io/badge/GCP-4285F4?style=for-the-badge&logo=googlecloud&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![BigQuery](https://img.shields.io/badge/BigQuery-4285F4?style=for-the-badge&logo=googlebigquery&logoColor=white)

> End-to-end MLOps pipeline for Air Quality Index (AQI) prediction — **92%+ model accuracy** — containerized with Docker and deployed on GCP Cloud Run.

---

## 📌 Overview

This project implements a production-grade MLOps pipeline that ingests air quality data, trains ensemble ML models, serves predictions via a REST API, and automates the entire workflow using CI/CD on Google Cloud Platform.

---

## 🏗️ Architecture

```
Data Ingestion (BigQuery)
        ↓
Data Pipeline (Python)
        ↓
Model Training (XGBoost + LightGBM)
        ↓
REST API (FastAPI)
        ↓
Containerization (Docker)
        ↓
Deployment (GCP Cloud Run)
        ↓
Dashboard (Streamlit)
```

---

## ✨ Key Features

- ✅ **92%+ accuracy** using XGBoost + LightGBM ensemble methods
- ✅ End-to-end ML pipeline: ingestion → training → serving
- ✅ **FastAPI** REST endpoint for real-time & batch AQI predictions
- ✅ **Docker** containerized for consistent deployment
- ✅ Deployed on **GCP Cloud Run** with automated CI pipeline
- ✅ **BigQuery** for scalable data ingestion
- ✅ Interactive **Streamlit** dashboard

---

## 📁 Project Structure

```
aqi-mlops-pipeline/
├── Data_pipeline/       # Data preprocessing scripts
├── data_ingestion/      # BigQuery ingestion logic
├── training/            # Model training pipeline
├── prediction/          # Prediction & inference logic
├── pipelines/           # End-to-end pipeline orchestration
├── aqi_dash/            # Streamlit dashboard
├── scripts/             # Utility scripts
├── sql/                 # SQL queries for BigQuery
├── requirements.txt     # Python dependencies
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- Docker
- GCP account with BigQuery & Cloud Run enabled

### Installation

```bash
git clone https://github.com/MishraAbhay03/aqi-mlops-pipeline.git
cd aqi-mlops-pipeline
pip install -r requirements.txt
```

### Run Locally

```bash
# Start FastAPI server
uvicorn app:app --reload

# Run Streamlit dashboard
streamlit run aqi_dash/app.py
```

### Docker

```bash
docker build -t aqi-mlops .
docker run -p 8000:8000 aqi-mlops
```

---

## 📊 Model Performance

| Model | Accuracy | RMSE |
|---|---|---|
| XGBoost | 91.2% | 8.3 |
| LightGBM | 90.8% | 8.6 |
| **Ensemble** | **92.4%** | **7.9** |

---

## 🛠️ Tech Stack

| Category | Tools |
|---|---|
| ML Models | XGBoost, LightGBM, Scikit-learn |
| API | FastAPI, Uvicorn |
| Cloud | GCP Cloud Run, BigQuery, Vertex AI |
| DevOps | Docker, CI/CD |
| Visualization | Streamlit, Matplotlib |

---

## 👤 Author

**Abhaykumar Mishra** — [GitHub](https://github.com/MishraAbhay03) · [LinkedIn](https://linkedin.com/in/YOUR_LINKEDIN)

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.
