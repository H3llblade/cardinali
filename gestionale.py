# gestionale.py
import streamlit as st
from datetime import datetime
import requests
import json
import base64
from discord_utils import invia_discord  # import della funzione aggiornata

st.set_page_config(layout="wide", page_title="Gestionale", page_icon="💻")

# -------------------------------
# CONFIG GITHUB
# -------------------------------
GITHUB_REPO_OWNER = st.secrets["GITHUB_OWNER"]
GITHUB_REPO_NAME  = st.secrets["GITHUB_REPO"]
GITHUB_FILE_PATH  = "data/finanze.json"
GITHUB_TOKEN      = st.secrets["GITHUB_PAT"]

GITHUB_API_URL = f"https://api.github.com/repos/{GITHUB_REPO_OWNER}/{GITHUB_REPO_NAME}/contents/{GITHUB_FILE_PATH}"
HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"}

# -------------------------------
# FUNZIONI GITHUB
# -------------------------------
def leggi_file_github():
    r = requests.get(GITHUB_API_URL, headers=HEADERS)
    if r.status_code == 200:
        content = r.json()["content"]
        decoded = base64.b64decode(content).decode("utf-8")
        return json.loads(decoded)
    else:
        # Inizializza tutte le chiavi necessarie
        return {
            "cassa": 0,
            "soldi_sporchi": 0,
            "fondo_cassa": 0,
            "movimenti": [],
            "foglie": 0,
            "panetti": 0,
            "bustine": 0
        }

def aggiorna_file_github(dati):
    r = requests.get(GITHUB_API_URL, headers=HEADERS)
    sha = r.json()["sha"] if r.status_code == 200 else None

    json_str = json.dumps(dati, indent=4)
    json_base64 = base64.b64encode(json_str.encode("utf-8")).decode("utf-8")
    payload = {"message": "Aggiornamento finanze", "content": json_base64}
    if sha:
        payload["sha"] = sha

    r = requests.put(GITHUB_API_URL, headers=HEADERS, json=payload)
    if r.status_code not in [200, 201]:
        st.error(f"Errore aggiornamento GitHub: {r.json()}")

# -------------------------------
# STATO STREAMLIT
# -------------------------------
if "dati" not in st.session_state:
    st.session_state.dati = leggi_file_github()

# -------------------------------
# UTILI
# -------------------------------
def formatta(num):
    return f"{round(num):,}".replace(",", ".")

# -------------------------------
# REGISTRA MOVIMENTO
# -------------------------------
def registra_movimento(tipo, causale, valore):
    """
    Registra un movimento, aggiorna GitHub, e invia su Discord solo se è finanziario
    """
    # Aggiungi il movimento
    st.session_state.dati["movimenti"].append({
        "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "tipo": tipo,
        "causale": causale,
        "valore": valore
    })

    # Aggiorna il totale
    st.session_state.dati[tipo] = st.session_state.dati.get(tipo, 0) + valore

    # Aggiorna GitHub
    aggiorna_file_github(st.session_state.dati)

    # Invia su Discord solo per i movimenti finanziari
    if tipo in ["cassa", "soldi_sporchi", "fondo_cassa"]:
        invia_discord(tipo, causale, valore, st.session_state.dati[tipo])
