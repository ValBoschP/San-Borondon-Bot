import discord
import os
import random 
from discord.ext import commands, tasks
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
CANAL_VOZ_ID = int(os.getenv('CANAL_ID'))
COOLDOWN_SEGUNDOS = 600

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot conectado exitosamente como {bot.user}')
    if not visibilidad_aleatoria.is_running():
        visibilidad_aleatoria.start()

@tasks.loop(seconds=COOLDOWN_SEGUNDOS)
async def visibilidad_aleatoria():
    canal = bot.get_channel(CANAL_VOZ_ID)
    
    if not canal:
        print("No se encontró el canal. Verifica que el ID sea correcto.")
        return

    rol_everyone = canal.guild.default_role

    hacer_visible = random.choice([True, False])

    try:
        if hacer_visible:
            await canal.set_permissions(rol_everyone, view_channel=True)
            print("El canal ahora es VISIBLE.")
        else:
            await canal.set_permissions(rol_everyone, view_channel=False)
            print("El canal ahora está OCULTO.")
            
    except discord.Forbidden:
        print("Error: El bot no tiene permiso de 'Gestionar Canales'.")

bot.run(TOKEN)