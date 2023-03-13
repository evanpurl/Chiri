import discord
from discord import app_commands
from discord.ext import commands


class clapcmd(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.checks.has_permissions(manage_roles=True)
    @app_commands.command(name="clap", description="Command for the bot to clap for you or a friend.")
    async def pat(self, interaction: discord.Interaction, user: discord.User = None):
        try:
            if user is None:
                await interaction.response.send_message(content=f"""{self.bot.user.name} claps for you 👏""", ephemeral=True)
            else:
                if user.id == self.bot.user.id:
                    await interaction.response.send_message(content=f"""{self.bot.user.name} claps for themselves. 👏""", ephemeral=True)
                else:
                    await interaction.response.send_message(content=f"""{self.bot.user.name} claps for {user.mention}! 👏""")
        except Exception as e:
            print(e)
            await interaction.response.send_message(content=f"""Something went wrong.""", ephemeral=True)


async def setup(bot):
    await bot.add_cog(clapcmd(bot))
