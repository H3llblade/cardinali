import streamlit as st
import requests
import json
import base64

st.set_page_config(layout="wide", page_title="Dashboard", page_icon="📊")

# -------------------------------
# CONFIG GITHUB
# -------------------------------
GITHUB_REPO_OWNER = st.secrets.get("GITHUB_OWNER", "")
GITHUB_REPO_NAME = st.secrets.get("GITHUB_REPO", "")
GITHUB_TOKEN = st.secrets.get("GITHUB_PAT", "")

HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}

FINANZE_FILE_PATH = "data/finanze.json"
ARMERIA_FILE_PATH = "data/armeria.json"

# -------------------------------
# DEFAULT DATI
# -------------------------------
DEFAULT_FINANZE = {
    "cassa": 0,
    "fondo_cassa": 0,
    "soldi_sporchi": 0,
    "movimenti": []
}

DEFAULT_ARMERIA = {
    "item_a": 0,
    "item_b": 0,
    "item_c": 0,
    "movimenti": []
}

# -------------------------------
# FUNZIONI GITHUB
# -------------------------------
def github_ok():
    return all([GITHUB_REPO_OWNER, GITHUB_REPO_NAME, GITHUB_TOKEN])


def get_github_api_url(file_path):
    return f"https://api.github.com/repos/{GITHUB_REPO_OWNER}/{GITHUB_REPO_NAME}/contents/{file_path}"


def leggi_file_github(file_path, default_data):
    if not github_ok():
        return default_data.copy()

    try:
        url = get_github_api_url(file_path)
        r = requests.get(url, headers=HEADERS, timeout=15)

        if r.status_code == 200:
            content = r.json().get("content", "")
            decoded = base64.b64decode(content).decode("utf-8")
            dati = json.loads(decoded)

            if isinstance(dati, dict):
                return dati

        return default_data.copy()

    except Exception:
        return default_data.copy()


def formatta(num):
    try:
        n = float(num)
        if n.is_integer():
            return f"{int(n):,}".replace(",", ".")
        return f"{n:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except Exception:
        return "0"


# -------------------------------
# LETTURA DATI
# -------------------------------
dati_finanze = leggi_file_github(FINANZE_FILE_PATH, DEFAULT_FINANZE)
dati_armeria = leggi_file_github(ARMERIA_FILE_PATH, DEFAULT_ARMERIA)

# -------------------------------
# HEADER
# -------------------------------
st.title("📊 Dashboard")
st.divider()

# ===============================
# DASHBOARD FINANZE
# ===============================
st.subheader("💰 Registro Finanze")

col1, col2, col3 = st.columns(3, gap="large")

with col1:
    st.markdown(
        f"<div style='background-color:#1E1E1E;padding:20px;border-radius:10px;text-align:center;'>"
        f"<h3>💰 CASSA</h3><h2>{formatta(dati_finanze.get('cassa', 0))} $</h2></div>",
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f"<div style='background-color:#1E1E1E;padding:20px;border-radius:10px;text-align:center;'>"
        f"<h3>💸 SOLDI SPORCHI</h3><h2>{formatta(dati_finanze.get('soldi_sporchi', 0))} $</h2></div>",
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        f"<div style='background-color:#1E1E1E;padding:20px;border-radius:10px;text-align:center;'>"
        f"<h3>💼 FONDO CASSA</h3><h2>{formatta(dati_finanze.get('fondo_cassa', 0))} $</h2></div>",
        unsafe_allow_html=True
    )

st.divider()

# ===============================
# DASHBOARD ARMERIA / MAGAZZINO
# ===============================
st.subheader("📦 Gestione Armeria")

col4, col5, col6 = st.columns(3, gap="large")

with col4:
    st.markdown(
        f"<div style='background-color:#1E1E1E;padding:20px;border-radius:10px;text-align:center;'>"
        f"<h3>🔫 Pistola</h3><h2>{formatta(dati_armeria.get('pistola', 0))}</h2></div>",
        unsafe_allow_html=True
    )

with col5:
    st.markdown(
        f"<div style='background-color:#1E1E1E;padding:20px;border-radius:10px;text-align:center;'>"
        f"<h3>🔇 Silenziatore</h3><h2>{formatta(dati_armeria.get('silenziatore', 0))}</h2></div>",
        unsafe_allow_html=True
    )

with col6:
    st.markdown(
        f"<div style='background-color:#1E1E1E;padding:20px;border-radius:10px;text-align:center;'>"
        f"<h3>🧱 Caricatore</h3><h2>{formatta(dati_armeria.get('caricatore', 0))}</h2></div>",
        unsafe_allow_html=True
    )
