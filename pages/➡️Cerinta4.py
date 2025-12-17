import streamlit as st
import pandas as pd
import plotly.express as px

st.title("🧮Cerinta 4 — Analiza coloana categorica")


df = st.session_state.get("df_filtered", None)
if df is None:
    df = st.session_state.get("df_original", None)

if df is None:
    st.warning("Incarca intai dataset-ul in Cerinta 1.")
    st.stop()

cat_cols = df.select_dtypes(exclude="number").columns.tolist()
if not cat_cols:
    st.error("Dataset-ul nu are coloane categorice (non-numerice).")
    st.stop()

col = st.selectbox("Selecteaza o coloana categorica", cat_cols)

freq = df[col].astype("object").fillna("NaN").value_counts(dropna=False)
freq_df = freq.reset_index()
freq_df.columns = [col, "frecventa"]
freq_df["procent"] = (freq_df["frecventa"] / freq_df["frecventa"].sum() * 100).round(2)

st.subheader("Count plot (bar chart) — frecvente")
fig = px.bar(freq_df, x=col, y="frecventa", title=f"Frecvente — {col}")
fig.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig, use_container_width=True)

st.subheader("Tabel frecvente absolute si procente")
st.dataframe(freq_df, use_container_width=True)
