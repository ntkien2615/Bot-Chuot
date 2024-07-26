import discord
from discord.ext import commands
from discord import app_commands


class legslash(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='mp5_leg', description='cẩn thận cặp giò của m đấy')
    @app_commands.describe(member='Chọn cái đứa nào ây')
    async def leg(self, interaction: discord.Interaction, member: discord.Member):
        if member == None:
            await interaction.response.send_message('Well, ko có ai làm sao có cặp giò', ephemeral=True)
            return
        elif member == interaction.user:
            await interaction.response.send_message(f"Thiệt luôn, mà cặp giò của bạn trông khá múp ấy {member}")
        else:
            await interaction.send_message(f"CAN THAN CAP GIO VOI HON DAI CUA M DAY <@{member}>")

async def setup(bot):
    await bot.add_cog(legslash(bot))