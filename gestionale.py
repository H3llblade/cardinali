import streamlit as st
from utils import leggi_file_github

st.set_page_config(page_title="Registro Finanze", page_icon="💰", layout="wide")

# Inizializza dati
if "dati" not in st.session_state:
    st.session_state.dati = leggi_file_github()

st.title("💰 Registro Finanze")
st.write("Usa il menu a sinistra per navigare tra le pagine")
