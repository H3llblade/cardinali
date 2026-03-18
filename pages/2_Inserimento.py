import streamlit as st
from gestionale import registra_movimento

st.title("📝 Inserimento Movimenti")

tipo = st.selectbox("Tipo movimento", ["cassa","soldi_sporchi","fondo_cassa","foglie","panetti","bustine"])
causale = st.text_input("Causale")
valore = st.number_input("Importo (+ / -)", value=0.0)

if st.button("Registra"):
    if causale.strip():
        registra_movimento(tipo, causale, valore)
        st.success(f"{tipo} aggiornato di {valore}")
        st.experimental_rerun()
