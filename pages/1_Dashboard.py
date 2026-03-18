import streamlit as st
from gestionale import aggiorna_dati_da_github, formatta

aggiorna_dati_da_github()

finanze = st.session_state.get("finanze", {})
coca = st.session_state.get("coca", {})

st.markdown("<h1 style='text-align:center;color:white;'>🦅 CARDINALI</h1>", unsafe_allow_html=True)
st.divider()

col_refresh_1, col_refresh_2 = st.columns([1, 6])
with col_refresh_1:
    if st.button("🔄 Aggiorna"):
        aggiorna_dati_da_github()
        st.rerun()

st.markdown("<h2 style='text-align:left;color:white;'>💰 Registro Finanze</h2>", unsafe_allow_html=True)
st.divider()

col1, col2, col3 = st.columns(3, gap="large")
with col1:
    st.markdown(
        f"<div style='background-color:#1E1E1E;color:white;padding:30px;border-radius:15px;text-align:center;'>"
        f"<h3>💰 Cassa</h3>"
        f"<h2>{formatta(finanze.get('cassa', 0))} $</h2>"
        f"</div>",
        unsafe_allow_html=True,
    )
with col2:
    st.markdown(
        f"<div style='background-color:#1E1E1E;color:white;padding:30px;border-radius:15px;text-align:center;'>"
        f"<h3>💸 Soldi Sporchi</h3>"
        f"<h2>{formatta(finanze.get('soldi_sporchi', 0))} $</h2>"
        f"</div>",
        unsafe_allow_html=True,
    )
with col3:
    st.markdown(
        f"<div style='background-color:#1E1E1E;color:white;padding:30px;border-radius:15px;text-align:center;'>"
        f"<h3>💼 Fondo Cassa</h3>"
        f"<h2>{formatta(finanze.get('fondo_cassa', 0))} $</h2>"
        f"</div>",
        unsafe_allow_html=True,
    )

st.divider()
st.markdown("<h2 style='text-align:left;color:white;'>🌿 Processo Coca</h2>", unsafe_allow_html=True)
st.divider()

col1, col2, col3 = st.columns(3, gap="large")
with col1:
    st.markdown(
        f"<div style='background-color:#3C3C3C;color:white;padding:30px;border-radius:15px;text-align:center;'>"
        f"<h3>🍃 Foglie</h3>"
        f"<h2>{formatta(coca.get('foglie', 0))}</h2>"
        f"</div>",
        unsafe_allow_html=True,
    )
with col2:
    st.markdown(
        f"<div style='background-color:#3C3C3C;color:white;padding:30px;border-radius:15px;text-align:center;'>"
        f"<h3>🧱 Panetti</h3>"
        f"<h2>{formatta(coca.get('panetti', 0))}</h2>"
        f"</div>",
        unsafe_allow_html=True,
    )
with col3:
    st.markdown(
        f"<div style='background-color:#3C3C3C;color:white;padding:30px;border-radius:15px;text-align:center;'>"
        f"<h3>💊 Bustine</h3>"
        f"<h2>{formatta(coca.get('bustine', 0))}</h2>"
        f"</div>",
        unsafe_allow_html=True,
    )
