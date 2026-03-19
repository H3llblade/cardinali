import streamlit as st
from gestionale import registra_movimento, registra_deposito

st.set_page_config(layout="wide")

st.title("📝 Inserimento Movimenti")
st.divider()

def reset_finanze():
    st.session_state.cassa_causale = ""
    st.session_state.cassa_valore = 0.0
    st.session_state.ss_causale = ""
    st.session_state.ss_valore = 0.0
    st.session_state.fc_causale = ""
    st.session_state.fc_valore = 0.0

def reset_deposito_form():
    st.session_state.item_nome = ""
    st.session_state.item_causale = ""
    st.session_state.item_valore = 0.0

defaults = {
    "cassa_causale": "",
    "cassa_valore": 0.0,
    "ss_causale": "",
    "ss_valore": 0.0,
    "fc_causale": "",
    "fc_valore": 0.0,
    "item_nome": "",
    "item_causale": "",
    "item_valore": 0.0,
}

for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

col1, col2, col3 = st.columns(3, gap="large")

with col1:
    st.subheader("💰 Cassa")
    cassa_causale = st.text_input("Causale Cassa", key="cassa_causale")
    cassa_valore = st.number_input("Valore Cassa", min_value=0.0, key="cassa_valore")
    if st.button("Registra Cassa", key="btn_cassa"):
        if cassa_causale.strip():
            ok = registra_movimento("cassa", cassa_causale, cassa_valore)
            if ok:
                reset_finanze()
                st.success(f"Cassa aggiornata di {cassa_valore}")
                st.rerun()
        else:
            st.warning("Inserisci una causale per la cassa.")

with col2:
    st.subheader("💸 Soldi Sporchi")
    ss_causale = st.text_input("Causale Soldi Sporchi", key="ss_causale")
    ss_valore = st.number_input("Valore Soldi Sporchi", min_value=0.0, key="ss_valore")
    if st.button("Registra Soldi Sporchi", key="btn_ss"):
        if ss_causale.strip():
            ok = registra_movimento("soldi_sporchi", ss_causale, ss_valore)
            if ok:
                reset_finanze()
                st.success(f"Soldi Sporchi aggiornati di {ss_valore}")
                st.rerun()
        else:
            st.warning("Inserisci una causale per i soldi sporchi.")

with col3:
    st.subheader("💼 Fondo Cassa")
    fc_causale = st.text_input("Causale Fondo Cassa", key="fc_causale")
    fc_valore = st.number_input("Valore Fondo Cassa", min_value=0.0, key="fc_valore")
    if st.button("Registra Fondo Cassa", key="btn_fc"):
        if fc_causale.strip():
            ok = registra_movimento("fondo_cassa", fc_causale, fc_valore)
            if ok:
                reset_finanze()
                st.success(f"Fondo Cassa aggiornato di {fc_valore}")
                st.rerun()
        else:
            st.warning("Inserisci una causale per il fondo cassa.")

st.divider()

st.subheader("📦 Deposito")

col4, col5, col6 = st.columns(3, gap="large")

with col4:
    item_nome = st.text_input("Nome item", key="item_nome")

with col5:
    item_causale = st.text_input("Causale item", key="item_causale")

with col6:
    item_valore = st.number_input("Quantità item", min_value=0.0, key="item_valore")

if st.button("Registra Item", key="btn_item"):
    if not item_nome.strip():
        st.warning("Inserisci il nome dell'item.")
    elif not item_causale.strip():
        st.warning("Inserisci una causale per l'item.")
    else:
        ok = registra_deposito(item_nome, item_valore)
        if ok:
            reset_deposito_form()
            st.success(f"{item_nome} aggiornato di {item_valore}")
            st.rerun()
