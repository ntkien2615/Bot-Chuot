import discord
from discord.ext import commands
from discord import app_commands
import random


from src.commands.base_command import FunCommand


class phenis(FunCommand):

    def __init__(self, discord_bot):
        super().__init__(discord_bot)

    @app_commands.command(name='phenis', description='xem cái của bạn bao nhiêu')
    @app_commands.describe(member='Người bạn muốn xem')
    async def phenis_command(self, interaction: discord.Interaction, member: discord.Member = None):
        if member is None:
            member = interaction.user
            
        def tao_day_bang():
            day_bang = ""
            for _ in range(1,random.randint(1,21)):
                day_bang +="="
            return day_bang
            
        bang = tao_day_bang()
        embed = discord.Embed(title= f"Phenis của {member}", color=discord.Color.random())
        embed.add_field(name="", value=f"8{bang}D", inline=True)
        await interaction.response.send_message(embed=embed)
