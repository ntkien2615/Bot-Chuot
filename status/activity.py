import discord
from discord.ext import commands, tasks
from itertools import cycle


class actvity(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.status = cycle([
            "Bot đã quay trở lại và thảm hại hơn xưa",
            "🎵 ...Ai dám nói trước sau này 🎵",
            "🎵 Chằng ai biết trước tương lai sau này 🎵",
            "🎵 Tình yêu đâu biết mai này có vẹn nguyên 🎵",
            "🎵 Còn nguyên như lời ta đã hứa trước đây 🎵",
            "🎵 Dẫu cho giông tố xô xa rời 🎵",
            "🎵 Còn mãi những điều đẹp đẽ say đắm một thời 🎵",
            "🎵 Nụ cười và giọt nước mắt rơi từng trao cùng ta 🎵",
            "🎵 Nhìn lại về phía mặt trời... 🎵"
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
