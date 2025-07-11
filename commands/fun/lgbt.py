import discord
from discord.ext import commands
from discord import app_commands
import random


from commands.base_command import FunCommand


class Lgbt(FunCommand):
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
    
    @app_commands.command(name='lgbt',description='lgbt?') 
    @app_commands.describe(user='Người bạn nghi là gay')
    async def lgbt_command(self, interaction: discord.Interaction, user:discord.Member = None):
        if user is None:
            await interaction.response.send_message('Nhập người nào vào đi',ephemeral=True)
            return
        else:      
            lgbt = self.random_file_read('./txt_files/lgbt.txt')
            embed = discord.Embed(title="", description="", color=discord.Color.random())
            embed.set_image(url=lgbt)

        await interaction.response.send_message(f"<@{user.id}>, 🏳️‍🌈?!?!",embed=embed)
