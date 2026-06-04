# 🌫️ End-to-End MLOps AQI Prediction System

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://docker.com)
[![GCP](https://img.shields.io/badge/GCP_Cloud_Run-4285F4?style=for-the-badge&logo=googlecloud&logoColor=white)](https://cloud.google.com)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)

> A production-grade MLOps pipeline for predicting Air Quality Index (AQI) using ensemble ML models, deployed on Google Cloud Run via Docker with automated CI.

---

## 📊 Results

| Metric | Value |
|--------|-------|
| Best Model Accuracy | **92%+** |
| Models Used | XGBoost, LightGBM (Ensemble) |
| Deployment | GCP Cloud Run (REST API) |
| Data Store | Google BigQuery |

---

## 🏗️ Architecture

```
 Raw Data (CSV / BigQuery)
        │
        ▼
  Data Ingestion Pipeline
        │
        ▼
  Feature Engineering & Validation
        │
        ▼
  Model Training (XGBoost + LightGBM)
        │
        ▼
  Model Registry & Evaluation
        │
        ▼
  FastAPI Prediction Service
        │
        ▼
  Docker Container → GCP Cloud Run
```

---

## 🛠️ Tech Stack

| Layer | Tools |
|-------|-------|
| ML Models | XGBoost, LightGBM, Scikit-learn |
| API | FastAPI |
| Containerization | Docker |
| Cloud | GCP Cloud Run, BigQuery |
| CI Pipeline | Automated |
| Language | Python 3.10+ |

---

## 📁 Project Structure

```
├── Data_pipeline/        # Data ingestion & preprocessing
├── data_ingestion/       # BigQuery connectors
├── training/             # Model training scripts
├── pipelines/            # ML pipeline orchestration
├── prediction/           # Inference logic
├── aqi_dash/             # Dashboard components
├── scripts/              # Utility scripts
├── sql/                  # BigQuery SQL queries
├── requirements.txt      # Dependencies
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Docker
- GCP account with BigQuery & Cloud Run enabled

### Local Setup

```bash
# Clone the repository
git clone https://github.com/MishraAbhay03/End-to-end-Mlops-AQI-Prediction-Sysytem.git
cd End-to-end-Mlops-AQI-Prediction-Sysytem

# Install dependencies
pip install -r requirements.txt

# Run the API locally
uvicorn prediction.main:app --reload
```

### Docker

```bash
# Build
docker build -t aqi-predictor .

# Run
docker run -p 8000:8000 aqi-predictor
```

### API Usage

```bash
curl -X POST http://localhost:8000/predict \
  -H 'Content-Type: application/json' \
  -d '{"pm25": 45.2, "pm10": 80.1, "no2": 30.5, "so2": 12.3}'
```

---

## 📈 Model Performance

- **XGBoost**: 90.2% accuracy
- **LightGBM**: 91.8% accuracy
- **Ensemble**: 92%+ accuracy
- Feature importance: PM2.5, PM10, NO2 are top predictors

---

## 👤 Author

**Abhaykumar Mishra**  
M.Sc. Data Science & AI | Mumbai  
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=flat&logo=linkedin)](https://linkedin.com/in/YOUR_LINKEDIN) [![GitHub](https://img.shields.io/badge/GitHub-Follow-181717?style=flat&logo=github)](https://github.com/MishraAbhay03)

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
