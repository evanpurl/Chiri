import discord
from discord import app_commands
from discord.ext import commands
from util.dbsetget import dbget, dbset

# Needs "manage role" perms
"Requires verifiedroleid in db"


def verifymessageembed(server):
    embed = discord.Embed(title=f"**{server.name} Verification Process**",
                          description=f"This server requires you to verify that you're a human. To do so, click the "
                                      f"Verify button below.",
                          color=discord.Color.blue())
    return embed


class Verifybuttonpanel(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Verify", emoji="✅", style=discord.ButtonStyle.green,
                       custom_id="Chiri:verify")
    async def verify_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            verrole = await dbget(interaction.guild.id, interaction.client.user.name, "verifiedroleid")
            role = discord.utils.get(interaction.guild.roles, id=verrole[0])
            if role:
                if role in interaction.user.roles:
                    await interaction.response.send_message(f"You have already been verified.", ephemeral=True)
                else:
                    await interaction.user.add_roles(role)
                    await interaction.response.send_message(f"You have been added to the Verified role.",
                                                            ephemeral=True)
            else:
                await interaction.response.send_message(f"Verified role does not exist, please contact an admin.",
                                                        ephemeral=True)

        except discord.Forbidden:
            await interaction.response.send_message(
                content=f"""Unable to set your role, make sure my role is higher than the role you're trying to add!""",
                ephemeral=True)


class verification(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="verifybutton", description="Command used by an admin to send the verify button message")
    @app_commands.checks.has_permissions(manage_roles=True)
    async def vbutton(self, interaction: discord.Interaction) -> None:
        try:
            await interaction.response.send_message(embed=verifymessageembed(interaction.guild),
                                                    view=Verifybuttonpanel())
        except Exception as e:
            print(e)

    @app_commands.command(name="verifyfor", description="Command used by an admin to add user to the Verified role")
    @app_commands.checks.has_permissions(manage_roles=True)
    async def verifyfor(self, interaction: discord.Interaction, user: discord.User) -> None:
        try:
            verrole = await dbget(interaction.guild.id, self.bot.user.name, "verifiedroleid")
            role = discord.utils.get(interaction.guild.roles, id=verrole[0])
            if role:
                if role in user.roles:
                    await interaction.response.send_message(f"User has already been verified.", ephemeral=True)
                else:
                    await user.add_roles(role)
                    await interaction.response.send_message(f"User has been added to the Verified role.",
                                                            ephemeral=True)
            else:
                await interaction.response.send_message(f"No verified role found, have you ran /setverifiedrole?",
                                                        ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message(
                content=f"""Unable to set your role, make sure my role is higher than the role you're trying to add!""",
                ephemeral=True)

    @app_commands.command(name="setverifiedrole", description="Command used to set the Verified role")
    @app_commands.checks.has_permissions(manage_roles=True)
    async def verifiedrole(self, interaction: discord.Interaction, role: discord.Role) -> None:
        try:
            await dbset(interaction.guild.id, self.bot.user.name, "verifiedroleid", role.id)
            await interaction.response.send_message(content=f"Verified role set to {role.mention}", ephemeral=True)
        except Exception as e:
            print(e)

    @app_commands.command(name="resetverifiedrole", description="Command used to reset the Verified role")
    @app_commands.checks.has_permissions(manage_roles=True)
    async def resetverifiedrole(self, interaction: discord.Interaction) -> None:
        try:
            await dbset(interaction.guild.id, self.bot.user.name, "verifiedroleid", 0)
            await interaction.response.send_message(f"Verified Role config has been reset.", ephemeral=True)
        except Exception as e:
            print(e)

    @verifyfor.error
    @verifiedrole.error
    @resetverifiedrole.error
    async def onerror(self, interaction: discord.Interaction, error: app_commands.MissingPermissions):
        await interaction.response.send_message(content=error,
                                                ephemeral=True)


async def setup(bot):
    await bot.add_cog(verification(bot))
    bot.add_view(Verifybuttonpanel())
