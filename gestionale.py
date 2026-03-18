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
GITHUB_FILE_PATH  = "finanze.json"
GITHUB_TOKEN      = st.secrets["GITHUB_PAT"]

GITHUB_API_URL = f"https://api.github.com/repos/{GITHUB_REPO_OWNER}/{GITHUB_REPO_NAME}/contents/{GITHUB_FILE_PATH}"
HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"}

# -------------------------------
# CONFIG DISCORD
# -------------------------------
WEBHOOK_URL = st.secrets.get("DISCORD_WEBHOOK_URL")  # webhook Discord

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
        # inizializza file se non esiste
        return {"cassa": 0, "fondo_cassa": 0, "soldi_sporchi": 0, "movimenti": []}

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
        if r.status_code == 204:
            st.success(f"Messaggio Discord inviato correttamente per {tipo}")
        else:
            st.error(f"Errore invio Discord: status {r.status_code} - {r.text}")
    except Exception as e:
        st.error(f"Eccezione invio Discord: {e}")

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

def registra_movimento(tipo, causale, valore):
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
# HEADER PRINCIPALE
# -------------------------------
st.markdown("<h1 style='text-align:center;color:white;'>🦅 CARDINALI</h1>", unsafe_allow_html=True)
st.divider()

# ===============================
# REGISTRO FINANZE
# ===============================
st.markdown("<h2 style='color:white;'>💰 Registro Finanze</h2>", unsafe_allow_html=True)
st.divider()

col1, col2, col3 = st.columns(3, gap="large")
with col1:
    st.markdown(f"<div style='background-color:#1E1E1E;color:white;padding:30px;border-radius:15px;text-align:center;'>"
                f"<h3>💰 Cassa</h3><h2>{formatta(st.session_state.dati.get('cassa',0))} $</h2></div>", unsafe_allow_html=True)
with col2:
    st.markdown(f"<div style='background-color:#1E1E1E;color:white;padding:30px;border-radius:15px;text-align:center;'>"
                f"<h3>💸 Soldi Sporchi</h3><h2>{formatta(st.session_state.dati.get('soldi_sporchi',0))} $</h2></div>", unsafe_allow_html=True)
with col3:
    st.markdown(f"<div style='background-color:#1E1E1E;color:white;padding:30px;border-radius:15px;text-align:center;'>"
                f"<h3>💼 Fondo Cassa</h3><h2>{formatta(st.session_state.dati.get('fondo_cassa',0))} $</h2></div>", unsafe_allow_html=True)

st.divider()

# ===============================
# SEZIONI DI INSERIMENTO MOVIMENTI
# ===============================
st.markdown("<h3 style='color:white;'>Inserimento Movimenti</h3>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3, gap="large")

with col1:
    causale = st.text_input("Causale Cassa", key="cassa_causale")
    valore = st.number_input("Importo Cassa", value=0.0, key="cassa_valore")
    if st.button("Registra Cassa", key="btn_cassa"):
        if causale.strip():
            registra_movimento("cassa", causale, valore)
            st.session_state.cassa_valore = 0.0
            st.session_state.cassa_causale = ""

with col2:
    causale = st.text_input("Causale Soldi Sporchi", key="soldi_sporchi_causale")
    valore = st.number_input("Importo Soldi Sporchi", value=0.0, key="soldi_sporchi_valore")
    if st.button("Registra Soldi Sporchi", key="btn_soldi_sporchi"):
        if causale.strip():
            registra_movimento("soldi_sporchi", causale, valore)
            st.session_state.soldi_sporchi_valore = 0.0
            st.session_state.soldi_sporchi_causale = ""

with col3:
    causale = st.text_input("Causale Fondo Cassa", key="fondo_cassa_causale")
    valore = st.number_input("Importo Fondo Cassa", value=0.0, key="fondo_cassa_valore")
    if st.button("Registra Fondo Cassa", key="btn_fondo_cassa"):
        if causale.strip():
            registra_movimento("fondo_cassa", causale, valore)
            st.session_state.fondo_cassa_valore = 0.0
            st.session_state.fondo_cassa_causale = ""

st.divider()
