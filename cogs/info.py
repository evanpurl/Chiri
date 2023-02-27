import datetime
import discord
from discord import app_commands
from discord.ext import commands


def cmdembed(bot, cmd, text):
    embed = discord.Embed(title=f"**{cmd} command**",
                          description=f"{text}",
                          color=discord.Color.blue(), timestamp=datetime.datetime.now())
    embed.set_author(name=bot.user.name, icon_url=bot.user.avatar)
    return embed


class infocmd(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="info", description="Command to check command info")
    @app_commands.checks.has_permissions(manage_channels=True)
    @app_commands.choices(command=[
        app_commands.Choice(name='welcomechannel', value=1),
        app_commands.Choice(name='defaultrole', value=2),
        app_commands.Choice(name='messagechannel', value=3),
        app_commands.Choice(name='verifiedrole', value=4),
        app_commands.Choice(name='pingrole', value=5),
        app_commands.Choice(name='verify', value=6),
        app_commands.Choice(name='verifyfor', value=7),
        app_commands.Choice(name='gender', value=8),
        app_commands.Choice(name='pronouns', value=9),
        app_commands.Choice(name='dmstatus', value=10),
        app_commands.Choice(name='purge', value=11),
        app_commands.Choice(name='warn', value=12),
        app_commands.Choice(name='report', value=13),
        app_commands.Choice(name='ping', value=14),
        app_commands.Choice(name='pat', value=15),
    ])
    async def info(self, interaction: discord.Interaction, command: app_commands.Choice[int], ephemeral: bool = False):
        try:
            if command.value == 1:  # set welcomechannel
                await interaction.response.send_message(
                    embed=cmdembed(bot=self.bot, cmd="set welcomechannel", text="The /set welcomechannel "
                                                                                "command is used to set "
                                                                                "your bot's welcome "
                                                                                "channel!."),
                    ephemeral=ephemeral)
            elif command.value == 2:  # set defaultrole
                await interaction.response.send_message(
                    embed=cmdembed(bot=self.bot, cmd="set defaultrole", text="The /set defaultrole "
                                                                             "command is used to set "
                                                                             "your members' default "
                                                                             "role when joining the server."),
                    ephemeral=ephemeral)
            elif command.value == 3:  # set messagechannel
                await interaction.response.send_message(
                    embed=cmdembed(bot=self.bot, cmd="set messagechannel", text="The /set messagechannel "
                                                                                "command is used to set "
                                                                                "your bot's message "
                                                                                "channel, which tracks edits and deletes of "
                                                                                "messages."),
                    ephemeral=ephemeral)
            elif command.value == 4:  # set verifiedrole
                await interaction.response.send_message(
                    embed=cmdembed(bot=self.bot, cmd="set verifiedrole", text="The /set verifiedrole "
                                                                              "command is used to set "
                                                                              "the role a member gets when running /verify."),
                    ephemeral=ephemeral)
            elif command.value == 5:  # set pingrole
                await interaction.response.send_message(
                    embed=cmdembed(bot=self.bot, cmd="set pingrole", text="The set pingrole "
                                                                          "command is used to set "
                                                                          "the role a member gets when running /ping."),
                    ephemeral=ephemeral)
            elif command.value == 6:  # verify
                await interaction.response.send_message(
                    embed=cmdembed(bot=self.bot, cmd="verify",
                                   text="The /verify command is used to verify you're a human on the server."),
                    ephemeral=ephemeral)
            elif command.value == 7:  # verifyfor
                await interaction.response.send_message(
                    embed=cmdembed(bot=self.bot, cmd="verifyfor",
                                   text="The /verifyfor command is used by an admin to verify a user."),
                    ephemeral=ephemeral)
            elif command.value == 8:  # gender
                await interaction.response.send_message(
                    embed=cmdembed(bot=self.bot, cmd="gender",
                                   text="The /gender command is used to set a role with your preferred gender."),
                    ephemeral=ephemeral)
            elif command.value == 9:  # pronouns
                await interaction.response.send_message(
                    embed=cmdembed(bot=self.bot, cmd="pronouns",
                                   text="The /pronouns command is used to set a role with your preferred pronouns."),
                    ephemeral=ephemeral)
            elif command.value == 10:  # dmstatus
                await interaction.response.send_message(
                    embed=cmdembed(bot=self.bot, cmd="dmstatus",
                                   text="The /dmstatus command is used to set your dmstatus as a role."),
                    ephemeral=ephemeral)
            elif command.value == 11:  # purge
                await interaction.response.send_message(
                    embed=cmdembed(bot=self.bot, cmd="purge",
                                   text="The /purge command is used by an admin to purge messages."),
                    ephemeral=ephemeral)
            elif command.value == 12:  # warn
                await interaction.response.send_message(
                    embed=cmdembed(bot=self.bot, cmd="warn",
                                   text="The /warn command is used by an admin to warn members."),
                    ephemeral=ephemeral)
            elif command.value == 13:  # report
                await interaction.response.send_message(
                    embed=cmdembed(bot=self.bot, cmd="report",
                                   text="The /report command is used by members to report a member."),
                    ephemeral=ephemeral)
            elif command.value == 14:  # ping
                await interaction.response.send_message(
                    embed=cmdembed(bot=self.bot, cmd="ping",
                                   text="The /ping command is used to add yourself to the ping role (If one is set)"),
                    ephemeral=ephemeral)
            elif command.value == 15:  # pat
                await interaction.response.send_message(
                    embed=cmdembed(bot=self.bot, cmd="pat",
                                   text=f"The /pat command is used to have {self.bot.user.name} pat yourself or a friend!"),
                    ephemeral=ephemeral)
        except Exception as e:
            print(e)

    @info.error
    async def onerror(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        await interaction.response.send_message(content=error,
                                                ephemeral=True)


async def setup(bot):
    await bot.add_cog(infocmd(bot))