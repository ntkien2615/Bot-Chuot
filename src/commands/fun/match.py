import discord
from discord.ext import commands
from discord import app_commands
import random


from src.commands.base_command import FunCommand


class match(FunCommand):
    def __init__(self,bot):
        super().__init__(bot)
    
    @app_commands.command(name='match', description='kiểm tra 2 người có hợp nhau không')
    @app_commands.describe(user1='Người thứ nhất', user2='Người thứ hai')
    async def match(self, interaction: discord.Interaction, user1: discord.Member, user2: discord.Member):
        if user1 is None or user2 is None:
            await interaction.response.send_message("Vui lòng nhập đúng cú pháp: /match <user1> <user2>, trộm vía chúng tôi không thể ghép người với m.a hoặc m.a với m.a được", ephemeral=True)
            return
        match = random.randint(0,100)
        embed = discord.Embed(title="", description=f'🔥 {user1.mention} và {user2.mention} có {match}% hợp nhau 🔥', color=discord.Color.random())
        await interaction.response.send_message(embed=embed)