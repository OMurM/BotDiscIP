import discord
from discord.ext import tasks
import requests
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))

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
