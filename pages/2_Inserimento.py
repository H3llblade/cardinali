import streamlit as st
from datetime import datetime
import requests
import json
import base64

st.set_page_config(layout="wide", page_title="Inserimento", page_icon="📝")

# -------------------------------
# CONFIG GITHUB
# -------------------------------
GITHUB_REPO_OWNER = st.secrets.get("GITHUB_OWNER", "")
GITHUB_REPO_NAME = st.secrets.get("GITHUB_REPO", "")
GITHUB_TOKEN = st.secrets.get("GITHUB_PAT", "")

FINANZE_FILE_PATH = "data/finanze.json"
ARMERIA_FILE_PATH = "data/armeria.json"

HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}

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
    "item1": 0,
    "item2": 0,
    "item3": 0,
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
# SESSION STATE
# -------------------------------
if "reset_finanze_flag" not in st.session_state:
    st.session_state.reset_finanze_flag = False

if "reset_armeria_flag" not in st.session_state:
    st.session_state.reset_armeria_flag = False

if "messaggio_ok" not in st.session_state:
    st.session_state.messaggio_ok = ""

defaults = {
    "cassa_causale": "",
    "cassa_valore": 0.0,
    "ss_causale": "",
    "ss_valore": 0.0,
    "fc_causale": "",
    "fc_valore": 0.0,
    "arm_item1_causale": "",
    "arm_item1_valore": 0.0,
    "arm_item2_causale": "",
    "arm_item2_valore": 0.0,
    "arm_item3_causale": "",
    "arm_item3_valore": 0.0,
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

if st.session_state.reset_armeria_flag:
    st.session_state.arm_item1_causale = ""
    st.session_state.arm_item1_valore = 0.0
    st.session_state.arm_item2_causale = ""
    st.session_state.arm_item2_valore = 0.0
    st.session_state.arm_item3_causale = ""
    st.session_state.arm_item3_valore = 0.0
    st.session_state.reset_armeria_flag = False


# -------------------------------
# FUNZIONI FINANZE
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

    dati = leggi_file_github(FINANZE_FILE_PATH, DEFAULT_FINANZE)

    dati.setdefault("cassa", 0)
    dati.setdefault("soldi_sporchi", 0)
    dati.setdefault("fondo_cassa", 0)

    if "movimenti" not in dati or not isinstance(dati["movimenti"], list):
        dati["movimenti"] = []

    dati["movimenti"].append({
        "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "tipo": tipo,
        "causale": causale,
        "valore": valore
    })

    dati[tipo] += valore

    return aggiorna_file_github(FINANZE_FILE_PATH, dati, f"Aggiornamento finanze: {tipo}")


# -------------------------------
# FUNZIONI ARMERIA
# -------------------------------
def registra_armeria(item_key, causale, valore):
    causale = str(causale).strip()

    if not causale:
        st.warning("Inserisci una causale valida.")
        return False

    try:
        valore = float(valore)
    except Exception:
        st.warning("Inserisci un valore valido.")
        return False

    if item_key not in ["item1", "item2", "item3"]:
        st.error("Item armeria non valido.")
        return False

    dati = leggi_file_github(ARMERIA_FILE_PATH, DEFAULT_ARMERIA)

    dati.setdefault("item1", 0)
    dati.setdefault("item2", 0)
    dati.setdefault("item3", 0)

    if "movimenti" not in dati or not isinstance(dati["movimenti"], list):
        dati["movimenti"] = []

    dati[item_key] += valore

    dati["movimenti"].append({
        "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "tipo": "armeria",
        "item": item_key,
        "causale": causale,
        "valore": valore
    })

    return aggiorna_file_github(ARMERIA_FILE_PATH, dati, f"Aggiornamento armeria: {item_key}")


# -------------------------------
# HEADER
# -------------------------------
st.title("📝 Inserimento")
st.divider()

if st.session_state.messaggio_ok:
    st.success(st.session_state.messaggio_ok)
    st.session_state.messaggio_ok = ""

# ===============================
# SEZIONE FINANZE
# ===============================
st.subheader("💰 Gestione Finanze")

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

st.divider()

# ===============================
# SEZIONE ARMERIA
# ===============================
st.subheader("🪖 Gestione Armeria")

col4, col5, col6 = st.columns(3, gap="large")

with col4:
    st.markdown("## 🔫 Pistola")
    arm_item1_causale = st.text_input("Causale Pistola", key="arm_pistola_causale")
    arm_item1_valore = st.number_input("Quantità Pistola (+ / -)", step=1.0, key="arm_pistola_valore")

    if st.button("✅ Registra Pistola", key="btn_pistola", use_container_width=True):
        if registra_armeria("pistola", arm_pistola_causale, arm_pistola_valore):
            st.session_state.messaggio_ok = "Pistola aggiornato"
            st.session_state.reset_armeria_flag = True
            st.rerun()

with col5:
    st.markdown("## 🧰 Silenziatore")
    arm_item2_causale = st.text_input("Causale Silenziatore", key="arm_silenziatore_causale")
    arm_item2_valore = st.number_input("Quantità Silenziatore (+ / -)", step=1.0, key="arm_silenziatore_valore")

    if st.button("✅ Registra Silenziatore", key="btn_item2", use_container_width=True):
        if registra_armeria("silenziatore", arm_silenziatore_causale, arm_silenziatore_valore):
            st.session_state.messaggio_ok = "Silenziatore aggiornato"
            st.session_state.reset_armeria_flag = True
            st.rerun()

with col6:
    st.markdown("## 📦 Caricatore")
    arm_item3_causale = st.text_input("Causale Caricatore", key="arm_caricatore_causale")
    arm_item3_valore = st.number_input("Quantità Caricatore (+ / -)", step=1.0, key="arm_caricatore_valore")

    if st.button("✅ Registra Caricatore", key="btn_caricatore", use_container_width=True):
        if registra_armeria("caricatore", arm_caricatore_causale, arm_caricatore_valore):
            st.session_state.messaggio_ok = "Caricatore aggiornato"
            st.session_state.reset_armeria_flag = True
            st.rerun()
