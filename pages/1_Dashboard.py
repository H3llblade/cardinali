import streamlit as st
from gestionale import st, formatta

dati = st.session_state.get("dati", {})

# ===============================
# PRIMO TITOLO: REGISTRO FINANZE
# ===============================
st.markdown("<h1 style='text-align:center;color:white;'>💰 Registro Finanze</h1>", unsafe_allow_html=True)
st.divider()

# TRE CONTATORI PRINCIPALI
col1, col2, col3 = st.columns(3, gap="large")
with col1:
    st.metric("💰 Cassa", dati.get("cassa",0))
with col2:
    st.metric("💸 Soldi Sporchi", dati.get("soldi_sporchi",0))
with col3:
    st.metric("💼 Fondo Cassa", dati.get("fondo_cassa",0))

st.divider()

# ===============================
# SECONDO TITOLO: PROCESSO COCA
# ===============================
st.markdown("<h1 style='text-align:center;color:white;'>🌿 Processo Coca</h1>", unsafe_allow_html=True)
st.divider()

# TRE CONTATORI DEL PROCESSO COCA
col1, col2, col3 = st.columns(3, gap="large")
with col1:
    st.metric("🍃 Foglie", dati.get("foglie",0))
with col2:
    st.metric("🧱 Panetti", dati.get("panetti",0))
with col3:
    st.metric("💊 Bustine", dati.get("bustine",0))
