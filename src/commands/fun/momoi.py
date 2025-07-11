import discord
from discord.ext import commands
from discord import app_commands
import random


from src.commands.base_command import FunCommand


class momoi(FunCommand):
    def __init__(self, bot):
        super().__init__(bot)
    
    def random_file_read(self, file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
            if lines:
                return random.choice(lines).strip()
        except (IndexError, FileNotFoundError) as e:
            print(f"Error in random_file_read: {e}")
            return None

    @app_commands.command(name='momoi',description='momoi ní...') 
    @app_commands.describe(user='Người muốn được đua xe')
    async def moimoi(self, interaction: discord.Interaction, user:discord.Member = None):
        if user is None:
            await interaction.response.send_message('Nhập người nào vào đi',ephemeral=True)
            return
        else:      
            momoi = self.random_file_read('src/txt_files/moimoi.txt')
            embed = discord.Embed(title="", description="", color=discord.Color.random())
            embed.set_image(url=momoi)

        await interaction.response.send_message(f"<@{user.id}>",embed=embed)