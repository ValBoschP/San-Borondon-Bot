import discord
import os
import random
import asyncio 
import json # Nuevo: para guardar el ranking
from discord.ext import commands, tasks
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
CANAL_VOZ_ID = int(os.getenv('CANAL_ID'))

categorias_texto = os.getenv('CATEGORIAS_PROHIBIDAS', '')
CATEGORIAS_PROHIBIDAS = [categoria.strip() for categoria in categorias_texto.split(',') if categoria.strip()]

intents = discord.Intents.default()
intents.message_content = True 

# case_insensitive=True hace que detecte EXPLORAR, explorar, EXplorar...
bot = commands.Bot(command_prefix='922', intents=intents, case_insensitive=True)

is_visible = False

# --- GESTIÓN DEL RANKING ---
def cargar_stats():
    if os.path.exists('stats.json'):
        with open('stats.json', 'r') as f:
            return json.load(f)
    return {}

def guardar_stats(stats):
    with open('stats.json', 'w') as f:
        json.dump(stats, f, indent=4)

@bot.event
async def on_ready():
    print(f'✅ Bot conectado como {bot.user}')
    print(f'Categorías protegidas (Lista negra): {CATEGORIAS_PROHIBIDAS}')
    
    canal = bot.get_channel(CANAL_VOZ_ID)
    if canal:
        rol_everyone = canal.guild.default_role
        await canal.set_permissions(rol_everyone, view_channel=False)
        print("La isla de San Borondón se ha ocultado al iniciar.")

    if not aparicion_automatica.is_running():
        aparicion_automatica.start()

# APARICION AUTOMATICA
@tasks.loop(seconds=1800)
async def aparicion_automatica():
    global is_visible
    
    if is_visible:
        return

    probabilidad_exito = 5
    tirada = random.randint(1, 100)

    if tirada <= probabilidad_exito:
        is_visible = True
        canal_voz = bot.get_channel(CANAL_VOZ_ID)
        
        if not canal_voz:
            print("Aviso: Revisa el ID del canal de voz en el .env")
            is_visible = False
            return

        rol_everyone = canal_voz.guild.default_role
        print("San Borondón ha aparecido asi por la cara.")
        await canal_voz.set_permissions(rol_everyone, view_channel=True)
        
        await asyncio.sleep(600)
        
        await canal_voz.set_permissions(rol_everyone, view_channel=False)
        is_visible = False
        print("San Borondón volvió a desaparecer.")
        
        categorias_validas = [cat for cat in canal_voz.guild.categories if cat.name not in CATEGORIAS_PROHIBIDAS]
        if categorias_validas:
            nueva_categoria = random.choice(categorias_validas)
            await canal_voz.edit(category=nueva_categoria)

# COMANDO EXPLORAR
@bot.command(name="explorar")
@commands.cooldown(1, 1200, commands.BucketType.user)
async def explorar(ctx):
    global is_visible
    
    if is_visible:
        ctx.command.reset_cooldown(ctx)
        await ctx.send("Mi hermano espabila que ya está visible sabes")
        return

    probabilidad_exito = 7.5
    tirada = random.uniform(1, 100) # Usamos uniform para admitir decimales en la tirada

    if tirada <= probabilidad_exito:
        is_visible = True
        
        # --- GUARDAR EN EL RANKING ---
        stats = cargar_stats()
        user_id = str(ctx.author.id)
        stats[user_id] = stats.get(user_id, 0) + 1
        guardar_stats(stats)
        # -----------------------------

        await ctx.send(f"Que locura, {ctx.author.mention}. Encontraste a San Borondon, brutal. \n**Tienen 10 minutos para entrar al canal antes de que vuelva a desaparecer**")
        
        canal = bot.get_channel(CANAL_VOZ_ID)
        rol_everyone = ctx.guild.default_role
        await canal.set_permissions(rol_everyone, view_channel=True)
        
        await asyncio.sleep(600)
        
        await canal.set_permissions(rol_everyone, view_channel=False)
        is_visible = False

        categorias_validas = [cat for cat in ctx.guild.categories if cat.name not in CATEGORIAS_PROHIBIDAS]
        if categorias_validas:
            nueva_categoria = random.choice(categorias_validas)
            await canal.edit(category=nueva_categoria)
            print(f"La isla ha se movió a la categoría: {nueva_categoria.name}")

        await ctx.send("La niebla tal ha vuelto, no se ve un carajo. San Borondón ha desaparecido")
        
    else:
        await ctx.send(f"{ctx.author.mention} bro no encontraste nada venga.")

# NUEVO COMANDO: RANKING
@bot.command(name="ranking")
async def ranking(ctx):
    stats = cargar_stats()
    if not stats:
        await ctx.send("Nadie ha encontrado la isla todavía, están todos en la mierda.")
        return

    # Ordenar por número de hallazgos
    ranking_ordenado = sorted(stats.items(), key=lambda item: item[1], reverse=True)
    
    mensaje = "🏆 **RANKING DE LOS TAL DE SAN BORONDÓN** 🏆\n"
    for i, (user_id, puntos) in enumerate(ranking_ordenado[:10], start=1):
        mensaje += f"{i}. <@{user_id}> - {puntos} veces encontrada\n"
    
    await ctx.send(mensaje)

@explorar.error
async def explorar_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        minutos = int(error.retry_after // 60)
        segundos = int(error.retry_after % 60)
        await ctx.send(f"{ctx.author.name} estas cansao hermano, para un poco y tal, tipo mas o menos **{minutos} minutos y {segundos} segundos**")

bot.run(TOKEN)