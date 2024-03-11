import discord
from discord.ext import commands
from discord import app_commands
import random


class diceslash(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='dice', description='tung xúc sắc theo các loại xúc sắc')
    @app_commands.describe(number='Chọn giá trị xúc sắc')
    @app_commands.choices(number=[
        discord.app_commands.Choice(name="4", value=4),
        discord.app_commands.Choice(name="6", value=6),
        discord.app_commands.Choice(name="8", value=8),
        discord.app_commands.Choice(name="12", value=12),
        discord.app_commands.Choice(name="20", value=20)
    ])
    async def dice(self, interaction: discord.Interaction, number: int):
        number_random = random.randint(1, number)
        await interaction.response.send_message(f'Kết quả từ xúc sắc {number} mặt: {number_random}')


async def setup(bot):
    await bot.add_cog(diceslash(bot))
