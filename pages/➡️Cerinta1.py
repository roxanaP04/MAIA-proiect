import streamlit as st
import pandas as pd

st.title("⬆️Cerinta 1 — Incarcare + Filtrare")

@st.cache_data
def load_data(file):
    name = file.name.lower()
    if name.endswith(".csv"):
        return pd.read_csv(file)
    elif name.endswith(".xlsx") or name.endswith(".xls"):
        return pd.read_excel(file)
    else:
        raise ValueError("Format neacceptat. Incearca CSV sau Excel.")

uploaded = st.file_uploader("Incarca un fisier CSV sau Excel", type=["csv", "xlsx", "xls"])

if uploaded is None:
    st.warning("Incarca un fisier ca sa continui.")
    st.stop()

try:
    df = load_data(uploaded)
    st.session_state["df_original"] = df.copy()
    st.success("Fișierul a fost citit corect!")
except Exception as e:
    st.error(f"Eroare la citire: {e}")
    st.stop()

st.subheader("Primele 10 randuri din dataset")
st.dataframe(df.head(10), use_container_width=True)

st.divider()
st.subheader("Filtrare date")

df_work = df.copy()
rows_before = len(df_work)

num_cols = df_work.select_dtypes(include="number").columns.tolist()
cat_cols = df_work.select_dtypes(exclude="number").columns.tolist()

st.write(f"Coloane numerice: **{len(num_cols)}** | Coloane categorice: **{len(cat_cols)}**")

with st.expander("Filtrare coloane numerice", expanded=True):
    for col in num_cols:
        col_min = float(df_work[col].min())
        col_max = float(df_work[col].max())
        if pd.isna(col_min) or pd.isna(col_max) or col_min == col_max:
            continue
        selected = st.slider(
            f"{col}",
            min_value=col_min,
            max_value=col_max,
            value=(col_min, col_max),
        )
        df_work = df_work[df_work[col].between(selected[0], selected[1], inclusive="both")]

with st.expander("Filtrare coloane categorice", expanded=True):
    for col in cat_cols:
        options = df[col].dropna().unique().tolist()
        if len(options) == 0:
            continue
        selected = st.multiselect(f"{col}", options=options, default=options)
        df_work = df_work[df_work[col].isin(selected) | df_work[col].isna()]

rows_after = len(df_work)

st.write(f"📌 Randuri inainte filtrare: **{rows_before}**")
st.write(f"📌 Randuri dupa filtrare: **{rows_after}**")

st.subheader("DataFrame filtrat")
st.dataframe(df_work, use_container_width=True)

st.session_state["df_filtered"] = df_work.copy()
