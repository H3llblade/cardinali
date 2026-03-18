import streamlit as st
from gestionale import st, formatta

dati = st.session_state.get("dati", {})

st.title("📊 Dashboard")

# REGISTRO FINANZIARIO AL CENTRO
st.subheader("📋 Registro Finanziario")
movimenti = dati.get("movimenti", [])
if movimenti:
    for mov in reversed(movimenti[-10:]):  # ultimi 10 movimenti
        st.markdown(
            f"<div style='background-color:#2C2C2C;padding:15px;border-radius:10px;margin-bottom:10px;'>"
            f"<b>🕒 {mov['data']}</b><br>"
            f"📂 <b>{mov['tipo']}</b><br>"
            f"📝 {mov['causale']}<br>"
            f"💰 Importo: {formatta(mov['valore'])} $"
            f"</div>", unsafe_allow_html=True
        )
else:
    st.info("Nessun movimento registrato")

st.divider()

# TRE CONTATORI SOTTO IL REGISTRO
col1, col2, col3 = st.columns(3, gap="large")
with col1:
    st.metric("💰 Cassa", dati.get("cassa",0))
with col2:
    st.metric("💸 Soldi Sporchi", dati.get("soldi_sporchi",0))
with col3:
    st.metric("💼 Fondo Cassa", dati.get("fondo_cassa",0))

st.divider()

# SEZIONE PROCESSO COCA
st.subheader("🌿 Processo Coca")
col1, col2, col3 = st.columns(3, gap="large")
with col1:
    st.metric("🍃 Foglie", dati.get("foglie",0))
with col2:
    st.metric("🧱 Panetti", dati.get("panetti",0))
with col3:
    st.metric("💊 Bustine", dati.get("bustine",0))
