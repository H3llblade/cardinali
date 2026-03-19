import streamlit as st
from gestionale import registra_movimento, registra_deposito

st.set_page_config(layout="wide")

st.title("📝 Inserimento Movimenti")
st.divider()

# =========================
# RESET CAMPI DOPO INVIO
# =========================
def reset_finanze():
    st.session_state.cassa_causale = ""
    st.session_state.cassa_valore = 0.0
    st.session_state.ss_causale = ""
    st.session_state.ss_valore = 0.0
    st.session_state.fc_causale = ""
    st.session_state.fc_valore = 0.0


def reset_magazzino():
    st.session_state.item1_causale = ""
    st.session_state.item1_valore = 0.0
    st.session_state.item2_causale = ""
    st.session_state.item2_valore = 0.0
    st.session_state.item3_causale = ""
    st.session_state.item3_valore = 0.0


# =========================
# INIZIALIZZAZIONE STATE
# =========================
defaults = {
    "cassa_causale": "",
    "cassa_valore": 0.0,
    "ss_causale": "",
    "ss_valore": 0.0,
    "fc_causale": "",
    "fc_valore": 0.0,
    "item1_causale": "",
    "item1_valore": 0.0,
    "item2_causale": "",
    "item2_valore": 0.0,
    "item3_causale": "",
    "item3_valore": 0.0,
}

for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# =========================
# SEZIONE FINANZE
# =========================
col1, col2, col3 = st.columns(3, gap="large")

with col1:
    st.subheader("💰 Cassa")
    cassa_causale = st.text_input("Causale Cassa", key="cassa_causale")
    cassa_valore = st.number_input("Valore Cassa", value=st.session_state.cassa_valore, key="cassa_valore")
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
    ss_valore = st.number_input("Valore Soldi Sporchi", value=st.session_state.ss_valore, key="ss_valore")
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
    fc_valore = st.number_input("Valore Fondo Cassa", value=st.session_state.fc_valore, key="fc_valore")
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

# =========================
# SEZIONE MAGAZZINO GENERICA
# =========================
st.subheader("📦 Magazzino")

col4, col5, col6 = st.columns(3, gap="large")

with col4:
    st.subheader("📦 Item 1")
    item1_causale = st.text_input("Causale Item 1", key="item1_causale")
    item1_valore = st.number_input("Valore Item 1", value=st.session_state.item1_valore, key="item1_valore")
    if st.button("Registra Item 1", key="btn_item1"):
        if item1_causale.strip():
            ok = registra_deposito("item_1", item1_valore)
            if ok:
                reset_magazzino()
                st.success(f"Item 1 aggiornato di {item1_valore}")
                st.rerun()
        else:
            st.warning("Inserisci una causale per Item 1.")

with col5:
    st.subheader("📦 Item 2")
    item2_causale = st.text_input("Causale Item 2", key="item2_causale")
    item2_valore = st.number_input("Valore Item 2", value=st.session_state.item2_valore, key="item2_valore")
    if st.button("Registra Item 2", key="btn_item2"):
        if item2_causale.strip():
            ok = registra_deposito("item_2", item2_valore)
            if ok:
                reset_magazzino()
                st.success(f"Item 2 aggiornato di {item2_valore}")
                st.rerun()
        else:
            st.warning("Inserisci una causale per Item 2.")

with col6:
    st.subheader("📦 Item 3")
    item3_causale = st.text_input("Causale Item 3", key="item3_causale")
    item3_valore = st.number_input("Valore Item 3", value=st.session_state.item3_valore, key="item3_valore")
    if st.button("Registra Item 3", key="btn_item3"):
        if item3_causale.strip():
            ok = registra_deposito("item_3", item3_valore)
            if ok:
                reset_magazzino()
                st.success(f"Item 3 aggiornato di {item3_valore}")
                st.rerun()
        else:
            st.warning("Inserisci una causale per Item 3.")
