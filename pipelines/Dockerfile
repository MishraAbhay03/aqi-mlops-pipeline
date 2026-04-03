FROM python:3.11

WORKDIR /app

COPY train_vertex.py .

RUN pip install --no-cache-dir \
    pandas \
    numpy \
    scikit-learn \
    lightgbm \
    xgboost \
    joblib \
    google-cloud-bigquery \
    google-cloud-storage \
    db-dtypes \
    pyarrow

CMD ["python", "train_vertex.py"]