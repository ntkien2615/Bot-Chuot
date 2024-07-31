import discord
from discord.ext import commands
from discord import app_commands
import asyncio
class Hack(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='hack',description='hack vào máy ai đó')
    @app_commands.describe(user='máy tính của ai')
    async def hack(self,interaction:discord.Interaction,user:discord.Member):
        if user == interaction.user:
            await interaction.response.send_message("Ông không thể hack chính ông đc, thử đứa khác đi")
            return

        await interaction.response.send_message(f"Initiating playful infiltration into <@{user.id}>'s system...")

        for i in range(5, 0, -1):
            await interaction.edit_original_response(content=f"Hacking progress: {i} seconds remaining...")
            await asyncio.sleep(1)  # Use asyncio.sleep for non-blocking delays

        # Conclude with a humorous message
        await interaction.edit_original_response(content=f"Hack complete! <@{user.id}>'s computer is now filled with... confetti! ")

async def setup(bot):
    await bot.add_cog(Hack(bot))
