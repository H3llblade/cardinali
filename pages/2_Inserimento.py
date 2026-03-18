import streamlit as st
from gestionale import registra_movimento, registra_coca

st.title("📝 Inserimento Movimenti")
st.divider()

col1, col2, col3 = st.columns(3, gap="large")

with col1:
    st.subheader("💰 Cassa")
    cassa_causale = st.text_input("Causale Cassa", key="cassa_causale")
    cassa_valore = st.number_input("Valore Cassa", value=0.0, key="cassa_valore")
    if st.button("Registra Cassa", key="btn_cassa"):
        if cassa_causale.strip():
            registra_movimento("cassa", cassa_causale, cassa_valore)
            st.success(f"Cassa aggiornata di {cassa_valore}")
            st.rerun()

with col2:
    st.subheader("💸 Soldi Sporchi")
    ss_causale = st.text_input("Causale Soldi Sporchi", key="ss_causale")
    ss_valore = st.number_input("Valore Soldi Sporchi", value=0.0, key="ss_valore")
    if st.button("Registra Soldi Sporchi", key="btn_ss"):
        if ss_causale.strip():
            registra_movimento("soldi_sporchi", ss_causale, ss_valore)
            st.success(f"Soldi Sporchi aggiornati di {ss_valore}")
            st.rerun()

with col3:
    st.subheader("💼 Fondo Cassa")
    fc_causale = st.text_input("Causale Fondo Cassa", key="fc_causale")
    fc_valore = st.number_input("Valore Fondo Cassa", value=0.0, key="fc_valore")
    if st.button("Registra Fondo Cassa", key="btn_fc"):
        if fc_causale.strip():
            registra_movimento("fondo_cassa", fc_causale, fc_valore)
            st.success(f"Fondo Cassa aggiornato di {fc_valore}")
            st.rerun()

st.divider()

col1, col2, col3 = st.columns(3, gap="large")

with col1:
    st.subheader("🍃 Foglie")
    foglie_valore = st.number_input("Valore Foglie", value=0.0, key="foglie_valore")
    if st.button("Registra Foglie", key="btn_foglie"):
        registra_coca("foglie", foglie_valore)
        st.success(f"Foglie aggiornate di {foglie_valore}")
        st.rerun()

with col2:
    st.subheader("🧱 Panetti")
    panetti_valore = st.number_input("Valore Panetti", value=0.0, key="panetti_valore")
    if st.button("Registra Panetti", key="btn_panetti"):
        registra_coca("panetti", panetti_valore)
        st.success(f"Panetti aggiornati di {panetti_valore}")
        st.rerun()

with col3:
    st.subheader("💊 Bustine")
    bustine_valore = st.number_input("Valore Bustine", value=0.0, key="bustine_valore")
    if st.button("Registra Bustine", key="btn_bustine"):
        registra_coca("bustine", bustine_valore)
        st.success(f"Bustine aggiornate di {bustine_valore}")
        st.rerun()
