import discord
from discord import app_commands
from discord.ext import commands
from util.dbsetget import dbset, dbget


class messagefunctions(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="setmessagechannel",
                          description="Command used by a moderator or admin set the message channel")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def setmessagechannel(self, interaction: discord.Interaction, channel: discord.TextChannel) -> None:
        try:
            await dbset(interaction.guild.id, self.bot.user.name, "messagechannelid", channel.id)
            await interaction.response.send_message(content=f"Message channel set to {channel}.", ephemeral=True)
        except Exception as e:
            print(e)

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        try:
            if len(message.content) <= 1500:
                msgchnl = await dbget(message.guild.id, self.bot.user.name, "messagechannelid")
                if msgchnl:
                    channel = discord.utils.get(message.guild.channels, id=msgchnl[0])
                    await channel.send(f"Message from {message.author.name} in channel {message.channel.mention} deleted: {message.content}")
            else:
                msgchnl = await dbget(message.guild.id, self.bot.user.name, "messagechannelid")
                if msgchnl:
                    channel = discord.utils.get(message.guild.channels, id=msgchnl[0])
                    await channel.send(
                         f"Message from {message.author.name} in channel {message.channel.mention} deleted: content too long to send.")
        except Exception as e:
            print(e)

    @commands.Cog.listener()
    async def on_message_edit(self, message_before: discord.Message, message_after: discord.Message):
        try:
            msgsum = sum([len(message_before.content), len(message_after.content)])
            if msgsum <= 1500:
                msgchnl = await dbget(message_before.guild.id, self.bot.user.name, "messagechannelid")
                if msgchnl:
                    channel = discord.utils.get(message_before.guild.channels, id=msgchnl[0])
                    await channel.send(f"Message from {message_before.author.name} in channel {message_before.channel.mention} edited from {message_before.content} to {message_after.content}")
            else:
                msgchnl = await dbget(message_before.guild.id, self.bot.user.name, "messagechannelid")
                if msgchnl:
                    channel = discord.utils.get(message_before.guild.channels, id=msgchnl[0])
                    await channel.send(
                        f"Message from {message_before.author.name} in channel {message_before.channel.mention} edited: content too long to send.")
        except Exception as e:
            print(e)


async def setup(bot: commands.Cog):
    await bot.add_cog(messagefunctions(bot))
