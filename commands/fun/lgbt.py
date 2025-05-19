import discord
from discord.ext import commands
from discord import app_commands
import random
from main import random_file_read


class Lgbt(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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
    async def moimoi(self, interaction: discord.Interaction, user:discord.Member):
        if (user == None) or (user == interaction.user):
            await interaction.response.send_message('Nhập người nào vào đi',ephemeral=True)
            return
        else:      
            lgbt = self.random_file_read('./txt_files/lgbt.txt')
            embed = discord.Embed(title="", description="", color=discord.Color.random())
            embed.set_image(url=lgbt)

        await interaction.response.send_message(f"<@{user.id}>, 🏳️‍🌈?!?!",embed=embed)

    

async def setup(bot):
    await bot.add_cog(Lgbt(bot))
