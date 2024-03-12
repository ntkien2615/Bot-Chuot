import discord
from discord.ext import commands, tasks
from itertools import cycle


class actvity(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.status = cycle([
            "Bot đã quay trở lại và thảm hại hơn xưa",
            "🎵 ...Vậy giờ người đừng tìm lại anh, nơi ai khác không phải anh 🎵",
            "🎵 Chẳng thể nào bận tâm, tim anh mãi luôn chân thành 🎵",
            "🎵 Liệu rằng lời xin lỗi đó có khiến ta còn như lúc đầu? 🎵",
            "🎵 Từng câu hát đã cố viết thêm những chương sau 🎵",
            "🎵 Giờ này nhìn về nhau nơi ấy còn đâu? 🎵",
            "🎵 Nụ cười em trên môi thay cho nỗi đau anh nơi này 🎵",
            "🎵 Màu trời em xanh mãi mỗi anh là mù mây 🎵",
            "🎵 Cứ như vậy đi 🎵",
            "🎵 Sóng đâu cản được gió mang thuyền xa... 🎵"
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
