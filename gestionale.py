# gestionale.py
import streamlit as st
from datetime import datetime
import requests
import json
import base64

st.set_page_config(layout="wide", page_title="Gestionale Finanze", page_icon="💰")

# -------------------------------
# CONFIG GITHUB
# -------------------------------
GITHUB_REPO_OWNER = st.secrets["GITHUB_OWNER"]
GITHUB_REPO_NAME  = st.secrets["GITHUB_REPO"]
GITHUB_FILE_PATH  = "finanze.json"
GITHUB_TOKEN      = st.secrets["GITHUB_PAT"]

GITHUB_API_URL = f"https://api.github.com/repos/{GITHUB_REPO_OWNER}/{GITHUB_REPO_NAME}/contents/{GITHUB_FILE_PATH}"
HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"}

# -------------------------------
# CONFIG DISCORD
# -------------------------------
WEBHOOK_URL = st.secrets.get("DISCORD_WEBHOOK_URL")

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
        return {
            "cassa": 0,
            "fondo_cassa": 0,
            "soldi_sporchi": 0,
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
# INVIO DISCORD                 
# -------------------------------
def invia_discord(tipo, causale, valore, totale):
    if not WEBHOOK_URL:
        st.warning("Webhook Discord non impostato!")
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
        r = requests.post(WEBHOOK_URL, json={"content": msg}, timeout=5)
    except Exception as e:
        st.error(f"Errore invio Discord: {e}")

# -------------------------------
# UTILI
# -------------------------------
def formatta(num):
    return f"{round(num):,}".replace(",", ".")

def registra_movimento(tipo, causale, valore):
    if "dati" not in st.session_state:
        st.session_state.dati = leggi_file_github()
    if tipo not in st.session_state.dati:
        st.session_state.dati[tipo] = 0
    st.session_state.dati["movimenti"].append({
        "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "tipo": tipo,
        "causale": causale,
        "valore": valore
    })
    st.session_state.dati[tipo] += valore
    aggiorna_file_github(st.session_state.dati)
    invia_discord(tipo, causale, valore, st.session_state.dati[tipo])

# -------------------------------
# INIZIALIZZAZIONE STATO
# -------------------------------
if "dati" not in st.session_state:
    st.session_state.dati = leggi_file_github()
