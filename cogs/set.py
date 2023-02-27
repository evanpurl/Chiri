import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import MissingPermissions
import datetime

from util.dbsetget import dbset

def cmdembed(bot, cmd, text):
    embed = discord.Embed(title=f"**{cmd} command**",
                          description=f"{text}",
                          color=discord.Color.blue(), timestamp=datetime.datetime.now())
    embed.set_author(name=bot.user.name, icon_url=bot.user.avatar)
    return embed


class setcmd(commands.GroupCog, name="set"):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="welcomechannel", description="Admin command to set configuration options.")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def welcomechannel(self, interaction: discord.Interaction, channel: discord.TextChannel):
        try:
            await dbset(interaction.guild.id, self.bot.user.name, "welcomechannelid", channel.id)
            await interaction.response.send_message(f"Your welcome channel has been set to {discord.utils.get(interaction.guild.channels, id=channel.id)}.", ephemeral=True)
        except Exception as e:
            print(e)
            await interaction.response.send_message(content=f"""Something went wrong.""", ephemeral=True)



    @app_commands.checks.has_permissions(manage_roles=True)
    @app_commands.command(name="defaultrole", description="Slash command for setting your server's Default role.")
    async def defaultrole(self, interaction: discord.Interaction, role: discord.Role):
        try:
            await dbset(interaction.guild.id, self.bot.user.name, "defaultroleid", role.id)
            await interaction.response.send_message(
                content=f"""You server's default role has been set to {role.name}""", ephemeral=True)
        except Exception as e:
            print(e)
            await interaction.response.send_message(content=f"""Something went wrong.""", ephemeral=True)

    @app_commands.command(name="messagechannel",
                          description="Command used by a moderator or admin set the message channel")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def messagechannel(self, interaction: discord.Interaction, channel: discord.TextChannel) -> None:
        try:
            await dbset(interaction.guild.id, self.bot.user.name, "messagechannelid", channel.id)
            await interaction.response.send_message(content=f"Message channel set to {channel}.", ephemeral=True)
        except Exception as e:
            print(e)

    @app_commands.command(name="verifiedrole", description="Command used by a moderator or admin set the verified role.")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def verifiedrole(self, interaction: discord.Interaction, role: discord.Role) -> None:
        try:
            await dbset(interaction.guild.id, self.bot.user.name, "verifiedroleid", role.id)
            await interaction.response.send_message(content=f"Verified role set to {role.mention}", ephemeral=True)
        except Exception as e:
            print(e)

    @app_commands.checks.has_permissions(manage_roles=True)
    @app_commands.command(name="pingrole", description="Admin command to set ping role")
    async def pingrole(self, interaction: discord.Interaction, role: discord.Role):
        try:
            await dbset(interaction.guild.id, self.bot.user.name, "pingroleid", role.id)
            await interaction.response.send_message(content=f"""Ping role has been set to {role.name}""",
                                                    ephemeral=True)
        except Exception as e:
            print(e)
            await interaction.response.send_message(content=f"""Something went wrong.""", ephemeral=True)



    @welcomechannel.error
    @defaultrole.error
    @messagechannel.error
    @verifiedrole.error
    @pingrole.error
    async def onerror(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        await interaction.response.send_message(content=error,
                                                ephemeral=True)


async def setup(bot):
    await bot.add_cog(setcmd(bot))