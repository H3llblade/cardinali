import discord
import json
import base64
import requests
from datetime import datetime

# -------------------------------
# CONFIG GITHUB
# -------------------------------
GITHUB_REPO_OWNER = "IL_TUO_OWNER"
GITHUB_REPO_NAME  = "IL_TUO_REPO"
GITHUB_TOKEN      = "IL_TUO_TOKEN_GITHUB"
HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"}

# Percorsi dei file JSON
FINANZE_FILE = "data/finanze.json"
COCA_FILE    = "data/processo_coca.json"

# -------------------------------
# FUNZIONI GITHUB
# -------------------------------
def leggi_file_github(file_path):
    url = f"https://api.github.com/repos/{GITHUB_REPO_OWNER}/{GITHUB_REPO_NAME}/contents/{file_path}"
    r = requests.get(url, headers=HEADERS)
    if r.status_code == 200:
        content = r.json()["content"]
        decoded = base64.b64decode(content).decode("utf-8")
        return json.loads(decoded)
    else:
        return {}

def aggiorna_file_github(dati, file_path):
    url = f"https://api.github.com/repos/{GITHUB_REPO_OWNER}/{GITHUB_REPO_NAME}/contents/{file_path}"
    r = requests.get(url, headers=HEADERS)
    sha = r.json().get("sha") if r.status_code == 200 else None

    json_str = json.dumps(dati, indent=4)
    json_base64 = base64.b64encode(json_str.encode("utf-8")).decode("utf-8")
    payload = {"message": f"Aggiornamento {file_path}", "content": json_base64}
    if sha:
        payload["sha"] = sha

    r = requests.put(url, headers=HEADERS, json=payload)
    if r.status_code not in [200, 201]:
        print(f"Errore aggiornamento GitHub: {r.json()}")

# -------------------------------
# LOGICA DEL BOT
# -------------------------------
TOKEN = "IL_TUO_TOKEN_DISCORD"  # Token bot Discord

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Bot online come {client.user}!")

@client.event
async def on_message(message):
    if message.author == client.user:
        return  # ignora messaggi del bot stesso

    # =========================
    # FINANZE
    # Comando: !registra <tipo> <valore> <causale>
    # es: !registra cassa 100 vendita
    # =========================
    if message.content.startswith("!registra"):
        try:
            parts = message.content.split()
            tipo = parts[1]  # cassa / soldi_sporchi / fondo_cassa
            valore = float(parts[2])
            causale = " ".join(parts[3:])
            
            dati = leggi_file_github(FINANZE_FILE)
            
            # aggiungi movimento
            dati["movimenti"].append({
                "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                "tipo": tipo,
                "causale": causale,
                "valore": valore
            })
            dati[tipo] += valore
            
            # aggiorna su GitHub
            aggiorna_file_github(dati, FINANZE_FILE)
            
            await message.channel.send(f"✅ Movimento registrato: {tipo} +{valore} $")
        except Exception as e:
            await message.channel.send(f"❌ Errore: {e}")

    # =========================
    # PROCESSO COCA
    # Comando: !coca <tipo> <valore>
    # es: !coca foglie 10
    # =========================
    if message.content.startswith("!coca"):
        try:
            parts = message.content.split()
            tipo = parts[1]  # foglie / panetti / bustine
            valore = float(parts[2])
            
            dati = leggi_file_github(COCA_FILE)
            dati[tipo] += valore
            aggiorna_file_github(dati, COCA_FILE)
            
            await message.channel.send(f"✅ Aggiornato {tipo} di {valore}")
        except Exception as e:
            await message.channel.send(f"❌ Errore: {e}")

client.run(TOKEN)
