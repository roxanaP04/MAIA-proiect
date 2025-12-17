import streamlit as st
import pandas as pd
import plotly.express as px

st.title("📋Cerinta 2 — Overview + Valori lipsa")


df = st.session_state.get("df_filtered", None)
if df is None:
    df = st.session_state.get("df_original", None)

if df is None:
    st.warning("Incarca intai dataset-ul in Cerinta 1.")
    st.stop()


st.subheader("Dimensiuni dataset")
st.write(f"Randuri: **{df.shape[0]}** | Coloane: **{df.shape[1]}**")


st.subheader("Tipuri de date pe coloana")
dtypes_df = pd.DataFrame({
    "coloana": df.columns,
    "dtype": df.dtypes.astype(str)
})
st.dataframe(dtypes_df, use_container_width=True)


st.subheader("Valori lipsa")
missing_count = df.isna().sum()
missing_percent = (missing_count / len(df) * 100).round(2)

missing_table = pd.DataFrame({
    "coloana": df.columns,
    "missing_count": missing_count.values,
    "missing_percent": missing_percent.values
}).sort_values("missing_count", ascending=False)

missing_cols = missing_table[missing_table["missing_count"] > 0]

st.write(f"Coloane cu valori lipsa: **{missing_cols.shape[0]}**")
st.dataframe(missing_table, use_container_width=True)


st.subheader("Grafic valori lipsa (procent per coloana)")
fig = px.bar(
    missing_table,
    x="coloana",
    y="missing_percent",
    title="Procent valori lipsa per coloana"
)
fig.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig, use_container_width=True)


st.subheader("Statistici descriptive pentru coloane numerice")
st.dataframe(df.describe().T, use_container_width=True)
