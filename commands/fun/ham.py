import discord
from discord.ext import commands
from discord import app_commands
import random


class match(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    @app_commands.command(name='ham', description='ham')
    @app_commands.describe(user='Người thứ nhất')
    async def match(self, interaction: discord.Interaction, user:discord.Member):
        if user == None:
            interaction.user = user
        match = random.randint(0,100)
        embed = discord.Embed(title="ham", description=f'🔥 {user.mention}', color=discord.Color.random())
        embed.set_image(url="https://th.bing.com/th/id/OIP.3I9zIQg4SUu9pMO9vZcosQHaEK?rs=1&pid=ImgDetMain")
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(match(bot))