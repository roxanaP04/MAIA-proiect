import streamlit as st
import pandas as pd
import plotly.express as px

st.title("🔢Cerinta 3 — Analiza coloana numerica")


df = st.session_state.get("df_filtered", None)
if df is None:
    df = st.session_state.get("df_original", None)

if df is None:
    st.warning("Incarca intai dataset-ul in Cerinta 1.")
    st.stop()

num_cols = df.select_dtypes(include="number").columns.tolist()
if not num_cols:
    st.error("Dataset-ul nu are coloane numerice.")
    st.stop()

col = st.selectbox("Selecteaza o coloana numerica", num_cols)

bins = st.slider("Numar bins (10-100)", min_value=10, max_value=100, value=30)

series = df[col].dropna()

st.subheader("Histogram interactiv")
fig_h = px.histogram(series, nbins=bins, title=f"Histograma — {col}")
st.plotly_chart(fig_h, use_container_width=True)

st.subheader("Box plot")
fig_b = px.box(series, title=f"Box plot — {col}")
st.plotly_chart(fig_b, use_container_width=True)

mean_val = float(series.mean()) if len(series) else float("nan")
median_val = float(series.median()) if len(series) else float("nan")
std_val = float(series.std()) if len(series) else float("nan")

st.subheader("Statistici")
c1, c2, c3 = st.columns(3)
c1.metric("Medie", f"{mean_val:.4f}")
c2.metric("Mediana", f"{median_val:.4f}")
c3.metric("Deviatie standard", f"{std_val:.4f}") 
