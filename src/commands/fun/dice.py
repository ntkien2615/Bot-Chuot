import discord
from discord.ext import commands
from discord import app_commands
import random
from src.commands.base_command import FunCommand


class DiceCommand(FunCommand):
    """Command to roll a dice with different faces."""
    
    def __init__(self, discord_bot):
        super().__init__(discord_bot)
        self.name = "dice"
        self.description = "Tung xúc sắc theo các loại xúc sắc"
        
    async def execute(self, interaction: discord.Interaction, number: int):
        """Execute the dice roll command."""
        number_random = random.randint(1, number)
        await interaction.response.send_message(f'Kết quả từ xúc sắc {number} mặt: {number_random}')
    
    @app_commands.command(name='dice', description='Tung xúc sắc theo các loại xúc sắc')
    @app_commands.describe(number='Chọn giá trị xúc sắc')
    @app_commands.choices(number=[
        discord.app_commands.Choice(name="4", value=4),
        discord.app_commands.Choice(name="6", value=6),
        discord.app_commands.Choice(name="8", value=8),
        discord.app_commands.Choice(name="12", value=12),
        discord.app_commands.Choice(name="20", value=20)
    ])
    async def dice(self, interaction: discord.Interaction, number: int):
        await self.execute(interaction, number)
