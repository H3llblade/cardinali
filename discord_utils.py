import requests
from datetime import datetime
import streamlit as st

WEBHOOK_URL = st.secrets.get("DISCORD_WEBHOOK_URL")  # Webhook Discord

def invia_discord(tipo: str, causale: str, valore: float, totale: float):
    """Invia messaggi su Discord per movimenti finanziari."""
    if not WEBHOOK_URL:
        st.warning("Webhook Discord non impostato!")
        return
    
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
