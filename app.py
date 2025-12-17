import streamlit as st

st.set_page_config(
    page_title="Proiect Streamlit",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown(
    """
    <div style="text-align:center;">
        <h1>📚Streamlit — Proiect MAIA</h1>
        <h4 style="color: gray;">Petrescu Gabriela-Roxana, grupa 1127</h4>
    </div>
    """,
    unsafe_allow_html=True
)

st.divider()

st.write("")

st.info(
    "📌 **Foloseste meniul din stanga pentru a naviga intre cerinte.**\n\n"
    "➡ **Incepe cu pagina Cerinta 1** ca sa incarci dataset-ul.\n\n"
    "✔ Dupa incarcare, dataset-ul ramane disponibil in toate celelalte pagini."
)

st.divider()

st.subheader("📂 Structura aplicatiei")

col1, col2 = st.columns(2)

with col1:
    st.markdown(
        """
        **Cerinta 1**
        - Incarcare fisier
        - Filtrare date
        - Vizualizare dataframe
        """
    )

    st.markdown(
        """
        **Cerinta 3**
        - Analiza coloana numerica
        - Histograma
        - Box plot
        """
    )

with col2:
    st.markdown(
        """
        **Cerinta 2**
        - Overview dataset
        - Valori lipsa
        - Statistici descriptive
        """
    )

    st.markdown(
        """
        **Cerinta 4 & 5**
        - Analiza categorica
        - Corelatii
        - Detectie outlieri
        """
    )

st.divider()
