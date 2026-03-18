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
GITHUB_TOKEN      = st.secrets["GITHUB_PAT"]
HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"}

# -------------------------------
# Funzioni generiche GitHub
# -------------------------------
def leggi_file_github(file_path):
    url = f"https://api.github.com/repos/{GITHUB_REPO_OWNER}/{GITHUB_REPO_NAME}/contents/{file_path}"
    r = requests.get(url, headers=HEADERS)
    if r.status_code == 200:
        content = r.json()["content"]
        decoded = base64.b64decode(content).decode("utf-8")
        return json.loads(decoded)
    else:
        return {}

def aggiorna_file_github(dati, file_path):
    url = f"https://api.github.com/repos/{GITHUB_REPO_OWNER}/{GITHUB_REPO_NAME}/contents/{file_path}"
    r = requests.get(url, headers=HEADERS)
    sha = r.json()["sha"] if r.status_code == 200 else None

    json_str = json.dumps(dati, indent=4)
    json_base64 = base64.b64encode(json_str.encode("utf-8")).decode("utf-8")
    payload = {"message": f"Aggiornamento {file_path}", "content": json_base64}
    if sha:
        payload["sha"] = sha

    r = requests.put(url, headers=HEADERS, json=payload)
    if r.status_code not in [200, 201]:
        st.error(f"Errore aggiornamento GitHub: {r.json()}")

# -------------------------------
# Stato Streamlit
# -------------------------------
if "finanze" not in st.session_state:
    st.session_state.finanze = leggi_file_github("data/finanze.json")
if "processo_coca" not in st.session_state:
    st.session_state.processo_coca = leggi_file_github("data/processo_coca.json")

# -------------------------------
# Utilità
# -------------------------------
def formatta(num):
    return f"{round(num):,}".replace(",", ".")

# -------------------------------
# Registra movimento finanziario
# -------------------------------
def registra_movimento(tipo, causale, valore):
    # aggiungi il movimento
    st.session_state.finanze["movimenti"].append({
        "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "tipo": tipo,
        "causale": causale,
        "valore": valore
    })

    # aggiorna il totale
    st.session_state.finanze[tipo] += valore

    # aggiorna GitHub
    aggiorna_file_github(st.session_state.finanze, "data/finanze.json")

    # invia solo per i tipi finanziari
    if tipo in ["cassa", "soldi_sporchi", "fondo_cassa"]:
        invia_discord(tipo, causale, valore, st.session_state.finanze[tipo])

# -------------------------------
# Registra valore Processo Coca
# -------------------------------
def registra_coca(tipo, valore):
    st.session_state.processo_coca[tipo] += valore
    aggiorna_file_github(st.session_state.processo_coca, "data/processo_coca.json")
