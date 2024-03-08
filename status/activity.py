import discord
from discord.ext import commands, tasks
from itertools import cycle


class actvity(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.status = cycle([
            "Bot tạm down để chuyển nhà",
            "🎵 Oh, love 🎵",
            "🎵 How I miss you every single day when I see you on those streets 🎵",
            "🎵 Oh, love 🎵",
            "🎵 Tell me there's a river I can swim that will bring you back to me 🎵",
            "🎵 Cause I don't know how to love someone else 🎵",
            "🎵 I don't know how to forget your face 🎵",
            "🎵 Oh, love 🎵",
            "🎵 God, I miss you every single day and now you're so far away...🎸🎸🎸 🎵"
        ])

    @tasks.loop(seconds=5.0)
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
