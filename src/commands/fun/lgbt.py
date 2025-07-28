import discord
from discord.ext import commands
from discord import app_commands
import random
from typing import Optional


from src.commands.base_command import FunCommand


class Lgbt(FunCommand):
    def __init__(self, discord_bot):
        super().__init__(discord_bot)

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
    async def lgbt_command(self, interaction: discord.Interaction, user: Optional[discord.Member] = None):
        if user is None:
            await interaction.response.send_message('Nhập người nào vào đi',ephemeral=True)
            return
        elif user == self.bot.user:
            await interaction.response.send_message('Nice try, diddy')
            return
        
        # NEW: Use image URLs from .env instead of .txt file
        lgbt_images = self.config.get_image_urls('LGBT_IMAGES')
        
        if lgbt_images:
            lgbt_url = random.choice(lgbt_images)
            embed = discord.Embed(title="", description="", color=discord.Color.random())
            embed.set_image(url=lgbt_url)
            await interaction.response.send_message(f"<@{user.id}>, 🏳️‍🌈?!?!", embed=embed)
        else:
            # Fallback to old method if no URLs in .env
            lgbt_url = self.random_file_read('src/txt_files/lgbt.txt')
            if lgbt_url:
                embed = discord.Embed(title="", description="", color=discord.Color.random())
                embed.set_image(url=lgbt_url)
                await interaction.response.send_message(f"<@{user.id}>, 🏳️‍🌈?!?!", embed=embed)
            else:
                await interaction.response.send_message("Không tìm thấy ảnh LGBT!", ephemeral=True)
