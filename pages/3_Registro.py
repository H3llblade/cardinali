import streamlit as st
from gestionale import st, formatta

st.title("📂 Registro Completo Movimenti")
movimenti = st.session_state.get("dati", {}).get("movimenti", [])

if movimenti:
    for mov in reversed(movimenti):
        st.markdown(
            f"<div style='background-color:#2C2C2C;padding:10px;border-radius:10px;margin-bottom:5px;'>"
            f"<b>🕒 {mov['data']}</b> | "
            f"📂 {mov['tipo']} | "
            f"📝 {mov['causale']} | "
            f"💰 {formatta(mov['valore'])} $"
            f"</div>", unsafe_allow_html=True
        )
else:
    st.info("Nessun movimento registrato")
