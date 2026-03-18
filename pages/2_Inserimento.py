import streamlit as st
from gestionale import registra_movimento

st.title("📝 Inserimento Movimenti")
st.divider()

# Tre colonne per inserimento diretto
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
