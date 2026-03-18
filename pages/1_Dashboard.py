import streamlit as st
from gestionale import st, formatta

dati = st.session_state.get("dati", {})

# ===============================
# TITOLO PRINCIPALE: CARDINALI
# ===============================
st.markdown("<h1 style='text-align:center;color:white;'>🦅 CARDINALI</h1>", unsafe_allow_html=True)
st.divider()

# ===============================
# PRIMO TITOLO: REGISTRO FINANZE
# ===============================
st.markdown("<h2 style='text-align:left;color:white;'>💰 Registro Finanze</h2>", unsafe_allow_html=True)
st.divider()

# TRE CONTATORI PRINCIPALI IN BOX COLORATI
col1, col2, col3 = st.columns(3, gap="large")
with col1:
    st.markdown(
        f"<div style='background-color:#1E1E1E;color:white;padding:30px;border-radius:15px;text-align:center;'>"
        f"<h3>💰 Cassa</h3>"
        f"<h2>{formatta(dati.get('cassa',0))} $</h2>"
        f"</div>", unsafe_allow_html=True)
with col2:
    st.markdown(
        f"<div style='background-color:#1E1E1E;color:white;padding:30px;border-radius:15px;text-align:center;'>"
        f"<h3>💸 Soldi Sporchi</h3>"
        f"<h2>{formatta(dati.get('soldi_sporchi',0))} $</h2>"
        f"</div>", unsafe_allow_html=True)
with col3:
    st.markdown(
        f"<div style='background-color:#1E1E1E;color:white;padding:30px;border-radius:15px;text-align:center;'>"
        f"<h3>💼 Fondo Cassa</h3>"
        f"<h2>{formatta(dati.get('fondo_cassa',0))} $</h2>"
        f"</div>", unsafe_allow_html=True)

st.divider()

# ===============================
# SECONDO TITOLO: PROCESSO COCA
# ===============================
st.markdown("<h2 style='text-align:left;color:white;'>🌿 Processo Coca</h2>", unsafe_allow_html=True)
st.divider()

# TRE CONTATORI DEL PROCESSO COCA IN BOX
col1, col2, col3 = st.columns(3, gap="large")
with col1:
    st.markdown(
        f"<div style='background-color:#3C3C3C;color:white;padding:30px;border-radius:15px;text-align:center;'>"
        f"<h3>🍃 Foglie</h3>"
        f"<h2>{formatta(dati.get('foglie',0))}</h2>"
        f"</div>", unsafe_allow_html=True)
with col2:
    st.markdown(
        f"<div style='background-color:#3C3C3C;color:white;padding:30px;border-radius:15px;text-align:center;'>"
        f"<h3>🧱 Panetti</h3>"
        f"<h2>{formatta(dati.get('panetti',0))}</h2>"
        f"</div>", unsafe_allow_html=True)
with col3:
    st.markdown(
        f"<div style='background-color:#3C3C3C;color:white;padding:30px;border-radius:15px;text-align:center;'>"
        f"<h3>💊 Bustine</h3>"
        f"<h2>{formatta(dati.get('bustine',0))}</h2>"
        f"</div>", unsafe_allow_html=True)
