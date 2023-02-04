import discord
from discord import app_commands
from discord.ext import commands
from util.dbsetget import dbget, dbset


# Needs "manage role" perms

class verification(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="setverifiedrole",
                          description="Command used by a moderator or admin set the verified role.")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def setverifiedrole(self, interaction: discord.Interaction, role: discord.Role) -> None:
        try:
            await dbset(interaction.guild.id, self.bot.user.name, "verifiedroleid", role.id)
            await interaction.response.send_message(content=f"Verified role set to {role.mention}", ephemeral=True)
        except Exception as e:
            print(e)


    @app_commands.command(name="verifyfor", description="Command used by an admin to add user to the Verified role")
    @app_commands.checks.has_permissions(manage_roles=True)
    async def verifyfor(self, interaction: discord.Interaction, user: discord.User) -> None:
        verrole = await dbget(interaction.guild.id, self.bot.user.name, "verifiedroleid")
        role = discord.utils.get(interaction.guild.roles, id=verrole[0])
        if role:
            if role in user.roles:
                await interaction.response.send_message(f"User has already been verified.", ephemeral=True)
            else:
                unverrole = await dbget(interaction.guild.id, self.bot.user.name, "defaultroleid")
                oldrole = discord.utils.get(interaction.guild.roles, id=unverrole[0])
                await user.add_roles(role)
                await user.remove_roles(oldrole)
                await interaction.response.send_message(f"User has been added to the Verified role.", ephemeral=True)
        else:
            await interaction.response.send_message(f"No verified role found, have you ran /setverifiedrole?", ephemeral=True)

    @app_commands.command(name="verify", description="Command used to add user to the Verified role")
    async def verify(self, interaction: discord.Interaction) -> None:
        try:
            verrole = await dbget(interaction.guild.id, self.bot.user.name, "verifiedroleid")
            role = discord.utils.get(interaction.guild.roles, id=verrole[0])
            if role:
                if role in interaction.user.roles:
                    await interaction.response.send_message(f"You have already been verified.", ephemeral=True)
                else:
                    unverrole = await dbget(interaction.guild.id, self.bot.user.name, "defaultroleid")
                    if unverrole:
                        oldrole = discord.utils.get(interaction.guild.roles, id=unverrole[0])
                        await interaction.user.remove_roles(oldrole)
                    await interaction.user.add_roles(role)
                    await interaction.response.send_message(f"You have been added to the Verified role.", ephemeral=True)
            else:
                await interaction.response.send_message(f"No verified role found, has an admin ran /setunverifiedrole?",
                                                        ephemeral=True)
        except Exception as e:
            print(e)


async def setup(bot):
    await bot.add_cog(verification(bot))
