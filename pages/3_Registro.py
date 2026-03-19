import streamlit as st
import pandas as pd
from gestionale import formatta, aggiorna_file_github, aggiorna_dati_da_github

st.set_page_config(layout="wide")

st.title("📂 Registro Movimenti")
st.divider()

# Ricarica sempre i dati aggiornati
aggiorna_dati_da_github()

finanze = st.session_state.get("finanze", {})
movimenti = finanze.get("movimenti", [])

if movimenti:
    df = pd.DataFrame(movimenti)

    # Ordine dal più recente al più vecchio
    df = df.iloc[::-1].reset_index(drop=True)

    # Formattazione opzionale della colonna valore
    if "valore" in df.columns:
        df["valore"] = df["valore"].apply(lambda x: f"{formatta(x)} $")

    st.dataframe(df, use_container_width=True, hide_index=True)

    st.divider()

    col1, col2 = st.columns([1, 5])

    with col1:
        if st.button("🔄 Aggiorna registro", use_container_width=True):
            aggiorna_dati_da_github()
            st.rerun()

    with col2:
        if st.button("🗑️ Reset Registro", use_container_width=True):
            st.session_state.finanze["movimenti"] = []

            aggiorna_file_github(
                "data/finanze.json",
                st.session_state.finanze,
                "Reset registro movimenti"
            )

            st.success("Registro resettato correttamente.")
            st.rerun()
else:
    st.info("Nessun movimento registrato.")

    st.divider()

    col1, col2 = st.columns([1, 5])

    with col1:
        if st.button("🔄 Aggiorna registro", use_container_width=True):
            aggiorna_dati_da_github()
            st.rerun()

    with col2:
        if st.button("🗑️ Reset Registro", use_container_width=True):
            st.session_state.finanze["movimenti"] = []

            aggiorna_file_github(
                "data/finanze.json",
                st.session_state.finanze,
                "Reset registro movimenti"
            )

            st.success("Registro resettato correttamente.")
            st.rerun()
