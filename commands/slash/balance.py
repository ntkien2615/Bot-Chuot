import discord, os
from discord import app_commands
from discord.ext import commands
import json

class Balance(commands.Cog):  # Capitalize class name for consistency
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="balance", description="Checks your (or someone else's) balance")  # Clearer description
    async def balance(self, interaction: discord.Interaction, member: discord.Member = None):
        if member is None:
            member = interaction.user

async def setup(bot):
    await bot.add_cog(Balance(bot))  # Use the corrected class name

