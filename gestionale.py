import streamlit as st
from datetime import datetime
import requests
import json
import base64

st.set_page_config(layout="wide", page_title="CARDINALI", page_icon="🦅")

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
COCA_FILE = "data/processo_coca.json"

# =========================
# CONFIG DISCORD
# =========================
WEBHOOK_URL = st.secrets.get("DISCORD_WEBHOOK_URL", "")

# =========================
# DEFAULT DATA
# =========================
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


# =========================
# FUNZIONI GITHUB
# =========================
def leggi_file_github(file_path, default_data):
    url = f"https://api.github.com/repos/{GITHUB_REPO_OWNER}/{GITHUB_REPO_NAME}/contents/{file_path}"

    try:
        r = requests.get(url, headers=HEADERS, timeout=15)

        if r.status_code == 200:
            content = r.json()["content"]
            decoded = base64.b64decode(content).decode("utf-8")
            return json.loads(decoded)

        return default_data.copy()

    except Exception as e:
        st.error(f"Errore lettura GitHub ({file_path}): {e}")
        return default_data.copy()


def aggiorna_file_github(file_path, dati, messaggio_commit):
    url = f"https://api.github.com/repos/{GITHUB_REPO_OWNER}/{GITHUB_REPO_NAME}/contents/{file_path}"

    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        sha = r.json().get("sha") if r.status_code == 200 else None

        json_str = json.dumps(dati, indent=4, ensure_ascii=False)
        json_base64 = base64.b64encode(json_str.encode("utf-8")).decode("utf-8")

        payload = {
            "message": messaggio_commit,
            "content": json_base64
        }

        if sha:
            payload["sha"] = sha

        put_r = requests.put(url, headers=HEADERS, json=payload, timeout=15)

        if put_r.status_code not in [200, 201]:
            st.error(f"Errore aggiornamento GitHub: {put_r.text}")

    except Exception as e:
        st.error(f"Errore scrittura GitHub ({file_path}): {e}")


# =========================
# CARICAMENTO DATI
# =========================
def carica_dati():
    st.session_state.finanze = leggi_file_github(FINANZE_FILE, DEFAULT_FINANZE)
    st.session_state.coca = leggi_file_github(COCA_FILE, DEFAULT_COCA)


def aggiorna_dati_da_github():
    carica_dati()


if "finanze" not in st.session_state or "coca" not in st.session_state:
    carica_dati()


# =========================
# UTILS
# =========================
def formatta(num):
    try:
        return f"{round(float(num)):,}".replace(",", ".")
    except Exception:
        return "0"


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


# =========================
# FINANZE
# =========================
def registra_movimento(tipo, causale, valore):
    if tipo not in ["cassa", "soldi_sporchi", "fondo_cassa"]:
        st.error(f"Tipo non valido: {tipo}")
        return

    try:
        valore = float(valore)
    except Exception:
        st.error("Valore non valido.")
        return

    finanze = st.session_state.get("finanze", DEFAULT_FINANZE.copy())

    if "movimenti" not in finanze:
        finanze["movimenti"] = []

    if tipo not in finanze:
        finanze[tipo] = 0

    finanze["movimenti"].append({
        "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "tipo": tipo,
        "causale": causale,
        "valore": valore
    })

    finanze[tipo] += valore
    st.session_state.finanze = finanze

    aggiorna_file_github(
        FINANZE_FILE,
        finanze,
        f"Aggiornamento finanze: {tipo}"
    )

    invia_discord(tipo, causale, valore, finanze[tipo])


# =========================
# PROCESSO COCA
# =========================
def registra_coca(tipo, valore):
    if tipo not in ["foglie", "panetti", "bustine"]:
        st.error(f"Tipo coca non valido: {tipo}")
        return

    try:
        valore = float(valore)
    except Exception:
        st.error("Valore non valido.")
        return

    coca = st.session_state.get("coca", DEFAULT_COCA.copy())

    if tipo not in coca:
        coca[tipo] = 0

    coca[tipo] += valore
    st.session_state.coca = coca

    aggiorna_file_github(
        COCA_FILE,
        coca,
        f"Aggiornamento processo coca: {tipo}"
    )
