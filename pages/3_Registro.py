import streamlit as st
from datetime import datetime
import requests
import json
import base64

st.set_page_config(layout="wide", page_title="Registro", page_icon="📋")

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

DEFAULT_FINANZE = {
    "cassa": 0,
    "fondo_cassa": 0,
    "soldi_sporchi": 0,
    "movimenti": []
}

DEFAULT_ARMERIA = {
    "pistola": 0,
    "silenziatore": 0,
    "caricatore": 0,
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


def aggiorna_file_github(file_path, dati, messaggio):
    if not github_ok():
        st.error("Configurazione GitHub mancante nelle secrets.")
        return False

    try:
        url = get_github_api_url(file_path)
        r = requests.get(url, headers=HEADERS, timeout=15)
        sha = r.json().get("sha") if r.status_code == 200 else None

        json_str = json.dumps(dati, indent=4, ensure_ascii=False)
        json_base64 = base64.b64encode(json_str.encode("utf-8")).decode("utf-8")

        payload = {
            "message": messaggio,
            "content": json_base64
        }

        if sha:
            payload["sha"] = sha

        put_r = requests.put(url, headers=HEADERS, json=payload, timeout=15)

        if put_r.status_code in [200, 201]:
            return True

        st.error(f"Errore aggiornamento GitHub: {put_r.text}")
        return False

    except Exception as e:
        st.error(f"Errore salvataggio GitHub: {e}")
        return False


# -------------------------------
# FUNZIONI UTILI
# -------------------------------
def parse_data(data_str):
    try:
        return datetime.strptime(data_str, "%d/%m/%Y %H:%M:%S")
    except Exception:
        return datetime.min


def formatta_valore(valore):
    try:
        n = float(valore)
        if n.is_integer():
            return str(int(n))
        return str(round(n, 2))
    except Exception:
        return "0"


# -------------------------------
# HEADER
# -------------------------------
st.title("📋 Registro")
st.divider()

col1, col2 = st.columns(2, gap="large")

# ===============================
# COLONNA SINISTRA - FINANZE
# ===============================
with col1:
    st.subheader("💰 Registro Finanze")

    dati_finanze = leggi_file_github(FINANZE_FILE_PATH, DEFAULT_FINANZE)
    mov_finanze = dati_finanze.get("movimenti", [])
    mov_finanze = sorted(
        mov_finanze,
        key=lambda x: parse_data(x.get("data", "")),
        reverse=True
    )

    if mov_finanze:
        for mov in mov_finanze:
            tipo = mov.get("tipo", "-").upper()
            data = mov.get("data", "-")
            causale = mov.get("causale", "-")
            valore = formatta_valore(mov.get("valore", 0))

            emoji = "💰"
            if mov.get("tipo") == "soldi_sporchi":
                emoji = "💸"
            elif mov.get("tipo") == "fondo_cassa":
                emoji = "💼"

            st.markdown(
                f"<div style='background-color:#2C2C2C;padding:15px;border-radius:10px;margin-bottom:10px;'>"
                f"<b>🕒 {data}</b><br>"
                f"{emoji} <b>{tipo}</b><br>"
                f"📝 Causale: {causale}<br>"
                f"💵 Importo: {valore}"
                f"</div>",
                unsafe_allow_html=True
            )
    else:
        st.info("Nessun movimento finanziario registrato")

    st.divider()

# ===============================
# COLONNA DESTRA - ARMERIA
# ===============================
with col2:
    st.subheader("🪖 Registro Armeria")

    dati_armeria = leggi_file_github(ARMERIA_FILE_PATH, DEFAULT_ARMERIA)
    mov_armeria = dati_armeria.get("movimenti", [])
    mov_armeria = sorted(
        mov_armeria,
        key=lambda x: parse_data(x.get("data", "")),
        reverse=True
    )

    if mov_armeria:
        for mov in mov_armeria:
            data = mov.get("data", "-")
            item = mov.get("item", "-")
            causale = mov.get("causale", "-")
            valore = formatta_valore(mov.get("valore", 0))

            emoji_item = "📦"
            if item == "pistola":
                emoji_item = "🔫"
            elif item == "silenziatore":
                emoji_item = "🔇"
            elif item == "caricatore":
                emoji_item = "🧱"

            st.markdown(
                f"<div style='background-color:#2C2C2C;padding:15px;border-radius:10px;margin-bottom:10px;'>"
                f"<b>🕒 {data}</b><br>"
                f"🪖 <b>ARMERIA</b><br>"
                f"{emoji_item} Item: {item}<br>"
                f"📝 Causale: {causale}<br>"
                f"🔢 Quantità: {valore}"
                f"</div>",
                unsafe_allow_html=True
            )
    else:
        st.info("Nessun movimento armeria registrato")

    st.divider()
