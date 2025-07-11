import discord
from discord.ext import commands
from discord import app_commands
import random


from src.commands.base_command import FunCommand


class ham(FunCommand):
    def __init__(self,bot):
        super().__init__(bot)
    
    @app_commands.command(name='ham', description='ham')
    @app_commands.describe(user='Người muốn ham')
    async def ham(self, interaction: discord.Interaction, user: discord.Member = None):
        if user is None:
            user = interaction.user
            
        embed = discord.Embed(title="ham", description=f'🔥 {user.mention}', color=discord.Color.random())
        embed.set_image(url="https://cdn.discordapp.com/emojis/1029699276953100298.webp?size=128&animated=true")
        await interaction.response.send_message(embed=embed)