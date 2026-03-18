# discord_utils.py
import requests
from datetime import datetime
import streamlit as st

# Recupera il webhook dal secrets di Streamlit
WEBHOOK_URL = st.secrets.get("DISCORD_WEBHOOK_URL")  # Inserisci qui il tuo webhook

def invia_discord(tipo: str, causale: str, valore: float, totale: float):
    """
    Invia un messaggio su Discord per i movimenti finanziari.
    
    Parametri:
    - tipo: "cassa", "soldi_sporchi" o "fondo_cassa"
    - causale: descrizione del movimento
    - valore: importo del movimento
    - totale: totale aggiornato della sezione
    """
    if not WEBHOOK_URL:
        st.warning("Webhook Discord non impostato!")
        return
    
    # Emoji per rendere il messaggio più leggibile
    emoji_tipo = "💰" if tipo == "cassa" else "💸" if tipo == "soldi_sporchi" else "💼"
    
    msg = (
        f"{emoji_tipo} **{tipo.upper()} registrato!**\n"
        f"📝 Causale: {causale}\n"
        f"💵 Importo: {round(valore)} $\n"
        f"📊 Totale {tipo}: {round(totale)} $\n"
        f"🕒 {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"
    )
    
    try:
        r = requests.post(WEBHOOK_URL, json={"content": msg}, timeout=5)
        if r.status_code == 204:
            st.success(f"Messaggio Discord inviato correttamente per {tipo}")
        else:
            st.error(f"Errore invio Discord: status {r.status_code} - {r.text}")
    except Exception as e:
        st.error(f"Eccezione invio Discord: {e}")
