import streamlit as st
import time
from gestionale import formatta, aggiorna_dati_da_github

# =========================
# AUTO REFRESH (senza librerie)
# =========================
if "last_refresh" not in st.session_state:
    st.session_state.last_refresh = time.time()

# ogni 5 secondi aggiorna
if time.time() - st.session_state.last_refresh > 5:
    st.session_state.last_refresh = time.time()
    st.rerun()

# =========================
# CARICAMENTO DATI
# =========================
aggiorna_dati_da_github()

finanze = st.session_state.get("finanze", {})
coca = st.session_state.get("coca", {})

# =========================
# UI
# =========================
st.markdown(
    "<h1 style='text-align:center; color:white;'>🦅 CARDINALI</h1>",
    unsafe_allow_html=True
)

st.divider()

# =========================
# REGISTRO FINANZE
# =========================
st.markdown(
    "<h2 style='color:white;'>💰 Registro Finanze</h2>",
    unsafe_allow_html=True
)

st.divider()

col1, col2, col3 = st.columns(3)

col1.metric("💰 Cassa", f"{formatta(finanze.get('cassa', 0))} $")
col2.metric("💸 Soldi Sporchi", f"{formatta(finanze.get('soldi_sporchi', 0))} $")
col3.metric("💼 Fondo Cassa", f"{formatta(finanze.get('fondo_cassa', 0))} $")

st.divider()

# =========================
# PROCESSO COCA
# =========================
st.markdown(
    "<h2 style='color:white;'>🌿 Processo Coca</h2>",
    unsafe_allow_html=True
)

st.divider()

col4, col5, col6 = st.columns(3)

col4.metric("🍃 Foglie", formatta(coca.get("foglie", 0)))
col5.metric("🧱 Panetti", formatta(coca.get("panetti", 0)))
col6.metric("💊 Bustine", formatta(coca.get("bustine", 0)))

st.divider()

# refresh manuale
if st.button("🔄 Aggiorna ora"):
    aggiorna_dati_da_github()
    st.rerun()
