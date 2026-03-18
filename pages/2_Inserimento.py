import streamlit as st
from gestionale import registra_movimento

st.title("📝 Inserimento Movimenti")
st.divider()

# Tre colonne compatte per inserimento dati
col1, col2, col3 = st.columns([1,2,1])

with col1:
    tipo = st.selectbox("Tipo movimento", 
                        ["cassa","soldi_sporchi","fondo_cassa","foglie","panetti","bustine"])

with col2:
    causale = st.text_input("Causale")

with col3:
    valore = st.number_input("Importo (+ / -)", value=0.0)

# Pulsante di registrazione sotto le colonne, centrato
if st.button("✅ Registra Movimento"):
    if causale.strip():
        registra_movimento(tipo, causale, valore)
        st.success(f"{tipo} aggiornato di {valore}")
        st.experimental_rerun()
    else:
        st.warning("Inserisci una causale valida")
