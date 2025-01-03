import discord
from discord.ext import commands
from discord import app_commands
import random
from main import random_file_read

class kissSlash(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    def random_file_read(self):
        return random_file_read("./txt_files/kiss.txt")

    @app_commands.command(name='kiss', description='Hôn đứa bạn của bạn')
    @app_commands.describe(user='Người bạn muốn hôn')
    async def kissSlash(self, interaction: discord.Interaction, user: discord.Member):
        if (user == None) or (user == interaction.user):
            await interaction.response.send_message('Nhập người nào vào đi', ephemeral=True)
            return
        else:
            try:
                embed = discord.Embed(title="",
                                    description=f"{interaction.user.mention} đã hôn {user.mention} 😘",
                                    color=discord.Colour.random())
                embed.set_image(url=self.random_file_read())
            except Exception as e:
                print(e)


async def setup(bot):
    await bot.add_cog(kissSlash(bot))