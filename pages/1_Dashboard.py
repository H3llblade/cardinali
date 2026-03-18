import streamlit as st
from streamlit_autorefresh import st_autorefresh
from gestionale import formatta, aggiorna_dati_da_github

# Aggiorna automaticamente la pagina ogni 5 secondi
st_autorefresh(interval=5000, key="dashboard_autorefresh")

# Ricarica i dati da GitHub / sorgente centrale
aggiorna_dati_da_github()

# Recupera i dati aggiornati
finanze = st.session_state.get("finanze", {})
coca = st.session_state.get("coca", {})

# Titolo pagina
st.markdown(
    "<h1 style='text-align:center; color:white;'>🦅 CARDINALI</h1>",
    unsafe_allow_html=True
)

st.divider()

# =========================
# REGISTRO FINANZE
# =========================
st.markdown(
    "<h2 style='text-align:left; color:white;'>💰 Registro Finanze</h2>",
    unsafe_allow_html=True
)

st.divider()

col1, col2, col3 = st.columns(3, gap="large")

with col1:
    st.markdown(
        f"""
        <div style='background-color:#1E1E1E;
                    color:white;
                    padding:30px;
                    border-radius:15px;
                    text-align:center;
                    box-shadow:0 4px 10px rgba(0,0,0,0.3);'>
            <h3>💰 Cassa</h3>
            <h2>{formatta(finanze.get('cassa', 0))} $</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f"""
        <div style='background-color:#1E1E1E;
                    color:white;
                    padding:30px;
                    border-radius:15px;
                    text-align:center;
                    box-shadow:0 4px 10px rgba(0,0,0,0.3);'>
            <h3>💸 Soldi Sporchi</h3>
            <h2>{formatta(finanze.get('soldi_sporchi', 0))} $</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        f"""
        <div style='background-color:#1E1E1E;
                    color:white;
                    padding:30px;
                    border-radius:15px;
                    text-align:center;
                    box-shadow:0 4px 10px rgba(0,0,0,0.3);'>
            <h3>💼 Fondo Cassa</h3>
            <h2>{formatta(finanze.get('fondo_cassa', 0))} $</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

st.divider()

# =========================
# PROCESSO COCA
# =========================
st.markdown(
    "<h2 style='text-align:left; color:white;'>🌿 Processo Coca</h2>",
    unsafe_allow_html=True
)

st.divider()

col4, col5, col6 = st.columns(3, gap="large")

with col4:
    st.markdown(
        f"""
        <div style='background-color:#2A2A2A;
                    color:white;
                    padding:30px;
                    border-radius:15px;
                    text-align:center;
                    box-shadow:0 4px 10px rgba(0,0,0,0.3);'>
            <h3>🍃 Foglie</h3>
            <h2>{formatta(coca.get('foglie', 0))}</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

with col5:
    st.markdown(
        f"""
        <div style='background-color:#2A2A2A;
                    color:white;
                    padding:30px;
                    border-radius:15px;
                    text-align:center;
                    box-shadow:0 4px 10px rgba(0,0,0,0.3);'>
            <h3>🧱 Panetti</h3>
            <h2>{formatta(coca.get('panetti', 0))}</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

with col6:
    st.markdown(
        f"""
        <div style='background-color:#2A2A2A;
                    color:white;
                    padding:30px;
                    border-radius:15px;
                    text-align:center;
                    box-shadow:0 4px 10px rgba(0,0,0,0.3);'>
            <h3>💊 Bustine</h3>
            <h2>{formatta(coca.get('bustine', 0))}</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

st.divider()

# Pulsante manuale opzionale
if st.button("🔄 Aggiorna ora"):
    aggiorna_dati_da_github()
    st.rerun()
