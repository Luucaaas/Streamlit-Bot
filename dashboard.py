import streamlit as st
import pandas as pd
import plotly.express as px
from google.oauth2 import service_account
from google.cloud import bigquery
from src.kpi import get_kpi_data

st.set_page_config(page_title="📊 Bot Amazon - KPI Dashboard", layout="wide")
st.title("📊 Tableau de bord du Bot Amazon")

# Authentification sécurisée via les secrets Streamlit
credentials_info = st.secrets["gcp"]
credentials = service_account.Credentials.from_service_account_info(credentials_info)


# Récupérer les données depuis BigQuery (en supposant que get_kpi_data utilise les credentials par défaut)
df = get_kpi_data()

# Vérifier les données
if df.empty:
    st.warning("Aucune donnée KPI trouvée.")
else:
    # Filtres
    with st.sidebar:
        st.header("🔍 Filtres")
        selected_account = st.selectbox("Compte Amazon", options=["Tous"] + sorted(df["account_id"].unique().tolist()))
        selected_status = st.multiselect("Statuts", options=df["event_type"].unique().tolist(), default=df["event_type"].unique().tolist())

    # Appliquer les filtres
    if selected_account != "Tous":
        df = df[df["account_id"] == selected_account]
    df = df[df["event_type"].isin(selected_status)]

    # Afficher les KPIs
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("📦 Tentatives", len(df))
    col2.metric("✅ Succès", len(df[df.event_type == "success"]))
    col3.metric("❌ Erreurs", len(df[df.event_type == "error"]))
    col4.metric("⛔ Indisponibles", len(df[df.event_type == "unavailable"]))

    # ➕ Pie chart : Répartition des événements
    event_counts = df["event_type"].value_counts().reset_index()
    event_counts.columns = ["event_type", "count"]
    fig = px.pie(event_counts, names="event_type", values="count", title="Répartition des types d'événements")
    st.plotly_chart(fig, use_container_width=True)

    # 📈 Graphique temporel
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    chart = df.groupby([df["timestamp"].dt.date, "event_type"]).size().unstack().fillna(0)
    st.line_chart(chart)

    # 📋 Table complète
    st.subheader("📋 Détail des données")
    st.dataframe(df)
