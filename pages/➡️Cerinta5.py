import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from scipy.stats import pearsonr

st.title("📉Cerinta 5 — Corelatii + Outlieri (IQR)")


df = st.session_state.get("df_filtered", None)
if df is None:
    df = st.session_state.get("df_original", None)

if df is None:
    st.warning("Incarca intai dataset-ul in Cerinta 1.")
    st.stop()

num_df = df.select_dtypes(include="number")
num_cols = num_df.columns.tolist()

if len(num_cols) < 2:
    st.error("Ai nevoie de minim 2 coloane numerice pentru corelatii.")
    st.stop()


st.subheader("Matrice de corelatie + heatmap")
corr = num_df.corr(numeric_only=True)

fig_hm = px.imshow(
    corr,
    text_auto=True,
    title="Heatmap corelatii (numerice)"
)
st.plotly_chart(fig_hm, use_container_width=True)

st.divider()


st.subheader("Scatter plot + Pearson")

x = st.selectbox("Selecteaza X", num_cols, index=0)
y = st.selectbox("Selecteaza Y", num_cols, index=1)

tmp = num_df[[x, y]].dropna()


fig_sc = px.scatter(
    tmp,
    x=x,
    y=y,
    title=f"Scatter: {x} vs {y}"
)

# OPTIONAL: linie de trend simpla (regresie liniara) cu numpy, fara statsmodels
if len(tmp) >= 2 and tmp[x].nunique() > 1:
    try:
        m, b = np.polyfit(tmp[x], tmp[y], 1)
        x_line = np.linspace(tmp[x].min(), tmp[x].max(), 100)
        y_line = m * x_line + b
        fig_sc.add_trace(go.Scatter(x=x_line, y=y_line, mode="lines", name="Trend line"))
    except Exception:
        pass

st.plotly_chart(fig_sc, use_container_width=True)

if len(tmp) >= 2 and tmp[x].nunique() > 1 and tmp[y].nunique() > 1:
    r, p = pearsonr(tmp[x], tmp[y])
    st.write(f"Coeficient Pearson r: **{r:.4f}** | p-value: **{p:.4g}**")
else:
    st.warning("Nu pot calcula Pearson (prea putine valori sau variatie insuficienta).")

st.divider()


st.subheader("Detectie outlieri cu metoda IQR")

outlier_rows = []

for col in num_cols:
    s = num_df[col].dropna()
    if len(s) < 4:
        outlier_rows.append([col, 0, 0.0])
        continue

    q1 = s.quantile(0.25)
    q3 = s.quantile(0.75)
    iqr = q3 - q1

    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr

    outliers = s[(s < lower) | (s > upper)]
    count = int(outliers.shape[0])
    pct = round(count / s.shape[0] * 100, 2) if s.shape[0] else 0.0

    outlier_rows.append([col, count, pct])

out_df = pd.DataFrame(outlier_rows, columns=["coloana", "nr_outlieri", "procent_outlieri"])

st.dataframe(out_df.sort_values("nr_outlieri", ascending=False), use_container_width=True)


st.subheader("Vizualizare outlieri (box plot)")

col_o = st.selectbox("Alege coloana pentru vizualizarea outlierilor", num_cols)

fig_box = px.box(
    num_df,
    y=col_o,
    points="outliers",
    title=f"Outlieri (IQR) — {col_o}"
)
st.plotly_chart(fig_box, use_container_width=True)
