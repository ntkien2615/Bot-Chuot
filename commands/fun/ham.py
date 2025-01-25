import discord
from discord.ext import commands
from discord import app_commands
import random


class ham(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    @app_commands.command(name='ham', description='ham')
    @app_commands.describe(user='Người thứ nhất')
    async def ham(self, interaction: discord.Interaction, user:discord.Member):
        if user == None:
            interaction.user = user
        embed = discord.Embed(title="ham", description=f'🔥 {user.mention}', color=discord.Color.random())
        embed.set_image(url="https://cdn.discordapp.com/emojis/1029699276953100298.webp?size=128&animated=true")
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(ham(bot))