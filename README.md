# San Borondon Bot

Un bot de Discord interactivo construido en Python, inspirado en la leyenda canaria de la isla errante. Este bot gestiona un canal de voz oculto que los usuarios deben "descubrir" mediante comandos. Si tienen exito, la isla se revela temporalmente antes de volver a desaparecer y moverse a una nueva ubicacion al azar dentro del servidor.

## Caracteristicas Principales
- **Minijuego de exploracion:** Los usuarios utilizan el comando `!explorar` para intentar encontrar la isla, basado en un sistema de probabilidad (por defecto 7.5% de exito).
- **Cooldowns individuales:** Limita el uso del comando a una vez cada 20 minutos por usuario para evitar el spam de comandos.
- **Visibilidad temporal y alertas:** Al ser descubierta, la isla se hace visible durante 10 minutos y notifica a todo el servidor mediante una mencion.
- **Isla errante:** Cuando la niebla vuelve a cubrir San Borondon (pasados los 10 minutos), el canal se mueve automaticamente a una categoria aleatoria del servidor.
- **Lista negra de categorias:** Permite excluir categorias especificas (como zonas de administracion o canales de depuracion) mediante configuracion para que el canal nunca aparezca alli.
- **Seguridad:** Protege las credenciales y configuraciones sensibles utilizando un archivo `.env`.

## Requisitos Previos
- Python 3.8 o superior.
- Una aplicacion de bot en el Discord Developer Portal con los permisos de "Manage Channels" y "Manage Roles".
- El **Message Content Intent** activado en la pestaña "Bot" del portal de desarrolladores de Discord.

## Instalacion y Configuracion
1. Clona o descarga este repositorio en tu maquina local.

2. Instala las dependencias necesarias abriendo tu terminal y ejecutando:
   ```bash
   pip install discord.py python-dotenv
   ```
3. Crea un archivo `.env` en la raiz del proyecto.
4. Añade tu configuracion al archivo `.env` sin usar comillas. Separa las categorias prohibidas por comas:
    ```PLAINTEXT
    DISCORD_TOKEN=tu_token_aqui
    CANAL_ID=123456789012345678
    CATEGORIAS_PROHIBIDAS=Categoria1,Categoria2,Categoria3
    ```

## Uso
Inicia el bot ejecutando el siguiente comando en tu terminal:
```bash
python san-borondon-bot.py
```
Una vez encendido, los usuarios podran interactuar con el bot escribiendo el comando `!explorar` en cualquier canal de texto.

## Ajustes Personalizados
Puedes modificar la dificultad y los tiempos editando las siguientes variables directamente en el archivo `bot.py`:´
- **Probabilidad de exito:** Busca la variable `probabilidad_exito = 7.5` y cambiala al porcentaje que desees (ejemplo: 10 para un 10%).
- **Tiempo de visibilidad:** Busca la linea `await asyncio.sleep(600)` y cambia `600` (10 minutos) por la cantidad de segundos que la isla debe permanecer visible.
- **Tiempo de espera (Cooldown):** Busca la linea `@commands.cooldown(1, 1800, commands.BucketType.user)` y cambia `1800` por los segundos de espera entre intentos por usuario (1800 = 30 minutos).