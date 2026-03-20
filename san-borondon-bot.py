import discord
import os
from discord.ext import commands, tasks
from dotenv import load_dotenv

load_dotenv()
# --- CONFIGURACIÓN PRINCIPAL ---
TOKEN = os.getenv('DISCORD_TOKEN')
CANAL_VOZ_ID = iny(os.getenv('CANAL_ID'))
COOLDOWN_SEGUNDOS = 900  # 10 minutos

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

canal_visible = True 

@bot.event
async def on_ready():
    print(f'Bot conectado exitosamente como {bot.user}')
    if not alternar_visibilidad.is_running():
        alternar_visibilidad.start()

@tasks.loop(seconds=COOLDOWN_SEGUNDOS)
async def alternar_visibilidad():
    global canal_visible
    
    canal = bot.get_channel(CANAL_VOZ_ID)
    
    if not canal:
        print("No se encontró el canal. Verifica que el ID sea correcto.")
        return

    rol_everyone = canal.guild.default_role

    try:
        if canal_visible:
            # Ocultamos el canal
            await canal.set_permissions(rol_everyone, view_channel=False)
            print("Canal ocultado.")
            canal_visible = False
        else:
            # Mostramos el canal
            await canal.set_permissions(rol_everyone, view_channel=True)
            print("Canal visible.")
            canal_visible = True
            
    except discord.Forbidden:
        print("Error: El bot no tiene permiso de 'Gestionar Canales'.")

bot.run(TOKEN)