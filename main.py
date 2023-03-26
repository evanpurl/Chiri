import asyncio
import discord
from discord.ext import commands
from database.database import gettoken
from database.testdbconnection import connect
from util.load_extensions import load_extensions
import logging
import logging.handlers

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = commands.Bot(command_prefix="$", intents=intents)


logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
logging.getLogger('discord.http').setLevel(logging.INFO)

handler = logging.handlers.RotatingFileHandler(
    filename='chiri.log',
    encoding='utf-8',
    maxBytes=32 * 1024 * 1024,  # 32 MiB
    backupCount=5,  # Rotate through 5 files
)
dt_fmt = '%Y-%m-%d %H:%M:%S'
formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')
handler.setFormatter(formatter)
logger.addHandler(handler)


# Main function to load extensions and then load bot.
async def main():
    async with client:
        try:
            token = await gettoken("chiri")
            await connect()
            await load_extensions(client)
            await client.start(token[0])
        except KeyboardInterrupt:
            pass


asyncio.run(main())  # Runs main function above
