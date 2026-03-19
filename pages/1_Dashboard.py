import streamlit as st
from gestionale import formatta, aggiorna_dati_da_github

st.set_page_config(layout="wide")

# =========================
# CARICAMENTO DATI
# =========================
aggiorna_dati_da_github()

finanze = st.session_state.get("finanze", {})
deposito = st.session_state.get("deposito", {})

# Compatibilità doppio formato:
# 1) {"items": {"foglie": 100}}
# 2) {"foglie": 100}
if isinstance(deposito, dict):
    if "items" in deposito and isinstance(deposito["items"], dict):
        items = deposito["items"]
    else:
        items = deposito
else:
    items = {}

# =========================
# STILE
# =========================
st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 100%;
}
.card {
    background-color: #1E1E1E;
    padding: 25px;
    border-radius: 18px;
    text-align: center;
    box-shadow: 0 6px 15px rgba(0,0,0,0.35);
    margin-bottom: 18px;
    min-height: 140px;
    display: flex;
    flex-direction: column;
    justify-content: center;
}
.card h3 {
    margin: 0 0 10px 0;
    color: #CFCFCF;
    font-size: 20px;
    font-weight: 600;
}
.card h1 {
    margin: 0;
    font-size: 34px;
    color: white;
    font-weight: 800;
}
.section-title {
    font-size: 28px;
    font-weight: 700;
    color: white;
    margin-top: 8px;
    margin-bottom: 12px;
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
# DEPOSITO
# =========================
st.markdown("<div class='section-title'>📦 Deposito</div>", unsafe_allow_html=True)

if items and isinstance(items, dict):
    lista_items = list(items.items())

    for i in range(0, len(lista_items), 3):
        blocco = lista_items[i:i+3]
        cols = st.columns(3, gap="large")

        for j in range(3):
            with cols[j]:
                if j < len(blocco):
                    nome, valore = blocco[j]
                    st.markdown(f"""
                    <div class="card">
                        <h3>{str(nome).replace("_", " ").title()}</h3>
                        <h1>{formatta(valore)}</h1>
                    </div>
                    """, unsafe_allow_html=True)
else:
    st.warning("Deposito vuoto oppure struttura dati non riconosciuta.")

st.divider()

col1, col2 = st.columns([1, 4])

with col1:
    if st.button("🔄 Aggiorna ora", use_container_width=True):
        aggiorna_dati_da_github()
        st.rerun()

with col2:
    with st.expander("Debug dati deposito"):
        st.write("st.session_state.deposito:")
        st.json(deposito)
        st.write("items usati dalla dashboard:")
        st.json(items)
