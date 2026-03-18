# pages/1_Dashboard.py
import streamlit as st
from gestionale import formatta, st

# -------------------------------
# Assicurati che tutte le chiavi esistano
# -------------------------------
if "dati" not in st.session_state:
    st.session_state.dati = {
        "cassa": 0,
        "soldi_sporchi": 0,
        "fondo_cassa": 0,
        "movimenti": [],
        "foglie": 0,
        "panetti": 0,
        "bustine": 0
    }

# Titolo principale centrato
st.markdown("<h1 style='text-align:center;color:white;'>🦅 CARDINALI</h1>", unsafe_allow_html=True)
st.divider()

# ===============================
# PRIMA RIGA: FINANZE
# ===============================
st.markdown("<h2 style='text-align:left;'>💰 Registro Finanze</h2>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3, gap="large")

with col1:
    st.markdown(
        f"<div style='background-color:#1E1E1E;padding:20px;border-radius:10px;text-align:center;'>"
        f"<h3>💰 Cassa</h3><h2>{formatta(st.session_state.dati.get('cassa',0))} $</h2></div>", 
        unsafe_allow_html=True
    )
with col2:
    st.markdown(
        f"<div style='background-color:#1E1E1E;padding:20px;border-radius:10px;text-align:center;'>"
        f"<h3>💸 Soldi Sporchi</h3><h2>{formatta(st.session_state.dati.get('soldi_sporchi',0))} $</h2></div>", 
        unsafe_allow_html=True
    )
with col3:
    st.markdown(
        f"<div style='background-color:#1E1E1E;padding:20px;border-radius:10px;text-align:center;'>"
        f"<h3>💼 Fondo Cassa</h3><h2>{formatta(st.session_state.dati.get('fondo_cassa',0))} $</h2></div>", 
        unsafe_allow_html=True
    )

st.divider()

# ===============================
# SECONDA RIGA: PROCESSO COCA
# ===============================
st.markdown("<h2 style='text-align:left;'>🌿 Processo Coca</h2>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3, gap="large")

with col1:
    st.markdown(
        f"<div style='background-color:#2C2C2C;padding:20px;border-radius:10px;text-align:center;'>"
        f"<h3>🍃 Foglie</h3><h2>{formatta(st.session_state.dati.get('foglie',0))}</h2></div>", 
        unsafe_allow_html=True
    )
with col2:
    st.markdown(
        f"<div style='background-color:#2C2C2C;padding:20px;border-radius:10px;text-align:center;'>"
        f"<h3>🧱 Panetti</h3><h2>{formatta(st.session_state.dati.get('panetti',0))}</h2></div>", 
        unsafe_allow_html=True
    )
with col3:
    st.markdown(
        f"<div style='background-color:#2C2C2C;padding:20px;border-radius:10px;text-align:center;'>"
        f"<h3>💊 Bustine</h3><h2>{formatta(st.session_state.dati.get('bustine',0))}</h2></div>", 
        unsafe_allow_html=True
    )
                                      ~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^
