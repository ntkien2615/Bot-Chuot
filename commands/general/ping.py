import discord
from discord.ext import commands
from discord import app_commands


class pingslash(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='ping', description='ping xem thử bot chết chưa')
    async def pingslash(self, interaction: discord.Interaction):
        try:
            await interaction.response.send_message(
                f'Bang, Headshot in {round(self.bot.latency*1000)} ms')
        except Exception as e:
            print(e)


async def setup(bot):
    await bot.add_cog(pingslash(bot))
