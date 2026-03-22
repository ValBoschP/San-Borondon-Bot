import discord
import os
import random
import asyncio 
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
CANAL_VOZ_ID = int(os.getenv('CANAL_ID'))

intents = discord.Intents.default()
intents.message_content = True 

bot = commands.Bot(command_prefix='922', intents=intents)

is_visible = False

@bot.event
async def on_ready():
    print(f'✅ Bot conectado exitosamente como {bot.user}')
    
    canal = bot.get_channel(CANAL_VOZ_ID)
    if canal:
        rol_everyone = canal.guild.default_role
        await canal.set_permissions(rol_everyone, view_channel=False)
        print("La isla de San Borondón se ha ocultado al iniciar.")

@bot.command(name="explorar")
@commands.cooldown(1, 1200, commands.BucketType.user)
async def explorar(ctx):
    global is_visible
    
    if is_visible:
        ctx.command.reset_cooldown(ctx)
        await ctx.send("Mi hermano espabila que ya está visible sabes")
        return

    probabilidad_exito = 7.5
    tirada = random.randint(1, 100)

    if tirada <= probabilidad_exito:
       
        is_visible = True
        await ctx.send(f"Que locura, {ctx.author.mention}. Encontraste a San Borondon, brutal. \n**Tienen 10 minutos para entrar al canal antes de que vuelva a desaparecer**")
        
        canal = bot.get_channel(CANAL_VOZ_ID)
        rol_everyone = ctx.guild.default_role
        
        await canal.set_permissions(rol_everyone, view_channel=True)
        
        await asyncio.sleep(600)
        
        await canal.set_permissions(rol_everyone, view_channel=False)
        is_visible = False
        await ctx.send("La niebla tal ha vuelto, no se ve un carajo. San Borondón ha desaparecido")
        
    else:

        await ctx.send(f"{ctx.author.mention} bro no encontraste nada venga.")

@explorar.error
async def explorar_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        minutos = int(error.retry_after // 60)
        segundos = int(error.retry_after % 60)
        await ctx.send(f"{ctx.author.name} estas cansao hermano, para un poco y tal, tipo mas o menos **{minutos} minutos y {segundos} segundos**")

bot.run(TOKEN)