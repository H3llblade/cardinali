import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import streamlit as st
from gestionale import registra_movimento, registra_deposito

st.set_page_config(layout="wide")

st.title("📝 Inserimento")
st.divider()


# =========================
# RESET CAMPI
# =========================
def reset_finanze():
    st.session_state.cassa_causale = ""
    st.session_state.cassa_valore = 0.0
    st.session_state.ss_causale = ""
    st.session_state.ss_valore = 0.0
    st.session_state.fc_causale = ""
    st.session_state.fc_valore = 0.0


def reset_magazzino():
    st.session_state.item1_nome = ""
    st.session_state.item1_causale = ""
    st.session_state.item1_valore = 0.0

    st.session_state.item2_nome = ""
    st.session_state.item2_causale = ""
    st.session_state.item2_valore = 0.0

    st.session_state.item3_nome = ""
    st.session_state.item3_causale = ""
    st.session_state.item3_valore = 0.0


# =========================
# DEFAULT SESSION STATE
# =========================
defaults = {
    "cassa_causale": "",
    "cassa_valore": 0.0,
    "ss_causale": "",
    "ss_valore": 0.0,
    "fc_causale": "",
    "fc_valore": 0.0,

    "item1_nome": "",
    "item1_causale": "",
    "item1_valore": 0.0,

    "item2_nome": "",
    "item2_causale": "",
    "item2_valore": 0.0,

    "item3_nome": "",
    "item3_causale": "",
    "item3_valore": 0.0,
}

for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


# =========================
# LAYOUT UNICO IN 3 COLONNE
# =========================
col1, col2, col3 = st.columns(3, gap="large")


# =========================
# COLONNA 1
# =========================
with col1:
    st.markdown("## 💰 Cassa")
    cassa_causale = st.text_input("Causale Cassa", key="cassa_causale")
    cassa_valore = st.number_input(
        "Valore Cassa",
        min_value=0.0,
        step=1.0,
        key="cassa_valore"
    )

    if st.button("✅ Registra Cassa", key="btn_cassa", use_container_width=True):
        if not cassa_causale.strip():
            st.warning("Inserisci una causale per la cassa.")
        else:
            ok = registra_movimento("cassa", cassa_causale, cassa_valore)
            if ok:
                reset_finanze()
                st.success(f"Cassa aggiornata di {cassa_valore}")
                st.rerun()

    st.divider()

    st.markdown("## 📦 Item 1")
    item1_nome = st.text_input("Nome Item 1", key="item1_nome")
    item1_causale = st.text_input("Causale Item 1", key="item1_causale")
    item1_valore = st.number_input(
        "Quantità Item 1",
        min_value=0.0,
        step=1.0,
        key="item1_valore"
    )

    if st.button("✅ Registra Item 1", key="btn_item1", use_container_width=True):
        if not item1_nome.strip():
            st.warning("Inserisci il nome del primo item.")
        elif not item1_causale.strip():
            st.warning("Inserisci una causale per il primo item.")
        else:
            ok = registra_deposito(item1_nome, item1_valore)
            if ok:
                reset_magazzino()
                st.success(f"{item1_nome} aggiornato di {item1_valore}")
                st.rerun()


# =========================
# COLONNA 2
# =========================
with col2:
    st.markdown("## 💸 Soldi Sporchi")
    ss_causale = st.text_input("Causale Soldi Sporchi", key="ss_causale")
    ss_valore = st.number_input(
        "Valore Soldi Sporchi",
        min_value=0.0,
        step=1.0,
        key="ss_valore"
    )

    if st.button("✅ Registra Soldi Sporchi", key="btn_ss", use_container_width=True):
        if not ss_causale.strip():
            st.warning("Inserisci una causale per i soldi sporchi.")
        else:
            ok = registra_movimento("soldi_sporchi", ss_causale, ss_valore)
            if ok:
                reset_finanze()
                st.success(f"Soldi Sporchi aggiornati di {ss_valore}")
                st.rerun()

    st.divider()

    st.markdown("## 📦 Item 2")
    item2_nome = st.text_input("Nome Item 2", key="item2_nome")
    item2_causale = st.text_input("Causale Item 2", key="item2_causale")
    item2_valore = st.number_input(
        "Quantità Item 2",
        min_value=0.0,
        step=1.0,
        key="item2_valore"
    )

    if st.button("✅ Registra Item 2", key="btn_item2", use_container_width=True):
        if not item2_nome.strip():
            st.warning("Inserisci il nome del secondo item.")
        elif not item2_causale.strip():
            st.warning("Inserisci una causale per il secondo item.")
        else:
            ok = registra_deposito(item2_nome, item2_valore)
            if ok:
                reset_magazzino()
                st.success(f"{item2_nome} aggiornato di {item2_valore}")
                st.rerun()


# =========================
# COLONNA 3
# =========================
with col3:
    st.markdown("## 💼 Fondo Cassa")
    fc_causale = st.text_input("Causale Fondo Cassa", key="fc_causale")
    fc_valore = st.number_input(
        "Valore Fondo Cassa",
        min_value=0.0,
        step=1.0,
        key="fc_valore"
    )

    if st.button("✅ Registra Fondo Cassa", key="btn_fc", use_container_width=True):
        if not fc_causale.strip():
            st.warning("Inserisci una causale per il fondo cassa.")
        else:
            ok = registra_movimento("fondo_cassa", fc_causale, fc_valore)
            if ok:
                reset_finanze()
                st.success(f"Fondo Cassa aggiornato di {fc_valore}")
                st.rerun()

    st.divider()

    st.markdown("## 📦 Item 3")
    item3_nome = st.text_input("Nome Item 3", key="item3_nome")
    item3_causale = st.text_input("Causale Item 3", key="item3_causale")
    item3_valore = st.number_input(
        "Quantità Item 3",
        min_value=0.0,
        step=1.0,
        key="item3_valore"
    )

    if st.button("✅ Registra Item 3", key="btn_item3", use_container_width=True):
        if not item3_nome.strip():
            st.warning("Inserisci il nome del terzo item.")
        elif not item3_causale.strip():
            st.warning("Inserisci una causale per il terzo item.")
        else:
            ok = registra_deposito(item3_nome, item3_valore)
            if ok:
                reset_magazzino()
                st.success(f"{item3_nome} aggiornato di {item3_valore}")
                st.rerun()
