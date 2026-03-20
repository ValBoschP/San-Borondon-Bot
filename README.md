# San-Borondon-Bot
Un bot de Discord ligero y automatizado construido en Python. Su funcion principal es alternar la visibilidad de un canal de voz especifico en intervalos de tiempo regulares, ocultandolo y mostrandolo al rol general del servidor.

Es una herramienta ideal para gestionar canales temporales, eventos programados o limitar el acceso a ciertas areas del servidor de forma intermitente.

## Caracteristicas Principales

- Alternancia automatica de los permisos de visualizacion (`view_channel`) para el rol `@everyone`.
- Ejecucion autonoma en segundo plano utilizando la extension `tasks` de `discord.py`.
- Configuracion segura: protege el Token del bot y el ID del canal utilizando variables de entorno (`.env`).

## Requisitos Previos

Antes de ejecutar este bot, necesitaras:

- Python 3.8 o superior instalado en tu sistema.
- Una aplicacion de bot creada en el Discord Developer Portal (con los permisos de "Manage Channels" y "Manage Roles").
- El Token secreto de tu bot.
- El ID numerico del canal de voz que deseas controlar (requiere tener el Modo Desarrollador activo en tu cliente de Discord).

## Instalacion y Configuracion

1. Clona este repositorio en tu maquina local o descarga los archivos.

2. Abre una terminal en la carpeta del proyecto e instala las dependencias necesarias ejecutando:
  ```bash
   pip install discord.py python-dotenv
  ```
3. Crea un archivo llamado exactamente `.env` en la raiz del directorio del proyecto.
4. Abre el archivo `.env` con un editor de texto y añade tus datos sin usar comillas:
   ```
   DISCORD_TOKEN=tu_token_aqui
   CHANNEL_ID=id_del_canal_aqui
   ```
_Nota: El repositorio incluye un archivo `.gitignore` configurado para ignorar el `.env`, garantizando que tus credenciales nunca se suban a GitHub._

## Uso
Para poner en marcha el bot, navega hasta el directorio del proyecto en tu terminal y ejecuta:
```bash
python san-borondon-bot.py
```
Si la configuracion es correcta, la consola mostrara un mensaje indicando que el bot se ha conectado exitosamente y el ciclo de alternancia de visibilidad comenzara de inmediato.

## Ajustes Personalizados
Puedes modificar el tiempo que el bot espera antes de cambiar la visibilidad del canal. Para ello, abre el archivo bot.py y busca la siguiente variable:
```python
COOLDOWN_SEGUNDOS = 600
```
Cambia `600` por la cantidad de segundos que prefieras (por ejemplo, `300` para 5 minutos). Se recomienda no usar valores excesivamente bajos para evitar limites de tasa (Rate Limits) por parte de la API de Discord.