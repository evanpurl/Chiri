import asyncio
import discord
from discord.ext import commands, tasks
from database.database import gettoken
from database.testdbconnection import connect
from util.load_extensions import load_extensions
import logging

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = commands.Bot(command_prefix="$", intents=intents)

handler = logging.FileHandler(filename='chiri.log', encoding='utf-8', mode='w')


# Main function to load extensions and then load bot.
async def main():
    async with client:
        try:
            token = await gettoken("chiri")
            await connect()
            await load_extensions(client)
            await client.run(token[0], log_handler=handler, log_level=logging.DEBUG)
        except KeyboardInterrupt:
            pass


asyncio.run(main())  # Runs main function above
