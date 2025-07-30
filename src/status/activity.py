import discord
from discord.ext import commands, tasks
from itertools import cycle


class BotActivity(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Không cần cycle status nữa, chỉ đặt một status cố định

    @tasks.loop(count=1)
    async def change_status(self):
        await self.bot.change_presence(status=discord.Status.online,
                                       activity=discord.Activity(
                                           type=discord.ActivityType.watching,
                                           name="Bot Comeback"))

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.wait_until_ready()
        self.change_status.start()


async def setup(bot):
    await bot.add_cog(BotActivity(bot))
