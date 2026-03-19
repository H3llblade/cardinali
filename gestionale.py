import streamlit as st
from datetime import datetime
import requests
import json
import base64

# =========================
# CONFIG PAGINA
# =========================
try:
    st.set_page_config(layout="wide", page_title="CARDINALI", page_icon="🦅")
except Exception:
    pass

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

DEFAULT_DEPOSITO = {
    "items": {}
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

    except Exception:
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
            raise Exception(f"GitHub API error: {put_r.status_code} - {put_r.text}")

    except Exception as e:
        st.error(f"Errore aggiornamento GitHub su {file_path}: {e}")


# =========================
# CARICAMENTO DATI
# =========================
def carica_dati():
    st.session_state.finanze = leggi_file_github(FINANZE_FILE, DEFAULT_FINANZE)
    st.session_state.deposito = leggi_file_github(DEPOSITO_FILE, DEFAULT_DEPOSITO)


def aggiorna_dati_da_github():
    carica_dati()


if "finanze" not in st.session_state or "deposito" not in st.session_state:
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
        return False

    try:
        valore = float(valore)
    except Exception:
        st.error("Valore non valido.")
        return False

    finanze = st.session_state.get("finanze", DEFAULT_FINANZE.copy())

    if "movimenti" not in finanze or not isinstance(finanze["movimenti"], list):
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
    return True


# =========================
# DEPOSITO DINAMICO
# =========================
def registra_deposito(nome_articolo, quantita):
    try:
        nome_articolo = str(nome_articolo).strip().lower()
        quantita = float(quantita)
    except Exception:
        st.error("Nome articolo o quantità non validi.")
        return False

    if not nome_articolo:
        st.error("Inserisci un nome articolo valido.")
        return False

    deposito = st.session_state.get("deposito", DEFAULT_DEPOSITO.copy())

    if "items" not in deposito or not isinstance(deposito["items"], dict):
        deposito["items"] = {}

    if nome_articolo not in deposito["items"]:
        deposito["items"][nome_articolo] = 0

    deposito["items"][nome_articolo] += quantita
    st.session_state.deposito = deposito

    aggiorna_file_github(
        DEPOSITO_FILE,
        deposito,
        f"Aggiornamento deposito: {nome_articolo}"
    )

    return True


def reset_deposito():
    st.session_state.deposito = {"items": {}}
    aggiorna_file_github(
        DEPOSITO_FILE,
        st.session_state.deposito,
        "Reset deposito"
    )
    return True
