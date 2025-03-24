import discord
from discord.ext import commands
from discord import app_commands
import asyncio

def game_board():
    pass

def phy_atk():
    pass

def mage_atk():
    pass

def shield_add():
    pass

def run_game():
    pass

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
            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=30.0, check=lambda reaction, user: user == opponent and reaction.message == interaction.message and reaction.emoji == '✅')
                await interaction.response.send_message(f'{opponent.mention} đã chấp nhận lời thách đấu, hãy bắt đầu!')
                await run_game()
            except asyncio.TimeoutError:
                await interaction.response.send_message(f'Có lẽ {opponent.mention} đã chuồn')



