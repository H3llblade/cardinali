import streamlit as st
import time
import requests
import json
import base64

st.set_page_config(layout="wide")

# =========================
# CONFIG GITHUB
# =========================
GITHUB_REPO_OWNER = st.secrets["GITHUB_OWNER"]
GITHUB_REPO_NAME = st.secrets["GITHUB_REPO"]
GITHUB_TOKEN = st.secrets["GITHUB_PAT"]

HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}

FINANZE_FILE = "data/finanze.json"
DEPOSITO_FILE = "data/deposito.json"

# =========================
# AUTO REFRESH
# =========================
if "last_refresh" not in st.session_state:
    st.session_state.last_refresh = time.time()

if time.time() - st.session_state.last_refresh > 5:
    st.session_state.last_refresh = time.time()
    st.rerun()

# =========================
# FUNZIONI
# =========================
def formatta(num):
    try:
        n = float(num)
        if n.is_integer():
            return f"{int(n):,}".replace(",", ".")
        return f"{n:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except Exception:
        return "0"


def leggi_file_github(file_path, default_data):
    url = f"https://api.github.com/repos/{GITHUB_REPO_OWNER}/{GITHUB_REPO_NAME}/contents/{file_path}"

    try:
        r = requests.get(url, headers=HEADERS, timeout=15)

        if r.status_code == 200:
            content = r.json()["content"]
            decoded = base64.b64decode(content).decode("utf-8")
            dati = json.loads(decoded)

            if isinstance(dati, dict):
                return dati

        return default_data

    except Exception as e:
        st.error(f"Errore lettura {file_path}: {e}")
        return default_data


def converti_valore(v):
    if isinstance(v, (int, float)):
        return float(v)
    if isinstance(v, str):
        try:
            return float(v.strip().replace(",", "."))
        except Exception:
            return None
    return None


def estrai_items_deposito(deposito):
    if not isinstance(deposito, dict):
        return {}

    # Supporta:
    # {"items": {"foglie": 100}}
    # {"foglie": 100}
    sorgente = deposito.get("items", deposito)

    if not isinstance(sorgente, dict):
        return {}

    items_puliti = {}
    for k, v in sorgente.items():
        valore = converti_valore(v)
        if valore is not None:
            items_puliti[str(k).strip().lower()] = valore

    return items_puliti


# =========================
# CARICAMENTO DATI DIRETTO
# =========================
finanze = leggi_file_github(FINANZE_FILE, {
    "cassa": 0,
    "fondo_cassa": 0,
    "soldi_sporchi": 0,
    "movimenti": []
})

deposito = leggi_file_github(DEPOSITO_FILE, {"items": {}})
items = estrai_items_deposito(deposito)

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

if items:
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
                        <h3>{nome.replace("_", " ").title()}</h3>
                        <h1>{formatta(valore)}</h1>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.empty()
else:
    st.warning("Nessun elemento presente nel deposito.")

st.divider()

col1, col2, col3 = st.columns([1, 1, 4])

with col2:
    if st.button("🔄 Aggiorna ora", use_container_width=True):
        st.rerun()

with st.expander("Debug deposito"):
    st.write("Contenuto raw di deposito.json:")
    st.json(deposito)
    st.write("Items letti dalla dashboard:")
    st.json(items)
    st.write("Path letto:", DEPOSITO_FILE)
    st.write("Repo letto:", f"{GITHUB_REPO_OWNER}/{GITHUB_REPO_NAME}")
