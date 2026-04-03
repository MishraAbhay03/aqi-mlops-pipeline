# End-to-End AQI Prediction MLOps Pipeline

## Project Overview

This project is an end-to-end MLOps pipeline for Air Quality Index (AQI) prediction.
The system collects air pollution data, processes it, trains multiple machine learning models, generates predictions, and deploys the prediction system through a dashboard and cloud deployment.

The project demonstrates a complete machine learning lifecycle including data ingestion, preprocessing, model training, prediction, pipeline automation, and deployment.

---

## Project Architecture

The pipeline follows this workflow:

Data Ingestion → Data Processing → Feature Engineering → Model Training → Model Storage → Prediction Pipeline → Dashboard → Deployment

---

## Project Structure

```
aqi-mlops-gcp/
│
├── aqi_dash/            # Dashboard application
├── data_ingestion/      # Data collection scripts
├── data_processing/     # Data preprocessing and cleaning
├── Data_pipeline/       # Pipeline automation
├── pipelines/           # Training & prediction pipelines
├── training/            # Model training scripts
├── prediction/          # Prediction scripts
├── sql/                 # SQL queries / database scripts
├── scripts/             # Utility scripts
│
├── models (.joblib)     # Trained ML models
├── requirements         # Python dependencies
├── README               # Project documentation
└── .gitignore
```

---

## Machine Learning Models Used

The project trains multiple models for different pollutants:

* Random Forest
* XGBoost
* LightGBM

Models are trained for:

* CO
* NO2
* SO2
* O3
* PM2.5
* PM10

All trained models are saved as `.joblib` files.

---

## Features

* Automated data ingestion pipeline
* Data preprocessing pipeline
* Multiple ML model training
* Model saving and loading
* Prediction pipeline
* AQI Dashboard
* End-to-end ML pipeline
* Docker & Cloud deployment ready
* Modular project structure

---

## Installation

Clone the repository:

```
git clone https://github.com/yourusername/End-to-end-Mlops-AQI-Prediction-System.git
cd End-to-end-Mlops-AQI-Prediction-System
```

Install dependencies:

```
pip install -r requirements
```

---

## Training the Models

Run the training pipeline:

```
python training/train.py
```

---

## Running Prediction

```
python prediction/predict.py
```

---

## Running Dashboard

```
python aqi_dash/app.py
```

---

## MLOps Pipeline Components

This project includes the following MLOps components:

* Data Ingestion
* Data Validation
* Data Processing
* Model Training
* Model Evaluation
* Model Storage
* Prediction Pipeline
* Dashboard Visualization
* Containerization
* Cloud Deployment

---

## Tools & Technologies Used

* Python
* Pandas
* NumPy
* Scikit-learn
* XGBoost
* LightGBM
* Flask / Dashboard
* Docker
* Google Cloud Run
* GitHub
* SQL

---

## Future Improvements

* CI/CD pipeline integration
* Model versioning
* Experiment tracking (MLflow)
* Data versioning
* Model monitoring
* Automated retraining pipeline

---

## Author

Abhaykumar Mishra
MSc Computer Science
AI/ML | Data Science | MLOps
