import discord
from discord.ext import commands
from discord import app_commands
from src.commands.base_command import GeneralCommand


class PingCommand(GeneralCommand):
    """Command to check the bot's latency."""
    
    category = "general"
    
    def __init__(self, discord_bot):
        super().__init__(discord_bot)
        self.name = "ping"
        self.description = "Kiểm tra độ trễ của bot"
    
    async def execute(self, interaction):
        """Execute the ping command."""
        try:
            await interaction.response.send_message(
                f'Bang, Headshot in {round(self.bot.latency*1000)} ms')
        except Exception as e:
            print(e)
    
    @app_commands.command(name='ping', description='Ping xem thử bot chết chưa')
    async def ping(self, interaction: discord.Interaction):
        await self.execute(interaction)
