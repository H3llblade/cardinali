import streamlit as st
from datetime import datetime
import requests
import json
import base64

st.set_page_config(layout="wide", page_title="Inserimento Finanze", page_icon="📝")

# -------------------------------
# CONFIG GITHUB
# -------------------------------
GITHUB_REPO_OWNER = st.secrets.get("GITHUB_OWNER", "")
GITHUB_REPO_NAME = st.secrets.get("GITHUB_REPO", "")
GITHUB_TOKEN = st.secrets.get("GITHUB_PAT", "")
GITHUB_FILE_PATH = "data/finanze.json"

GITHUB_API_URL = ""
if GITHUB_REPO_OWNER and GITHUB_REPO_NAME:
    GITHUB_API_URL = f"https://api.github.com/repos/{GITHUB_REPO_OWNER}/{GITHUB_REPO_NAME}/contents/{GITHUB_FILE_PATH}"

HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}

DEFAULT_DATI = {
    "cassa": 0,
    "fondo_cassa": 0,
    "soldi_sporchi": 0,
    "movimenti": []
}

# -------------------------------
# FUNZIONI GITHUB
# -------------------------------
def github_ok():
    return all([GITHUB_REPO_OWNER, GITHUB_REPO_NAME, GITHUB_TOKEN, GITHUB_API_URL])


def leggi_file_github():
    if not github_ok():
        return DEFAULT_DATI.copy()

    try:
        r = requests.get(GITHUB_API_URL, headers=HEADERS, timeout=15)
        if r.status_code == 200:
            content = r.json().get("content", "")
            decoded = base64.b64decode(content).decode("utf-8")
            dati = json.loads(decoded)

            if not isinstance(dati, dict):
                return DEFAULT_DATI.copy()

            dati.setdefault("cassa", 0)
            dati.setdefault("fondo_cassa", 0)
            dati.setdefault("soldi_sporchi", 0)
            dati.setdefault("movimenti", [])

            return dati

        return DEFAULT_DATI.copy()

    except Exception:
        return DEFAULT_DATI.copy()


def aggiorna_file_github(dati):
    if not github_ok():
        st.error("Configurazione GitHub mancante nelle secrets.")
        return False

    try:
        r = requests.get(GITHUB_API_URL, headers=HEADERS, timeout=15)
        sha = r.json().get("sha") if r.status_code == 200 else None

        json_str = json.dumps(dati, indent=4, ensure_ascii=False)
        json_base64 = base64.b64encode(json_str.encode("utf-8")).decode("utf-8")

        payload = {
            "message": "Aggiornamento finanze",
            "content": json_base64
        }

        if sha:
            payload["sha"] = sha

        put_r = requests.put(GITHUB_API_URL, headers=HEADERS, json=payload, timeout=15)

        if put_r.status_code in [200, 201]:
            return True

        st.error(f"Errore aggiornamento GitHub: {put_r.text}")
        return False

    except Exception as e:
        st.error(f"Errore salvataggio GitHub: {e}")
        return False


# -------------------------------
# STATO
# -------------------------------
if "dati_finanze" not in st.session_state:
    st.session_state.dati_finanze = leggi_file_github()

if "reset_finanze_flag" not in st.session_state:
    st.session_state.reset_finanze_flag = False

defaults = {
    "cassa_causale": "",
    "cassa_valore": 0.0,
    "ss_causale": "",
    "ss_valore": 0.0,
    "fc_causale": "",
    "fc_valore": 0.0,
    "messaggio_ok": ""
}

for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# reset sicuro PRIMA dei widget
if st.session_state.reset_finanze_flag:
    st.session_state.cassa_causale = ""
    st.session_state.cassa_valore = 0.0
    st.session_state.ss_causale = ""
    st.session_state.ss_valore = 0.0
    st.session_state.fc_causale = ""
    st.session_state.fc_valore = 0.0
    st.session_state.reset_finanze_flag = False


# -------------------------------
# FUNZIONE REGISTRA MOVIMENTO
# -------------------------------
def registra_movimento(tipo, causale, valore):
    causale = str(causale).strip()

    if not causale:
        st.warning("Inserisci una causale valida.")
        return False

    try:
        valore = float(valore)
    except Exception:
        st.warning("Inserisci un valore valido.")
        return False

    if tipo not in ["cassa", "soldi_sporchi", "fondo_cassa"]:
        st.error("Tipo movimento non valido.")
        return False

    dati = leggi_file_github()

    dati["movimenti"].append({
        "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "tipo": tipo,
        "causale": causale,
        "valore": valore
    })

    dati[tipo] += valore

    if aggiorna_file_github(dati):
        st.session_state.dati_finanze = dati
        return True

    return False


# -------------------------------
# HEADER
# -------------------------------
st.title("📝 Inserimento Finanze")
st.divider()

if st.session_state.messaggio_ok:
    st.success(st.session_state.messaggio_ok)
    st.session_state.messaggio_ok = ""

col1, col2, col3 = st.columns(3, gap="large")

with col1:
    st.markdown("## 💰 Cassa")
    cassa_causale = st.text_input("Causale Cassa", key="cassa_causale")
    cassa_valore = st.number_input("Importo Cassa (+ / -)", step=1.0, key="cassa_valore")

    if st.button("✅ Registra Cassa", key="btn_cassa", use_container_width=True):
        if registra_movimento("cassa", cassa_causale, cassa_valore):
            st.session_state.messaggio_ok = "Movimento Cassa registrato"
            st.session_state.reset_finanze_flag = True
            st.rerun()

with col2:
    st.markdown("## 💸 Soldi Sporchi")
    ss_causale = st.text_input("Causale Soldi Sporchi", key="ss_causale")
    ss_valore = st.number_input("Importo Soldi Sporchi (+ / -)", step=1.0, key="ss_valore")

    if st.button("✅ Registra Soldi Sporchi", key="btn_ss", use_container_width=True):
        if registra_movimento("soldi_sporchi", ss_causale, ss_valore):
            st.session_state.messaggio_ok = "Movimento Soldi Sporchi registrato"
            st.session_state.reset_finanze_flag = True
            st.rerun()

with col3:
    st.markdown("## 💼 Fondo Cassa")
    fc_causale = st.text_input("Causale Fondo Cassa", key="fc_causale")
    fc_valore = st.number_input("Importo Fondo Cassa (+ / -)", step=1.0, key="fc_valore")

    if st.button("✅ Registra Fondo Cassa", key="btn_fc", use_container_width=True):
        if registra_movimento("fondo_cassa", fc_causale, fc_valore):
            st.session_state.messaggio_ok = "Movimento Fondo Cassa registrato"
            st.session_state.reset_finanze_flag = True
            st.rerun()
