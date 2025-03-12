import discord
from discord.ext import commands
from discord import app_commands
import asyncio

class Pvp(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='pvp', description='Chơi pvp với người')
    @app_commands.describe(opponent='Người chơi bạn muốn chiến')
    async def pvp(self, interaction: discord.Interaction, opponent: discord.User):
        if opponent == interaction.user:
            await interaction.response.send_message('Bạn tự đấm bản thân à?')
        else:
            await interaction.response.send_message(f'{opponent.mention}, bạn nhận được lời thách đấu từ {interaction.user.mention}!, hãy bấm vào ô tick để tiếp tục')
            await interaction.message.add_reaction('✅')


