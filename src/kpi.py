from google.cloud import bigquery
from google.oauth2 import service_account
import pandas as pd
import streamlit as st

# Création du client BigQuery à partir des secrets Streamlit
credentials_info = st.secrets["gcp"]
credentials = service_account.Credentials.from_service_account_info(credentials_info)
client = bigquery.Client(credentials=credentials, project=credentials_info["project_id"])

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
        st.error(f"Erreur BigQuery : {e}")
        return pd.DataFrame()
