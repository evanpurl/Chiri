import asyncio
import discord
from discord.ext import commands, tasks
from database.database import gettoken
from database.testdbconnection import connect
from util.load_extensions import load_extensions

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = commands.Bot(command_prefix="$", intents=intents)


# Main function to load extensions and then load bot.
async def main():
    async with client:
        try:
            token = await gettoken("Chiri")
            await connect()
            await load_extensions(client)
            await client.start(token[0])
        except KeyboardInterrupt:
            pass


asyncio.run(main())  # Runs main function above
