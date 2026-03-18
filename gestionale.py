import streamlit as st
from datetime import datetime
import requests
import json
import base64

st.set_page_config(layout="wide", page_title="CARDINALI", page_icon="🦅")

# -------------------------------
# CONFIG GITHUB
# -------------------------------
GITHUB_REPO_OWNER = st.secrets["GITHUB_OWNER"]
GITHUB_REPO_NAME  = st.secrets["GITHUB_REPO"]
GITHUB_TOKEN      = st.secrets["GITHUB_PAT"]

HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"}

FINANZE_FILE = "data/finanze.json"
COCA_FILE = "data/processo_coca.json"

# -------------------------------
# CONFIG DISCORD
# -------------------------------
WEBHOOK_URL = st.secrets.get("DISCORD_WEBHOOK_URL")

# -------------------------------
# FUNZIONI GITHUB GENERICHE
# -------------------------------
def leggi_file_github(file_path, default_data):
    url = f"https://api.github.com/repos/{GITHUB_REPO_OWNER}/{GITHUB_REPO_NAME}/contents/{file_path}"
    r = requests.get(url, headers=HEADERS)

    if r.status_code == 200:
        content = r.json()["content"]
        decoded = base64.b64decode(content).decode("utf-8")
        return json.loads(decoded)

    return default_data.copy()

def aggiorna_file_github(file_path, dati, messaggio_commit):
    url = f"https://api.github.com/repos/{GITHUB_REPO_OWNER}/{GITHUB_REPO_NAME}/contents/{file_path}"
    r = requests.get(url, headers=HEADERS)
    sha = r.json().get("sha") if r.status_code == 200 else None

    json_str = json.dumps(dati, indent=4)
    json_base64 = base64.b64encode(json_str.encode("utf-8")).decode("utf-8")

    payload = {
        "message": messaggio_commit,
        "content": json_base64
    }

    if sha:
        payload["sha"] = sha

    r = requests.put(url, headers=HEADERS, json=payload)

    if r.status_code not in [200, 201]:
        st.error(f"Errore aggiornamento GitHub: {r.text}")

# -------------------------------
# DEFAULT DATA
# -------------------------------
DEFAULT_FINANZE = {
    "cassa": 0,
    "fondo_cassa": 0,
    "soldi_sporchi": 0,
    "movimenti": []
}

DEFAULT_COCA = {
    "foglie": 0,
    "panetti": 0,
    "bustine": 0
}

# -------------------------------
# CARICAMENTO DATI
# -------------------------------
def carica_dati():
    st.session_state.finanze = leggi_file_github(FINANZE_FILE, DEFAULT_FINANZE)
    st.session_state.coca = leggi_file_github(COCA_FILE, DEFAULT_COCA)

def aggiorna_dati_da_github():
    carica_dati()

if "finanze" not in st.session_state or "coca" not in st.session_state:
    carica_dati()

# -------------------------------
# UTILI
# -------------------------------
def formatta(num):
    return f"{round(num):,}".replace(",", ".")

def invia_discord(tipo, causale, valore, totale):
    if not WEBHOOK_URL:
        return

    try:
        emoji_tipo = "💰" if tipo == "cassa" else "💸" if tipo == "soldi_sporchi" else "💼"
        msg = (
            f"{emoji_tipo} **{tipo.upper()} registrato!**\n"
            f"📝 Causale: {causale}\n"
            f"💵 Importo: {round(valore)} $\n"
            f"📊 Totale {tipo}: {round(totale)} $\n"
            f"🕒 {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"
        )
        requests.post(WEBHOOK_URL, json={"content": msg}, timeout=5)
    except Exception:
        pass

# -------------------------------
# FINANZE
# -------------------------------
def registra_movimento(tipo, causale, valore):
    if tipo not in ["cassa", "soldi_sporchi", "fondo_cassa"]:
        st.error(f"Tipo non valido: {tipo}")
        return

    st.session_state.finanze["movimenti"].append({
        "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "tipo": tipo,
        "causale": causale,
        "valore": valore
    })

    st.session_state.finanze[tipo] += valore

    aggiorna_file_github(
        FINANZE_FILE,
        st.session_state.finanze,
        f"Aggiornamento finanze: {tipo}"
    )

    invia_discord(tipo, causale, valore, st.session_state.finanze[tipo])

# -------------------------------
# PROCESSO COCA
# -------------------------------
def registra_coca(tipo, valore):
    if tipo not in ["foglie", "panetti", "bustine"]:
        st.error(f"Tipo coca non valido: {tipo}")
        return

    if tipo not in st.session_state.coca:
        st.session_state.coca[tipo] = 0

    st.session_state.coca[tipo] += valore

    aggiorna_file_github(
        COCA_FILE,
        st.session_state.coca,
        f"Aggiornamento processo coca: {tipo}"
    )
