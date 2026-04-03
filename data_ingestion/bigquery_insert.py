from google.cloud import bigquery

client = bigquery.Client()
dataset_id = "aqi_mlops"

def insert_rows(table, rows):
    table_id = f"{client.project}.{dataset_id}.{table}"

    if isinstance(rows, dict):
        rows = [rows]

    errors = client.insert_rows_json(table_id, rows)

    if errors:
        print("Errors:", errors)
    else:
        print(f"Inserted {len(rows)} rows into {table}")