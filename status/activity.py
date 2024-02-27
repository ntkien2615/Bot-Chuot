import discord
from discord.ext import commands, tasks
from itertools import cycle


class actvity(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.status = cycle([
            "Bot tạm down để chuyển nhà"
        ])

    @tasks.loop(seconds=30.0)
    async def change_status(self):
        await self.bot.change_presence(status=discord.Status.online,
                                       activity=discord.Activity(
                                           type=discord.ActivityType.watching,
                                           name=next(self.status)))

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.wait_until_ready()
        self.change_status.start()


async def setup(bot):
    await bot.add_cog(actvity(bot))
