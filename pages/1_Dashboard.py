import streamlit as st
import time
from gestionale import formatta, aggiorna_dati_da_github

# =========================
# CONFIG PAGINA
# =========================
st.set_page_config(layout="wide")

# =========================
# AUTO REFRESH
# =========================
if "last_refresh" not in st.session_state:
    st.session_state.last_refresh = time.time()

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
# STILE CSS
# =========================
st.markdown("""
<style>
.card {
    background-color: #1E1E1E;
    padding: 25px;
    border-radius: 18px;
    text-align: center;
    box-shadow: 0 6px 15px rgba(0,0,0,0.4);
}
.card h3 {
    margin-bottom: 10px;
    color: #bbbbbb;
}
.card h1 {
    margin: 0;
    font-size: 36px;
    color: white;
}
.section-title {
    font-size: 26px;
    color: white;
    margin-top: 20px;
}
</style>
""", unsafe_allow_html=True)

# =========================
# TITOLO
# =========================
st.markdown(
    "<h1 style='text-align:center; color:white;'>🦅 CARDINALI</h1>",
    unsafe_allow_html=True
)

st.divider()

# =========================
# REGISTRO FINANZE
# =========================
st.markdown("<div class='section-title'>💰 Registro Finanze</div>", unsafe_allow_html=True)
st.divider()

col1, col2, col3 = st.columns(3, gap="large")

with col1:
    st.markdown(f"""
    <div class="card">
        <h3>💰 Cassa</h3>
        <h1>{formatta(finanze.get('cassa', 0))} $</h1>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="card">
        <h3>💸 Soldi Sporchi</h3>
        <h1>{formatta(finanze.get('soldi_sporchi', 0))} $</h1>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="card">
        <h3>💼 Fondo Cassa</h3>
        <h1>{formatta(finanze.get('fondo_cassa', 0))} $</h1>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# =========================
# PROCESSO COCA
# =========================
st.markdown("<div class='section-title'>🌿 Processo Coca</div>", unsafe_allow_html=True)
st.divider()

col4, col5, col6 = st.columns(3, gap="large")

with col4:
    st.markdown(f"""
    <div class="card">
        <h3>🍃 Foglie</h3>
        <h1>{formatta(coca.get('foglie', 0))}</h1>
    </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown(f"""
    <div class="card">
        <h3>🧱 Panetti</h3>
        <h1>{formatta(coca.get('panetti', 0))}</h1>
    </div>
    """, unsafe_allow_html=True)

with col6:
    st.markdown(f"""
    <div class="card">
        <h3>💊 Bustine</h3>
        <h1>{formatta(coca.get('bustine', 0))}</h1>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# =========================
# REFRESH MANUALE
# =========================
if st.button("🔄 Aggiorna ora"):
    aggiorna_dati_da_github()
    st.rerun()
