import requests
import json
import base64
from datetime import datetime
import streamlit as st

# Config GitHub (puoi modificare dopo con i tuoi secrets)
GITHUB_API_URL = "https://api.github.com/repos/tuo_username/tuo_repo/contents/finanze.json"
HEADERS = {"Authorization": f"token TUO_TOKEN_GITHUB"}

WEBHOOK_URL = None  # Se vuoi Discord, metti il webhook qui

def leggi_file_github():
    # Inizializza dati se il file non esiste
    return {"cassa": 0, "fondo_cassa": 0, "soldi_sporchi": 0, "movimenti": []}

def aggiorna_file_github(dati):
    # Funzione placeholder per aggiornare GitHub (poi puoi implementare)
    pass

def registra_movimento(tipo, causale, valore):
    dati = st.session_state.dati

    dati["movimenti"].append({
        "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "tipo": tipo,
        "causale": causale,
        "valore": valore
    })

    dati[tipo] += valore
    # aggiorna_file_github(dati)  # opzionale per ora

def formatta(num):
    return f"{round(num):,}".replace(",", ".")
