import discord
from discord.ext import commands
from discord import app_commands
import random


class momoi(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    def random_file_read(self, file_path):
            try:
                with open(file_path, "r") as f:
                    lines = f.readlines()
                if lines:
                    return random.choice(lines).strip()
            except (IndexError, FileNotFoundError) as e:
                return None

    @app_commands.command(name='momoi',description='momoi ní...') 
    @app_commands.describe(user='Người muốn được đua xe')
    async def moimoi(self, interaction:discord.Interaction, user:discord.Member):
        if (userr == None) or (user == interaction.user):
            await interaction.response.send_message('Nhập người nào vào đi',ephemeral=True)
            return
        else:      
            momoi = self.random_file_read('./txt_files/moimoi.txt')
            embed = discord.Embed(title="", description="", color=discord.Color.random())
            embed.set_image(url=momoi)

        await interacton.response.send_message(f"<@{user.id}>",embed=embed)

async def setup(bot):
    await bot.add_cog(momoi(bot))