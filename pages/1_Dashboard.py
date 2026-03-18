import streamlit as st
from gestionale import registra_movimento

st.title("📝 Inserimento Movimenti")
st.divider()

# ===============================
# PRIMA RIGA: FINANZE
# ===============================
col1, col2, col3 = st.columns(3, gap="large")

# -------- COLONNA 1: CASSA --------
with col1:
    st.subheader("💰 Cassa")
    cassa_causale = st.text_input("Causale Cassa", key="cassa_causale")
    cassa_valore = st.number_input("Valore Cassa", value=0.0, key="cassa_valore")
    if st.button("Registra Cassa", key="btn_cassa"):
        if cassa_causale.strip():
            registra_movimento("cassa", cassa_causale, cassa_valore)
            st.success(f"Cassa aggiornata di {cassa_valore}")
            st.session_state.cassa_causale = ""
            st.session_state.cassa_valore = 0.0
            st.experimental_rerun()

# -------- COLONNA 2: SOLDI SPORCHI --------
with col2:
    st.subheader("💸 Soldi Sporchi")
    ss_causale = st.text_input("Causale Soldi Sporchi", key="ss_causale")
    ss_valore = st.number_input("Valore Soldi Sporchi", value=0.0, key="ss_valore")
    if st.button("Registra Soldi Sporchi", key="btn_ss"):
        if ss_causale.strip():
            registra_movimento("soldi_sporchi", ss_causale, ss_valore)
            st.success(f"Soldi Sporchi aggiornati di {ss_valore}")
            st.session_state.ss_causale = ""
            st.session_state.ss_valore = 0.0
            st.experimental_rerun()

# -------- COLONNA 3: FONDO CASSA --------
with col3:
    st.subheader("💼 Fondo Cassa")
    fc_causale = st.text_input("Causale Fondo Cassa", key="fc_causale")
    fc_valore = st.number_input("Valore Fondo Cassa", value=0.0, key="fc_valore")
    if st.button("Registra Fondo Cassa", key="btn_fc"):
        if fc_causale.strip():
            registra_movimento("fondo_cassa", fc_causale, fc_valore)
            st.success(f"Fondo Cassa aggiornato di {fc_valore}")
            st.session_state.fc_causale = ""
            st.session_state.fc_valore = 0.0
            st.experimental_rerun()

st.divider()

# ===============================
# SECONDA RIGA: PROCESSO COCA
# ===============================
col1, col2, col3 = st.columns(3, gap="large")

# -------- COLONNA 1: FOGLIE --------
with col1:
    st.subheader("🍃 Foglie")
    foglie_causale = st.text_input("Causale Foglie", key="foglie_causale")
    foglie_valore = st.number_input("Valore Foglie", value=0.0, key="foglie_valore")
    if st.button("Registra Foglie", key="btn_foglie"):
        if foglie_causale.strip():
            registra_movimento("foglie", foglie_causale, foglie_valore)
            st.success(f"Foglie aggiornate di {foglie_valore}")
            st.session_state.foglie_causale = ""
            st.session_state.foglie_valore = 0.0
            st.experimental_rerun()

# -------- COLONNA 2: PANETTI --------
with col2:
    st.subheader("🧱 Panetti")
    panetti_causale = st.text_input("Causale Panetti", key="panetti_causale")
    panetti_valore = st.number_input("Valore Panetti", value=0.0, key="panetti_valore")
    if st.button("Registra Panetti", key="btn_panetti"):
        if panetti_causale.strip():
            registra_movimento("panetti", panetti_causale, panetti_valore)
            st.success(f"Panetti aggiornati di {panetti_valore}")
            st.session_state.panetti_causale = ""
            st.session_state.panetti_valore = 0.0
            st.experimental_rerun()

# -------- COLONNA 3: BUSTINE --------
with col3:
    st.subheader("💊 Bustine")
    bustine_causale = st.text_input("Causale Bustine", key="bustine_causale")
    bustine_valore = st.number_input("Valore Bustine", value=0.0, key="bustine_valore")
    if st.button("Registra Bustine", key="btn_bustine"):
        if bustine_causale.strip():
            registra_movimento("bustine", bustine_causale, bustine_valore)
            st.success(f"Bustine aggiornate di {bustine_valore}")
            st.session_state.bustine_causale = ""
            st.session_state.bustine_valore = 0.0
            st.experimental_rerun()
