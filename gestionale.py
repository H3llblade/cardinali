import streamlit as st
from datetime import datetime
import requests
import json
import base64

try:
    st.set_page_config(layout="wide", page_title="CARDINALI", page_icon="🦅")
except Exception:
    pass

GITHUB_REPO_OWNER = st.secrets.get("GITHUB_OWNER", "")
GITHUB_REPO_NAME = st.secrets.get("GITHUB_REPO", "")
GITHUB_TOKEN = st.secrets.get("GITHUB_PAT", "")
WEBHOOK_URL = st.secrets.get("DISCORD_WEBHOOK_URL", "")

HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}

FINANZE_FILE = "data/finanze.json"
DEPOSITO_FILE = "data/deposito.json"
WEBHOOK_URL = st.secrets.get("DISCORD_WEBHOOK_URL", "")

DEFAULT_FINANZE = {
    "cassa": 0,
    "fondo_cassa": 0,
    "soldi_sporchi": 0,
    "movimenti": []
}

DEFAULT_DEPOSITO = {
    "items": {}
}


def parse_json_safely(value):
    """Converte stringhe JSON annidate in oggetti Python."""
    current = value

    for _ in range(3):
        if isinstance(current, str):
            try:
                current = json.loads(current)
            except Exception:
                break
        else:
            break

    return current


def leggi_file_github(file_path, default_data):
    url = f"https://api.github.com/repos/{GITHUB_REPO_OWNER}/{GITHUB_REPO_NAME}/contents/{file_path}"

    try:
        r = requests.get(url, headers=HEADERS, timeout=15)

        if r.status_code == 200:
            content = r.json()["content"]
            decoded = base64.b64decode(content).decode("utf-8")
            dati = parse_json_safely(decoded)

            if not isinstance(dati, dict):
                return default_data.copy()

            return dati

        return default_data.copy()

    except Exception as e:
        print(f"Errore lettura GitHub ({file_path}): {e}")
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


def normalizza_deposito(deposito):
    deposito = parse_json_safely(deposito)

    if not isinstance(deposito, dict):
        return {"items": {}}

    def converti_valore(v):
        if isinstance(v, (int, float)):
            return float(v)
        if isinstance(v, str):
            try:
                return float(v.strip().replace(",", "."))
            except Exception:
                return None
        return None

    # Caso 1: formato {"items": {...}}
    if "items" in deposito:
        items = parse_json_safely(deposito["items"])

        if isinstance(items, dict):
            items_puliti = {}
            for k, v in items.items():
                valore = converti_valore(v)
                if valore is not None:
                    items_puliti[str(k).strip().lower()] = valore

            return {"items": items_puliti}

    # Caso 2: formato vecchio {"foglie":100} oppure {"foglie":"100"}
    items_puliti = {}
    for k, v in deposito.items():
        valore = converti_valore(v)
        if valore is not None:
            items_puliti[str(k).strip().lower()] = valore

    return {"items": items_puliti}


def carica_dati():
    finanze = leggi_file_github(FINANZE_FILE, DEFAULT_FINANZE)
    deposito = leggi_file_github(DEPOSITO_FILE, DEFAULT_DEPOSITO)

    if not isinstance(finanze, dict):
        finanze = DEFAULT_FINANZE.copy()

    deposito = normalizza_deposito(deposito)

    st.session_state.finanze = finanze
    st.session_state.deposito = deposito


def aggiorna_dati_da_github():
    carica_dati()


if "finanze" not in st.session_state:
    st.session_state.finanze = DEFAULT_FINANZE.copy()

if "deposito" not in st.session_state:
    st.session_state.deposito = DEFAULT_DEPOSITO.copy()


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

    deposito = st.session_state.get("deposito", {"items": {}})

    if not isinstance(deposito, dict):
        deposito = {"items": {}}

    if "items" not in deposito or not isinstance(deposito["items"], dict):
        deposito["items"] = {}

    if nome_articolo not in deposito["items"]:
        deposito["items"][nome_articolo] = 0

    deposito["items"][nome_articolo] += quantita
    st.session_state.deposito = deposito

    aggiorna_file_github(
        "data/deposito.json",
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
