from google.cloud import bigquery
import pandas as pd


client = bigquery.Client.from_service_account_json("assets/key.json")  

def get_kpi_data():
    QUERY = """
    SELECT timestamp, event_type, account_id, product_url
    FROM `amazon-bot-kpi.bot_metrics.kpi_table`
    ORDER BY timestamp DESC
    LIMIT 10000
    """
    try:
        df = client.query(QUERY).to_dataframe()
        return df
    except Exception as e:
        print("Erreur BigQuery:", e)
        return pd.DataFrame()