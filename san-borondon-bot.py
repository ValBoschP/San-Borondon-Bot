import discord
import os
import random
import asyncio 
import json 
from discord.ext import commands, tasks
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
CANAL_VOZ_ID = int(os.getenv('CANAL_ID'))

categorias_texto = os.getenv('CATEGORIAS_PROHIBIDAS', '')
CATEGORIAS_PROHIBIDAS = [categoria.strip() for categoria in categorias_texto.split(',') if categoria.strip()]

intents = discord.Intents.default()
intents.message_content = True 

bot = commands.Bot(command_prefix=['922', '922 '], intents=intents, case_insensitive=True)

is_visible = False

# --- LISTA MODULAR DE EVENTOS ---
EVENTOS_FALLO = [
    {"peso": 5, "tipo": "bueno", "texto": "Pero que leches, {mention}! Un ferry de Fred Olsen pasó a toda hostia y su estela disipó la niebla de golpe. **Puedes volver a usar `922explorar` AHORA MISMO**"},
    {"peso": 7, "tipo": "malo", "texto": "{mention}, se acaba de meter una calima nivel carnavales 2020. Si apenas puedes respirar, menos vas a ver San Borondón."},
    {"peso": 7, "tipo": "malo", "texto": "{mention}, se te acercó un guiri perdido en un patinete acuático preguntando dónde está el Siam Park. Perdiste todo el tiempo intentando explicarle."},
    {"peso": 7, "tipo": "malo", "texto": "{mention}, te paraste a comerte un bocadillo de pata con queso y te olvidaste de buscar."},
    {"peso": 7, "tipo": "malo", "texto": "{mention}, un choco gigante te acaba de cumear un chorro de tinta directo en la cara. No ves un carajo, espabila."},
    {"peso": 7, "tipo": "malo", "texto": "{mention}, te quedaste esperando a que pasara la guagua, pero te dejó tirado porque iba llena. Puta titsa siempre la misma mrda"},
    {"peso": 7, "tipo": "malo", "texto": "{mention}, te cruzaste con una romería. Te dieron un vaso de vino y un pincho de carne fiesta, y se te olvidó por completo lo que estabas buscando."},
    {"peso": 20, "tipo": "malo", "texto": "{mention} bro no encontraste nada venga."}
]

PESOS_EVENTOS = [evento["peso"] for evento in EVENTOS_FALLO]
# ---------------------------------

# --- GESTIÓN DEL RANKING ---
def cargar_stats():
    if os.path.exists('stats.json'):
        try:
            with open('stats.json', 'r') as f:
                return json.load(f)
        except Exception as e:
            print("Aviso: El archivo stats.json estaba vacío. Empezando de cero.")
            return {}
    return {}

def guardar_stats(stats):
    with open('stats.json', 'w') as f:
        json.dump(stats, f, indent=4)
# ---------------------------

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
        try:
            canal_voz = bot.get_channel(CANAL_VOZ_ID) or await bot.fetch_channel(CANAL_VOZ_ID)
            
            if not canal_voz:
                print("Aviso: Revisa el ID del canal de voz en el .env")
                return

            rol_everyone = canal_voz.guild.default_role
            print("San Borondón ha aparecido así por la cara.")
            await canal_voz.set_permissions(rol_everyone, view_channel=True)
            
            await asyncio.sleep(600)
            
            await canal_voz.set_permissions(rol_everyone, view_channel=False)
            print("San Borondón volvió a desaparecer.")
            
            categorias_validas = [cat for cat in canal_voz.guild.categories if cat.name not in CATEGORIAS_PROHIBIDAS]
            if categorias_validas:
                nueva_categoria = random.choice(categorias_validas)
                await canal_voz.edit(category=nueva_categoria)
        except Exception as e:
            print(f"Error en aparición automática: {e}")
        finally:
            is_visible = False

# COMANDO EXPLORAR
@bot.command(name="explorar")
@commands.cooldown(1, 1200, commands.BucketType.user)
async def explorar(ctx):
    global is_visible
    
    if is_visible:
        ctx.command.reset_cooldown(ctx)
        await ctx.send("Mi hermano espabila que ya está visible sabes")
        return

    probabilidad_exito = 10
    tirada = random.uniform(1, 100) 

    if tirada <= probabilidad_exito:
        is_visible = True
        try:
            stats = cargar_stats()
            user_id = str(ctx.author.id)
            stats[user_id] = stats.get(user_id, 0) + 1
            guardar_stats(stats)

            await ctx.send(f"Que locura, {ctx.author.mention}. Encontraste a San Borondon, brutal. \n**Tienen 10 minutos para entrar al canal antes de que vuelva a desaparecer**")
            
            canal = bot.get_channel(CANAL_VOZ_ID)
            if not canal:
                try:
                    canal = await bot.fetch_channel(CANAL_VOZ_ID)
                except Exception:
                    canal = None

            if canal:
                rol_everyone = ctx.guild.default_role
                await canal.set_permissions(rol_everyone, view_channel=True)
                
                await asyncio.sleep(600)
                
                await canal.set_permissions(rol_everyone, view_channel=False)

                categorias_validas = [cat for cat in ctx.guild.categories if cat.name not in CATEGORIAS_PROHIBIDAS]
                if categorias_validas:
                    nueva_categoria = random.choice(categorias_validas)
                    await canal.edit(category=nueva_categoria)
                    print(f"La isla se movió a la categoría: {nueva_categoria.name}")

                await ctx.send("La niebla tal ha vuelto, no se ve un carajo. San Borondón ha desaparecido")
            else:
                print("Error: No se encontró el canal de voz especificado.")
        except Exception as e:
            print(f"Error procesando el descubrimiento de la isla: {e}")
        finally:
            is_visible = False
        
    else:
        # --- GESTOR DE EVENTOS ---
        evento_elegido = random.choices(EVENTOS_FALLO, weights=PESOS_EVENTOS, k=1)[0]
        
        mensaje_final = evento_elegido["texto"].format(mention=ctx.author.mention)
        
        if evento_elegido["tipo"] == "bueno":
            ctx.command.reset_cooldown(ctx)
            
        await ctx.send(mensaje_final)

# COMANDO RANKING
@bot.command(name="ranking")
async def ranking(ctx):
    stats = cargar_stats()
    if not stats:
        await ctx.send("Nadie ha encontrado la isla todavía, están todos perdidos.")
        return

    ranking_ordenado = sorted(stats.items(), key=lambda item: item[1], reverse=True)
    
    mensaje = "🏆 **RANKING DE EXPLORADORES DE SAN BORONDÓN** 🏆\n"
    for i, (user_id, puntos) in enumerate(ranking_ordenado[:10], start=1):
        mensaje += f"**{i}.** <@{user_id}> - {puntos} veces encontrada\n"
    
    await ctx.send(mensaje)

@explorar.error
async def explorar_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        minutos = int(error.retry_after // 60)
        segundos = int(error.retry_after % 60)
        await ctx.send(f"{ctx.author.mention} estas cansao hermano, para un poco y tal, tipo mas o menos **{minutos} minutos y {segundos} segundos**.")

bot.run(TOKEN)