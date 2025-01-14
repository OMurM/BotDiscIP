import discord
from discord.ext import tasks
import requests

TOKEN = 'MTMyODg2NTc4MzU1MTYyNzMxNQ.GCuGWn.hQc5aNmohSZSYJE6x92rNwCSSOqP9TMFqxgSn4'
CHANNEL_ID = 1328866536282132524

intents = discord.Intents.default()
client = discord.Client(intents=intents)

def obtener_ip_publica():
    try:
        response = requests.get('https://api.ipify.org')
        if response.status_code == 200:
            return response.text
        else:
            return "Error al obtener la IP pública"
    except Exception as e:
        return f"Error: {e}"

@tasks.loop(minutes=10)
async def enviar_ip():
    channel = client.get_channel(CHANNEL_ID)
    if channel:
        ip = obtener_ip_publica()
        await channel.send(f"Tu IP pública actual es: {ip}")

@client.event
async def on_ready():
    print(f'Bot conectado como {client.user}')
    enviar_ip.start()
client.run(TOKEN)
