import discord
from discord.ext import commands
from discord import app_commands
import random


class match(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    @app_commands.command(name='match', description='kiểm tra 2 người có hợp nhau không')
    @app_commands.describe(user1='Người thứ nhất', user2='Người thứ hai')
    async def match(self, interaction: discord.Interaction, user1:discord.Member, user2:discord.Member):
        if user1 == None or user2 == None:
            await interaction.response.send_message("Vui lòng nhập đúng cú pháp: /match <user1> <user2>, trộm vía chúng tôi không thể ghép người với m.a hoặc m.a với m.a được", empheral=True)
            return
        match = random.randint(0,100)
        embed = discord.Embed(title="", description=f'🔥 {user1.mention} và {user2.mention} có {match}% hợp nhau 🔥', color=discord.Color.random())
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(match(bot))