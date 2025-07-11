import discord
from discord.ext import commands
from discord import app_commands
import random


from src.commands.base_command import FunCommand


class kissSlash(FunCommand):

    def __init__(self, discord_bot):
        super().__init__(discord_bot)
    
    def random_file_read(self, file_path=None):
        if not file_path:
            file_path = "src/txt_files/kiss.txt"
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
            if lines:
                return random.choice(lines).strip()
        except (IndexError, FileNotFoundError) as e:
            print(f"Error in random_file_read: {e}")
            return None

    @app_commands.command(name='kiss', description='Hôn đứa bạn của bạn')
    @app_commands.describe(user='Người bạn muốn hôn')
    async def kiss_command(self, interaction: discord.Interaction, user: discord.Member = None):
        if user is None or user == interaction.user:
            await interaction.response.send_message('Nhập người nào vào đi', ephemeral=True)
            return
        else:
            try:
                embed = discord.Embed(title="",
                                    description=f"{interaction.user.mention} đã hôn {user.mention} 😘",
                                    color=discord.Colour.random())
                embed.set_image(url=self.random_file_read("src/txt_files/kiss.txt"))
                await interaction.response.send_message(embed=embed)
            except Exception as e:
                print(e)
                await interaction.response.send_message('Đã xảy ra lỗi khi thực hiện lệnh.', ephemeral=True)