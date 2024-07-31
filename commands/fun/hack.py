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
        second = 5
        await interaction.response.send_message(f'Bắt đầu tiến hành cuộc tấn công nguy hiểm vào máy tính của <@{user.id}> trong {second}s')
        for i in range(1,5):
            second -= 1
            await interaction.response.edit_message(f'Bắt đầu tiến hành cuộc tấn công nguy hiểm vào máy tính của <@{user.id}> trong {second}s')
            asyncio.sleep(1)        

async def setup(bot):
    await bot.add_cog(Hack(bot))
